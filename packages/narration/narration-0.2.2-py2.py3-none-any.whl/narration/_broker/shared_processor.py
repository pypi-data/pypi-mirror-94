from concurrent.futures._base import Future
from queue import Queue

from narration._broker.dispatch_status import DispatchStatus
from narration._handler.client.common.thread.base_sender_thread import BaseSenderThread
from narration._handler.common.callable import Record_Signal
from narration._handler.common.payload.record_payload import RecordPayload
from narration._handler.common.thread.base_op_thread import BaseOpThread
from narration._handler.server.common.thread.base_receiver_thread import BaseReceiverThread


class SharedBackgroundDispatcher:
    def __init__(self, thread_create=None, thread_destroy=None):
        self._dispatcher_thread: BaseOpThread = None
        self._dispatcher_thread_create = thread_create
        self._dispatcher_thread_destroy = thread_destroy
        self._handler_id_to_record_emitters = {}
        self._handler_id_to_transformer = {}

    @property
    def usage_count(self):
        return len(list(self._handler_id_to_record_emitters.keys()))

    def bind(self, handler_id: str = None, record_emitter: Record_Signal = None):
        if self.usage_count == 0:
            self._start_dispatching()

        self._register_handler(handler_id=handler_id, record_emitter=record_emitter)

    def unbind(self, handler_id: str = None):
        self._unregister_handler(handler_id=handler_id)

        if self.usage_count == 0:
            self._stop_dispatching()

    def _create_or_get_dispatcher_thread(self):
        existed = self._dispatcher_thread is not None
        if not existed:
            self._dispatcher_thread = self._dispatcher_thread_create()
            self._dispatcher_thread_create = None
        return self._dispatcher_thread, existed

    def _start_dispatching(self):
        dispatcher_thread, existed = self._create_or_get_dispatcher_thread()
        if not existed:
            dispatcher_thread.start()

    def _stop_dispatching(self):
        if self._dispatcher_thread is not None and self._dispatcher_thread.is_alive():
            self._dispatcher_thread_destroy(self._dispatcher_thread)

    def _register_handler(
        self, handler_id: str = None, record_emitter: Record_Signal = None, transformer=None
    ):
        self._handler_id_to_record_emitters[handler_id] = record_emitter
        self._handler_id_to_transformer[handler_id] = transformer

        if transformer is not None:
            record_emitter.connect(transformer)

    def _unregister_handler(self, handler_id: str = None):
        record_emitter = self._handler_id_to_record_emitters.get(handler_id)
        transformer = self._handler_id_to_transformer.get(handler_id)

        if transformer is not None:
            record_emitter.disconnect(transformer)

        self._handler_id_to_transformer.pop(handler_id, None)
        self._handler_id_to_record_emitters.pop(handler_id, None)


class SharedReceiverProcessor(SharedBackgroundDispatcher):
    def __init__(self, thread_create=None, thread_destroy=None):
        super().__init__(thread_create, thread_destroy)

    @property
    def thread(self) -> BaseReceiverThread:
        return self._dispatcher_thread

    def _register_handler(
        self, handler_id: str = None, record_emitter: Record_Signal = None, transformer=None
    ):
        self.thread.add_handler_id_to_record_emitter(
            handler_id=handler_id, record_emitter=record_emitter
        )
        super()._register_handler(
            handler_id=handler_id, record_emitter=record_emitter, transformer=transformer
        )

    def _unregister_handler(self, handler_id: str = None):
        self.thread.remove_handler_id_to_record_emitter(handler_id=handler_id)
        super()._unregister_handler(handler_id=handler_id)


class SharedSenderProcessor(SharedBackgroundDispatcher):
    def __init__(self, thread_create=None, thread_destroy=None):
        super().__init__(thread_create, thread_destroy)

    @property
    def thread(self) -> BaseSenderThread:
        return self._dispatcher_thread

    @property
    def queue(self) -> Queue:
        return self._dispatcher_thread.queue

    def _register_handler(
        self, handler_id: str = None, record_emitter: Record_Signal = None, transformer=None
    ):
        def forward_to_dispatcher_queue(payload: RecordPayload):
            dispatch_status = DispatchStatus(payload=payload, future=Future())

            def add_to_queue(_):
                return self.queue.put(dispatch_status, block=True, timeout=None)

            dispatch_status.emit(emitter=add_to_queue, drop_completion_if_successful=True)
            return dispatch_status

        super()._register_handler(
            handler_id=handler_id,
            record_emitter=record_emitter,
            transformer=forward_to_dispatcher_queue,
        )

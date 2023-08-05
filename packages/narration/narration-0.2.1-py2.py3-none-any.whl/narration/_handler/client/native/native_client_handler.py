import threading

from narration._misc.constants import DispatchMode
from narration._handler.client.common.handler.base_client_handler import BaseClientHandler
from narration._handler.client.common.thread.base_sender_thread import BaseSenderThread
from narration._handler.client.native.native_sender_thread import NativeSenderThread
from narration._handler.common.util.utils import wait_for_event


class NativeClientHandler(BaseClientHandler):
    def __init__(
        self,
        uuid: str = None,
        name: str = None,
        queue=None,
        level=None,
        on_close_timeout: float = 1.0,
        message_dispatching: DispatchMode = DispatchMode.SYNC,
        group_id: str = None,
    ):
        super().__init__(
            uuid=uuid,
            name=name,
            level=level,
            on_close_timeout=on_close_timeout,
            message_dispatching=message_dispatching,
            group_id=group_id,
        )
        self._native_queue = queue

        group_id = "native-group-id"
        processing_ready, self._group_id = self._assign_processor(
            group_id=group_id,
            record_emitter=self._record_emitter,
        )
        wait_for_event(processing_ready, 60, self._processor.thread.is_alive)

    def _create_processor_thread(
        self, thread_name: str = None, processing_ready: threading.Event = None
    ) -> BaseSenderThread:
        return NativeSenderThread(
            name=thread_name,
            sender_ready=processing_ready,
            queue=self._queue,
            native_queue=self._native_queue,
        )

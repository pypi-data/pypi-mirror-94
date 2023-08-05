from typing import Dict

from narration._broker.shared_processor import (
    SharedBackgroundDispatcher,
    SharedReceiverProcessor,
    SharedSenderProcessor,
)

import threading

from narration._handler.common.misc.op_type import OpType
from narration._handler.common.callable import (
    Record_Signal,
    Callable_Thread_Create,
    Callable_Thread_Destroy,
)

lock = threading.Lock()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ProcessorBroker(metaclass=Singleton):
    def __init__(self):
        self._processors: Dict[str, SharedBackgroundDispatcher] = {}
        self._mutex = threading.Lock()

    def _key(self, role_type: OpType = None, group_id: str = None):
        return f"{role_type.name}-{group_id}"

    def bind(
        self,
        role_type: OpType = None,
        group_id: str = None,
        handler_id: str = None,
        thread_create: Callable_Thread_Create = None,
        thread_destroy: Callable_Thread_Destroy = None,
        record_emitter: Record_Signal = None,
    ) -> SharedBackgroundDispatcher:
        with self._mutex:
            key = self._key(role_type=role_type, group_id=group_id)
            processor = self._processors.get(key, None)
            existed = processor is not None
            if not existed:
                if role_type == OpType.RECEIVE:
                    processor = SharedReceiverProcessor(
                        thread_create=thread_create, thread_destroy=thread_destroy
                    )
                elif role_type == OpType.SEND:
                    processor = SharedSenderProcessor(
                        thread_create=thread_create, thread_destroy=thread_destroy
                    )
                else:
                    raise NotImplementedError()

                self._processors[key] = processor

            processor.bind(handler_id=handler_id, record_emitter=record_emitter)
            return processor

    def unbind(
        self, role_type: OpType = None, group_id: str = None, handler_id: str = None
    ) -> threading.Event:
        with self._mutex:
            key = self._key(role_type=role_type, group_id=group_id)
            processor = self._processors.get(key, None)
            if processor is not None:
                processor.unbind(handler_id=handler_id)
                if processor.usage_count == 0:
                    self._processors.pop(key, None)
                return processor.thread.shutdown_completed
            else:
                shutdown_completed = threading.Event()
                shutdown_completed.set()
                return shutdown_completed


PROCESSOR_BROKER = ProcessorBroker()

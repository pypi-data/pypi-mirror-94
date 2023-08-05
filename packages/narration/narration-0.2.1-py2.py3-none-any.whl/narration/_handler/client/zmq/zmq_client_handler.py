import logging
import threading
from queue import Queue

import zmq

from narration._debug.myself import get_debug_logger
from narration._misc.constants import DispatchMode, NARRATION_DEBUG_HANDLER_ZMQ_PREFIX
from narration._handler.client.common.handler.base_client_handler import BaseClientHandler
from narration._handler.client.common.thread.base_sender_thread import BaseSenderThread
from narration._handler.client.zmq.zmq_sender_thread import ZmqSenderThread
from narration._handler.common.util.utils import wait_for_event

_log = get_debug_logger(NARRATION_DEBUG_HANDLER_ZMQ_PREFIX)


class ZMQClientHandler(BaseClientHandler):
    def __init__(
        self,
        uuid: str = None,
        name=None,
        address: str = None,
        level=logging.DEBUG,
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

        self._socket_type = zmq.PUSH
        self._address = address

        self._group_id = self._address
        processing_ready, self._group_id = self._assign_processor(
            group_id=self._address,
            record_emitter=self._record_emitter,
        )
        wait_for_event(processing_ready, 60, self._processor.thread.is_alive)
        _log.debug("Client addres: %s, group id %s", self._address, self._group_id)

    def _create_processor_thread(
        self, thread_name: str = None, processing_ready: threading.Event = None
    ) -> BaseSenderThread:
        return ZmqSenderThread(
            name=thread_name,
            sender_ready=processing_ready,
            socket_type=self._socket_type,
            address=self._address,
            queue=Queue(-1),
        )

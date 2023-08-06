import logging
import threading

import zmq

from narration._misc.constants import DispatchMode
from narration._handler.common.util.utils import wait_for_event
from narration._handler.server.common.handler.base_server_handler import BaseServerHandler
from narration._handler.server.common.thread.base_receiver_thread import BaseReceiverThread
from narration._handler.server.zmq.zmq_receiver_thread import ZmqReceiverThread


class ZMQServerHandler(BaseServerHandler):
    def __init__(
        self,
        uuid: str = None,
        name=None,
        target_handler: logging.Handler = None,
        address: str = "tcp://127.0.0.1",
        level=logging.DEBUG,
        on_close_timeout: float = 1.0,
        message_dispatching: DispatchMode = DispatchMode.SYNC,
    ):
        super().__init__(
            uuid=uuid,
            name=name,
            target_handler=target_handler,
            level=level,
            on_close_timeout=on_close_timeout,
            message_dispatching=message_dispatching,
            group_id=None,
        )

        self._socket_type = zmq.PULL
        self._address = address
        self._socket = None

        processing_ready, self._group_id = self._assign_processor(
            group_id=self._address,
            record_emitter=self._record_emitter,
        )
        wait_for_event(processing_ready, 60, self._processor.thread.is_alive)

        self._address = self._processor.thread.address

    def _create_processor_thread(
        self, thread_name: str = None, processing_ready: threading.Event = None
    ) -> BaseReceiverThread:
        return ZmqReceiverThread(
            name=thread_name,
            receiver_ready=processing_ready,
            socket_type=self._socket_type,
            address=self._address,
        )

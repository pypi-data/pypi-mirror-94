import logging

import blinker

from narration._handler.common.record.utils import mark_remote_record, has_remote_record_marker
from narration._misc.constants import DispatchMode
from narration._handler.common.callable import Record_Signal
from narration._handler.common.handler.base_handler import BaseHandler
from narration._handler.common.misc.op_type import OpType


class BaseServerHandler(BaseHandler):
    """The BaseServerHandler creates a connection between the main
    process and its children processes.

    The XXXXServerHandler is expected to be set up by the main process.

    """

    def __init__(
        self,
        uuid: str = None,
        name=None,
        target_handler: logging.Handler = None,
        level=logging.DEBUG,
        on_close_timeout: float = 1.0,
        message_dispatching: DispatchMode = DispatchMode.SYNC,
        group_id: str = None,
    ):
        super().__init__(
            uuid=uuid,
            name=name,
            type=OpType.RECEIVE,
            level=target_handler.level if target_handler is not None else level,
            on_close_timeout=on_close_timeout,
            message_dispatching=message_dispatching,
            group_id=group_id,
        )

        if target_handler is None:
            target_handler = logging.StreamHandler()
        self.target_handler = target_handler

        self.setFormatter(self.target_handler.formatter)
        self.filters = self.target_handler.filters

        self._address = None

        self._record_emitter: Record_Signal = blinker.Signal()
        self._record_emitter.connect(self.emit)

    @property
    def address(self):
        return self._address

    def setFormatter(self, fmt):
        super().setFormatter(fmt)
        if self.target_handler is not None:
            self.target_handler.setFormatter(fmt)

    def emit(self, record):
        if self.target_handler is not None:
            if has_remote_record_marker(record=record, state=True):
                self.target_handler.handle(record)

    def close(self):
        shutdown_completed = super().close()
        if self.target_handler is not None:
            self.target_handler.flush()
        return shutdown_completed

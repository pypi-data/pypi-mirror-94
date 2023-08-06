import concurrent
from typing import List

import blinker

from narration._broker.dispatch_status import DispatchStatus
from narration._misc.constants import DispatchMode, NARRATION_DEBUG_HANDLER_PREFIX
from narration._handler.common.callable import Record_Signal
from narration._handler.common.handler.base_handler import BaseHandler
from narration._handler.common.misc.op_type import OpType
from narration._handler.common.payload.record_payload import RecordPayload
from narration._debug.myself import get_debug_logger

_log = get_debug_logger(NARRATION_DEBUG_HANDLER_PREFIX)


class BaseClientHandler(BaseHandler):
    def __init__(
        self,
        uuid: str = None,
        name: str = None,
        record_emitter: Record_Signal = blinker.Signal(),
        level=None,
        on_close_timeout: float = 1.0,
        message_dispatching: DispatchMode = DispatchMode.SYNC,
        group_id: str = None,
    ):
        super().__init__(
            uuid=uuid,
            name=name,
            type=OpType.SEND,
            level=level,
            on_close_timeout=on_close_timeout,
            message_dispatching=message_dispatching,
            group_id=group_id,
        )
        self._server_notified = False
        self._record_emitter = record_emitter
        self._unacked_dispatches = []
        self._unacked_timeout = 0.1

    def emit(self, record):
        try:
            payload = RecordPayload(record=record, handler_id=self._uuid)
            if self._record_emitter is None:
                _log.error(
                    "No record emitter set for sending message to shared processor. Handler id: %s. Record: %s",
                    self._uuid,
                    record,
                )
                self.handleError(record)
                return

            for receiver, dispatch_status in self._record_emitter.send(payload):
                timeout = None if self._message_dispatching == DispatchMode.SYNC else 0
                _log.debug(
                    "handler to send message %s with timeout=%s",
                    dispatch_status.payload.record,
                    timeout,
                )
                pending_dispatches = self._check_statuses(
                    dispatch_statuses=[dispatch_status],
                    timeout=timeout,
                    stop_tracking_failed_dispatch=False,
                )
                self._unacked_dispatches.extend(pending_dispatches)
        except (BaseException):
            # Record will not be sent later.
            _log.error("Record sending failed. Record: %s", record, exc_info=1)
            self.handleError(record)

    def _check_statuses(
        self,
        dispatch_statuses: List[DispatchStatus] = 0,
        timeout=None,
        stop_tracking_failed_dispatch: bool = False,
    ):
        pending_status = []
        for dispatch_status in dispatch_statuses:
            record = dispatch_status.payload.record
            try:
                dispatch_status.future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                # Record may still be sent later. no error
                pending_status.append(dispatch_status)
                _log.warning(
                    "Record sending timeout. Record may not have been dispatch yet. Record: %s",
                    record,
                )
            except (concurrent.futures.CancelledError, BaseException):
                # Record will not be sent later.
                _log.error("Record sending failed. Record: %s", record, exc_info=1)
                self.handleError(record)
            else:
                _log.debug("Record dispatched: %s", record)

        if stop_tracking_failed_dispatch:
            return []
        return pending_status

    def flush(self) -> None:
        self._unacked_dispatches = self._check_statuses(
            dispatch_statuses=self._unacked_dispatches,
            timeout=self._unacked_timeout,
            stop_tracking_failed_dispatch=True,
        )

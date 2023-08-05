import logging
import threading
from asyncio.exceptions import CancelledError
from typing import Dict

from narration._handler.common.record.utils import mark_remote_record
from narration._misc.constants import NARRATION_DEBUG_HANDLER_THREAD_PREFIX
from narration._handler.common.payload.serialization.record_payload import (
    to_record_payload,
    to_nonbinary_payload,
)
from narration._handler.common.payload.record_payload import RecordPayload
from narration._handler.common.thread.base_op_thread import BaseOpThread
from narration._handler.common.misc.op_type import OpType
from narration._handler.common.socket.base_socket import BaseSocket
from narration._handler.common.socket.exception.readtimeoutexception import ReadTimeoutException
from narration._handler.common.callable import Record_Signal
from narration._debug.myself import get_debug_logger

_log = get_debug_logger(NARRATION_DEBUG_HANDLER_THREAD_PREFIX)


class BaseReceiverThread(BaseOpThread):
    def __init__(
        self,
        name: str = None,
        receiver_ready: threading.Event = None,
        handler_id_to_record_emitters: Dict[str, Record_Signal] = {},
        daemon: bool = False,
        read_timeout: float = 1.0,
        *args,
        **kwargs,
    ):
        super().__init__(
            name=name,
            op_startup_completed=receiver_ready,
            daemon=daemon,
            op_timeout=read_timeout,
            op_type=OpType.RECEIVE,
            *args,
            **kwargs,
        )
        self._handler_id_to_record_emitters = handler_id_to_record_emitters

    def add_handler_id_to_record_emitter(
        self, handler_id: str = None, record_emitter: Record_Signal = None
    ):
        emitter = self._handler_id_to_record_emitters.get(handler_id, None)
        if emitter is None:
            self._handler_id_to_record_emitters[handler_id] = record_emitter

    def remove_handler_id_to_record_emitter(self, handler_id: str = None):
        self._handler_id_to_record_emitters.pop(handler_id, None)

    async def _operate(self, socket: BaseSocket = None, queue=None, op_timeout=None) -> bool:
        def has_read_record(record):
            return record is not None

        try:
            payload = await self._read_payload_from_socket(socket=socket, op_timeout=op_timeout)
            record = payload.record
            handler_id = payload.handler_id
            record_emitter = self._handler_id_to_record_emitters.get(handler_id, None)

            _log.debug(
                "Record received with handler id %s %s: %s",
                handler_id,
                f"discarded" if record_emitter is None else f"to be dispatched to {record_emitter}",
                record,
            )

            if record is None:
                return has_read_record(record)
            elif handler_id is None:
                return has_read_record(record)
            elif record_emitter is None:
                return has_read_record(record)

            mark_remote_record(record=record, state=True)
            record_emitter.send(record)
            return has_read_record(record)
        except ReadTimeoutException:
            _log.critical("Receiving message timeout", exc_info=1)
            return has_read_record(None)
        except BaseException as e:
            # Stop thread
            ignore_exception = isinstance(e, CancelledError)
            if not ignore_exception:
                _log.critical("Receiving message failed", exc_info=1)
                raise

    def _to_log_record(self, raw_record: object = None) -> logging.LogRecord:
        return logging.makeLogRecord(raw_record) if raw_record is not None else None

    async def _read_payload_from_socket(
        self, socket: BaseSocket = None, op_timeout=None
    ) -> RecordPayload:
        binary_payload = await socket.read_payload(op_timeout=op_timeout)
        raw_payload = to_nonbinary_payload(binary_payload)
        payload = to_record_payload(raw_payload=raw_payload)
        _log.debug("New record received from %s. Record: %s", payload.handler_id, payload.record)
        return payload

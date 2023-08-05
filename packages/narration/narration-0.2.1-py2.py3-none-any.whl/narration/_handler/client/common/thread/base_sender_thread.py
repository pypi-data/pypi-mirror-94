from __future__ import annotations

import asyncio
import functools
import threading
from asyncio.exceptions import CancelledError
from concurrent.futures.thread import ThreadPoolExecutor
from queue import Empty, Queue

from narration._broker.dispatch_status import DispatchStatus
from narration._misc.constants import NARRATION_DEBUG_HANDLER_THREAD_PREFIX
from narration._handler.common.payload.serialization.record_payload import (
    to_raw_record_payload,
    to_binary_payload,
)
from narration._handler.common.thread.base_op_thread import BaseOpThread
from narration._handler.common.misc.op_type import OpType
from narration._handler.common.socket.exception.optimeoutexception import OpTimeoutException
from narration._handler.common.socket.base_socket import BaseSocket
from narration._debug.myself import get_debug_logger

_log = get_debug_logger(NARRATION_DEBUG_HANDLER_THREAD_PREFIX)


class NoPayloadException(BaseException):
    pass


class BaseSenderThread(BaseOpThread):
    def __init__(
        self,
        name=None,
        sender_ready: threading.Event = None,
        daemon=False,
        write_timeout: float = 1.0,
        queue: Queue[DispatchStatus] = None,
        *args,
        **kwargs,
    ):
        super().__init__(
            name=name,
            op_startup_completed=sender_ready,
            daemon=daemon,
            op_timeout=write_timeout,
            op_type=OpType.SEND,
            *args,
            **kwargs,
        )
        self._queue = queue
        self._pending_dispatch_status = None
        self._pool = ThreadPoolExecutor(
            max_workers=1, thread_name_prefix=f"blocking_io_{self.name}"
        )
        self._blocking_io_interupted = threading.Event()

    @property
    def queue(self) -> Queue[DispatchStatus]:
        return self._queue

    async def get_from_queue(self, timeout=0.25, interrupted: threading.Event = None):
        def blocking_queue_read(timeout, interrupted_cond: threading.Event):
            while True:
                if interrupted_cond.wait(0.1):
                    raise InterruptedError("blocking io interrupted")

                try:
                    return self.queue.get(
                        block=True, timeout=timeout if timeout is not None else 0.25
                    )
                except Empty:
                    # nothing in the queue
                    pass

        return await self._loop.run_in_executor(
            self._pool, blocking_queue_read, timeout, interrupted
        )

    async def _operate(self, socket: BaseSocket = None, op_timeout=None) -> bool:
        def raise_exception(exeption):
            def foo(*args):
                raise exeption

            return foo

        def return_value(value):
            def foo(*args):
                return value

            return foo

        consumed = False
        record_written = False
        dispatch_status: DispatchStatus = None
        retry_pending = self._pending_dispatch_status is not None
        try:
            dispatch_status = (
                self._pending_dispatch_status
                if retry_pending
                else await self.get_from_queue(
                    timeout=op_timeout, interrupted=self._blocking_io_interupted
                )
            )
            payload = dispatch_status.payload
            has_payload = payload is not None

            if not has_payload:
                consumed = True
                record_written = False
                dispatch_status.emit(
                    emitter=raise_exception(NoPayloadException()),
                    drop_completion_if_successful=False,
                )
            else:
                raw_payload = to_raw_record_payload(payload=payload)
                if raw_payload is not None:
                    result = await self._write_payload_to_socket(
                        socket=socket,
                        raw_payload=raw_payload,
                        op_timeout=op_timeout,
                        retrying=retry_pending,
                    )
                    record_written = result is None
                    dispatch_status.emit(
                        emitter=return_value(record_written),
                        drop_completion_if_successful=False,
                    )
                    consumed = record_written
                    self._pending_dispatch_status = None
            return record_written
        except OpTimeoutException:
            self._pending_dispatch_status = dispatch_status
            return record_written
        except BaseException as e:
            # Stop thread
            if dispatch_status is not None:
                consumed = True
                dispatch_status.emit(
                    emitter=raise_exception(e), drop_completion_if_successful=False
                )
            ignore_exception = isinstance(e, CancelledError)
            if not ignore_exception:
                _log.critical("Sending message failed", exc_info=1)
                raise
        finally:
            if consumed:
                self._queue.task_done()

    async def _write_payload_to_socket(
        self,
        socket: BaseSocket = None,
        raw_payload: object = None,
        op_timeout=0,
        retrying: bool = False,
    ):
        _log.debug(
            "%s record to send (%s) %s",
            "Retry" if retrying else "New",
            op_timeout + "s" if op_timeout is not None else "no timeout",
            raw_payload,
        )
        binary_payload = to_binary_payload(data=raw_payload)
        return await socket.write_payload(binary_payload, op_timeout=op_timeout)

    def shutdown(self, timeout: float = None):
        # Wait till shutdown thread reading from the queue stops
        super().shutdown(timeout=timeout)

        # Shutdown "blocking io" thread pool
        self._blocking_io_interupted.set()
        self._pool.shutdown(wait=True)

        # Cancel all pending queue record status, otherwise wait till they complete
        try:
            while True:
                dispatch_status = self.queue.get_nowait()
                try:
                    future = dispatch_status.future
                    if future.done():
                        continue

                    _log.debug("Try cancelling dispatch status %s", dispatch_status.payload)
                    cancelled = future.cancel()
                    if not cancelled:
                        try:
                            future.result(timeout=None)
                        except BaseException:
                            _log.warning(
                                "%s raised exception.", dispatch_status.payload, exc_info=1
                            )
                            pass
                finally:
                    self.queue.task_done()
        except Empty:
            # Queue cleared
            pass
        finally:
            # Queue is cleared by now. Join will return immediately (otherwise programer error)
            self.queue.join()

import logging
import os
import threading
from threading import Event
from uuid import uuid4
from typing import Dict, List

import attr

from narration._handler.client.native.native_client_handler import NativeClientHandler
from narration._handler.common.handler.base_handler import BaseHandler
from narration._handler.forwarder.forward_handler import ForwardHandler
from narration.constants import (
    Backend,
)
from narration._misc.constants import (
    DispatchMode,
    NARRATION_HANDLER_PREFIX,
    NARRATION_DEBUG_LOG_PREFIX,
)
from narration._handler.client.zmq.zmq_client_handler import ZMQClientHandler
from narration._handler.server.common.handler.base_server_handler import BaseServerHandler
from narration._handler.server.native.native_server_handler import NativeServerHandler
from narration._handler.server.zmq.zmq_server_handler import ZMQServerHandler
from narration._debug.myself import get_debug_logger

_log = get_debug_logger(NARRATION_DEBUG_LOG_PREFIX)


def _create_client_handler_factory(kwargs: Dict = {}):
    backend = kwargs.pop("backend")
    if backend is None:
        backend = Backend.DEFAULT

    if backend == Backend.NATIVE:
        return NativeClientHandler(**kwargs)
    elif backend == Backend.ZMQ:
        return ZMQClientHandler(**kwargs)


def _create_server_handler_factory(
    process_start_method: str = None, ctx=None, ctx_manager=None, **kwargs
):
    """
    Factory to create a multiprocessing aware logging _handler instance
    :param kwargs: Keyword arguments:
    {
        name: str                         Native/ZMQ
        target_handler: Handler           Native/ZMQ
        queue: Queue (or similar),        Native
        server_address: str               ZMQ                 Eg: tcp://127.0.0.1 or tcp://127.0.0.1:9000
        level: int                        Native/ZMQ
        process_start_method: str         Native/ZMQ
        on_close_timeout: int             Native/ZMQ          5 (in seconds)
        message_dispatching: DispatchMode ZMQ
    }
    :return ServerHandler, {} (Or None,None if no process starting method is identified nor no multiprocessing aware
    _handler should be returned)
    """
    if None in [process_start_method, ctx_manager]:
        return None, {}

    backend = kwargs.pop("backend")
    if backend is None:
        backend = Backend.DEFAULT

    uuid = uuid4().urn
    kwargs.update(uuid=uuid)

    settings = {
        "level": kwargs.get("level", logging.DEBUG),
        "start_method": process_start_method,
        "backend": backend,
        "uuid": uuid,
        "on_close_timeout": kwargs.get("on_close_timeout", 5.0),
        "message_dispatching": kwargs.get("message_dispatching", DispatchMode.SYNC),
    }

    if backend == Backend.NATIVE:
        queue = kwargs.get("queue", None)
        queue_missing = queue is None
        if queue_missing:
            queue = ctx_manager.Queue(-1)
            kwargs.update(queue=queue)

        settings.update(queue=queue)
        handler = NativeServerHandler(**kwargs), settings
        settings.update(group_id=handler.group_id)
        return handler, settings
    elif backend == Backend.ZMQ:
        address = kwargs.get("address", None)
        address_missing = address is None
        if address_missing:
            # ZMQ will auto assign the port
            address = "tcp://127.0.0.1"

        kwargs.update(address=address)
        handler = ZMQServerHandler(**kwargs)
        settings.update(address=handler.address)
        settings.update(group_id=handler.group_id)
        return handler, settings


def setup_client_handlers(
    logger=None,
    handler_name_to_client_handler_settings: Dict = {},
    create_client_handler_factory=_create_client_handler_factory,
):
    # Add client handlers
    for (
        handler_name,
        client_handler_settings,
    ) in handler_name_to_client_handler_settings.items():
        start_method = client_handler_settings.get("start_method")
        client_handler_settings2 = {
            key: client_handler_settings[key]
            for key in client_handler_settings
            if key != "start_method"
        }
        client_handler_settings2.update(name=handler_name)
        handler = create_client_handler_factory(client_handler_settings2)
        handler.name = handler_name

        # Remove forked main process's logger's handler if process was forked
        _closed_forked_handler(logger=logger, handler_id=handler.uuid)

        # Add client _handler
        logger.addHandler(handler)


def setup_server_handlers(
    logger=None,
    ctx=None,
    ctx_manager=None,
    backend=Backend.DEFAULT,
    message_dispatch_mode=DispatchMode.SYNC,
    create_server_handler_factory=_create_server_handler_factory,
):
    """Wraps a logger's handlers with ServerHandler instances.
       This utility function will setup the correct inter process communication to retrieve logs from child processes,
       regardless of the process start method used (fork, spawn, forkserver)

    :param logger: Logger whose handlers to wrap. Default: Python root logger.
    :return Tuple[ServerHandler's name, dict of client _handler settings]. The dict must be considered opaque.
    """
    if logger is None:
        logger = logging.getLogger()

    settings = {}

    handler_name = "server"
    kwargs = {
        "name": f"{NARRATION_HANDLER_PREFIX}{handler_name}",
        "target_handler": ForwardHandler(level=logging.DEBUG, logger=logger),
        "level": logging.DEBUG,
        "process_start_method": ctx.get_start_method(),
        "ctx": ctx,
        "ctx_manager": ctx_manager,
        "backend": backend,
        "on_close_timeout": 5.0,
        "message_dispatching": message_dispatch_mode,
    }
    server_handler, client_handler_settings = create_server_handler_factory(**kwargs)
    if server_handler is not None:
        logger.addHandler(server_handler)
        settings[handler_name] = client_handler_settings

    return settings


@attr.s(kw_only=True, frozen=True, auto_attribs=True)
class HandlerTeardownStatus:
    logger: logging.Logger = None
    handler: BaseHandler = None
    shutdown_completed: Event = None


def teardown_handlers(loggers: List[logging.Logger] = [], timeout=None):
    # Many loggers may share the same read/write thread ressources, hence shuting down resources must be requested on ALL
    # loggers to be effective and not deadlock the application

    # Request logger handler shutdown for all handlers
    handler_shutdown_statuses = []
    for logger in loggers:
        shutdown_statuses = _teardown_handlers(logger=logger)
        handler_shutdown_statuses.extend(shutdown_statuses)

    # Wait for all handlers to be fully shutdown
    for s in handler_shutdown_statuses:
        s.shutdown_completed.wait(timeout=timeout)


def _teardown_handlers(logger=None) -> List[HandlerTeardownStatus]:
    """Unwraps a logger's handlers from their ServerHandler instances

    :param logger: Logger whose handlers to wrap. Default: Python root logger.
    """
    if logger is None:
        logger = logging.getLogger()

    removed_handlers = []

    # Select handlers to remove
    for handler in logger.handlers:
        if isinstance(handler, BaseHandler):
            removed_handlers.append((logger, handler, True))

    # Initiate shutdown for all handlers
    handler_shutdown_statuses = []
    for logger, handler, restore_original_handler in removed_handlers:
        if not restore_original_handler:
            continue

        target_handler = handler.target_handler if isinstance(handler, BaseServerHandler) else None
        logger.removeHandler(handler)
        if target_handler is not None:
            logger.addHandler(target_handler)
        shutdown_completed = _shutdown_handler_resources(handler=handler)
        handler_shutdown_statuses.append(
            HandlerTeardownStatus(
                logger=logger, handler=handler, shutdown_completed=shutdown_completed
            )
        )

    return handler_shutdown_statuses


def _shutdown_handler_resources(handler: BaseHandler = None) -> threading.Event:
    shutdown_completed = None
    name = f"Shutdown handler resources: {handler}"
    _log.debug("%s ...", name)
    try:
        handler.acquire()
        shutdown_completed = handler.close()
        handler.release()
    finally:
        _log.debug(
            "%s %s shutdown",
            name,
            "fully"
            if shutdown_completed is not None and shutdown_completed.is_set()
            else "not yet",
        )
        return shutdown_completed


def _closed_forked_handler(logger: logging.Logger = None, handler_id: str = None):
    handlers = [h for h in logger.handlers if isinstance(h, BaseHandler)]
    # Remove forked main process's logger's handlers if process was forked
    forked_handler = next(filter(lambda h: h.uuid == handler_id, handlers), None)
    if forked_handler is not None and forked_handler.pid == os.getppid():
        _log.debug("Discarding forked handler by removing+closing it: %s", forked_handler)
        # This handler was created in parent process
        logger.removeHandler(forked_handler)
        forked_handler.close()

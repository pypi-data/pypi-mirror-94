# https://gitlab.com/peick/starlog/-/blob/master/starlog/handlers/zmq_handler.py

import errno
from typing import List, Tuple

import zmq as zmq
import zmq.asyncio as zmqaio

from narration._handler.common.socket.exception.bindfailedexception import BindFailedException
from narration._misc.constants import NARRATION_DEBUG_HANDLER_SOCKET_ZMQ_PREFIX
from narration._handler.common.socket.base_socket import BaseSocket
from narration._debug.myself import get_debug_logger
from narration._handler.common.util.utils import retry, requires_random_bind

_log = get_debug_logger(NARRATION_DEBUG_HANDLER_SOCKET_ZMQ_PREFIX)
_log.debug("pyzmq v%s & libzmq v%s", zmq.__version__, zmq.zmq_version())


def _get_poll_type(socket_type):
    if socket_type == zmq.PUSH:
        return zmq.POLLOUT
    elif socket_type == zmq.PULL:
        return zmq.POLLIN
    return zmq.POLLIN | zmq.POLLOUT | zmq.POLLERR


class ZmqResilientSocket(BaseSocket):
    UNRECOVERABLE_ERRORS = [
        # "Permission denied"
        errno.EACCES,
    ]

    # http://api.zeromq.org/3-0:zmq-setsockopt
    DEFAULT_SOCKET_OPTIONS = {
        # 1000ms before giving up sending a message (app will # need to retry will be needed)
        zmq.SNDTIMEO: 1000,
        zmq.RCVTIMEO: -1,  # in milliseconds. -1 = block until a message is available
        zmq.LINGER: 1000,  # in milliseconds. Duration before closed socket's message are deleted, to finilize socket closing
        zmq.RCVBUF: 0,  # 0 = Use OS default
        zmq.SNDBUF: 0,  # 0 = Use OS default
        # Max number of pending message to send held in memory (before dropping or block sending)
        zmq.SNDHWM: 1000,
        # Max number of pending message to read held in memory (before dropping or block sending)
        zmq.RCVHWM: 1000,
    }

    def __init__(
        self,
        socket_type,
        address,
        backoff_factor=2.0,
        tries=3,
        check=None,
        socket_options: List[Tuple[int, int]] = DEFAULT_SOCKET_OPTIONS,
    ):
        self._socket_type = socket_type
        self._address = address

        self._context = None
        self._socket = None
        self._socket_options = socket_options
        self._poll_type = _get_poll_type(self._socket_type)

        def _log_bind_attempt(self, _trial, last_trial=False):
            if last_trial:
                _log.error("bind to %s failed. Aborting.", self._address)
            else:
                _log.warning("bind to %s failed. Retrying", self._address)

        def _log_connect_attempt(self, _trial, last_trial=False):
            if last_trial:
                _log.error("connect to %s failed. Aborting.", self._address)
            else:
                _log.warning("connect to %s failed. Retrying.", self._address)

        self._retry_bind = retry(
            zmq.ZMQError,
            tries=tries,
            backoff_factor=backoff_factor,
            check=check,
            retry_log=_log_bind_attempt,
        )

        self._retry_connect = retry(
            zmq.ZMQError,
            tries=tries,
            backoff_factor=backoff_factor,
            check=check,
            retry_log=_log_connect_attempt,
        )

        self._poller = zmqaio.Poller()

    def _poller_register(self, socket: zmq.Socket = None, flags: int = 0):
        _log.debug("Register socket %s with poller %s with flags:%s", socket, self._poller, flags)
        self._poller.register(socket=socket, flags=flags)

    def _poller_unregister(self, socket: zmq.Socket = None):
        _log.debug("Unregister socket %s from poller %s", socket, self._poller)
        self._poller.unregister(socket=socket)

    def bind(self):
        bind_with_retries = self._retry_bind(self._bind)
        bind_with_retries()

    def _bind(self):
        socked_poll_registered = False
        try:
            self._socket = self._close_socket()
            self._context = self._get_or_create_context()
            self._socket = self._create_socket(context=self._context, socket_type=self._socket_type)
            self._set_socket_options(self._socket)

            if requires_random_bind(self._address):
                port = self._socket.bind_to_random_port(self._address)
                self._address = "%s:%d" % (self._address, port)
            else:
                self._socket._bind_to_socket(self._address)

            self._poller_register(socket=self._socket, flags=self._poll_type)
            socked_poll_registered = True
        except zmq.ZMQError as error:
            if socked_poll_registered and self._socket is not None:
                self._poller_unregister(socket=self._socket)

            if error.errno in self.UNRECOVERABLE_ERRORS:
                raise BindFailedException(str(error))

            raise error

    def connect(self):
        connect_with_retries = self._retry_connect(self._connect)
        connect_with_retries()

    def _connect(self):
        socket_poll_registered = False
        try:
            self._socket = self._close_socket()
            self._context = self._get_or_create_context()
            self._socket = self._create_socket(context=self._context, socket_type=self._socket_type)
            self._set_socket_options(self._socket)
            self._socket.connect(self._address)
            self._poller_register(socket=self._socket, flags=self._poll_type)
            socket_poll_registered = True
        except Exception as e:
            if socket_poll_registered and self._socket is not None:
                self._poller_unregister(socket=self._socket)
            raise e

    def _set_socket_options(self, socket):
        if not self._socket_options:
            return

        for option, value in self._socket_options.items():
            socket.setsockopt(option, value)

    async def send_bytes(self, data: bytes, timeout=None):
        # timeout must be in milliseconds. None = no timeout
        timeout = timeout * 1000 if timeout is not None else (-1 if timeout is None else timeout)
        socks = await self._poller.poll(timeout=timeout)
        socks = dict(socks)
        # Data can be written to socket
        if socks.get(self._socket) == zmq.POLLOUT:
            try:
                return await self._socket.send(data, flags=0)
            except zmq.ZMQError:
                self.connect()
                return self._socket.send(data, flags=0)

        raise zmq.ZMQError(errno=errno.EAGAIN)

    async def recv_bytes(self, timeout=None) -> bytes:
        # timeout must be in milliseconds. None = no timeout
        timeout = timeout * 1000 if timeout is not None else (-1 if timeout is None else timeout)
        socks = await self._poller.poll(timeout=timeout)
        socks = dict(socks)

        # Data can be read from socket
        if socks.get(self._socket) == zmq.POLLIN:
            try:
                return await self._socket.recv(flags=0)
            except zmq.ZMQError as error:
                if error.errno == errno.EAGAIN:
                    # read timeout
                    raise error

                self.bind()

        raise zmq.ZMQError(errno=errno.EAGAIN)

    def close(self):
        """Close the zmq socket and destroy the zmq context."""
        self._socket = self._close_socket()
        self._context = self._destroy_context()

    def _get_or_create_context(self):
        return self._context if self._context is not None else zmqaio.Context(io_threads=1)

    def _destroy_context(self):
        """Destroy the zmq context."""
        if self._context is not None and not self._context.closed:
            _log.debug("Destroy context: %s", self._context)
            self._context.destroy()
        return None

    def _create_socket(self, context=None, socket_type=None):
        _log.debug("Create socket on context %s of socket type %s", context, socket_type)
        return context.socket(socket_type)

    def _close_socket(self):
        """Close the zmq socket."""
        if self._socket is not None and not self._socket.closed:
            self._poller_unregister(socket=self._socket)
            _log.debug("Closing socket: %s", self._socket)
            self._socket.close()
        return None

    @property
    def address(self):
        assert not requires_random_bind(self._address)
        return self._address

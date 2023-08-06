import logging
import os
import sys
import loguru
from typing import List

_narration_loggers_configured = {}
_narration_loggers_enabled = {}
_narration_loggers = {}


class Logger2(logging.Logger):
    def __init__(self, name, level):
        super().__init__(name, level)

    def isEnabledFor(self, level: int) -> bool:
        # Do not use logging._acquireLock.
        # Reason: baseHandler's close() tries to shutdown the BaseHandler's receive/sender thread. The thread sometimes
        # log records, which internally would call logging._acquireLock. Thereby creating a deadlock when 2 different
        # threads try to acquire the lock
        return level >= self.getEffectiveLevel()


class LoguruHandler(logging.Handler):
    def __init__(self, logger, level):
        super(LoguruHandler, self).__init__(level)
        self._logger = logger
        self.METHODS = {
            logging.NOTSET: loguru.logger.debug,
            logging.DEBUG: loguru.logger.debug,
            logging.INFO: loguru.logger.info,
            logging.WARN: loguru.logger.warning,
            logging.WARNING: loguru.logger.warning,
            logging.ERROR: loguru.logger.error,
            logging.CRITICAL: loguru.logger.critical,
        }

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            _log = self.METHODS[record.levelno]
            _log(msg)
        except Exception as e:
            self.handleError(record)


def get_debug_logger(
    name: str = None,
    env_name: str = "DEBUG",
    env_value_default: str = "0",
    env_value_enabled: str = "1",
    level=logging.DEBUG,
):
    enabled = os.environ.get(env_name, env_value_default) == env_value_enabled
    return _get_debug_logger(name=name, enabled_override=enabled, level=level)


def is_debug_logger_enabled(name: str = None):
    global _narration_loggers_enabled
    return _narration_loggers_enabled.get(name, False)


def configure_debug_loggers(names: List[str] = [], enabled: bool = None, level=logging.DEBUG):
    for name in names:
        _configure_debug_logger_once(name=name, enabled=enabled, level=level)


def _get_logger(name: str = None):
    global _narration_loggers

    logger = _narration_loggers.get(name, None)
    if logger is None:
        _logger = loguru.logger
        logger = Logger2(name=name, level=logging.NOTSET)
        _narration_loggers[name] = logger
    return logger


def _get_debug_logger(name: str = None, enabled_override: bool = None, level: int = logging.DEBUG):
    configure_debug_loggers(names=[name], enabled=enabled_override, level=level)
    return _get_logger(name=name)


def _configure_debug_logger_once(name=None, enabled: bool = None, level=logging.DEBUG):
    global _narration_loggers_configured
    global _narration_loggers_enabled
    global _narration_loggers

    logger = _get_logger(name=name)

    # Do not reconfigure if enabled has not changed
    if _narration_loggers_configured.get(name, None) is not None:
        if enabled is None:
            return
        if not enabled == logger.disabled:
            return

    logger.disabled = not enabled
    logger.setLevel(level if enabled else logging.CRITICAL)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(name)s:PID%(process)d:T%(thread)d:%(levelname)s:%(message)s"
        )

        count = len(list(_narration_loggers.keys()))
        if count == 0:
            loguru.add(sys.stderr, format="{message}", level="DEBUG")

        handler = LoguruHandler(loguru, level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info("%s _debug logger activated", name)

    _narration_loggers_configured[name] = True
    _narration_loggers_enabled[name] = enabled

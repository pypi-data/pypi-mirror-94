import logging
import attr


@attr.s(kw_only=True, frozen=True, auto_attribs=True)
class RecordPayload:
    record: logging.LogRecord = None
    handler_id: str = None

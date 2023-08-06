from typing import Dict

import msgpack

from narration._handler.common.payload.record_payload import RecordPayload
from narration._handler.common.payload.serialization.generic import (
    json_encode_log_record,
    json_decode_log_record,
)


def to_raw_record_payload(payload: RecordPayload = None) -> Dict:
    return {
        "record": json_encode_log_record(payload.record),
        "handler_id": payload.handler_id,
    }


def to_record_payload(raw_payload: Dict = None) -> RecordPayload:
    record = json_decode_log_record(raw_payload.get("record", {}))
    handler_id = raw_payload.get("handler_id")
    return RecordPayload(record=record, handler_id=handler_id)


def to_binary_payload(data: Dict = {}) -> bytes:
    return msgpack.packb(data)


def to_nonbinary_payload(data: bytes = None) -> Dict:
    return msgpack.unpackb(data)

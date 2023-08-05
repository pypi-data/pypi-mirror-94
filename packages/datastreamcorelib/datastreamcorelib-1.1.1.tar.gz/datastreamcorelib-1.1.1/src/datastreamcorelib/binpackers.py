"""Un/packing helpers."""
from typing import Any, List, Sequence, Union
import base64
import uuid

import msgpack  # type: ignore  # Get rid of error: Cannot find implementation or library stub for module


def uuid_to_b64(msgid: uuid.UUID) -> str:
    """Encode UUID to url-safe base64"""
    return base64.urlsafe_b64encode(msgid.bytes).decode("ascii")


def b64_to_uuid(instr: Union[bytes, str]) -> uuid.UUID:
    """Decode base64 to UUID object"""
    if not isinstance(instr, str):
        instr = instr.decode("ascii")
    inbytes = base64.urlsafe_b64decode(instr)
    return uuid.UUID(bytes=inbytes)


def msgpack_pack(indata: Any) -> bytes:
    """MsgPack packing with explicitly defined settings."""
    return msgpack.packb(indata, use_bin_type=True)  # type: ignore   # The module lacks hints


def msgpack_unpack(indata: bytes) -> Any:
    """MsgPack unpacking with explicitly defined settings."""
    return msgpack.unpackb(indata, raw=False)


def ensure_utf8(instr: Union[bytes, str]) -> bytes:
    """Make sure input is bytes, encode UTF-8 if not."""
    if isinstance(instr, str):
        return instr.encode("utf-8")
    return instr


def ensure_utf8_list(inlst: Union[Sequence[bytes], Sequence[str]]) -> List[bytes]:
    """Make sure all elements are bytes, see `ensure_utf8`."""
    return [ensure_utf8(item) for item in inlst]


def ensure_str(instr: Union[bytes, str]) -> str:
    """Make sure input is str, decode UTF-8 if not."""
    if isinstance(instr, bytes):
        return instr.decode("utf-8")
    return instr


def ensure_str_list(inlst: Union[Sequence[bytes], Sequence[str]]) -> List[str]:
    """Make sure all elements are str, see `ensure_str`."""
    return [ensure_str(item) for item in inlst]


def normalize_uri_topic_list(inval: Union[bytes, str, Sequence[str], Sequence[bytes]]) -> List[bytes]:
    """Normalize input to list of utf8 encoded bytes, convert input of bytes/str into single element"""
    if isinstance(inval, (str, bytes)):
        return [ensure_utf8(inval)]
    return ensure_utf8_list(inval)

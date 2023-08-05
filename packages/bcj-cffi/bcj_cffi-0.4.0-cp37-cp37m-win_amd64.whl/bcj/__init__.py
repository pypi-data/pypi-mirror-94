from typing import Union

try:
    from importlib.metadata import PackageNotFoundError  # type: ignore
    from importlib.metadata import version  # type: ignore
except ImportError:
    from importlib_metadata import PackageNotFoundError  # type: ignore
    from importlib_metadata import version  # type: ignore

__copyright__ = 'Copyright (C) 2020,2021 Hiroshi Miura'

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no-cover
    # package is not installed
    __version__ = "unknown"

from _bcj import ffi, lib  # type: ignore


class BCJFilter:

    def __init__(self, func, readahead: int, is_encoder: bool, stream_size: int = 0):
        self.is_encoder = is_encoder
        self.buffer = bytearray()
        self.state = ffi.new('UInt32 *', 0)
        self.ip = 0
        #
        self._readahead = readahead
        self.stream_size: int = stream_size
        self.method = func

    def _arm_code(self, buf, size):
        return lib.ARM_Convert(buf, size, self.ip, self.is_encoder)

    def _armt_code(self, buf, size):
        return lib.ARMT_Convert(buf, size, self.ip, self.is_encoder)

    def _sparc_code(self, buf, size):
        return lib.SPARC_Convert(buf, size, self.ip, self.is_encoder)

    def _ppc_code(self, buf, size):
        return lib.PPC_Convert(buf, size, self.ip, self.is_encoder)

    def _x86_code(self, buf, size):
        return lib.x86_Convert(buf, size, self.ip, self.state, self.is_encoder)

    def _ia64_code(self, buf, size):
        return lib.IA64_Convert(buf, size, self.ip, self.is_encoder)

    def _decode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        self.buffer.extend(data)
        size = len(self.buffer)
        buf = ffi.from_buffer(self.buffer, require_writable=True)
        out_size = self.method(buf, size)
        result = ffi.buffer(buf, out_size)
        self.ip += out_size
        self.buffer = self.buffer[out_size:]
        if self.ip >= self.stream_size - self._readahead:
            return bytes(result) + self.buffer[-self._readahead:]
        return bytes(result)

    def _encode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        self.buffer.extend(data)
        size = len(self.buffer)
        buf = ffi.from_buffer(self.buffer, require_writable=True)
        out_size = self.method(buf, size)
        result = ffi.buffer(buf, out_size)
        self.ip += out_size
        self.buffer = self.buffer[out_size:]
        return bytes(result)

    def _flush(self):
        return bytes(self.buffer)


class BCJDecoder(BCJFilter):

    def __init__(self, size: int):
        super().__init__(self._x86_code, 5, False, size)

    def decode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        return self._decode(data)


class BCJEncoder(BCJFilter):

    def __init__(self):
        super().__init__(self._x86_code, 5, True)

    def encode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        return self._encode(data)

    def flush(self):
        return self._flush()


class SparcDecoder(BCJFilter):

    def __init__(self, size: int):
        super().__init__(self._sparc_code, 4, False, size)

    def decode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        return self._decode(data)


class SparcEncoder(BCJFilter):

    def __init__(self):
        super().__init__(self._sparc_code, 4, True)

    def encode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        return self._encode(data)

    def flush(self):
        return self._flush()


class PpcDecoder(BCJFilter):

    def __init__(self, size: int):
        super().__init__(self._ppc_code, 4, False, size)

    def decode(self, data: Union[bytes, bytearray, memoryview], max_length: int = -1) -> bytes:
        return self._decode(data)


class PpcEncoder(BCJFilter):

    def __init__(self):
        super().__init__(self._ppc_code, 4, True)

    def encode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        return self._encode(data)

    def flush(self):
        return self._flush()


class ArmtDecoder(BCJFilter):

    def __init__(self, size: int):
        super().__init__(self._armt_code, 4, False, size)

    def decode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        return self._decode(data)


class ArmtEncoder(BCJFilter):

    def __init__(self):
        super().__init__(self._armt_code, 4, True)

    def encode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        return self._encode(data)

    def flush(self):
        return self._flush()


class ArmDecoder(BCJFilter):

    def __init__(self, size: int):
        super().__init__(self._arm_code, 4, False, size)

    def decode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        return self._decode(data)


class ArmEncoder(BCJFilter):

    def __init__(self):
        super().__init__(self._arm_code, 4, True)

    def encode(self, data: Union[bytes, bytearray, memoryview]) -> bytes:
        return self._encode(data)

    def flush(self):
        return self._flush()

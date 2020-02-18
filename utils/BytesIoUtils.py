from io import BytesIO


def read_one_byte(file: BytesIO) -> bytes:
    return file.read(1)


def read_unsigned_byte(file: BytesIO) -> int:
    return int(file.read(1).hex(), 16)


def read_two_bytes(file: BytesIO) -> bytes:
    return file.read(2)


def read_unsigned_short(file: BytesIO) -> int:
    return int(file.read(2).hex(), 16)


def read_four_bytes(file: BytesIO) -> bytes:
    return file.read(4)


def read_unsigned_int(file: BytesIO) -> int:
    return int(file.read(4).hex(), 16)


def read_designated_bytes(file: BytesIO, length: int):
    return file.read(length)

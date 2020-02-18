from typing import BinaryIO


def read_one_byte(file: BinaryIO) -> bytes:
    return file.read(1)


def read_unsigned_byte(file: BinaryIO) -> int:
    return int(file.read(1).hex(), 16)


def read_two_bytes(file: BinaryIO) -> bytes:
    return file.read(2)


def read_unsigned_short(file: BinaryIO) -> int:
    return int(file.read(2).hex(), 16)


def read_four_bytes(file: BinaryIO) -> bytes:
    return file.read(4)


def read_unsigned_int(file: BinaryIO) -> int:
    return int(file.read(4).hex(), 16)


def read_designated_bytes(file: BinaryIO, length: int):
    return file.read(length)

import codecs
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import BinaryIO, TypeVar, List, Generic

import utils.CalculationUtils
from utils.FileReadUtils import read_designated_bytes, read_unsigned_short


class ConstantPoolTag(Enum):
    CONSTANT_UTF8 = 1
    CONSTANT_CLASS = 7
    CONSTANT_String = 8
    CONSTANT_FIELD_REF = 9
    CONSTANT_METHOD_REF = 10
    CONSTANT_NAME_AND_TYPE = 12


class Info(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, tag) -> None:
        self.tag = tag


class Empty(Info):

    def __init__(self, tag) -> None:
        super().__init__(tag)


class Utf8(Info):

    def __init__(self, length: int, utf8_bytes: str) -> None:
        super().__init__(ConstantPoolTag.CONSTANT_UTF8)
        self.length = length
        self.bytes = utf8_bytes


class Class(Info):

    def __init__(self, name_index: int) -> None:
        super().__init__(ConstantPoolTag.CONSTANT_CLASS)
        self.name_index = name_index


class String(Info):

    def __init__(self, string_index: int) -> None:
        super().__init__(ConstantPoolTag.CONSTANT_String)
        self.string_index = string_index


class MethodRef(Info):

    def __init__(self, class_index: int, name_and_type_index: int) -> None:
        super().__init__(ConstantPoolTag.CONSTANT_METHOD_REF)
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index


class FieldRef(Info):

    def __init__(self, class_index: int, name_and_type_index: int) -> None:
        super().__init__(ConstantPoolTag.CONSTANT_FIELD_REF)
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index


class NameAndType(Info):

    def __init__(self, name_index: int, descriptor_index: int) -> None:
        super().__init__(ConstantPoolTag.CONSTANT_NAME_AND_TYPE)
        self.name_index = name_index
        self.descriptor_index = descriptor_index


T = TypeVar('T', bound=Info)


class ConstantPool(Generic[T]):

    def __init__(self, file: BinaryIO, constant_pool_count: int) -> None:
        self.file = file
        self.constant_pool_count = constant_pool_count

    @property
    def read_constant_pool(self) -> List[T]:
        constant_pool_items: List[T] = [Empty]

        for c in range(self.constant_pool_count - 1):
            tag = ConstantPoolTag(utils.CalculationUtils.hex_to_decimal(self.file.read(1).hex()))

            if tag == ConstantPoolTag.CONSTANT_UTF8:
                length = read_unsigned_short(self.file)
                designated_bytes: str = codecs.decode(read_designated_bytes(self.file, length).hex(),
                                                      'hex_codec').decode('utf-8')
                constant_pool_items.append(Utf8(length, designated_bytes))
            elif tag == ConstantPoolTag.CONSTANT_CLASS:
                name_index: int = read_unsigned_short(self.file)
                constant_pool_items.append(Class(name_index))
            elif tag == ConstantPoolTag.CONSTANT_String:
                string_index = read_unsigned_short(self.file)
                constant_pool_items.append(String(string_index))
            elif tag == ConstantPoolTag.CONSTANT_FIELD_REF:
                class_index = read_unsigned_short(self.file)
                name_and_type_index = read_unsigned_short(self.file)
                constant_pool_items.append(FieldRef(class_index, name_and_type_index))
            elif tag == ConstantPoolTag.CONSTANT_METHOD_REF:
                class_index = read_unsigned_short(self.file)
                name_and_type_index = read_unsigned_short(self.file)
                constant_pool_items.append(MethodRef(class_index, name_and_type_index))
            elif tag == ConstantPoolTag.CONSTANT_NAME_AND_TYPE:
                class_index = read_unsigned_short(self.file)
                name_and_type_index = read_unsigned_short(self.file)
                constant_pool_items.append(NameAndType(class_index, name_and_type_index))

        return constant_pool_items

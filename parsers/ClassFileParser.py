from typing import BinaryIO, TypeVar, List, Generic

from loggers.Logger import Logger
from .Attributes import Attributes, AttributeInfo
from .ConstantPool import ConstantPool, Info
from .Fields import Fields
from .Methods import Methods
from utils.FileReadUtils import read_four_bytes, read_two_bytes, read_unsigned_short

T = TypeVar('T', bound=Info)
S = TypeVar('S', bound=AttributeInfo)


class ClassFile(Generic[T, S]):

    def __init__(self, magic: bytes, minor_version: bytes, major_version: bytes, constant_pool_count: int,
                 cp_info: List[T],
                 access_flags: bytes, this_class: bytes,
                 super_class: bytes, interfaces_count: int, interfaces: [], fields_count, field_info,
                 methods_count: int, method_info,
                 attributes_count: int,
                 attribute_info: S) -> None:
        self.magic = magic
        self.minor_version = minor_version
        self.major_version = major_version
        self.constant_pool_count = constant_pool_count
        self.cp_info = cp_info
        self.access_flags = access_flags
        self.this_class = this_class
        self.super_class = super_class
        self.interfaces = interfaces
        self.interfaces_count = interfaces_count
        self.fields_count = fields_count
        self.field_info = field_info
        self.methods_count = methods_count
        self.method_info = method_info
        self.attributes_count = attributes_count
        self.attribute_info = attribute_info


def log_class_file(class_file: ClassFile):
    logger = Logger(__name__)
    logger.info("magic = {}".format(class_file.magic))
    logger.info("minor_version = {}".format(class_file.minor_version))
    logger.info("major_version = {}".format(class_file.major_version))
    logger.info("constant_pool_count = {}".format(class_file.constant_pool_count))
    for i, cp in enumerate(class_file.cp_info):
        logger.info("cp_info[{}] = {}".format(i, cp))
    logger.info("access_flags = {}".format(class_file.access_flags))
    logger.info("this_class = {}".format(class_file.this_class))
    logger.info("super_class = {}".format(class_file.super_class))
    logger.info("interfaces_count = {}".format(class_file.interfaces_count))
    logger.info("interfaces = {}".format(class_file.interfaces))
    logger.info("fields_count = {}".format(class_file.fields_count))
    for i, f in enumerate(class_file.field_info):
        logger.info("field_info[{}] = {}".format(i, f))
    logger.info("methods_count = {}".format(class_file.methods_count))
    for i, m in enumerate(class_file.method_info):
        logger.info("method_info[{}] = {}".format(i, m))
    logger.info("attributes_count = {}".format(class_file.attributes_count))
    logger.info("attribute_info = {}".format(class_file.attribute_info))


class ClassFileParser(object):
    def __init__(self, file: BinaryIO) -> None:
        self.file = file

    def read_class_file(self):
        magic = self.read_magic()
        minor_version = self.read_minor_version()
        major_version = self.read_major_version()
        constant_pool_count = self.read_constant_pool_count()
        cp_info = self.read_constant_pool(constant_pool_count)
        access_flags = self.read_access_flags()
        this_class = self.read_this_class()
        super_class = self.read_super_class()
        interfaces_count = self.read_interfaces_count()
        interfaces = self.read_interfaces(interfaces_count)
        fields_count = self.read_fields_count()
        field_info = self.read_fields(cp_info, interfaces_count)
        methods_count = self.read_methods_count()
        method_info = self.read_methods(cp_info, methods_count)
        attributes_count = self.read_attributes_count()
        attribute_info = self.read_attributes(cp_info, attributes_count)

        class_file = ClassFile(magic, minor_version, major_version, constant_pool_count, cp_info, access_flags,
                               this_class,
                               super_class,
                               interfaces_count, interfaces, fields_count, field_info, methods_count, method_info,
                               attributes_count,
                               attribute_info)

        log_class_file(class_file)
        return class_file

    def read_magic(self) -> bytes:
        return read_four_bytes(self.file)

    def read_minor_version(self) -> bytes:
        return read_two_bytes(self.file)

    def read_major_version(self) -> bytes:
        return read_two_bytes(self.file)

    def read_access_flags(self) -> bytes:
        return read_two_bytes(self.file)

    def read_this_class(self) -> bytes:
        return read_two_bytes(self.file)

    def read_super_class(self) -> bytes:
        return read_two_bytes(self.file)

    def read_interfaces_count(self) -> int:
        return read_unsigned_short(self.file)

    def read_interfaces(self, count: int):
        data = {}
        interfaces = read_two_bytes(self.file) if count != 0 else 0
        data["count"] = count
        data["interfaces"] = interfaces
        return data

    def read_constant_pool_count(self) -> int:
        return read_unsigned_short(self.file)

    def read_constant_pool(self, count: int) -> List[T]:
        constant_pool = ConstantPool(self.file, count)
        return constant_pool.read_constant_pool

    def read_fields_count(self) -> int:
        return read_unsigned_short(self.file)

    def read_fields(self, constant_pool, fields_count):
        fields = Fields(self.file, constant_pool, fields_count)
        return fields.read_fields()

    def read_methods_count(self) -> int:
        return read_unsigned_short(self.file)

    def read_methods(self, constant_pool, methods_count):
        methods = Methods(self.file, constant_pool, methods_count)
        return methods.read_methods()

    def read_attributes_count(self) -> int:
        return read_unsigned_short(self.file)

    def read_attributes(self, constant_pool, attributes_count):
        attributes = Attributes(self.file, constant_pool, attributes_count)
        return attributes.read_attribute()

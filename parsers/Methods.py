from typing import List

from parsers.Attributes import Attributes
import utils.FileReadUtils


class MethodInfo(object):

    def __init__(self, access_flags, name_index, descriptor_index, attributes_count, attribute_info) -> None:
        self.access_flags = access_flags
        self.name_index = name_index
        self.descriptor_index = descriptor_index
        self.attributes_count = attributes_count
        self.attribute_info = attribute_info


class Methods(object):
    def __init__(self, file, constant_pool, methods_count) -> None:
        self.file = file
        self.constant_pool = constant_pool
        self.methods_count = methods_count

    def read_methods(self) -> List[MethodInfo]:
        methods = []

        for c in range(self.methods_count):
            access_flags = utils.FileReadUtils.read_two_bytes(self.file)
            name_index = self.constant_pool[utils.FileReadUtils.read_unsigned_short(self.file)]
            descriptor_index = self.constant_pool[utils.FileReadUtils.read_unsigned_short(self.file)]
            attributes_count = utils.FileReadUtils.read_unsigned_short(self.file)

            attributes = Attributes(self.file, self.constant_pool, attributes_count)
            attribute_info = attributes.read_attributes()

            method = MethodInfo(access_flags, name_index, descriptor_index, attributes_count, attribute_info)
            methods.append(method)

        return methods

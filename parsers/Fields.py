from typing import List

from parsers.Attributes import Attributes
import utils.FileReadUtils


class FieldInfo(object):

    def __init__(self, access_flags, name_index, descriptor_index, attributes_count, attribute_info) -> None:
        self.access_flags = access_flags
        self.name_index = name_index
        self.descriptor_index = descriptor_index
        self.attributes_count = attributes_count
        self.attribute_info = attribute_info


class Fields(object):
    def __init__(self, file, constant_pool, fields_count) -> None:
        self.file = file
        self.constant_pool = constant_pool
        self.fields_count = fields_count

    def read_fields(self) -> List[FieldInfo]:
        fields = []

        for c in range(self.fields_count):
            access_flags = utils.FileReadUtils.read_two_bytes(self.file)
            name_index = self.constant_pool[utils.FileReadUtils.read_unsigned_short(self.file)]
            descriptor_index = self.constant_pool[utils.FileReadUtils.read_unsigned_short(self.file)]
            attributes_count = utils.FileReadUtils.read_unsigned_short(self.file)

            attributes = Attributes(self.file, self.constant_pool, attributes_count)
            attribute_info = attributes.read_attributes()

            field = FieldInfo(access_flags, name_index, descriptor_index, attributes_count, attribute_info)
            fields.append(field)

        return fields

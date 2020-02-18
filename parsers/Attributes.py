from enum import Enum

import utils.FileReadUtils


class AttributeNameIndex(Enum):
    Code = "Code"
    LineNumberTable = "LineNumberTable"
    SourceFile = "SourceFile"


class AttributeInfo(object):

    def __init__(self, attribute_name_index, attribute_length) -> None:
        self.attribute_name_index = attribute_name_index
        self.attribute_length = attribute_length


class CodeAttribute(AttributeInfo):

    def __init__(self, attribute_name_index, attribute_length, max_stack, max_locals, code_length, code,
                 exception_table_length, exception_table, attributes_count, attribute_info) -> None:
        super().__init__(attribute_name_index, attribute_length)
        self.max_stack = max_stack
        self.max_locals = max_locals
        self.code_length = code_length
        self.code = code
        self.exception_table_length = exception_table_length
        self.exception_table = exception_table
        self.attributes_count = attributes_count
        self.attribute_info = attribute_info


class LineNumberTableAttribute(AttributeInfo):

    def __init__(self, attribute_name_index, attribute_length, line_number_table_length, line_number_table) -> None:
        super().__init__(attribute_name_index, attribute_length)
        self.line_number_table_length = line_number_table_length
        self.line_number_table = line_number_table


class LineNumberTable(object):

    def __init__(self, start_pc, line_number) -> None:
        self.start_pc = start_pc
        self.line_number = line_number


class SourceFileAttribute(object):

    def __init__(self, attribute_name_index, attribute_length, sourcefile_index) -> None:
        self.attribute_name_index = attribute_name_index
        self.attribute_length = attribute_length
        self.sourcefile_index = sourcefile_index


class ExceptionTable(object):

    def __init__(self, start_pc, end_pc, handler_pc, catch_type) -> None:
        self.start_pc = start_pc
        self.end_pc = end_pc
        self.handler_pc = handler_pc
        self.catch_type = catch_type


class Attributes(object):
    def __init__(self, file, constant_pool, attributes_count) -> None:
        self.file = file
        self.constant_pool = constant_pool
        self.attributes_count = attributes_count

    def read_attributes(self):

        attributes = []
        for c in range(self.attributes_count):
            attribute = self.read_attribute()
            attributes.append(attribute)
        return attributes

    def read_attribute(self):
        utf8 = self.constant_pool[utils.FileReadUtils.read_unsigned_short(self.file)]
        attribute_name_index = AttributeNameIndex(utf8.bytes)
        attribute_length = utils.FileReadUtils.read_four_bytes(self.file)

        if attribute_name_index == AttributeNameIndex.Code:
            max_stack = utils.FileReadUtils.read_two_bytes(self.file)
            max_locals = utils.FileReadUtils.read_two_bytes(self.file)
            code_length = utils.FileReadUtils.read_unsigned_int(self.file)
            code = utils.FileReadUtils.read_designated_bytes(self.file, code_length)
            exception_table_length = utils.FileReadUtils.read_unsigned_short(self.file)

            exception_tables = []
            for c in range(exception_table_length):
                start_pc = utils.FileReadUtils.read_two_bytes(self.file)
                end_pc = utils.FileReadUtils.read_two_bytes(self.file)
                handler_pc = utils.FileReadUtils.read_two_bytes(self.file)
                catch_type = utils.FileReadUtils.read_two_bytes(self.file)
                exception_table = ExceptionTable(start_pc, end_pc, handler_pc, catch_type)
                exception_tables.append(exception_table)

            code_attribute_attributes_count = utils.FileReadUtils.read_unsigned_short(self.file)
            attribute_info = []
            for c1 in range(code_attribute_attributes_count):
                attribute = self.read_attribute()
                attribute_info.append(attribute)

            code_attribute = CodeAttribute(attribute_name_index, attribute_length, max_stack, max_locals,
                                           code_length, code,
                                           exception_table_length, exception_tables,
                                           code_attribute_attributes_count,
                                           attribute_info)
            return code_attribute
        elif attribute_name_index == AttributeNameIndex.LineNumberTable:
            line_number_table_length = utils.FileReadUtils.read_unsigned_short(self.file)

            line_number_tables = []
            for c in range(line_number_table_length):
                start_pc = utils.FileReadUtils.read_two_bytes(self.file)
                line_number = utils.FileReadUtils.read_two_bytes(self.file)
                line_number_table = LineNumberTable(start_pc, line_number)
                line_number_tables.append(line_number_table)
            line_number_table_attribute = LineNumberTableAttribute(attribute_name_index, attribute_length,
                                                                   line_number_table_length, line_number_tables)
            return line_number_table_attribute
        elif attribute_name_index == AttributeNameIndex.SourceFile:
            sourcefile_index = self.constant_pool[utils.FileReadUtils.read_unsigned_short(self.file)]
            sourcefile_attribute = SourceFileAttribute(attribute_name_index, attribute_length, sourcefile_index)

            return sourcefile_attribute
        else:
            return None

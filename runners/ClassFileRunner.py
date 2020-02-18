from enum import Enum
from importlib import import_module
from io import BytesIO
from typing import List

import parsers.ClassFileParser
from parsers.Attributes import CodeAttribute
from parsers.ConstantPool import String, FieldRef, MethodRef, Utf8
from parsers.Methods import MethodInfo
from utils.BytesIoUtils import read_unsigned_byte, read_unsigned_short


class Opcode(Enum):
    ALOAD_0 = "2a"
    INVOKE_SPECIAL = "b7"
    NOP = "00"
    ACONST_NULL = "01"
    RETURN = "b1"
    GET_STATIC = "b2"
    LDC = "12"
    INVOKE_VIRTUAL = "b6"


class ClassFileRunner(object):

    def __init__(self, class_file: parsers.ClassFileParser.ClassFile) -> None:
        self.class_file = class_file

    def run(self):
        operand_stack = []
        constant_pool = self.class_file.cp_info
        methods: List[MethodInfo] = self.class_file.method_info

        for method in methods:
            for attribute in method.attribute_info:
                if type(attribute) == CodeAttribute:
                    code_attribute: CodeAttribute = attribute
                    code = BytesIO(code_attribute.code)

                    for byte in iter(lambda: code.read(1), b''):
                        op_code = Opcode(byte.hex())

                        if op_code == Opcode.ALOAD_0:
                            break
                        elif op_code == Opcode.NOP:
                            break
                        elif op_code == Opcode.INVOKE_SPECIAL:
                            break
                        elif op_code == Opcode.ACONST_NULL:
                            break
                        elif op_code == Opcode.RETURN:
                            break
                        elif op_code == Opcode.GET_STATIC:
                            constant_pool_index = read_unsigned_short(code)
                            data = constant_pool[constant_pool_index]
                            if type(data) == FieldRef:
                                class_info = constant_pool[data.class_index]
                                callee_class = constant_pool[class_info.name_index].bytes

                                name_and_type = constant_pool[data.name_and_type_index]

                                # out
                                field = constant_pool[name_and_type.name_index].bytes
                                # フィールドの型情報
                                method_return = constant_pool[name_and_type.descriptor_index].bytes

                                class_path_list = callee_class.split('/')
                                class_name = class_path_list[-1]
                                class_path = "packages." + ".".join(class_path_list[:-1])

                                mod = import_module(class_path + "." + class_name)
                                field_val = getattr(getattr(mod, class_name), field)

                                val = {
                                    "path": field_val,
                                    "return": method_return
                                }
                                operand_stack.append(val)

                        elif op_code == Opcode.LDC:
                            constant_pool_index = read_unsigned_byte(code)
                            data = constant_pool[constant_pool_index]
                            if type(data) == String:
                                value = constant_pool[data.string_index]
                                if type(value) == Utf8:
                                    value = value.bytes
                                operand_stack.append(value)
                        elif op_code == Opcode.INVOKE_VIRTUAL:
                            constant_pool_index = read_unsigned_short(code)
                            data = constant_pool[constant_pool_index]
                            if type(data) == MethodRef:
                                method_ref = data

                                name_and_type = constant_pool[method_ref.name_and_type_index]
                                method_name = constant_pool[name_and_type.name_index].bytes

                                argument_string = constant_pool[name_and_type.descriptor_index].bytes
                                argument_size = len(argument_string.split(";")) - 1

                                argument = []

                                for _ in range(argument_size):
                                    argument.append(operand_stack.pop())

                                method = operand_stack.pop()

                                getattr(method["path"], method_name)(*argument)

                        else:
                            raise RuntimeError("Unknown Opcode!")

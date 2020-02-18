import sys

import parsers
from runners.ClassFileRunner import ClassFileRunner


def run(class_file_name):
    with open(class_file_name + ".class", 'rb') as file:
        parser = parsers.ClassFileParser.ClassFileParser(file)
        class_file = parser.read_class_file()
        runner = ClassFileRunner(class_file)
        runner.run()


if __name__ == '__main__':
    args = sys.argv
    run(args[1])

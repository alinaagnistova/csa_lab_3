from collections import namedtuple
from enum import Enum
import json

class Opcode(str,Enum):
    #поток программы
    HLT = "halt"
    JMP = "jmp"
    JZ = "jz"
    #регистры
    MOV = "mov"
    STORE = "store"
    #арифметика
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"
    #сравнения
    EQ = "equals"
    NE = "negative"
    LT = "left"
    GT = "right"
    #ввод вывод
    INPUT = "input"
    OUTPUT = "output"
    def __repr__(self):
        """Переопределение стандартного поведения `__str__` для `Enum`: вместо
        `Opcode.INC` вернуть `increment`.
        """
        return f"'{self.value}'"

def write_code(filename, code):
    with open(filename, "w", encoding='utf-8') as file:
        # for i in code:
            # file.write(str(i) + "\n")
        file.write(json.dumps(code, indent=4))
def read_code(filename):
    with open(filename, encoding='utf-8') as file:
        code = json.loads(file.read())
    for instr in code:
        instr['opcode'] = Opcode(instr['opcode'])
    return code
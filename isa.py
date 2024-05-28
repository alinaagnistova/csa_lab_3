from collections import namedtuple
from enum import Enum
import json
#todo bin_code
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
        return f"'{self.value}'"

def write_json_code(filename, code):
    with open(filename, "w", encoding='utf-8') as file:
        file.write(json.dumps(code, indent=4))
def read_json_code(filename):
    with open(filename, encoding='utf-8') as file:
        code = json.loads(file.read())
    for instr in code:
        instr['opcode'] = Opcode(instr['opcode'])
    return code
def write_bin_code(filename, code):
    with open(filename, "wb") as file:
        for instr in code:
            opcode = instr['opcode'].value
            arg1 = instr.get('arg1', 0)
            arg2 = instr.get('arg2', 0)
            # Кодируем инструкцию в 32-битное целое число
            binary_instruction = (Opcode[opcode].value << 24) | (arg1 << 12) | arg2
            # Пишем инструкцию в файл
            file.write(binary_instruction.to_bytes(4, byteorder='big', signed=False))
def read_bin_code(filename):
    code = []
    with open(filename, "rb") as file:
        while True:
            bytes_read = file.read(4)
            if not bytes_read:
                break
            # Конвертируем байты обратно в инструкцию
            binary_instruction = int.from_bytes(bytes_read, byteorder='big', signed=False)
            opcode_num = (binary_instruction >> 24) & 0xFF
            arg1 = (binary_instruction >> 12) & 0xFFF
            arg2 = binary_instruction & 0xFFF
            opcode = Opcode._value2member_map_[opcode_num]  # Используем маппинг номера на член Enum
            instr = {
                'opcode': opcode,
                'arg1': arg1,
                'arg2': arg2
            }
            code.append(instr)
    return code
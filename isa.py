import logging
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
    JE = "je" #jump if equals
    JNE = "jne" # jump if not equals
    JL = "jl" #jump if less
    JG = "jg" #jump if greater
    #IO
    INPUT = "input"
    OUTPUT = "output"
    def __repr__(self):
        return f"'{self.value}'"
    """
    As program memory is 16-bit, only last byte is represented, first is 0x00
    Opcodes can be divided into groups:
    1. Program flow     - starts with 1
    2. Stack operations - starts with 01
    3. Arithmetics      - starts with 0001
    4. IO               - starts with 00001
    5. Regs              - starts with 001
    """
BinOpcodes = dict(halt=0b10000000, jmp=0b10000010, jz=0b10000011, mov=0b01000010, store=0b01000011,add=0b00010010,sub=0b00010011,mul=0b00010100,div=0b00010101,mod=0b00010110,je=0b10000100,jne=0b10000101,jl=0b10000110,jg=0b10000111,input=0b00001000,output=0b00001001)

BinRegs = dict(rx1=0b00100000,rx2=0b00100001,rx3=0b00100010,rx4=0b00100100,rx5=0b00101000,rx6=0b00110000,rx7=0b00110001,rx8=0b00110010,rx9=0b00110100,rx10=0b00111000,rx11=0b00111001,rx12=0b00111010,rx13=0b00111100,rx14=0b00111101,rx15=0b00111110)
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
            opcode_bin = BinOpcodes[instr['opcode'].value]
            if 'arg1' in instr:
                arg1_bin = BinRegs[instr['arg1']] if instr['arg1'] in BinRegs else 0
            else:
                arg1_bin = 0
            if 'arg2' in instr:
                if isinstance(instr['arg2'], str) and instr['arg2'] in BinRegs:
                    arg2_bin = BinRegs[instr['arg2']]
                else:
                    arg2_bin = int(instr['arg2'])
            else:
                arg2_bin = 0
            binary_instruction = (opcode_bin << 24) | (arg1_bin << 12) | arg2_bin & 0xFFF
            print(binary_instruction.to_bytes(4, byteorder='big', signed=False))
            file.write(binary_instruction.to_bytes(4, byteorder='big', signed=False))
            # arg1 = instr.get('arg1', 0)
            # arg2 = instr.get('arg2', 0)
            # Кодируем инструкцию в 32-битное целое число
            # binary_instruction = (Opcode[opcode].value << 24) | (arg1 << 12) | arg2
            # Пишем инструкцию в файл
            # file.write(binary_instruction.to_bytes(4, byteorder='big', signed=False))
def read_bin_code(filename):
    code = []
    with open(filename, "rb") as file:
        while True:
            bytes_read = file.read(4)
            if not bytes_read:
                break
            # Конвертируем 4 байта в 32-битное целое число
            binary_instruction = int.from_bytes(bytes_read, byteorder='big', signed=False)

            # Извлекаем опкод
            opcode_num = (binary_instruction >> 24) & 0xFF
            # Найдем строковое представление опкода
            try:
                opcode = next(key for key, value in BinOpcodes.items() if value == opcode_num)
            except StopIteration:
                # Если опкод не найден, выводим ошибку и номер неправильного опкода
                logging.error(f"Unknown opcode: {opcode_num:#04x} at position {file.tell() - 4}")
                continue
                # todo
                # opcode = next(key for key, value in BinOpcodes.items() if value == opcode_num)

            # Извлекаем аргументы
            arg1_bin = (binary_instruction >> 12) & 0xFFF
            arg2_bin = binary_instruction & 0xFFF

            # Преобразуем числовые представления аргументов обратно в идентификаторы регистров или оставляем как есть
            arg1 = next(key for key, value in BinRegs.items() if
                        value == arg1_bin) if arg1_bin in BinRegs.values() else arg1_bin
            arg2 = next(key for key, value in BinRegs.items() if
                        value == arg2_bin) if arg2_bin in BinRegs.values() else arg2_bin

            # Создаем словарь для инструкции
            instr = {
                'opcode': opcode,
                'arg1': arg1,
                'arg2': arg2
            }
            code.append(instr)

    return code
    # code = []
    # with open(filename, "rb") as file:
    #     while True:
    #         bytes_read = file.read(4)
    #         if not bytes_read:
    #             break
    #         # Конвертируем байты обратно в инструкцию
    #         binary_instruction = int.from_bytes(bytes_read, byteorder='big', signed=False)
    #         opcode_num = (binary_instruction >> 24) & 0xFF
    #         arg1 = (binary_instruction >> 12) & 0xFFF
    #         arg2 = binary_instruction & 0xFFF
    #         opcode = Opcode._value2member_map_[opcode_num]  # Используем маппинг номера на член Enum
    #         instr = {
    #             'opcode': opcode,
    #             'arg1': arg1,
    #             'arg2': arg2
    #         }
    #         code.append(instr)
    # return code
#4 байта опкоду 4 байта й арг 4 байта арг
# расшифровка

import logging
import os
from collections import namedtuple
from enum import Enum
import json


class Opcode(str, Enum):
    # поток программы
    HLT = "halt"
    JMP = "jmp"
    JZ = "jz"
    # регистры
    MOV = "mov"
    STORE = "store"
    # арифметика
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"
    # сравнения
    JE = "je"  # jump if equals
    JNE = "jne"  # jump if not equals
    JL = "jl"  # jump if less
    JG = "jg"  # jump if greater
    # IO
    INPUT = "input"
    OUTPUT = "output"

    def __repr__(self):
        return f"'{self.value}'"


BinOpcodes = {
    "halt": 0b1100000000000000,
    "jmp": 0b1100000100000000,
    "jz": 0b1100001000000000,
    "mov": 0b1100001100000000,
    "store": 0b1100010000000000,
    "add": 0b1100010100000000,
    "sub": 0b1100011000000000,
    "mul": 0b1100011100000000,
    "div": 0b1100100000000000,
    "mod": 0b1100100100000000,
    "je": 0b1100101000000000,
    "jne": 0b1100101100000000,
    "jl": 0b1100110000000000,
    "jg": 0b1100110100000000,
    "input": 0b1100111000000000,
    "output": 0b1100111100000000,
}
# 24 bit
BinRegs = {
    "rx0": 0b10100000 << 16,
    "rx1": 0b10100001 << 16,
    "rx2": 0b10100010 << 16,
    "rx3": 0b10100100 << 16,
    "rx4": 0b10101000 << 16,
    "rx5": 0b10110000 << 16,
    "rx6": 0b10110001 << 16,
    "rx7": 0b10110010 << 16,
    "rx8": 0b10110100 << 16,
    "rx9": 0b10111000 << 16,
    "rx10": 0b10111001 << 16,
    "rx11": 0b10111010 << 16,
    "rx12": 0b10111100 << 16,
    "rx13": 0b10111101 << 16,
    "rx14": 0b10111110 << 16,
    "rx15": 0b10111111 << 16,
}


def write_json_code(filename, code):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(json.dumps(code, indent=4))


def read_json_code(filename):
    with open(filename, encoding="utf-8") as file:
        code = json.loads(file.read())
    for instr in code:
        instr["opcode"] = Opcode(instr["opcode"])
    return code


def write_bin_code(filename, code):
    with open(filename, "wb") as file:
        for instr in code:
            opcode_bin = BinOpcodes[instr["opcode"].value]
            if "arg1" in instr:
                arg1_bin = BinRegs[instr["arg1"]] if instr["arg1"] in BinRegs else 0
            else:
                arg1_bin = 0
            if "arg2" in instr:
                if isinstance(instr["arg2"], str) and instr["arg2"] in BinRegs:
                    arg2_bin = BinRegs[instr["arg2"]]
                else:
                    arg2_bin = int(instr["arg2"])
            else:
                arg2_bin = 0
            binary_instruction = (opcode_bin << 48) | (arg1_bin << 24) | arg2_bin
            binary_instruction.to_bytes(8, byteorder="big", signed=False)
            file.write(binary_instruction.to_bytes(8, byteorder="big", signed=False))


def read_bin_code(filename):
    code = []
    with open(filename, "rb") as file:
        while True:
            bytes_read = file.read(8)
            if not bytes_read:
                break
            binary_instruction = int.from_bytes(
                bytes_read, byteorder="big", signed=False
            )
            opcode_num = (binary_instruction >> 48) & 0xFFFF
            try:
                opcode = next(
                    key for key, value in BinOpcodes.items() if value == opcode_num
                )
            except StopIteration:
                logging.error(
                    f"Unknown opcode: {opcode_num:#04x} at position {file.tell() - 8}"
                )
                continue

            arg1_bin = (binary_instruction >> 24) & 0xFFFFFF
            arg2_bin = binary_instruction & 0xFFFFFF

            arg1 = (
                next(key for key, value in BinRegs.items() if value == arg1_bin)
                if arg1_bin in BinRegs.values()
                else arg1_bin
            )
            arg2 = (
                next(key for key, value in BinRegs.items() if value == arg2_bin)
                if arg2_bin in BinRegs.values()
                else arg2_bin
            )

            instr = {"opcode": opcode, "arg1": arg1, "arg2": arg2}
            code.append(instr)
    return code

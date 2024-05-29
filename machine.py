import logging

from isa import Opcode


class DataPath:
    def __init__(self, data_mem_size, instr_mem_size, input_buffer):
        self.data_mem = [0] * data_mem_size
        self.instr_mem = [None] * instr_mem_size
        self.zero_flag = False #
        self.output_buffer = []
        self.input_buffer = input_buffer
        self.stack = [0] * data_mem_size
        self.val_to_mov = 0
        self.registers = {
            'rx0': 0x0,  # Регистр, постоянно хранящий 0
            'rx1': 0x0,  # Регистр текущей инструкции
            'rx2': 0x0,  # Data address
            'rx3': 0,  # Регистры данных
            'rx4': 0,
            'rx5': 0,
            'rx6': 0,
            'rx7': 0,
            'rx8': 0,
            'rx9': 0,
            'rx10': 0,
            'rx11': 0,
            'rx12': 0,
            'rx13': 0,
            'rx14': data_mem_size - 1,  # stack pointer
            'rx15': 0  # jmp_arg
        }
    def zero(self, result):
        if result == 0:
            self.zero_flag = True

    def output(self, reg, string_mode):
        ch = 0
        if string_mode == 1:
            ch = chr(self.registers.get(reg))
        else:
            ch = self.registers.get(reg)
        logging.info('output: %s << %s', repr(self.output_buffer), repr(ch))
        self.output_buffer.append(ch)

    def write(self, reg):
        self.data_mem[self.registers.get('rx2')] = self.registers.get(reg)

    def input(self):
        if len(self.input_buffer) == 0:
            raise EOFError()
        ch = self.input_buffer.pop(0)
        self.data_mem[self.registers.get('rx2')] = ord(ch)

    def latch_register(self, reg):
        self.registers[reg] = self.val_to_mov

    def latch_program_counter(self, sel_next):
        if sel_next:
            self.registers['rx1'] += 1
        else:
            self.registers['rx1'] = self.val_to_mov

        assert self.registers['rx1'] < len(self.data_mem), "Out of instruction memory: {}".format(self.registers['rx1'])

    def latch_data_mem_counter(self, sel_next):
        if sel_next:
            self.registers['rx2'] += 1
        else:
            self.registers['rx2'] = self.val_to_mov

        assert self.registers['rx2'] < len(self.instr_mem), "Out of data memory: {}".format(self.registers['rx2'])


class ALU:
    def __init__(self, data_path):
        self.data_path = data_path
    def add(self, left, right):
        res = int(left) + int(right)
        self.data_path.set_flags(res)
        return res

    def sub(self, left, right):
        res = int(left) - int(right)
        self.data_path.set_flags(res)
        return res

    def mul(self, left, right):
        res = int(left) * int(right)
        self.data_path.set_flags(res)
        return res

    def div(self, left, right):
        res = int(left) // int(right)
        self.data_path.set_flags(res)
        return res
    def mod(self, left, right):
        res = int(left) % int(right)
        self.data_path.set_flags(res)
        return res
class ControlUnit:
    def __init__(self, program, data_path, alu):
        self.program = program
        self.data_path = data_path
        self.alu = alu
        self._tick = 0
    def tick(self):
        self._tick += 1
    def get_curr_tick(self):
        return self._tick
    def load_program(self):
        for i in range(0, len(self.program)):
            self.data_path.instr_mem[i] = self.program[i]
    def decode_and_execute_instruction(self):
        cur_instr = self.data_path.instr_mem[self.data_path.registers.get("rx1")]
        opcode = cur_instr['opcode']
        jmp_instr = False #todo
        #todo match case?
        if opcode is Opcode.HLT:
            raise StopIteration()
        if opcode is Opcode.MOV:
            self.tick()
        if opcode is Opcode.STORE:
            self.tick()
        if opcode is Opcode.JMP:
            self.tick()
        if opcode is Opcode.JZ:
            self.tick()
        if opcode in {Opcode.ADD, Opcode.DIV, Opcode.MOD, Opcode.SUB,Opcode.MUL}:
            self.tick()
        if opcode in {Opcode.NE, Opcode.EQ, Opcode.GT, Opcode.LT}:
            self.tick()
        if opcode is Opcode.INPUT:
            self.tick()
        if opcode is Opcode.OUTPUT:
            self.tick()



import logging

from isa import Opcode


class DataPath:
    def __init__(self, data_mem_size, instr_mem_size, input_buffer):
        self.data_mem = [0] * data_mem_size
        self.instr_mem = [None] * instr_mem_size
        self.zero_flag = False
        self.neg_flag = False
        self.output_buffer = []
        self.input_buffer = input_buffer
        self.val_to_mov = 0  # можно передавать через функцию
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
            'rx14': 0,
            'rx15': 0  # jmp_arg
        }

    def set_flags(self, result):
        if result == 0:
            self.zero_flag = True
        if result < 0:
            self.neg_flag = True

    def drop_flags(self):
        self.zero_flag = False
        self.neg_flag = False

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
        jmp_instr = False
        # todo match case?
        if opcode is Opcode.HLT:
            raise StopIteration()
        if opcode is Opcode.MOV:
            if cur_instr['arg2'] == "rx2":
                self.data_path.val_to_ld = self.data_path.data_mem[self.data_path.registers.get("rx2")]
            else:
                self.data_path.val_to_ld = cur_instr['arg2']
            self.tick()

            self.data_path.latch_register(cur_instr['arg1'])
            self.tick()
        if opcode is Opcode.STORE:
            self.data_path.write(cur_instr['arg1'])
            self.tick()
            self.data_path.latch_data_mem_counter(True)
            self.tick()
        if opcode is Opcode.JMP:
            self.data_path.val_to_ld = self.data_path.registers.get("rx15")
            self.data_path.latch_program_counter(False)
            self.tick()
            jmp_instr = True
        if opcode is Opcode.JZ:
            self.tick()
        if opcode in {Opcode.ADD, Opcode.DIV, Opcode.MOD, Opcode.SUB, Opcode.MUL}:
            res_reg = cur_instr['arg1']
            if opcode is Opcode.ADD:
                self.data_path.val_to_ld = self.alu.add(self.data_path.registers.get(res_reg),
                                                        self.data_path.registers.get(cur_instr['arg2']))
            if opcode is Opcode.SUB:
                self.data_path.val_to_ld = self.alu.sub(self.data_path.registers.get(res_reg),
                                                        self.data_path.registers.get(cur_instr['arg2']))
            if opcode is Opcode.MUL:
                self.data_path.val_to_ld = self.alu.mul(self.data_path.registers.get(res_reg),
                                                        self.data_path.registers.get(cur_instr['arg2']))
            if opcode is Opcode.DIV:
                self.data_path.val_to_ld = self.alu.div(self.data_path.registers.get(res_reg),
                                                        self.data_path.registers.get(cur_instr['arg2']))
            if opcode is Opcode.MOD:
                self.data_path.val_to_ld = self.alu.mod(self.data_path.registers.get(res_reg),
                                                        self.data_path.registers.get(cur_instr['arg2']))
            self.tick()

            self.data_path.latch_register(res_reg)
            self.tick()
        if opcode in {Opcode.JE, Opcode.JG, Opcode.JL, Opcode.JNE}:
            arg1 = self.data_path.registers.get(cur_instr['arg1'])
            arg2 = self.data_path.registers.get(cur_instr['arg2'])
            self.alu.sub(arg1, arg2)
            self.tick()
            self.data_path.val_to_ld = self.data_path.registers.get("rx15")
            if opcode is Opcode.JE:
                if self.data_path.zero_flag:
                    self.data_path.latch_program_counter(False)
                    jmp_instr = True
            if opcode is Opcode.JG:
                if not self.data_path.zero_flag and not self.data_path.neg_flag:
                    self.data_path.latch_program_counter(False)
                    jmp_instr = True
            if opcode is Opcode.JL:
                if not self.data_path.zero_flag and self.data_path.neg_flag:
                    self.data_path.latch_program_counter(False)
                    jmp_instr = True
            if opcode is Opcode.JNE:
                if not self.data_path.zero_flag:
                    self.data_path.latch_program_counter(False)
                    jmp_instr = True
            self.tick()

        if opcode is Opcode.INPUT:
            self.data_path.input()
            self.tick()
            self.data_path.latch_data_mem_counter(True)
            self.tick()
        if opcode is Opcode.OUTPUT:
            self.data_path.output(cur_instr['arg1'], cur_instr['arg2'])
            self.tick()
        self.data_path.drop_flags()
        self.tick()
        if not jmp_instr:
            self.data_path.latch_program_counter(True)
            self.tick()
def __repr__(self):
    return "{{TICK: {}, RX1: {}, RX2: {}, RX3: {}, RX4: {}, RX5: {}, RX6: {}, RX7: {}, RX8: {}, RX9: {}, " \
           "RX10: {}, RX11: {}, RX12: {}, RX13: {}, RX14: {}, RX15: {}}}" \
        .format(self._tick,
                self.data_path.registers.get(
                    "rx1"),
                self.data_path.registers.get(
                    "rx2"),
                self.data_path.registers.get(
                    "rx3"),
                self.data_path.registers.get(
                    "rx4"),
                self.data_path.registers.get(
                    "rx5"),
                self.data_path.registers.get(
                    "rx6"),
                self.data_path.registers.get(
                    "rx7"),
                self.data_path.registers.get(
                    "rx8"),
                self.data_path.registers.get(
                    "rx9"),
                self.data_path.registers.get(
                    "rx10"),
                self.data_path.registers.get(
                    "rx11"),
                self.data_path.registers.get(
                    "rx12"),
                self.data_path.registers.get(
                    "rx13"),
                self.data_path.registers.get(
                    "rx14"),
                self.data_path.registers.get(
                    "rx15"),
                )
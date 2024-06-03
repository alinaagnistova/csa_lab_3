import logging
import sys

from isa import Opcode, read_bin_code

class DataPath:
    def __init__(self, data_mem_size, instr_mem_size, input_buffer):
        self.data_mem = [0] * data_mem_size
        self.instr_mem = [None] * instr_mem_size
        self.zero_flag = False
        self.neg_flag = False
        self.output_buffer = []
        self.input_buffer = input_buffer
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
        if ch != chr(0):
            self.output_buffer.append(ch)
            logging.info('output: %s << %s', repr(self.output_buffer), repr(ch))

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
        if opcode == Opcode.HLT.value:
            raise StopIteration()
        if opcode == Opcode.MOV.value:
            if cur_instr['arg2'] == "rx2":
                self.data_path.val_to_mov = self.data_path.data_mem[self.data_path.registers.get("rx2")]
            else:
                if cur_instr['arg2'] in self.data_path.registers:
                    self.data_path.val_to_mov = self.data_path.registers.get(cur_instr['arg2'])
                else:
                    self.data_path.val_to_mov = cur_instr['arg2']
            self.tick()

            self.data_path.latch_register(cur_instr['arg1'])
            self.tick()
        if opcode == Opcode.STORE.value:
            self.data_path.write(cur_instr['arg1'])
            self.tick()

            self.data_path.latch_data_mem_counter(True)
            self.tick()

        if opcode == Opcode.JMP.value:
            self.data_path.val_to_mov = self.data_path.registers.get("rx15")
            self.data_path.latch_program_counter(False)
            self.tick()
            jmp_instr = True
        if opcode == Opcode.JZ.value:
            self.tick()
        if opcode in {Opcode.ADD.value, Opcode.DIV.value, Opcode.MOD.value, Opcode.SUB.value, Opcode.MUL.value}:
            res_reg = cur_instr['arg1']
            if opcode == Opcode.ADD.value:
                self.data_path.val_to_mov = self.alu.add(self.data_path.registers.get(res_reg),
                                                        self.data_path.registers.get(cur_instr['arg2']))
            if opcode == Opcode.SUB.value:
                self.data_path.val_to_mov = self.alu.sub(self.data_path.registers.get(res_reg),
                                                        self.data_path.registers.get(cur_instr['arg2']))
            if opcode == Opcode.MUL.value:
                self.data_path.val_to_mov = self.alu.mul(self.data_path.registers.get(res_reg),
                                                        self.data_path.registers.get(cur_instr['arg2']))
            if opcode == Opcode.DIV.value:
                self.data_path.val_to_mov = self.alu.div(self.data_path.registers.get(res_reg),
                                                        self.data_path.registers.get(cur_instr['arg2']))
            if opcode == Opcode.MOD.value:
                self.data_path.val_to_mov = self.alu.mod(self.data_path.registers.get(res_reg),
                                                        self.data_path.registers.get(cur_instr['arg2']))
            self.tick()

            self.data_path.latch_register(res_reg)
            self.tick()

        if opcode in {Opcode.JE.value, Opcode.JG.value, Opcode.JL.value, Opcode.JNE.value}:
            arg1 = self.data_path.registers.get(cur_instr['arg1'])
            arg2 = self.data_path.registers.get(cur_instr['arg2'])
            self.alu.sub(arg1, arg2)
            self.tick()
            self.data_path.val_to_mov = self.data_path.registers.get("rx15")
            if opcode == Opcode.JE.value:
                if self.data_path.zero_flag:
                    self.data_path.latch_program_counter(False)
                    jmp_instr = True
            if opcode == Opcode.JG.value:
                if not self.data_path.zero_flag and not self.data_path.neg_flag:
                    self.data_path.latch_program_counter(False)
                    jmp_instr = True
            if opcode == Opcode.JL.value:
                if not self.data_path.zero_flag and self.data_path.neg_flag:
                    self.data_path.latch_program_counter(False)
                    jmp_instr = True
            if opcode == Opcode.JNE.value:
                if not self.data_path.zero_flag:
                    self.data_path.latch_program_counter(False)
                    jmp_instr = True
            self.tick()

        if opcode == Opcode.OUTPUT.value:
            self.data_path.output(cur_instr['arg1'], cur_instr['arg2'])
            self.tick()

        if opcode == Opcode.INPUT.value:
            self.data_path.input()
            self.tick()

            self.data_path.latch_data_mem_counter(True)
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

def simulation(code, input_token, instr_limit, iter_limit):
    data_path = DataPath(2048, instr_limit, input_token)
    alu = ALU(data_path)
    control_unit = ControlUnit(code, data_path, alu)
    instr_counter = 0
    try:
        control_unit.load_program()
    except IndexError:
        logging.error("Too many instructions. Please, increase size of instruction memory.")

    try:
        while True:
            assert iter_limit > instr_counter, "Too many iterations. " \
                                               "Please, increase iteration limit or correct your program."
            control_unit.decode_and_execute_instruction()
            instr_counter += 1
            logging.debug(repr(control_unit))
    except EOFError:
        logging.info('Input buffer is empty!')
    except StopIteration:
        instr_counter += 1
        pass
    return control_unit.data_path.output_buffer, control_unit.get_curr_tick(), instr_counter


def main(args):
    assert len(args) == 2, "Wrong amount of arguments. Please, read instruction carefully."
    code_file, input_file = args
    input_token = ""
    if input_file != "":
        with open(input_file, encoding="utf-8") as file:
            input_text = file.read()
            input_token = []
            for ch in input_text:
                input_token.append(ch)
            input_token.append(chr(0))

    code = read_bin_code(code_file)
    output, ticks, instr_amount = simulation(code, input_token, instr_limit=2048, iter_limit=100000000)
    logging.info("output:  %s, ticks: %s", repr(output), repr(ticks))
    print("Output buffer: {} | ticks: {} | amount_instr: {}".format(
        ''.join(map(str, output)),
        repr(ticks),
        repr(instr_amount))
    )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    main(sys.argv[1:])

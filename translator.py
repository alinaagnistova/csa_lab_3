import re

from isa import write_code, Opcode
import sys
from typing import Dict, Set
data_address = 0x0
instr_address = 0x0
res_code = []
var_address = []
variables = []
reg_counter = 3 #todo, cause 0-2 supposed to be special regs, but I have only one now (rx2)
def update_reg_data(): #todo
    global reg_counter
    reg_counter+=1
    if reg_counter > 15:
        reg_counter = 3
def get_reg_data(): #todo
    global reg_counter
    if reg_counter == 3:
        return 11
    else:
        return reg_counter - 1
def keywords():
    return {"int", "string", "while", "if","input", "print"}
def comparison_words():
    return {">", "<", ">=", "<=", "==", "!="}
def binary_words():
    return {"*", "/", "%", "+", "-"}
def symbols():
    return {"(", ")","{","}","=", "\""}
def symbol2opcode(symbol):
    return{
        'mov': Opcode.MOV,
        'store': Opcode.STORE,
        'input': Opcode.INPUT,
        'print': Opcode.OUTPUT,
        'jmp': Opcode.JMP,
        'jz': Opcode.JZ,
        '>': Opcode.GT,
        '<': Opcode.LT,
        '==': Opcode.EQ,
        '%': Opcode.MOD,
        '-': Opcode.SUB,
        '+': Opcode.ADD,
        '!=': Opcode.NE,
        '/': Opcode.DIV,
        '*': Opcode.MUL,
    }.get(symbol)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self):
        return f"Token(type='{self.type}', value='{self.value}')"
def parse(filename):
    with open(filename, encoding="utf-8") as file:
        code = file.read()
    code = code.split("\n")
    return code
def tokenize(parsed_code):
    tokens = []
    code = re.findall(r'\w+|[^\s\w]', parsed_code)
    print(code)
    for word in code:
        if word in keywords():
            tokens.append(Token('KEYWORD', word))
        elif word.isdigit():
            tokens.append(Token('NUMBER', float(word)))
        elif word in binary_words():
            tokens.append(Token('BINARY', word))
        elif word in comparison_words():
            tokens.append(Token('COMPARE', word))
        elif word in symbols():
            tokens.append(Token('SYMBOL', word))
        elif re.match(r'^".*"$', word):
            tokens.append(Token('VAR_STRING', word))
        else:
            tokens.append(Token('NAME_STRING', word))
    return tokens

def translate(filename):
    code = parse(filename)
    tokens = tokenize(code)
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type == 'KEYWORD' and (token.value == 'int' or token.value == 'string') and tokens[i+2] == '=':
            i = parse_alloc(tokens, i)
        elif token.type == 'KEYWORD' and token.value == 'if':
            i = parse_alloc(tokens, i)
        elif token.type == 'KEYWORD' and token.value == 'while':
            i = parse_alloc(tokens,i)
        elif token.type == 'KEYWORD' and token.value == 'input':
            i = parse_input(tokens,i)
        elif token.type == 'KEYWORD' and token.value == 'print':
            i = parse_print(tokens, i)
        else:
            i+=1
    return res_code


def parse_alloc(tokens, i):
    global data_address
    reg_name = "rx" + str(reg_counter)
    name = tokens[i+1].value
    if tokens[i].value == 'int':
        add_var_to_map(name, 'int')
        add_mov_instr(reg_name, tokens[i+3].value)
        add_store_instr(reg_name)
        update_reg_data()
    elif tokens[i].value == 'string':
        add_var_to_map(name, 'string')
        string_value = tokens[i + 3].value.strip("\"")
        for char in string_value:
            add_mov_instr(reg_name, ord(char))
            add_store_instr(reg_name)
            update_reg_data()
    return i + 5


# def parse_assign(line):
    # line = line.replace(';', '').split()
    # result = {'opcode': Opcode.STORE}
    # if len(line) == 3:
    #     if is_num_in_arg(line[2]):
    #         add_mov_instr('rx' + str(reg_counter), line[2])
    #         update_reg_data()
    #         result.update({
    #             'arg1': 'rx' + str(get_reg_data())
    #         })
    #     else:
    #         result.update({
    #             'arg1': 'rx' + str(mov_var(get_var_address(line[2])))
    #         })
    # else:
    #     result.update({
    #         'arg1': #parse_extra_action(row[2:])todo
    #     })
    # add_mov_instr('rx2', get_var_address(line[0]))
    # return result
def is_num_in_arg(line):
    try:
        float(line)
        return True
    except ValueError:
        return False
def parse_input(tokens, i):
    global instr_address
    input_name = tokens[i+2].value
    add_mov_instr("rx2", get_var_address(input_name))
    res_code.append({'opcode': Opcode.INPUT})
    instr_address += 1
    return i+4
def parse_print(tokens, i):
    print_name = tokens[i+2].value
    output(print_name)
    return i+4
def parse_operation(line):
    parse_comparison(line)
    parse_body(line)
def parse_comparison(line):
    print("hi")
def parse_body(line):
    print("hi")
def parse_while(line):
    print("hi")
def parse_if(line):
    print("hi")


def output(variable): #todo how to print num and string, whats the diff?
    global instr_address
    for var in var_address:
        if var['name'] == variable:
            reg_to_print = mov_var(var['addr'])
            if var['type'] == 'string':
                res_code.append({'opcode': Opcode.OUTPUT, 'arg1': 'rx' + str(reg_to_print), 'arg2': 1})
            else:
                res_code.append({'opcode': Opcode.OUTPUT, 'arg1': 'rx' + str(reg_to_print), 'arg2': 0})
            update_reg_data()
            instr_address += 1

def add_store_instr(reg):
    global instr_address, data_address
    res_code.append({'opcode': Opcode.STORE, 'arg1': reg})
    instr_address += 1
    data_address += 1

def add_mov_instr(reg, val):
    res_code.append({'opcode': Opcode.MOV, 'arg1': reg, 'arg2': val})
    #address_instr_mem += 1
    #todo smth else needed here?
def get_var_address(name):
    for var in var_address:
        if var['name'] == name:
            return var['addr']

def add_var_to_map(name, type):
    variables.add(name)
    var = {
        'addr': data_address,
        'name': name,
        'type': type
    }
    var_address.append(var)
def mov_var(addr):
    add_mov_instr('rx2', addr)
    reg_data = 'rx' + str(reg_counter)
    add_mov_instr(reg_data,'rx2')
    #todo change_data_reg()
    return #todo get_prev_data_reg()

def main():
    code = """int n = 6
        print(i)"""
    code_d = translate(code)
    print(code_d)

if __name__ == '__main__':
    main()
import re

from isa import write_code, Opcode
import sys
from typing import Dict, Set
#todo it seems i need to rewrite parse_expression and parse_operation
data_address = 0x0
instr_address = 0x0
res_code = []
var_address = []
variables = set()
reg_counter = 3  # todo, cause 0-2 supposed to be special regs, but I have only one now (rx2)
jmp_stack = []
last_operation = ''

def update_reg_data():  # todo
    global reg_counter
    print(f"Updating register from {reg_counter}", end=' ')
    reg_counter += 1
    if reg_counter > 15:
        reg_counter = 3
    print(f"to {reg_counter}")


def get_reg_data():  # todo
    global reg_counter
    if reg_counter == 3:
        return 11
    else:
        return reg_counter - 1


def keywords():
    return {"int", "string", "while", "if", "input", "print"}


def comparison_words():
    return {">", "<", ">=", "<=", "==", "!="}


def binary_words():
    return {"*", "/", "%", "+", "-"}


def symbols():
    return {"(", ")", "{", "}", "="}


def symbol2opcode(symbol):
    return {
        'halt': Opcode.HLT,
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
    # with open(filename, encoding="utf-8") as file:
    #     code = file.read()
    coded = filename
    code = coded.split("\n")
    return " ".join(code)


def tokenize(parsed_code):
    tokens = []
    code = re.findall(r'\".*?\"|\w+|[^\s\w]+', parsed_code) #r'\w+|[^\s\w]'
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
        elif re.match(r'^".*"$', word): #r'^".*"$'
            tokens.append(Token('VAR_STRING', word))
        else:
            tokens.append(Token('NAME_STRING', word))
    return tokens


def translate(filename):
    global instr_address
    code = parse(filename)
    tokens = tokenize(code)
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type == 'KEYWORD' and (token.value == 'int' or token.value == 'string') and tokens[i + 2].value == '=':
            i = parse_alloc(tokens, i)
        elif token.type == 'NAME_STRING' and tokens[i + 1].value == '=':
            i = parse_assign(tokens, i)
        elif token.type == 'KEYWORD' and token.value == 'if':
            jmp_stack.append({'com_addr': instr_address, 'arg': 0, 'type': 'if'})
            add_mov_instr('rx15',0) #todo why rx15?
            res_code.append(parse_condition(tokens[i:]))
            while i < len(tokens) and tokens[i].value != '{':
                i += 1
            # i += 1
            instr_address += 1
        elif token.type == 'KEYWORD' and token.value == 'while':
            jmp_stack.append({'com_addr': instr_address, 'arg': 0, 'type': 'while'})
            print("Stack after push:", jmp_stack)
            add_mov_instr('rx15',0)
            res_code.append(parse_condition(tokens[i:]))
            # parse_expression(tokens)
            while i < len(tokens) and tokens[i].value != '{':
                i += 1
            # i += 1
            instr_address += 1
        elif token.type == 'KEYWORD' and token.value == 'input':
            i = parse_input(tokens, i)
        elif token.type == 'KEYWORD' and token.value == 'print':
            i = parse_print(tokens, i)
        elif token.type == 'SYMBOL' and token.value == '}':
            print(f"Stack before pop: {jmp_stack}")
            jmp_arg = jmp_stack.pop()
            if jmp_arg['type'] == 'while':
                add_mov_instr("rx15", jmp_arg["com_addr"])
                res_code.append({'opcode': symbol2opcode("jmp")})
                instr_address += 1
                res_code[jmp_arg["com_addr"]].update({'arg2': instr_address})
                i += 1
            elif jmp_arg['type'] == 'if':
                res_code[jmp_arg["com_addr"]].update({'arg2': instr_address})
                i += 1
        else:
            i += 1
    res_code.append({'opcode': symbol2opcode("halt")})
    instr_address += 1
    return res_code


def parse_alloc(tokens, i):
    global data_address
    reg_name = "rx" + str(reg_counter)
    name = tokens[i + 1].value
    if tokens[i].value == 'int':
        add_var_to_map(name, 'int')
        add_mov_instr(reg_name, tokens[i + 3].value)
        add_store_instr(reg_name)
        update_reg_data()
    elif tokens[i].value == 'string':
        add_var_to_map(name, 'string')
        string_value = tokens[i + 3].value.strip("\"")
        for char in string_value:
            add_mov_instr(reg_name, ord(char))
            add_store_instr(reg_name)
            update_reg_data()
    return i + 4


def parse_assign(tokens, i):
    result = {'opcode': Opcode.STORE}
    name = tokens[i].value
    value = tokens[i+2]
    if value.type == 'int':
        add_mov_instr('rx'+ str(reg_counter), value.value)
        update_reg_data()
        result.update({
            'arg1': 'rx' + str(get_reg_data())
        })
    elif value.type == 'NAME_STRING':
        result.update({
            'arg1': 'rx' + str(mov_var(get_var_address(value.value)))
        })
    else:
        result.update({
            'arg1': parse_expression(tokens[i+2:])
        })
    add_mov_instr('rx2', get_var_address(name))
    res_code.append(result)
    return i + 3 #todo what if expression complicated
def is_num_in_arg(line):
    try:
        float(line)
        return True
    except ValueError:
        return False


def parse_input(tokens, i):
    global instr_address
    input_name = tokens[i + 2].value
    add_mov_instr("rx2", get_var_address(input_name))
    res_code.append({'opcode': Opcode.INPUT})
    instr_address += 1
    return i + 4


def parse_print(tokens, i):
    print_name = tokens[i + 2].value
    output(print_name)
    return i + 4


# def parse_operation(tokens, i):
#     result = {
#         'opcode': None,
#         'arg1': 0,
#         'arg2': 0,
#     }
#     if tokens[i].type == 'KEYWORD' and tokens[i].value in ['if', 'while']:
#         global parsed_tokens
#         left = []
#         right = []
#         idx = 0
#         j = 0
#         parsed_tokens = tokens[i + 1:]
#         while j < len(parsed_tokens):
#             token = parsed_tokens[j]
#             if token.type == 'COMPARE':
#                 idx = j
#                 left = parsed_tokens[:j]
#                 right = parsed_tokens[j+1:]
#         if len(left) > 1:
#             result.update({'arg1': parse_expression(left)})
#         else:
#             if left[0] in variables:
#                 reg = 'rx' + str(mov_var(get_var_address(left[0])))
#                 result.update({'arg1': reg})
#             elif is_num_in_arg(left[0]):
#                 add_mov_instr("rx" + str(reg_counter), int(left[0]))
#                 result.update({'arg1': "rx" + str(reg_counter)})
#                 update_reg_data()
#         if len(right) > 1:
#             result.update({'arg2': parse_expression(right)})
#         else:
#             if right[0] in variables:
#                 reg = 'rx' + str(mov_var(get_var_address(right[0])))
#                 result.update({'arg1': reg})
#             elif is_num_in_arg(right[0]):
#                 add_mov_instr("rx" + str(reg_counter), int(right[0]))
#                 result.update({'arg2': "rx" + str(reg_counter)})
#                 update_reg_data()
#     result.update({'opcode': symbol2opcode(parsed_tokens[idx].value)})
#
#         # parse_comparison(tokens, i+1)
#     # parse_body(tokens, i)


# def parse_comparison(tokens, i):
#     global instr_address,reg_counter
#     start = i + 1
#     end = start
#     depth = 1
#     while depth > 0 and end < len(tokens):
#         if tokens[end].value == '(':
#             depth += 1
#         elif tokens[end].value == ')':
#             depth -= 1
#         end += 1
#     end -= 1
#     condition_tokens = tokens[start:end]
#     parse_expression(condition_tokens)
#     return end
def parse_extra_action(tokens):
    global instr_address
    result = {'opcode': None}
    if tokens[1].type == 'BINARY':
        result.update({
            'opcode': symbol2opcode(tokens[1].value)
        })
        if is_num_in_arg(tokens[0].value):
            add_mov_instr('rx' + str(reg_counter), tokens[0].value)
            update_reg_data()
            result.update({'arg1': 'rx' + str(reg_counter - 1)})
        else:
            result.update({'arg1': 'rx' + str(mov_var(get_var_address(tokens[0].value)))})
        if is_num_in_arg(tokens[2].value):
            add_mov_instr('rx' + str(reg_counter), tokens[2].value)
            update_reg_data()
            result.update({'arg1': 'rx' + str(reg_counter - 1)})
        else:
            result.update({'arg1': 'rx' + str(mov_var(get_var_address(tokens[2].value)))})
        res_code.append(result)
        instr_address += 1
    else:
        result = {
            'opcode': symbol2opcode(tokens[1].value),
            'arg1': tokens[0].value,
            'arg2': tokens[2].value
        }
        res_code.append(result)
        instr_address += 1
    return result.get('arg1')
def parse_condition(tokens):
    global instr_address
    token_to_remove = ['(', ')', 'if', 'while']
    parsed_tokens = [token for token in tokens if token.value not in token_to_remove]
    i = 0  # Начальный индекс поиска
    while i < len(parsed_tokens) and parsed_tokens[i].value not in ['{', '}']:
        i += 1
    # tokens до i - это токены условия
    condition_tokens = parsed_tokens[:i]
    result = {
        'opcode': None,
        'arg1': 0,
        'arg2': 0,
    }
    if condition_tokens:
        left = []
        right = []
        idx = 0
        while idx < len(condition_tokens):
            if condition_tokens[idx].type == 'COMPARE':
                left.extend(condition_tokens[:idx])
                right.extend(condition_tokens[idx + 1:])
                print(condition_tokens[:idx])
            idx += 1
        if idx < len(condition_tokens):
            comparison_op = condition_tokens[idx]
            right = condition_tokens[idx + 1:]
        # for i in range(0, len(tokens)):
        #     if tokens[i].type == 'BINARY':
        #         idx = i
        #         left = tokens[:i]
        #         right = tokens[i+1:]
        if len(left) > 1:
            result.update({'arg1': parse_extra_action(left)})
        else:
            if left[0].value in variables:
                reg = 'rx' + str(mov_var(get_var_address(left[0].value)))
                result.update({'arg1': reg})
            elif is_num_in_arg(left[0].value):
                add_mov_instr("rx" + str(reg_counter), int(left[0].value))
                result.update({'arg1': "rx" + str(reg_counter)})
                update_reg_data()
        if len(right) > 1:
            result.update({'arg2': parse_extra_action(right)})
        else:
            if right[0].value in variables:
                reg = 'rx' + str(mov_var(get_var_address(right[0].value)))
                result.update({'arg1': reg})
            elif is_num_in_arg(right[0].value):
                add_mov_instr("rx" + str(reg_counter), int(right[0].value))
                result.update({'arg2': "rx" + str(reg_counter)})
                update_reg_data()
        result.update({'opcode': symbol2opcode(tokens[idx].value)})
    return result


def parse_expression(tokens):
    global instr_address
    reg_stack = []
    op_stack = []
    # i = start
    def apply_operator():
        global instr_address
        """Функция для применения оператора к двум последним операндам в стеке."""
        operator_token = op_stack.pop()
        right = reg_stack.pop() if reg_stack else 'rx0'
        left = reg_stack.pop() if reg_stack else 'rx0'
        operator = symbol2opcode(operator_token.value)
        res_code.append({'opcode': operator, 'arg1': left, 'arg2': right})
        update_reg_data()
        instr_address += 1
        return 'rx' + str(get_reg_data() - 1)

    i = 0
    while i < len(tokens) and tokens[i].value != '{':
        token = tokens[i]
        if token.type == 'NUMBER' or token.type == 'NAME_STRING':
            if token.type == 'NUMBER':
                if is_num_in_arg(token.value):
                    reg = 'rx' + str(reg_counter)
                    add_mov_instr(reg, token.value)
                    update_reg_data()
                    reg_stack.append(reg)
            else:
                reg = 'rx' + str(mov_var(get_var_address(token.value)))
                reg_stack.append(reg)
        elif token.type in ['BINARY', 'COMPARE']:
            while (op_stack and op_stack[-1].type != 'SYMBOL' and precedence(op_stack[-1].value) >= precedence(token.value)):
                apply_operator()
            op_stack.append(token)
        i+=1
    while op_stack:
        apply_operator()
    return reg_stack[-1] if reg_stack else 'rx0', i  # Ensure we skip the '{' by not incrementing i here



def precedence(op):
    """Returns the precedence of the operators."""
    return {
        '+': 1, '-': 1,
        '*': 2, '/': 2, '%': 2,
        '==': 3, '!=': 3, '>': 3, '<': 3, '>=': 3, '<=': 3
    }.get(op, 0)



def output(variable):
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
    global instr_address
    res_code.append({'opcode': Opcode.MOV, 'arg1': reg, 'arg2': val})
    instr_address += 1
    # todo smth else needed here?


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
    add_mov_instr(reg_data, 'rx2')
    update_reg_data()
    return get_reg_data()


def main():
    code = """ int x = 0
    if (x > 2) {
    print(x)
    }
            """
    code_d = translate(code)
    print(code_d)


if __name__ == '__main__':
    main()

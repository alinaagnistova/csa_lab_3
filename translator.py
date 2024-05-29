import re, sys
# todo why we dont use jz, check it tmrw!!!!!!!!!!!!!!
# todo delete desparating types int, string
from isa import write_json_code, Opcode

data_address = 0x0
instr_address = 0x0
res_code = []
var_address = []
variables = set()
reg_counter = 3
jmp_stack = []
jz_stack = []


def update_reg_data():
    global reg_counter
    reg_counter += 1
    if reg_counter > 13:
        reg_counter = 3


def get_reg_data():
    global reg_counter
    if reg_counter == 3:
        return 13
    else:
        return reg_counter - 1


def keywords():
    return {"int", "string", "while", "if", "input", "print"}


def comparison_words():
    return {">", "<", ">=", "<=", "==", "!="}


def binary_words():
    return {"*", "/", "%", "+", "-"}


def symbols():
    return {"(", ")", "{", "}", "=", ";"}


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
    code = filename
    code = code.split("\n")
    return " ".join(code)


def tokenize(parsed_code):
    tokens = []
    code = re.findall(r'\".*?\"|\w+|[^\s\w]+', parsed_code)
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
    global instr_address
    code = parse(filename)
    tokens = tokenize(code)
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type == 'KEYWORD' and (token.value == 'int' or token.value == 'string') and tokens[i + 2].value == '=':
            i = parse_alloc(tokens, i)
        elif token.type == 'NAME_STRING' and tokens[i + 1].value == '=':
            end = i + 2
            while end < len(tokens) and tokens[end].value != ';':
                end += 1
            i = parse_assign(tokens[i:end], i)
        elif token.type == 'KEYWORD' and token.value == 'if':
            jmp_stack.append({'com_addr': instr_address, 'arg': 0, 'type': 'if'})
            add_mov_instr('rx15', 0)
            res_code.append(parse_condition(tokens[i:]))
            while i < len(tokens) and tokens[i].value != '{':
                i += 1
            instr_address += 1
        elif token.type == 'KEYWORD' and token.value == 'while':
            jmp_stack.append({'com_addr': instr_address, 'arg': 0, 'type': 'while'})
            add_mov_instr('rx15', 0)
            res_code.append(parse_condition(tokens[i:]))
            while i < len(tokens) and tokens[i].value != '{':
                i += 1
            instr_address += 1
        elif token.type == 'KEYWORD' and token.value == 'input':
            i = parse_input(tokens, i)
        elif token.type == 'KEYWORD' and token.value == 'print':
            i = parse_print(tokens, i)
        elif token.type == 'SYMBOL' and token.value == '}':
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
            add_mov_instr('rx' + str(reg_counter), ord(char))
            update_reg_data()
            add_var_to_map(name, 'string')
            add_store_instr('rx' + str(get_reg_data()))
    return i + 4


def parse_assign(tokens, i):
    result = {'opcode': Opcode.STORE}
    name = tokens[0].value
    # value = tokens[2]
    # print("name", name)
    # print("value", value)
    if len(tokens) == 3:
        if is_num_in_arg(tokens[2].value):
            add_mov_instr('rx' + str(reg_counter), tokens[2].value)
            update_reg_data()
            result.update({
                'arg1': 'rx' + str(get_reg_data())
            })
        elif tokens[2].type == 'NAME_STRING':
            result.update({
                'arg1': 'rx' + str(mov_var(get_var_address(tokens[2].value)))
            })
    else:
        result.update({
            'arg1': parse_complex_expr(tokens[2:])
        })
    add_mov_instr('rx2', get_var_address(name))
    res_code.append(result)
    return i + len(tokens)  # todo what if expression complicated (i + 3)


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


def parse_complex_expr(tokens):
    global instr_address, reg_counter
    if len(tokens) < 3:
        return 'rx0'  # default register in case of parsing error or empty expression

    # Stack for operands (registers or immediate values)
    operand_stack = []
    operator_stack = []

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type in ['NUMBER', 'NAME_STRING']:
            if is_num_in_arg(token.value):
                reg_name = 'rx' + str(reg_counter)
                add_mov_instr(reg_name, token.value)
                update_reg_data()
                operand_stack.append(reg_name)
            else:
                var_reg = 'rx' + str(mov_var(get_var_address(token.value)))
                operand_stack.append(var_reg)
        elif token.type == 'BINARY':
            while (operator_stack and precedence(operator_stack[-1]) >= precedence(token.value)):
                perform_operation(operand_stack, operator_stack)
            operator_stack.append(token.value)
        i += 1

    # Process any remaining operations
    while operator_stack:
        perform_operation(operand_stack, operator_stack)

    return operand_stack[-1] if operand_stack else 'rx0'  # Return the last register holding the result


def perform_operation(operand_stack, operator_stack):
    right = operand_stack.pop() if len(operand_stack) > 0 else 'rx0'
    left = operand_stack.pop() if len(operand_stack) > 0 else 'rx0'
    operator = operator_stack.pop()
    result_reg = 'rx' + str(reg_counter)
    opcode = symbol2opcode(operator)
    add_mov_instr(result_reg, left)
    res_code.append({'opcode': opcode, 'arg1': left, 'arg2': right})
    update_reg_data()
    operand_stack.append(result_reg)


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
            result.update({'arg2': 'rx' + str(reg_counter - 1)})
        else:
            result.update({'arg2': 'rx' + str(mov_var(get_var_address(tokens[2].value)))})
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
    i = 0
    while i < len(parsed_tokens) and parsed_tokens[i].value not in ['{', '}']:
        i += 1
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


# def parse_expression(tokens):
#     global instr_address, reg_counter
#     result = {
#         'opcode': None
#     }
#     operand_stack = []
#     operator_stack = []
#
#     def apply_operation():
#         global instr_address
#         right = operand_stack.pop()
#         left = operand_stack.pop()
#         operator = operator_stack.pop()
#         opcode = symbol2opcode(operator.value)
#         temp_reg = 'rx' + str(reg_counter)
#         add_mov_instr(temp_reg, left)
#         update_reg_data()
#         result_reg = 'rx' + str(reg_counter - 1)
#
#         add_mov_instr(result_reg, right)
#         res_code.append({
#             'opcode': opcode,
#             'arg1': temp_reg,
#             'arg2': result_reg
#         })
#         instr_address += 1
#
#         # Помещаем результат обратно в стек операндов
#         operand_stack.append(result_reg)
#
#     i = 0
#     while i < len(tokens):
#         token = tokens[i]
#         if token.type == 'NUMBER':
#             add_mov_instr('rx' + str(reg_counter), token.value)
#             update_reg_data()
#             result.update({'arg1': 'rx' + str(reg_counter - 1)})
#         elif token.type == 'NAME_STRING':
#             result.update({'arg2': 'rx' + str(mov_var(get_var_address(token.value)))})
#         elif token.type == 'BINARY':
#             operator_stack.append(token.value)
#             result.update({
#                 'opcode': symbol2opcode(token.value)
#             })
#             while (operator_stack and precedence(operator_stack[-1].value) >= precedence(token.value)):
#                 # result = {
#                 #     'opcode': symbol2opcode(token.value),
#                 #     'arg1': part_to_parse[0],
#                 #     'arg2': part_to_parse[2]
#                 # }
#                 res_code.append(result)
#                 instr_address += 1
#             # operator_stack.append(token)
#         i += 1
#
#     # Применяем оставшиеся операции
#     # while operator_stack:
#     #     apply_operation()
#
#     return result.get('arg1')
#     global instr_address, reg_counter
#     reg_stack = []
#     op_stack = []
#     def apply_operator():
#         global instr_address
#         operator_token = op_stack.pop()
#         right = reg_stack.pop() if reg_stack else 'rx0'
#         print("right:" , right)
#         left = reg_stack.pop() if reg_stack else 'rx0'
#         print("left:" , left)
#         operator = symbol2opcode(operator_token.value)
#         res_code.append({'opcode': operator, 'arg1': left, 'arg2': right})
#         print("opeartor", {'opcode': operator, 'arg1': left, 'arg2': right})
#         update_reg_data()
#         instr_address += 1
#         return 'rx' + str(get_reg_data() - 1)
#
#     i = 0
#     while i < len(tokens):
#         token = tokens[i]
#         if token.type == 'NUMBER' or token.type == 'NAME_STRING':
#             if token.type == 'NUMBER':
#                 if is_num_in_arg(token.value):
#                     reg = 'rx' + str(reg_counter)
#                     add_mov_instr(reg, token.value)
#                     update_reg_data()
#                     reg_stack.append(reg)
#             else:
#                 reg = 'rx' + str(mov_var(get_var_address(token.value)))
#                 reg_stack.append(reg)
#         elif token.type in ['BINARY', 'COMPARE']:
#             while (op_stack and op_stack[-1].type != 'SYMBOL' and precedence(op_stack[-1].value) >= precedence(token.value)):
#                 apply_operator()
#             op_stack.append(token)
#         i+=1
#     while op_stack:
#         apply_operator()
#     return reg_stack[-1] if reg_stack else 'rx0'  # Ensure we skip the '{' by not incrementing i here


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


# todo write_bin_code
def main():  # args
    code = """int n = 0;
    n = 4;
                """
    code_d = translate(code)
    print(code_d)
    # assert len(args) == 2, "Wrong arguments"
    # source, target = args
    # opcodes = translate(source)
    # write_json_code(target, opcodes)


if __name__ == '__main__':
    # main(sys.argv[1:])
    main()

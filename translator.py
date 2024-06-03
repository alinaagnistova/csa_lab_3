import re
import sys
from isa import Opcode, write_bin_code

data_address = 0x0
instr_address = 0x0
res_code = []
mnemonics = []
var_address = []
variables = set()
reg_counter = 3
jmp_stack = []
jz_stack = []


def update_reg_data():
    global reg_counter
    reg_counter += 1
    if reg_counter > 14:
        reg_counter = 3


def get_reg_data():
    if reg_counter == 3:
        return 14
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
        "halt": Opcode.HLT,
        "mov": Opcode.MOV,
        "store": Opcode.STORE,
        "input": Opcode.INPUT,
        "print": Opcode.OUTPUT,
        "jmp": Opcode.JMP,
        "jz": Opcode.JZ,
        ">": Opcode.JL,
        "<": Opcode.JG,
        "==": Opcode.JNE,
        "%": Opcode.MOD,
        "-": Opcode.SUB,
        "+": Opcode.ADD,
        "!=": Opcode.JE,
        "/": Opcode.DIV,
        "*": Opcode.MUL,
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
    # code = filename
    code = code.split("\n")
    return " ".join(code)


def tokenize(parsed_code):
    tokens = []
    code = re.findall(r"\".*?\"|\w+|[^\s\w]+", parsed_code)
    for word in code:
        if word in keywords():
            tokens.append(Token("KEYWORD", word))
        elif word.isdigit():
            tokens.append(Token("NUMBER", float(word)))
        elif word in binary_words():
            tokens.append(Token("BINARY", word))
        elif word in comparison_words():
            tokens.append(Token("COMPARE", word))
        elif word in symbols():
            tokens.append(Token("SYMBOL", word))
        elif re.match(r'^".*"$', word):
            tokens.append(Token("VAR_STRING", word))
        else:
            tokens.append(Token("NAME_STRING", word))
    return tokens


def translate(filename):
    global instr_address
    code = parse(filename)
    tokens = tokenize(code)
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if (
            token.type == "KEYWORD"
            and (token.value == "int" or token.value == "string")
            and tokens[i + 2].value == "="
        ):
            i = parse_alloc(tokens, i)
        elif token.type == "NAME_STRING" and tokens[i + 1].value == "=":
            end = i + 2
            while end < len(tokens) and tokens[end].value != ";":
                end += 1
            i = parse_assign(tokens[i:end], i)
            instr_address += 1
        elif token.type == "KEYWORD" and token.value == "if":
            jmp_stack.append({"com_addr": len(res_code), "arg": 0, "type": "if"})
            add_mov_instr("rx15", 0)
            condition_tokens = extract_condition(tokens, i)
            res_code.append(parse_condition(condition_tokens))
            instr_address += 1
            while i < len(tokens) and tokens[i].value != "{":
                i += 1
        elif token.type == "KEYWORD" and token.value == "while":
            jmp_stack.append({"com_addr": len(res_code), "arg": 0, "type": "while"})
            add_mov_instr("rx15", 0)
            res_code.append(parse_condition(tokens[i:]))
            while i < len(tokens) and tokens[i].value != "{":
                i += 1
            instr_address += 1
        elif token.type == "KEYWORD" and token.value == "input":
            i = parse_input(tokens, i)
        elif token.type == "KEYWORD" and token.value == "print":
            i = parse_print(tokens, i)
        elif token.type == "SYMBOL" and token.value == "}":
            jmp_arg = jmp_stack.pop()
            if jmp_arg["type"] == "while":
                add_mov_instr("rx15", jmp_arg["com_addr"])
                res_code.append({"opcode": symbol2opcode("jmp")})
                instr_address += 1
                res_code[jmp_arg["com_addr"]].update({"arg2": len(res_code)})
                i += 1
            elif jmp_arg["type"] == "if":
                res_code[jmp_arg["com_addr"]].update({"arg2": len(res_code)})
                i += 1
        else:
            i += 1
    res_code.append({"opcode": symbol2opcode("halt")})
    mnemonics.append("halt")
    instr_address += 1
    return res_code, mnemonics


def extract_condition(tokens, start_idx):
    condition_tokens = []
    i = start_idx
    while i < len(tokens) and tokens[i].value != "{":
        condition_tokens.append(tokens[i])
        i += 1
    return condition_tokens


def parse_alloc(tokens, i):
    global data_address
    reg_name = "rx" + str(reg_counter)
    name = tokens[i + 1].value
    if tokens[i].value == "int":
        add_var_to_map(name, "int")
        add_mov_instr(reg_name, tokens[i + 3].value)
        add_store_instr(reg_name)
        update_reg_data()
        mnemonics.append(f"mov {reg_name} {tokens[i + 3].value}")
        mnemonics.append(f"store {reg_name}")
    elif tokens[i].value == "string":
        string_value = tokens[i + 3].value.strip('"') + chr(0)
        for char in string_value:
            add_mov_instr("rx" + str(reg_counter), ord(char))
            update_reg_data()
            add_var_to_map(name, "string")
            add_store_instr("rx" + str(get_reg_data()))
            mnemonics.append(f"mov {str(reg_counter)} {ord(char)}")
            mnemonics.append(f"store rx{str(get_reg_data())}")
    return i + 4


def parse_assign(tokens, i):
    result = {"opcode": Opcode.STORE}
    name = tokens[0].value
    if len(tokens) == 3:
        if is_num_in_arg(tokens[2].value):
            add_mov_instr("rx" + str(reg_counter), tokens[2].value)
            update_reg_data()
            result.update({"arg1": "rx" + str(get_reg_data())})
        elif tokens[2].type == "NAME_STRING":
            result.update(
                {"arg1": "rx" + str(mov_var(get_var_address(tokens[2].value)))}
            )
    else:
        result.update({"arg1": parse_complex_expr(tokens[2:])})
    add_mov_instr("rx2", get_var_address(name))
    res_code.append(result)
    mnemonics.append("halt")
    return i + len(tokens)


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
    mnemonics.append("input")
    res_code.append({"opcode": Opcode.INPUT})
    instr_address += 1
    return i + 4


def parse_print(tokens, i):
    print_name = tokens[i + 2].value
    var_out(print_name)
    return i + 4


def parse_complex_expr(tokens):
    global instr_address
    if len(tokens) < 3:
        return "rx0"
    operand_stack = []
    operator_stack = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type in ["NUMBER", "NAME_STRING"]:
            if is_num_in_arg(token.value):
                reg_name = "rx" + str(reg_counter)
                add_mov_instr(reg_name, token.value)
                update_reg_data()
                operand_stack.append(reg_name)
            else:
                var_reg = "rx" + str(mov_var(get_var_address(token.value)))
                operand_stack.append(var_reg)
        elif token.type == "BINARY":
            while operator_stack and precedence(operator_stack[-1]) >= precedence(
                token.value
            ):
                perform_operation(operand_stack, operator_stack)
            operator_stack.append(token.value)
        i += 1
    while operator_stack:
        perform_operation(operand_stack, operator_stack)

    return operand_stack[-1] if operand_stack else "rx0"


def perform_operation(operand_stack, operator_stack):
    right = operand_stack.pop() if len(operand_stack) > 0 else "rx0"
    left = operand_stack.pop() if len(operand_stack) > 0 else "rx0"
    operator = operator_stack.pop()
    result_reg = "rx" + str(reg_counter)
    opcode = symbol2opcode(operator)
    mnemonics.append(f"{opcode} {left} {right}")
    res_code.append({"opcode": opcode, "arg1": left, "arg2": right})
    add_mov_instr(result_reg, left)
    update_reg_data()
    operand_stack.append(result_reg)


def parse_extra_action(tokens):
    global instr_address
    result = {"opcode": None}
    if tokens[1].type == "BINARY":
        result.update({"opcode": symbol2opcode(tokens[1].value)})
        if is_num_in_arg(tokens[0].value):
            add_mov_instr("rx" + str(reg_counter), tokens[0].value)
            update_reg_data()
            result.update({"arg1": "rx" + str(reg_counter - 1)})
        else:
            result.update(
                {"arg1": "rx" + str(mov_var(get_var_address(tokens[0].value)))}
            )
        if is_num_in_arg(tokens[2].value):
            add_mov_instr("rx" + str(reg_counter), tokens[2].value)
            update_reg_data()
            result.update({"arg2": "rx" + str(reg_counter - 1)})
        else:
            result.update(
                {"arg2": "rx" + str(mov_var(get_var_address(tokens[2].value)))}
            )
        mnemonics.append(f"{result['opcode']} {result['arg1']} {result['arg2']}")
        res_code.append(result)
        instr_address += 1
    else:
        result = {
            "opcode": symbol2opcode(tokens[1].value),
            "arg1": tokens[0].value,
            "arg2": tokens[2].value,
        }
        mnemonics.append(
            f"{symbol2opcode(tokens[1].value)} {tokens[0].value} {tokens[2].value}"
        )
        res_code.append(result)
        instr_address += 1
    return result.get("arg1")


def parse_condition(tokens):
    global instr_address
    token_to_remove = ["(", ")", "if", "while"]
    parsed_tokens = [token for token in tokens if token.value not in token_to_remove]
    i = 0
    while i < len(parsed_tokens) and parsed_tokens[i].value not in ["{", "}"]:
        i += 1
    condition_tokens = parsed_tokens[:i]
    result = {
        "opcode": None,
        "arg1": 0,
        "arg2": 0,
    }
    if condition_tokens:
        left = []
        right = []
        idx = 0
        while idx < len(condition_tokens):
            if condition_tokens[idx].type == "COMPARE":
                left.extend(condition_tokens[:idx])
                right.extend(condition_tokens[idx + 1 :])
            idx += 1
        if idx < len(condition_tokens):
            right = condition_tokens[idx + 1 :]
        if len(left) > 1:
            result.update({"arg1": parse_extra_action(left)})
        else:
            if left[0].value in variables:
                reg = "rx" + str(mov_var(get_var_address(left[0].value)))
                result.update({"arg1": reg})
            elif is_num_in_arg(left[0].value):
                add_mov_instr("rx" + str(reg_counter), int(left[0].value))
                result.update({"arg1": "rx" + str(reg_counter)})
                update_reg_data()
        if len(right) > 1:
            result.update({"arg2": parse_extra_action(right)})
        else:
            if right[0].value in variables:
                reg = "rx" + str(mov_var(get_var_address(right[0].value)))
                result.update({"arg1": reg})
            elif is_num_in_arg(right[0].value):
                add_mov_instr("rx" + str(reg_counter), int(right[0].value))
                result.update({"arg2": "rx" + str(reg_counter)})
                update_reg_data()
            elif right[0].value == '"0"':
                result.update({"arg2": "rx0"})
            elif right[0].value == "EOF":
                result.update({"arg2": "rx0"})
    result.update({"opcode": symbol2opcode(tokens[idx].value)})
    mnemonics.append(f"{result['opcode']} {result['arg1']} {result['arg2']}")
    return result


def precedence(op):
    return {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "%": 2,
        "==": 3,
        "!=": 3,
        ">": 3,
        "<": 3,
        ">=": 3,
        "<=": 3,
    }.get(op, 0)


def var_out(variable):
    global instr_address
    for var in var_address:
        if var["name"] == variable:
            reg_to_print = mov_var(var["addr"])
            if var["type"] == "string":
                res_code.append(
                    {
                        "opcode": Opcode.OUTPUT,
                        "arg1": "rx" + str(reg_to_print),
                        "arg2": 1,
                    }
                )
                mnemonics.append(f"output {'rx' + str(reg_to_print)} {1}")
            else:
                res_code.append(
                    {
                        "opcode": Opcode.OUTPUT,
                        "arg1": "rx" + str(reg_to_print),
                        "arg2": 0,
                    }
                )
                mnemonics.append(f"output {'rx' + str(reg_to_print)} {0}")
            update_reg_data()
            instr_address += 1


def add_store_instr(reg):
    global instr_address, data_address
    res_code.append({"opcode": Opcode.STORE, "arg1": reg})
    mnemonics.append(f"store {reg}")
    instr_address += 1
    data_address += 1


def add_mov_instr(reg, val):
    global instr_address
    res_code.append({"opcode": Opcode.MOV, "arg1": reg, "arg2": val})
    mnemonics.append(f"mov {reg} {val}")
    instr_address += 1


def get_var_address(name):
    for var in var_address:
        if var["name"] == name:
            return var["addr"]


def add_var_to_map(name, v_type):
    global data_address
    variables.add(name)
    var = {"addr": data_address, "name": name, "type": v_type}
    var_address.append(var)


def mov_var(addr):
    add_mov_instr("rx2", addr)
    reg_data = "rx" + str(reg_counter)
    add_mov_instr(reg_data, "rx2")
    update_reg_data()
    return get_reg_data()


def main(args):
    assert len(args) == 3, "Wrong arguments"
    source, target_mnem, target2 = args
    opcodes, mnemonics = translate(source)
    if target_mnem is not None:
        with open(target_mnem, "w") as f:
            for line in mnemonics:
                f.write(line + "\n")
    write_bin_code(target2, opcodes)


if __name__ == "__main__":
    main(sys.argv[1:])

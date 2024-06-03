# Архитектура компьютера. Лабораторная работа №3
- Агнистова Алина Юрьевна P3225
- `alg -> asm | risc | harv | hw | instr | binary -> struct | stream | port | cstr | prob1 | cache`
- Базовый вариант

## Язык программирования
- `alg` - javascript-подобный язык программирования.
- Типы данных: `int`,`string`
- Поддерживаемые математические операции:
  - `+` - бинарный плюс
  - `-` - бинарный минус
  - `/` - целочисленное деление
  - `%` - остаток от деления
  - `=` - присваивание
- Операции сравнения:
  - `!=` - не равно
  - `==` - равно
  - `>` - больше
  - `<` - меньше
- Циклы: `while(comparison){...body...}`
- Условные операторы: `if(comparison){...body...}`
- Операции ввода: `input()`
- Операции вывода: `print()` <br>

### BNF
```
<program>         ::= <statement> | <program> <statement>
<statement>       ::= <var_declaration> | <var_assignment> | <while_statement> | <if_statement> | <read_statement> | <print_statement> 
<var_declaration> ::= <type> <name> "=" <expression> <nl>
<type>            ::= <int> | <string>
<int>             ::= <number>
<string>          ::= "\"[\w\s,.:;!?()\\-]+\""
<name>            ::= [a-zA-Z]+
<nl>              ::= "\n"
<expression>      ::= <term> | <term> <binary_op> <term>
<term>            ::= <name> | <number>
<number>          ::= [0-9]+
<var_assignment>  ::= <name> "=" <expression> <nl>
<while_statement> ::= "while" "(" <comparison> ")" "{" <program> "}" <nl>
<if_statement>    ::= "if" "(" <comparison> ")" "{" <program> "}" <nl>
<comparison>      ::= <expression> <comparison_op> <expression>
<read_statement>  ::= "input("<name>")" <nl>
<print_statement> ::= "print("<name>')" <nl>
<binary_op>       ::= "+" | "-" | "*" | "/" | "%"
<comparison_op>   ::= "==" | "!=" | ">" | "<" | ">=" | "<="
```
### Семантика
- Название переменной не может начинаться с цифры
- Поддержка строковых литералов, необходимо указывать строки в кавычках
- Последовательное выполнение кода
- После каждой строки кода необходимо указывать перенос строки
  
Пример:

```
int sum = 0;
int i = 0;
while (i < 1000){
    if (i%3 == 0){
        if (i % 5 == 0){
            sum = sum + 1;
}
}
i = i + 1;
}
print(i);
```
```
string str = "hello!";
print(str);
```

## Организация памяти

Работа с памятью
Модель памяти процессора:

Память инструкций и память данных разделены на два модуля. Доступ к памяти осуществляется с помощью отдельных операций store/load. Одна инструкция укладывается в 1 машинное слово.
- Память данных. Машинное слово -- 24 бита, знаковое. Линейное адресное пространство. Реализуется списком чисел, являющихся пространством памяти.
- Память команд. Машинное слово -- 62 бита.
В процессоре всего расположено 16 регистров.
Размер регистра - 32 бита.
* `rx0` - регистр, постоянно хранящий 0
* `rx1` - регистр текущей инструкции
* `rx2` - регистр текущей адресации в модуле памяти данных
* `rx3 - rx14` - регистры общего назначения
* `rx15` - регистр для загрузки аргумента для прыжка
Присутствует два флага состояния на выходах АЛУ - Zero Flag и Negative Flag
Адреса расположения данных в памяти определяются во время трансляции линейно от начала адресного пространства.

## Система команд 

| Синтаксис            | Кол-во тактов | Комментарий                                   |
|:------------------ --|:--------------|:----------------------------------------------|
| `MOV` (reg) (int)    | 4             | int -> reg                                    |
| `MOV` (reg) rx2      | 4             | data_mem[rx2] -> reg                          |
| `STORE` (reg)        | 4             | reg -> data_mem[rx2]                          |
| `ADD` (reg1) (reg2)  | 4             | reg1 + reg2 -> reg1                           |
| `SUB` (reg1) (reg2)  | 4             | reg1 - reg2 -> reg1                           |
| `MUL` (reg1) (reg2)  | 4             | reg1 * reg2 -> reg1                           |
| `DIV` (reg1) (reg2)  | 4             | reg1 / reg2 -> reg1                           |
| `MOD` (reg1) (reg2)  | 4             | reg1 % reg2 -> reg1                           |
| `JLE` (reg1) (reg2)  | 4             | reg1 == reg2 -> reg1                          |
| `JNE` (reg1) (reg2)  | 4             | reg1 != reg2 -> reg1                          |
| `JG` (reg1) (reg2)   | 4             | reg1 > reg2 -> reg1                           |
| `JE`  (reg1) (reg2)  | 4             | reg1 < reg2 -> reg1                           |           
| `INPUT`              | 4             | i_buf -> data_mem[rx2]                        |
| `OUTPUT` (reg)       | 3             | reg -> o_buf<br/>ch(reg) -> o_buf             |
| `JMP`                | 2             | rx15 -> rx1                                   |
| `HLT`                | 1             |                                               |


- Машинный код сериализуется в бинарный код.
- Сначала в бинарный код записываем всю выделенную data memory
- Затем в бинарный код переводится список словарей с ключами opcode и args. Пример словаря:  `{'opcode': 'mov', 'arg1': rx2, 'arg2': 0}`
## Транслятор

Интерфейс командной строки: `translator.py <input_file> <target_json_file> <target_bin_file>`
Реализовано в модуле [translator.py](./translator.py)

Этапы трансляции:

- Загрузка исходного кода
- Разбиение кода на токены
- Проход по токена 
- Построение алгоритма работы программы
- Выгрузка алгоритма в конечный файл
### Модель процессора
Реализовано в модуле [machine.py](./machine.py)

#### DataPath & ControlUnit
![схема](https://github.com/alinaagnistova/csa_lab_3/assets/116123766/dbec1dec-7255-4b70-9b41-94a98e4d41bc)
- Сигналы приходят от Control Unit
- Сигналы реализованы в виде методов класса
- `ALU` - АЛУ для выполнения арифметических операций
- `Data address` - указатель на данные
- `input/output` - порты ввода/вывода

Особенности работы модели:

- Для журнала состояний процессора используется стандартный модуль logging.
- Количество инструкций для моделирования ограничено hardcoded константой.
- Остановка моделирования осуществляется при помощи исключений:
  - `EOFError` -- если нет данных для чтения из порта ввода-вывода;
  - `StopIteration` -- если выполнена инструкция `halt`.
- Управление симуляцией реализовано в функции `simulation`.
## Тестирование

1. [hello world](./golden/hello.yml) - выводит `Hello, world!` в stdin.
2. [cat](./golden/cat.yml) - программа `cat`, повторяем ввод на выводе.
3. [hello_user_name](./golden/hello_user.yml) - чтение имени из файла и вывод приветствия
4. [prob5](./golden/prob1.yml) - problem 1
Golden тесты реализованы тут: [integration_test](./gloden_tests.py)

Пример запуска теста:
```shell
DEBUG    root:machine.py:277 {TICK: 4, RX1: 1, RX2: 0, RX3: 72, RX4: 0, RX5: 0, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 8, RX1: 2, RX2: 1, RX3: 72, RX4: 0, RX5: 0, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 12, RX1: 3, RX2: 1, RX3: 72, RX4: 101, RX5: 0, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 16, RX1: 4, RX2: 2, RX3: 72, RX4: 101, RX5: 0, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 20, RX1: 5, RX2: 2, RX3: 72, RX4: 101, RX5: 108, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 24, RX1: 6, RX2: 3, RX3: 72, RX4: 101, RX5: 108, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 28, RX1: 7, RX2: 3, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 32, RX1: 8, RX2: 4, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 36, RX1: 9, RX2: 4, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 40, RX1: 10, RX2: 5, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 44, RX1: 11, RX2: 5, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 48, RX1: 12, RX2: 6, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 0, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 52, RX1: 13, RX2: 6, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 56, RX1: 14, RX2: 7, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 0, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 60, RX1: 15, RX2: 7, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 64, RX1: 16, RX2: 8, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 0, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 68, RX1: 17, RX2: 8, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 72, RX1: 18, RX2: 9, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 0, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 76, RX1: 19, RX2: 9, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 80, RX1: 20, RX2: 10, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 0, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 84, RX1: 21, RX2: 10, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 88, RX1: 22, RX2: 11, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 0, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 92, RX1: 23, RX2: 11, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 96, RX1: 24, RX2: 12, RX3: 72, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 100, RX1: 25, RX2: 12, RX3: 0, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 104, RX1: 26, RX2: 13, RX3: 0, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 108, RX1: 27, RX2: 0, RX3: 0, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 112, RX1: 28, RX2: 0, RX3: 0, RX4: 72, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  INFO     root:machine.py:52 output: ['H'] << 'H'
  DEBUG    root:machine.py:277 {TICK: 115, RX1: 29, RX2: 0, RX3: 0, RX4: 72, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 119, RX1: 30, RX2: 1, RX3: 0, RX4: 72, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 123, RX1: 31, RX2: 1, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e'] << 'e'
  DEBUG    root:machine.py:277 {TICK: 126, RX1: 32, RX2: 1, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 130, RX1: 33, RX2: 2, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 134, RX1: 34, RX2: 2, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e', 'l'] << 'l'
  DEBUG    root:machine.py:277 {TICK: 137, RX1: 35, RX2: 2, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 141, RX1: 36, RX2: 3, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 119, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 145, RX1: 37, RX2: 3, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e', 'l', 'l'] << 'l'
  DEBUG    root:machine.py:277 {TICK: 148, RX1: 38, RX2: 3, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 152, RX1: 39, RX2: 4, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 114, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 156, RX1: 40, RX2: 4, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 100, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e', 'l', 'l', 'o'] << 'o'
  DEBUG    root:machine.py:277 {TICK: 159, RX1: 41, RX2: 4, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 163, RX1: 42, RX2: 5, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 167, RX1: 43, RX2: 5, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e', 'l', 'l', 'o', ','] << ','
  DEBUG    root:machine.py:277 {TICK: 170, RX1: 44, RX2: 5, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 174, RX1: 45, RX2: 6, RX3: 0, RX4: 72, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 178, RX1: 46, RX2: 6, RX3: 0, RX4: 32, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e', 'l', 'l', 'o', ',', ' '] << ' '
  DEBUG    root:machine.py:277 {TICK: 181, RX1: 47, RX2: 6, RX3: 0, RX4: 32, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 185, RX1: 48, RX2: 7, RX3: 0, RX4: 32, RX5: 108, RX6: 101, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 189, RX1: 49, RX2: 7, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e', 'l', 'l', 'o', ',', ' ', 'w'] << 'w'
  DEBUG    root:machine.py:277 {TICK: 192, RX1: 50, RX2: 7, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 196, RX1: 51, RX2: 8, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 108, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 200, RX1: 52, RX2: 8, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o'] << 'o'
  DEBUG    root:machine.py:277 {TICK: 203, RX1: 53, RX2: 8, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 207, RX1: 54, RX2: 9, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 108, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 211, RX1: 55, RX2: 9, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r'] << 'r'
  DEBUG    root:machine.py:277 {TICK: 214, RX1: 56, RX2: 9, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 218, RX1: 57, RX2: 10, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 111, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 222, RX1: 58, RX2: 10, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 108, RX13: 108, RX14: 44, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l'] << 'l'
  DEBUG    root:machine.py:277 {TICK: 225, RX1: 59, RX2: 10, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 108, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 229, RX1: 60, RX2: 11, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 108, RX13: 108, RX14: 44, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 233, RX1: 61, RX2: 11, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 108, RX13: 108, RX14: 100, RX15: 0}
  INFO     root:machine.py:52 output: ['H', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd'] << 'd'
  DEBUG    root:machine.py:277 {TICK: 236, RX1: 62, RX2: 11, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 108, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 240, RX1: 63, RX2: 12, RX3: 0, RX4: 32, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 108, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 244, RX1: 64, RX2: 12, RX3: 0, RX4: 0, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 108, RX13: 108, RX14: 100, RX15: 0}
  DEBUG    root:machine.py:277 {TICK: 247, RX1: 65, RX2: 12, RX3: 0, RX4: 0, RX5: 108, RX6: 119, RX7: 111, RX8: 111, RX9: 32, RX10: 114, RX11: 111, RX12: 108, RX13: 108, RX14: 100, RX15: 0}
  INFO     root:machine.py:300 output:  ['H', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd'], ticks: 247

```

CI:
`poetry` - управления зависимостями для языка программирования Python.
`coverage` - формирование отчёта об уровне покрытия исходного кода.
`pytest` - утилита для запуска тестов.
`ruff` - утилита для форматирования и проверки стиля кодирования.
Запускается при пуше в репозиторий на ветку мастер 
Тестовые процессы:
`test` - запуск тестов
`lint` - запуск линтера

| ФИО            | алг.  | LoC | code байт | code инстр. | инстр.  | такт.    | вариант                                                                 |
|----------------|-------|-----|-----------|-------------|---------|----------|--------------------------------------------------------------------------|
| Агнистова А.Ю. | hello | 2   | 528       |             | 66      | 247      | `alg | risc | harv | hw | instr | binary | stream | port | cstr | prob1` | 
| Агнистова А.Ю. | cat   | 6   | 128       | -           | 64      | 236      | `alg | risc | harv | hw | instr | binary | stream | port | cstr | prob1` |
| Агнистова А.Ю. | prob1 | 16  | 488       | -           | 36456   | 142282   | `alg | risc | harv | hw | instr | binary | stream | port | cstr | prob1` |


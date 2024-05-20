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
  - `>=` - больше или равно
  - `<=` - меньше или равно
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
- Поддержка целочисленных литералов в диапазоне $[-2^{31}; 2^{31} - 1]$
- Поддержка строковых литералов, необходимо указывать строки в кавычках
- Последовательное выполнение кода
- После каждой строки кода необходимо указывать перенос строки
  
Пример:

```
int sum = 0
int i = 0
while (i < 1000){
    if (i%3 == 0){
        if (i % 5 == 0){
            sum = sum + 1
}
}
i = i + 1
}
print(i)
```
```
string str = "hello!"
print(str)
```

## Организация памяти
```
risc -- система команд должна быть упрощенной, в духе RISC архитектур:
- стандартизированная длина команд;
- операции над данными осуществляются только в рамках регистров;
- доступ к памяти и ввод-вывод -- отдельные операции (с учётом специфики вашего варианта mem/port);
harv - Гарвардская архитектура
hw - Control Unit реализуется как часть модели
instr -- процессор необходимо моделировать с точностью до каждой инструкции (наблюдается состояние после каждой инструкции).
binary -- бинарное представление.
- Требуются настоящие бинарные файлы, а не текстовые файлы с 0 и 1.
stream
Ввод-вывод осуществляется как поток токенов. Есть в примере. Логика работы:
- при старте модели у вас есть буфер, в котором представлены все данные ввода (['h', 'e', 'l', 'l', 'o']);
- при обращении к вводу (выполнение инструкции) модель процессора получает "токен" (символ) информации;
- если данные в буфере кончились -- останавливайте моделирование;
- вывод данных реализуется аналогично, по выполнении команд в буфер вывода добавляется ещё один символ;
- по окончании моделирования показать все выведенные данные;
- логика работы с буфером реализуется в рамках модели на Python.
port -- port-mapped (специальные инструкции для ввода-вывода)
- адресация портов ввода-вывода должна присутствовать.
cstr -- Null-terminated (C string)
```
Работа с памятью

Модель памяти процессора:

Память инструкций и память данных разделены на два модуля. Доступ к памяти осуществляется с помощью отдельных операций store/load. Одна инструкция укладывается в 1 машинное слово.
- Память данных. Машинное слово -- 32 бита, знаковое. Линейное адресное пространство. Реализуется списком чисел, являющихся пространством памяти.
- Память команд. Машинное слово -- 32 бита. Реализуется списком чисел, описывающих инструкции.
Модель памяти должна включать:

Какие виды памяти и регистров доступны программисту?
Где хранятся инструкции, процедуры и прерывания?
Где хранятся статические и динамические данные?

А также данный раздел должен включать в себя описание того, как происходит работа с 1) литералами, 2) константами, 3) переменными, 4) инструкциями, 5) процедурами, 6) прерываниями во время компиляции и исполнения. К примеру:

В каких случаях литерал будет использован при помощи непосредственной адресации?
В каких случаях литерал будет сохранён в статическую память?
Как будут размещены литералы, сохранённые в статическую память, друг относительно друга?
Как будет размещаться в память литерал, требующий для хранения несколько машинных слов?
В каких случаях переменная будет отображена на регистр?
Как будет разрешаться ситуация, если регистров недостаточно для отображения всех переменных?
В каких случаях переменная будет отображена на статическую память?
В каких случаях переменная будет отображена на стек?
И так далее по каждому из пунктов в зависимости от варианта...

## Система команд 

Особенности процессора:

- Машинное слово - 32 бита
- 4 регистра
- размер команд и типы аргументов фиксированы, имеет 4 типа
  - Register
  - Immediate
  - Branch
  - Jump
- каждая инструкция выполняется за 5 этапов (по такту на каждый)
  - `fetch_instruction` - загрузка инструкции из памяти данных
  - `decode_instruction` - декодирование инструкций
  - `execute` - выполнение инструкций (вычисления в АЛУ, вычисления флагов по результату сравнения в branch comparator)
  - `memory_access` - доступ к памяти - для инструкций
  - `write_back` - запись результирующего значения (из памяти или АЛУ в регистр). На этом же этапе в инструкциях переходов переписывается значение pc'a

### Набор инструкций
| Синтаксис           | Кол-во тактов | Комментарий                                   |
|:--------------------|:--------------|:----------------------------------------------|
| `MOV` (reg) (int)    | 4             | int -> reg                                    |
| `GET` (reg) rx2      | 4             | data_mem[rx2] -> reg                          |
| `STORE` (reg)        | 4             | reg -> data_mem[rx2]                          |
| `ADD` (reg1) (reg2)  | 4             | reg1 + reg2 -> reg1                           |
| `SUB` (reg1) (reg2)  | 4             | reg1 - reg2 -> reg1                           |
| `MUL` (reg1) (reg2)  | 4             | reg1 * reg2 -> reg1                           |
| `DIV` (reg1) (reg2)  | 4             | reg1 / reg2 -> rx13<br/>reg1 % reg2 -> rx14   |
| `MOD` (reg1) (reg2)  | 4             | reg1 / reg2 -> rx13<br/>reg1 % reg2 -> rx14   |
| EQ (reg1) (reg2)     | 4             | reg1 == reg2 -> reg1                              |
| NE (reg1) (reg2)     | 4             | reg1 != reg2 -> reg1                              |
| GT (reg1) (reg2)     | 4             | reg1 > reg2 -> reg1                               |
| LT  (reg1) (reg2)    | 4             | reg1 < reg2 -> reg1                               
| `INPUT`              | 4             | i_buf -> data_mem[rx2]??                        |
| `OUTPUT` (reg)       | 3??           | reg -> o_buf<br/>ch(reg) -> o_buf???             |
| `JMP`                | 2             | rx15 -> rx1                                   |
| `JZ` (reg1) (reg2)   | 4             | zero_flag  => rx15 -> rx1 ??                  |
| `HLT`                | 1             |                                               |

| Инструкция | Номер | операнды          | Тип         | Пояснение              |
|:-----------|-------|:------------------|:------------|------------------------|
| HALT       | 0     | 0                 | Instruction | Останов                |
| LW         | 1     | 2 (reg, reg)      | Register    | dmem [rs2] -> rd       |
| SW         | 2     | 2 (reg, reg)      | Register    | rs1 -> dmem [rs2]      |
| LWI        | 3     | 2 (reg, imm)      | Immediate   | dmem [imm] -> rd       |
| SWI        | 4     | 2 (reg, imm)      | Immediate   | rs1 -> dmem [imm]      |
| JMP        | 5     | 1 (imm)           | Jump        | PC - imm -> PC         |
| BEQ        | 6     | 3 (rs1, rs2, imm) | Branch      | rs1 == rs2 ? imm -> pc |
| BNE        | 7     | 3 (rs1, rs2, imm) | Branch      | rs1 != rs2 ? imm -> pc |
| BLT        | 8     | 3 (rs1, rs2, imm) | Branch      | rs1 < rs2 ? imm -> pc  |
| BGT        | 9     | 3 (rs1, rs2, imm) | Branch      | rs1 > rs2 ? imm -> pc  |
| BNL        | 10    | 3 (rs1, rs2, imm) | Branch      | rs1 >= rs2 ? imm -> pc |
| BNG        | 11    | 3 (rs1, rs2, imm) | Branch      | rs1 <= rs2 ? imm -> pc |
| SEQ        | 12    | 3 (reg, reg, reg) | Register    | rs1 == rs2 -> rd       |
| SNE        | 13    | 3 (reg, reg, reg) | Register    | rs1 != rs2 -> rd       |
| SGT        | 14    | 3 (reg, reg, reg) | Register    | rs1 > rs2 -> rd        |
| SLT        | 15    | 3 (reg, reg, reg) | Register    | rs1 < rs2 -> rd        |
| SNL        | 16    | 3 (reg, reg, reg) | Register    | rs1 >= rs2 -> rd       |
| SNG        | 17    | 3 (reg, reg, reg) | Register    | rs1 <= rs2 -> rd       |
| AND        | 18    | 3 (reg, reg, reg) | Register    | rs1 & rs2 -> rd        |
| OR         | 19    | 3 (reg, reg, reg) | Register    | rs1 \| rs2 -> rd       |
| ADD        | 20    | 3 (reg, reg, reg) | Register    | rs1 + rs2 -> rd        |
| SUB        | 21    | 3 (reg, reg, reg) | Register    | rs1 - rs2 -> rd        |
| MUL        | 22    | 3 (reg, reg, reg) | Register    | rs1 * rs2 -> rd        |
| DIV        | 23    | 3 (reg, reg, reg) | Register    | rs1 / rs2 -> rd        |
| REM        | 24    | 3 (reg, reg, reg) | Register    | rs1 % rs2 -> rd        |
| ADDI       | 25    | 3 (reg, reg, imm) | Immediate   | rs1 + imm -> rd        |
| MULI       | 26    | 3 (reg, reg, imm) | Immediate   | rs1 + imm -> rd        |
| SUBI       | 27    | 3 (reg, reg, imm) | Immediate   | rs1 + imm -> rd        |
| DIVI       | 28    | 3 (reg, reg, imm) | Immediate   | rs1 + imm -> rd        |
| REMI       | 29    | 3 (reg, reg, imm) | Immediate   | rs1 + imm -> rd        |


### Регистры

Процессор в модели содержит 4 регистра общего назначения

#### Непосредственное значение

Для того чтобы загружать значения непосредственно в DataPath существует функциональный элемент - Immediately Generator.

### Кодирование инструкций

Инструкции представляют собой 32-битные машинные слова в следующем формате

- `rd` - register destination - регистр, куда будет записано значение после выполнения инструкции
- `rs1` и `rs2` - register source 1,2 - регистры, значения которых будут использоваться для вычисления результата операции
- `imm`* - immediate - непосредственное значение
- `opcode` - номер инструкции

```ascii


  31        30   29   28   27      26   25       5   4    0    Bits
+-----------------------------------------------------------+
|      rd      |   rs1   |    rs2     |            | opcode | Register type
+-----------------------------------------------------------+
|      rd      |   rs1   | imm[22:21] | imm[20:0]  | opcode | Immediate type
+-----------------------------------------------------------+
|  imm[22:21]  |   rs1   |    rs2     | imm[20:0]  | opcode | Branch type
+-----------------------------------------------------------+
|                       imm                        | opcode | Jump type
+-----------------------------------------------------------+
```

\* imm - имеет переменный размер, соответствующая типу инструкции часть извлекается из инструкции в immediate generator

#### Binary

Программы так же представлены в виде бинарного представления

- Машинный код сериализуется в бинарный код.
- Сначала в бинарный код записываем всю выделенную data memory
- Затем в бинарный код переводится список словарей с ключами opcode и args. Пример словаря:  `{'opcode': 'LW', 'args': [1, 4, 0]}`

## Транслятор

Интерфейс командной строки: `translator.py <input_file> <target_json_file> <target_bin_file>`

Реализовано в модуле [translator.py](./translator.py)

Этапы трансляции (функция translate):
- preprocess - Предобработка. Удаление пустых строк и комментариев, а также построчное разбиение
- tokenize - Токенизация. Трансформирование текста в deque токенов.
- buildAST - Перевод представления, полученного после токенизации, в дерево AST.
- translate - Трансляция АСТ в машинный код.
- 
### Модель процессора

Реализовано в модуле [machine.py](./machine.py)

#### DataPath & ControlUnit

![Scheme](Scheme.png)

#### ControlUnit

Реализован в классе `ControlUnit`.

- Hardwired (реализовано полностью на python).
- Моделирование на уровне инструкций.
- Трансляция инструкции в последовательность (5 тактов) сигналов: `tick_by_tick`.

Особенности работы модели:

- Для журнала состояний процессора используется стандартный модуль logging.
- Количество инструкций для моделирования ограничено hardcoded константой.
- Остановка моделирования осуществляется при помощи исключений:
  - `EOFError` -- если нет данных для чтения из порта ввода-вывода;
  - `StopIteration` -- если выполнена инструкция `halt`.
- Управление симуляцией реализовано в функции `simulate`.

## Тестирование

1. [hello world](./golden/hello.yml) - выводит `Hello, world!` в stdin.
2. [cat](./golden/cat.yml) - программа `cat`, повторяем ввод на выводе.
3. [hello_user_name](./golden/hello_user_name.yml) - чтение имени из файла и вывод приветствия
4. [prob5](./golden/prob5.yml) - problem 5

Golden тесты реализованы тут: [integration_test](./integration_test.py)

CI:

``` yaml
name: CI

on:
  push:
    branches: [ "master" ]
  pull_request:
    branches: [ "master" ]

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    - name: Install poetry
      run: pip install poetry
    - name: Set up Python 3.10.6
      uses: actions/setup-python@v4
      with:
        python-version: "3.10.6"
        cache: "poetry"
    - name: Install project
      run: |
        poetry install
    - name: Lint with ruff
      run: |
        poetry run python -m ruff translator.py
        poetry run python -m ruff machine.py
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Install poetry
      run: pip install poetry
    - name: Set up Python 3.10.6
      uses: actions/setup-python@v4
      with:
        python-version: "3.10.6"
        cache: "poetry"
    - name: Install project
      run: |
        poetry install
    - name: Run tests
      run: |
        poetry run pytest --update-goldens
    needs: lint
```

где:

- `python3-coverage` -- формирование отчёта об уровне покрытия исходного кода.
- `pytest` -- утилита для запуска тестов.
- `pycodestyle` -- утилита для проверки форматирования кода. `E501` (длина строк)
- `pylint` -- утилита для проверки качества кода. Некоторые правила отключены в отдельных модулях с целью упрощения кода.
- Docker image `python-tools` включает в себя все перечисленные утилиты. Его конфигурация: [Dockerfile](./Dockerfile).

Пример использования и журнал работы процессора на примере `prob5`:

```bash
python .\translator.py .\programs\prob5.alg .\programs\prob5.json .\programs\prob5.bin
python .\machine.py .\programs\prob5.bin .\programs\input.txt
```

[prob5.json](programs/prob5.bin)
[prob5.bin](programs/prob5.bin)


Текст вывода и ход работы [тут](./golden/prob5.yml)

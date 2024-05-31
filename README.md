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
| `DIV` (reg1) (reg2)  | 4             | reg1 / reg2 -> reg1   |
| `MOD` (reg1) (reg2)  | 4             | reg1 % reg2 -> reg1   |
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

# Computer Science Architecture Lab 3

Степанов Михаил Андреевич P33312

## Вариант

'alg | risc | harv | hw | instr | struct | stream | port | prob5'

* 'alg' - java/javascript подобный язык
* 'risc' - система команд должна быть упрощенной, в духе RISC архитектур
* 'harv' - Гарвардская архитектура
* 'hw' - Control Unit реализован как часть модели, микрокода нет
* 'instr' - каждая инструкиция расписана по-тактово, но в журнале фиксируется только результат выполнения
* 'struct' - в виде высокоуровневой структуры данных. Одна инструкция укладывается в одно машинное слово
* 'stream' - ввод-вывод осуществляется как поток токенов
* 'port' - port-mapped
* 'prob5' - Project Euler. Problem 5

## Язык программирования

Использована упрощенная версия языка JavaScript
Типизация: статическая сильная неявная

* Объявление переменных через ключевое слово `let`
* Доступен цикл `while`
* Доступна функция ввода `input()` и функция вывода `print()`
* Доступна инструкция ветвления `if`
* Разрешенные математические операции:
  * `+` - бинарный плюс
  * `-` -  бинарный минус
  * `=` - присваивание
  * `*` - умножение
  * `%` - остаток от деления
  * `!=`, `==`, `>=`, `>`, `<=`, `<` - операции сравнения 

### BNF

#### `<program> ::= (<source element>)+`
#### `<source element> ::= <statement>`
#### `<statement> ::= <allocation statement> | <assignment statement> | <if statement> | <iteration statement> | <read statement> | <print statement>`
#### `<allocation statement> ::= "let" <name> "=" <number> | <row> ";"`
#### `<assignment statement> ::= <name> "=" <number> | <name> | <expression> ";"`
#### `<if statement> ::= "if" (<name> | <expression> | <number>) <comparison sign> (<name> | <expression> | <number>) "\n{" (<statement>)+ "}"`
#### `<iteration statement> ::= "while" (<name> | <expression> | <number>) <comparison sign> (<name> | <expression> | <number>) "\n{" (<statement>)+ "}"`
#### `<read statement> ::= "input(" <name> ");"`
#### `<print statement> ::= "print( <name> ");"`
#### `<expression> ::= (<name> | <number>) <operation sign> (<name> | <number>)`
#### `<comparison sign> ::= "!=" | "==" | ">" | "<" | "<=" | ">="`
#### `<name> ::= [a-zA-Z]+`
#### `<number> ::= [0-9]+`
#### `<row> ::= "[a-zA-Z]*"`
#### `<operation sign> ::= "+" | "-" | "/" | "%" | "*"`

### Пример
```javascript
let n = 2520;
let i = 20;
while (i > 0)
{
if (n % i == 0)
{
i = i - 1;
}
else
{
n = n + 2520;
i = 20;
}
if (i == 1)
{
print(n);
}
}
```

```javascript
let temp = "hello, world";
print(temp);
```

## Процессор

Реализован в модуле [machine.py](./machine.py)

Интерфейс командной строки с запуском модуля: `python machine.py <target_file> <input_file>`

### Модель процессора
![Processor](./proc.png)

Управляющие сигналы:
* Sel(rx1)  - выставить значение регистра rx1
  * 1 - увеличить на 1
  * 0 - загрузить значение из вне
* Sel(rx2) - выставить значение регистра rx2
  * 1 - увеличить на 1
  * 0 - загрузить значние из вне
* Sel(reg) - загрузить значение в указанный регистр

### Организация памяти

Память инструкций и данных раделены на два модуля.
Доступ к памяти может осуществляться только через store/load инструкции согласно RISC-архитектуре

Модель памяти процессора:
* Память команд - Машинное слово не определено, реализация при помощи массива словарей
* Память данных - 32 бита, знаковое

Размер памяти данных - 2048
Размер памяти инструкций - 2048

В процессоре всего расположено 16 регистров.
Размер регистра - 32 бита.
* `rx0` - регистр, постоянно хранящий 0
* `rx1` - регистр текущей инструкции
* `rx2` - регистр текущей адресации в модуле памяти данных
* `rx3 - rx11` - регистры общего назначения
* `rx12` - указатель стека
* `rx13` - регистр, хранящий результат операции '/'
* `rx14` - регистр, хранящий результат операции '%'
* `rx15` - регистр для загрузки аргумента для прыжка

Присутствует два флага состояния на выходах АЛУ - Zero Flag и Negative Flag 

Адреса расположения данных в памяти определяются во время трансляции линейно от начала адресного пространства.

### Набор инструкций
| Синтаксис           | Кол-во тактов | Комментарий                                   |
|:--------------------|:--------------|:----------------------------------------------|
| `ld` (reg) (int)    | 4             | int -> reg                                    |
| `ld` (reg) rx2      | 4             | data_mem[rx2] -> reg                          |
| `wr` (reg)          | 4             | reg -> data_mem[rx2]                          |
| `add` (reg1) (reg2) | 4             | reg1 + reg2 -> reg1                           |
| `sub` (reg1) (reg2) | 4             | reg1 - reg2 -> reg1                           |
| `mul` (reg1) (reg2) | 4             | reg1 * reg2 -> reg1                           |
| `div` (reg1) (reg2) | 4             | reg1 / reg2 -> rx13<br/>reg1 % reg2 -> rx14   |
| `input`             | 4             | i_buf -> data_mem[rx2]                        |
| `print` (reg) (1/0) | 3             | reg -> o_buf<br/>ch(reg) -> o_buf             |
| `jmp`               | 2             | rx15 -> rx1                                   |
| `inc` (reg)         | 4             | reg + 1 -> reg                                |
| `dec` (reg)         | 4             | reg - 1 -> reg                                |
| `jle` (reg1) (reg2) | 4             | zero_flag OR neg_flag => rx15 -> rx1          |
| `jl` (reg1) (reg2)  | 4             | NOT zero_flag AND neg_flag => rx15 -> rx1     |
| `jne` (reg1) (reg2) | 4             | NOT zero_flag  => rx15 -> rx1                 |
| `je` (reg1) (reg2)  | 4             | zero_flag  => rx15 -> rx1                     |
| `jge` (reg1) (reg2) | 4             | zero_flag OR NOT neg_flag => rx15 -> rx1      |
| `jg` (reg1) (reg2)  | 4             | NOT zero_flag AND NOT neg_flag => rx15 -> rx1 |
| `hlt`               | 1             |                                               |

Устройства ввода/вывода определены как два буфера данных, условно относящиеся к определенному порту

## Кодирование 

### Структура команды

* Машинный код представлен в формате JSON списка операционных команд
* Одна инструкция - словарь, содаержащий операционный код и аргументы

```json
{
    "opcode": "ld",
    "arg1": "rx15",
    "arg2": 22
}
```

* `opcode` - код операции
* `arg1` - первый аргумент (может отсутствовать) 
* `arg2` - второй аргумент аргумент (может отсутствовать)

### Транслятор

Реализован в модуле [translator.py](./translator.py)

Интерфейс командной строки с запуском модуля: `python translator.py <source_file> <target_file>`

Этапы трансляции:
* Загрузка исходного кода
* Рекурсивный проход по строкам в файле и обработка их в соответствии с регулярными выражениями
* Построение алгоритма работы программы
* Выгрузка алгоритма в конечный файл

Пример:

```javascript
let temp = "";
input(temp);
while (temp != EOF)
{
print(temp);
input(temp);
}
```

```json
[
    {
        "opcode": "ld",
        "arg1": "rx3",
        "arg2": 0
    },
    {
        "opcode": "wr",
        "arg1": "rx3"
    },
    {
        "opcode": "ld",
        "arg1": "rx2",
        "arg2": 0
    },
    {
        "opcode": "input"
    },
    {
        "opcode": "ld",
        "arg1": "rx15",
        "arg2": 15
    },
    {
        "opcode": "ld",
        "arg1": "rx2",
        "arg2": 0
    },
    {
        "opcode": "ld",
        "arg1": "rx4",
        "arg2": "rx2"
    },
    {
        "opcode": "je",
        "arg1": "rx4",
        "arg2": "rx0"
    },
    {
        "opcode": "ld",
        "arg1": "rx2",
        "arg2": 0
    },
    {
        "opcode": "ld",
        "arg1": "rx5",
        "arg2": "rx2"
    },
    {
        "opcode": "print",
        "arg1": "rx5",
        "arg2": 1
    },
    {
        "opcode": "ld",
        "arg1": "rx2",
        "arg2": 0
    },
    {
        "opcode": "input"
    },
    {
        "opcode": "ld",
        "arg1": "rx15",
        "arg2": 4
    },
    {
        "opcode": "jmp"
    },
    {
        "opcode": "halt"
    }
]
```

## Аппробация

* Исходные коды готовых программ
  * [hello_test.js](./tests/hello_test.js)
  * [cat_test.js](./tests/cat_test.js)
  * [prob5_test.js](./tests/prob5_test.js)
* Результаты работы транслятора
  * [hello.out](./tests/hello.out) 
  * [cat.out](./tests/cat.out) 
  * [prob5.out](./tests/prob5.out) 
* Входные данные для программ
  * [privet_input.txt](./tests/privet_input.txt)

Описание тестов - [integration_tests.py](./integration_tests.py)

Пример запуска теста:
```shell
> ./translator.py ./tests/hello_test.js ./tests/hello.out
> ./machine.py ./tests/hello.out ./privet_input.txt

DEBUG:root:{TICK: 4, RX1: 1, RX2: 0, RX3: 104, RX4: 0, RX5: 0, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 8, RX1: 2, RX2: 1, RX3: 104, RX4: 0, RX5: 0, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 12, RX1: 3, RX2: 1, RX3: 104, RX4: 101, RX5: 0, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 16, RX1: 4, RX2: 2, RX3: 104, RX4: 101, RX5: 0, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 20, RX1: 5, RX2: 2, RX3: 104, RX4: 101, RX5: 108, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 24, RX1: 6, RX2: 3, RX3: 104, RX4: 101, RX5: 108, RX6: 0, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 28, RX1: 7, RX2: 3, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 32, RX1: 8, RX2: 4, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 0, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 36, RX1: 9, RX2: 4, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 40, RX1: 10, RX2: 5, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 0, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 44, RX1: 11, RX2: 5, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 48, RX1: 12, RX2: 6, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 0, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 52, RX1: 13, RX2: 6, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 56, RX1: 14, RX2: 7, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 0, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 60, RX1: 15, RX2: 7, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 64, RX1: 16, RX2: 8, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 0, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 68, RX1: 17, RX2: 8, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 72, RX1: 18, RX2: 9, RX3: 104, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 76, RX1: 19, RX2: 9, RX3: 114, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 80, RX1: 20, RX2: 10, RX3: 114, RX4: 101, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 84, RX1: 21, RX2: 10, RX3: 114, RX4: 108, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 88, RX1: 22, RX2: 11, RX3: 114, RX4: 108, RX5: 108, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 92, RX1: 23, RX2: 11, RX3: 114, RX4: 108, RX5: 100, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 96, RX1: 24, RX2: 12, RX3: 114, RX4: 108, RX5: 100, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 100, RX1: 25, RX2: 0, RX3: 114, RX4: 108, RX5: 100, RX6: 108, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 104, RX1: 26, RX2: 0, RX3: 114, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: [] << 'h'
DEBUG:root:{TICK: 107, RX1: 27, RX2: 0, RX3: 114, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 111, RX1: 28, RX2: 1, RX3: 114, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 44, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 115, RX1: 29, RX2: 1, RX3: 114, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h'] << 'e'
DEBUG:root:{TICK: 118, RX1: 30, RX2: 1, RX3: 114, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 122, RX1: 31, RX2: 2, RX3: 114, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 119, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 126, RX1: 32, RX2: 2, RX3: 114, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h', 'e'] << 'l'
DEBUG:root:{TICK: 129, RX1: 33, RX2: 2, RX3: 114, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 133, RX1: 34, RX2: 3, RX3: 114, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 137, RX1: 35, RX2: 3, RX3: 108, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h', 'e', 'l'] << 'l'
DEBUG:root:{TICK: 140, RX1: 36, RX2: 3, RX3: 108, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 144, RX1: 37, RX2: 4, RX3: 108, RX4: 108, RX5: 100, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 148, RX1: 38, RX2: 4, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h', 'e', 'l', 'l'] << 'o'
DEBUG:root:{TICK: 151, RX1: 39, RX2: 4, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 155, RX1: 40, RX2: 5, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 111, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 159, RX1: 41, RX2: 5, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h', 'e', 'l', 'l', 'o'] << ','
DEBUG:root:{TICK: 162, RX1: 42, RX2: 5, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 166, RX1: 43, RX2: 6, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 170, RX1: 44, RX2: 6, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h', 'e', 'l', 'l', 'o', ','] << ' '
DEBUG:root:{TICK: 173, RX1: 45, RX2: 6, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 177, RX1: 46, RX2: 7, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 111, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 181, RX1: 47, RX2: 7, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h', 'e', 'l', 'l', 'o', ',', ' '] << 'w'
DEBUG:root:{TICK: 184, RX1: 48, RX2: 7, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 188, RX1: 49, RX2: 8, RX3: 108, RX4: 108, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 192, RX1: 50, RX2: 8, RX3: 108, RX4: 111, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h', 'e', 'l', 'l', 'o', ',', ' ', 'w'] << 'o'
DEBUG:root:{TICK: 195, RX1: 51, RX2: 8, RX3: 108, RX4: 111, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 199, RX1: 52, RX2: 9, RX3: 108, RX4: 111, RX5: 111, RX6: 104, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 203, RX1: 53, RX2: 9, RX3: 108, RX4: 111, RX5: 111, RX6: 114, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o'] << 'r'
DEBUG:root:{TICK: 206, RX1: 54, RX2: 9, RX3: 108, RX4: 111, RX5: 111, RX6: 114, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 210, RX1: 55, RX2: 10, RX3: 108, RX4: 111, RX5: 111, RX6: 114, RX7: 44, RX8: 101, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 214, RX1: 56, RX2: 10, RX3: 108, RX4: 111, RX5: 111, RX6: 114, RX7: 44, RX8: 108, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r'] << 'l'
DEBUG:root:{TICK: 217, RX1: 57, RX2: 10, RX3: 108, RX4: 111, RX5: 111, RX6: 114, RX7: 44, RX8: 108, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 221, RX1: 58, RX2: 11, RX3: 108, RX4: 111, RX5: 111, RX6: 114, RX7: 44, RX8: 108, RX9: 32, RX10: 108, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
DEBUG:root:{TICK: 225, RX1: 59, RX2: 11, RX3: 108, RX4: 111, RX5: 111, RX6: 114, RX7: 44, RX8: 108, RX9: 32, RX10: 100, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output: ['h', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l'] << 'd'
DEBUG:root:{TICK: 228, RX1: 60, RX2: 11, RX3: 108, RX4: 111, RX5: 111, RX6: 114, RX7: 44, RX8: 108, RX9: 32, RX10: 100, RX11: 119, RX12: 2047, RX13: 0, RX14: 0, RX15: 0}
INFO:root:output:  ['h', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd'], ticks: 228
Output buffer: hello, world | ticks: 228 | amount_instr: 61
```


| ФИО          | алг.  | LoC | code байт | code инстр. | инстр.  | такт.    | вариант                                                          |
|--------------|-------|-----|-----------|-------------|---------|----------|------------------------------------------------------------------|
| Степанов М.А | hello | 2   | -         | 61          | 61      | 228      | `alg - risc - harv- hw - instr - struct - stream - port - prob5` | 
| Степанов М.А | cat   | 7   | -         | 16          | 67      | 252      | `alg - risc - harv- hw - instr - struct - stream - port - prob5` |
| Степанов М.А | prob5 | 18  | -         | 42          | 5065441 | 19378001 | `alg - risc - harv- hw - instr - struct - stream - port - prob5` |


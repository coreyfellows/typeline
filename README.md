# typeline
Python argparse wrapper using signature introspection and type annotations


Basic Usage

```python
from typeline import Typeline

app = Typeline()
@app.command
def echo(print_back):
    print(print_back)
app.run()
```

```bash
./python app.py echo "hello world"
>> hello world
```

Any parameters that are keyword only parameters will be set up as optional prefixed by --. Use the * parameter to separate the positional parameters and the optional params. Parameters with _ will use a - on the command line

```python
@app.command
def echo(print_back, *, reverse_string):
    if reverse_string:
        print_back = print_back[::-1]
    print(print_back)
```

```bash
./python app.py echo "hello world" --reverse-string 1
>> dlrow olleh
```

Default Values

Default values can be provided in two ways, either with the 'default' value in the add_argument kwargs provided by a type annotation, or by the default value of the parameter

```python
@app.command
def echo(print_back, *, print_back2="this will also be printed"):
    print(print_back, print_back2)
```

```bash
./python app.py echo "hello world"
>> hello world this will also be printed
```

Type Annotation

You can provide either a dictionary or a callable as the type annotation.
The dictionary will be passed to argparse's add_argument as the kwargs.
If a callable is provided the callable must return a dictionary for add_argument. Unannotated values are assumed to be a string

This package contains some commonly used annotations.

Basic Types

```python
from typeline.types import Integer

@app.command
def add(val1: Integer, val2: Integer):
    print(val1 + val2)
```

```bash
./python app.py add 1 2
>> 3
```

```python
from typeline.types import String, Flag

@app.command
def echo(print_back: String, *, reverse_string: Flag):
    if reverse_string:
        print_back = print_back[::-1]
    print(print_back)
```

```bash
./python app.py echo "hello world"
>> hello world

./python app.py echo "hello world" --reverse-string
>> dlrow olleh
```

```python
from typeline.types import String, OutFile

@app.command
def echo(print_back: String, output_file: OutFile):
    output_file.write(print_back)
```

```bash
./python app.py echo "hello world" example.txt
cat example.txt
>> hello world
```


```python
from typeline.types import List

@app.command
def echo(print_back: List):
    output_file.write(print_back)
```

```bash
./python app.py echo example hello world 123
>> ['example', 'hello', 'world', '123']
```

```python
from typeline.types import List, Integer

@app.command
def echo(print_back: List(Integer, nargs=2)):
    print(print_back)
```

```bash
./python app.py echo 1 2
>> [1, 2]
```

Documentation

The WithHelp annotation will add a help string to each parameter. Annotations can automatically add help as you go and WithHelp will retain the current help text. For example, List(Integer, nargs=2) will add a description of the type to the help text.


```python
from typeline.types import List, Integer, WithHelp

@app.command
def echo(
    print_back: WithHelp(List(Integer, nargs=2), "The list of integers to print")
    ):
    print(print_back)
```

```bash
./python app.py echo --help
>> usage: driver.py echo [-h] print_back print_back
>>
>> positional arguments:
>>   print_back  List<int> length=2: The list of integers to print

>> optional arguments:
>>   -h, --help  show this help message and exit
```
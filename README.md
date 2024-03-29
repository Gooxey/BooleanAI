# BooleanAI

A different approch to create an AI

### Concept

The idea behind this AI model is to imitate the human brain cell's ability to learn and to form groups with other neighboring cells.

#### The Rules

- Every Cell needs a path to at least one output and one input. If one path is missing, the Cell gets destroyed.
- Cells cannot connect to a Cell which is already connected to the first one.
- Output Cells and Inputs do not need any connections

#### The Parameters

Listed below are all parameters the user can customize to modify how the AI develops during its training phase. All of these values are stored in binary code in a file called the AIData file. It can be modified using a tool which is currently still in development.

- `maxtries`: Maximum amount of times the AI will try to do a random based process
- `performencecycles`: Amount of times the AI calculates the performance, before it concludes how good the AI was doing
- `createmin`: Amount of connections a Cell has to create
- `createmax`: Amount of connections a Cell can create
- `createchance`: Chance more connections than required get created
- `spawnchance`: Chance a new connection creates a new Cell
- `destroymin`: Amount of connections a Cell has to destroy
- `destroymax`: Amount of connections a Cell can destroy
- `destroychance`: Chance more connections than required get destroyed
- `statementchangemin`: Percentage of statements that have to change
- `statementchangemax`: Percentage of statements that can change
- `statementchangechance`: Chance more statements than required get changed
- `inputcount`: Amount of inputs
- `outputcount`: Amount of outputs

#### The AIData file

The data to initiate the AI is stored in a [AINAME]_AIData.dat file. The way the AI stores its values in there is in binary form, so the file is fast to read and therefore the AI fast to initiate.
The way the values are converted is in a 3-Bit system. The possible combinations are:

- Signals:
    - 001: Marks the end of an integer sequence
    - 011: Marks the end of the parameter section
- Integers:
    - 100: A Binary 0
    - 101: A Binary 1
- Booleans:
    - 110: True
    - 111: False

Stored first are always the parameters and some additional information the AI needs. After that, the Cells are stored by first storing the first Cell's table and then storing the first Cell's inputs, then the second, then the third and so on.

#### The cells

The Cells are basically just lists of outputs a cell will give back depending on how the input is given. To get these outputs, they form a so-called connection to a cell, which gives them the ability to read if this cell is giving a positive or negative output (True or False).
![InsideTheCell](https://github.com/Gooxey/BooleanAI/blob/f2cae8865bb7789e6f26f0b2d6ea0e2e2cbe3be0/images/InsideTheCell.png)

There are two types of Cells. First, there are the Output-cells which cannot be destroyed because they are the last Cells to process the inputs and give back an output. That is the reason why it is required to specify the number of Output-cells you want to have. Unlike the first type, the second type is allowed to be destroyed or generated by other Cells, but other than that, they are just like the Output-cells.

#### The Learning Process

The AI learns by letting each Cell create and/or destroy connections to other Cells, so the AI can grow its network to provide an optimal size for a specific task. Additionally, the Cells can also generate a new cell and form its connection to it instead, by chance, instead of creating a connection to another Cell. This should hopefully give this model an advantage towards the already existing model, because it is adapting to a task in every way possible, just like the brain is.
The second step is to let each Cell change their internal table, so the resulting outputs are changing with each generation a little, to hopefully increase the chances the AI does its job better.

## Features

- Can initiate an AI automatically based on a AIData file provided at the initiation of the AI (The filewiter.py script can be used to generate such file)
- Process inputs given in a list to some output
- Train the AI by providing the right answer and designing your own performance calculator

## Installation

```bash
# create the library from source files located in ./booleanai/
$ python setup.py bdist_wheel
# install the created library
$ pip install .\dist\booleanai-0.1.0-py3-none-any.whl
```

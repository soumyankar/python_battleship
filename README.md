# python_battleship
A simplistic Battleship game written in Python for Vrije Universiteit's Software Testing course

## Pre commands

In case you may not want to download these packages, start a virtual environment with virtualenv or pipenv. Ex:
```
virtualenv venv

# Unix/Linux
source venv/bin/activate

# or Windows
venv/source/Activate.bat
```

```
pip install -r requirements.txt
```



## Quick Start

```zsh
sh ./run.sh
```

## Building Binary or Executable

First, ensure that you are on the OS that you want to build for. e.g. to build a mac binary you must be on macOS.

Then, run the make command for your OS, the options are:
```
make linux
make mac
make windows
```

## Running Built Code

### Mac
```
./mac/battleship
```

### Linux
```
./linux/battleship
```

### Windows
```
./windows/battleship.exe
```
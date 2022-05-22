import sys
from cx_Freeze import setup, Executable


build_exe_options = {
    "packages": ["os", "sys", "random", "time"], 
    "excludes": ["tkinter"],
    "includes": ["inputimeout"]
}

base = None

setup(  name = "battleship",
        version = "0.1",
        description = "The game of battleship!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("battleship.py", base=base)])
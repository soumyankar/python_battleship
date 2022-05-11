#!/bin/bash

# make sure you've activated your virtual environment
pip install cx_Freeze
cxfreeze -c battleship.py --target-dir mac
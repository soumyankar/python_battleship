#!/bin/bash

DIR=$(pwd)

# create env file to load, if it doesn't exist
if [ ! -f $DIR/.env ]; then
    touch .env
    cat .env.example > .env
fi

# Load .env file
export $(egrep -v '^#' $DIR/.env | xargs)

python3 ./battleship.py
#!/bin/bash

if [[ ! -d venv ]]
then
    make venv
fi

./venv/bin/python3 run_terminal.py

exit 0
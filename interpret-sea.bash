#!/bin/bash

input_dir="input"
paths=()

for (( i=1; i <= "$#"; i++ ))
do
    if [[ "${!i}" == "-s" ]]
    then
        (( i++ ))
        input_dir="${!i}"
        continue
    fi

    paths+=("${!i}")
done

if [[ ! -d venv ]]
then
    make venv
fi

./venv/bin/python3 run_files.py "interpret" "$input_dir"

exit 0
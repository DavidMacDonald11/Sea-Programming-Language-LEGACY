#!/bin/bash

project="$(pwd)"
input_dir="input"
output_dir="output"
bin_dir="bin"
paths=()

for (( i=1; i <= "$#"; i++ ))
do
    if [[ "${!i}" == "-s" ]]
    then
        (( i++ ))
        input_dir="${!i}"
        continue
    fi

    if [[ "${!i}" == "-c" ]]
    then
        (( i++ ))
        output_dir="${!i}"
        continue
    fi

    if [[ "${!i}" == "-b" ]]
    then
        (( i++ ))
        bin_dir="${!i}"
        continue
    fi

    paths+=("${!i}")
done

if [[ ! -d venv ]]
then
    make venv
fi

if [[ -f "$output_dir/clean.bash" ]]
then
    cd "$output_dir"
    ./clean.bash
    cd "$project"
fi

if [[ -f "$bin_dir/clean.bash" ]]
then
    cd "$bin_dir"
    ./clean.bash
    cd "$project"
fi

source venv/bin/activate

./venv/bin/python3 main.py "$input_dir" "$output_dir" "$bin_dir" "${paths[@]}"

exit 0

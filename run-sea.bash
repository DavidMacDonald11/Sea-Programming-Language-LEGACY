#!/bin/bash

bin_dir="bin"
args=()
compile_args=()

for (( i=1; i <= "$#"; i++ ))
do
    if [[ "${!i}" == "-a" ]]
    then
        (( i++ ))
        args+=("${!i}")
        continue
    fi

    compile_args+=("${!i}")

    if [[ "${!i}" == "-b" ]]
    then
        (( i++ ))
        bin_dir="${!i}"
        compile_args+=("${bin_dir}")
        continue
    fi
done

./compile-sea.bash -b "$bin_dir" "${compile_args[@]}"

echo -e "Running program...\n"

cd "$bin_dir"
./program

exit 0

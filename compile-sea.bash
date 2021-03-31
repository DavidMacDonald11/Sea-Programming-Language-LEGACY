#!/bin/bash

./transpile-sea.bash "$@"

bin_dir="bin"
output_dir="output"

for (( i=1; i <= "$#"; i++ ))
do
    if [[ "${!i}" == "-b" ]]
    then
        (( i++ ))
        bin_dir="${!i}"
        continue
    fi

    if [[ "${!i}" == "-c" ]]
    then
        (( i++ ))
        output_dir="${!i}"
        continue
    fi
done

cd "$output_dir"
./compile-c.bash -b "../$bin_dir" $(cat files.tmp | tr "\n" " ")

exit 0

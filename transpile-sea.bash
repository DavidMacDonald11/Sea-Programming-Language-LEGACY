#!/bin/bash

src_dir="src"
bin_dir="bin"
rest=""

for (( i=1; i <= "$#"; i++ ))
do
    if [[ "$i" -eq "1" ]]
    then
        src_dir="${!i}"
        continue
    fi

    if [[ "$i" -eq "2" ]]
    then
        bin_dir="${!i}"
        continue
    fi

    rest+="${!i} "
done

if [[ ! -d venv ]]
then
    make venv
fi

source venv/bin/activate

./venv/bin/python3 main.py "$src_dir" "$bin_dir" "$rest"

exit 0

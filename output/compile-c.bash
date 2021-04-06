#!/bin/bash

bin_dir="../bin"
files=()

for (( i=1; i <= "$#"; i++ ))
do
    if [[ "${!i}" == "-b" ]]
    then
        (( i++ ))
        bin_dir="${!i}"
        continue
    fi

    file="$bin_dir/${!i}"
    echo "Compiling $file ..."

    file="${file%.c}.o"
    cc -c "${!i}" -o "$file"

    files+=("$file")
done

if [[ ${#files[@]} -ne 0 ]]
then
    echo "Building program..."
    eval cc "${files[@]}" -o "$bin_dir"/program
fi

exit 0

#!/bin/bash

files=""

for (( i=1; i <= "$#"; i++ ))
do
    file="bin/${!i}"
    echo "Compiling $file ..."

    file="${file%.c}.o"

    cc -c "${!i}" -o "$file"

    files+="$file "
done

if [[ "$files" != "" ]]
then
    echo "Building program..."
    cc $files -o bin/program
fi

exit 0

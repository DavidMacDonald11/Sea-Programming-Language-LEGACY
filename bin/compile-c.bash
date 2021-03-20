#bin/bash

files=""

for (( i=1; i <= "$#"; i++ ))
do
    file="bin/${!i}"
    file="${file%.c}.o"

    cc -c "${!i}" -o "$file"

    files+="$file"
done

echo "$files"

cc "$files" -o "bin/program"

exit 0
#!/bin/bash

if [[ "$0" != "./clean.bash" ]]
then
    echo "Must run clean.bash from inside of the folder for safety."
    exit 1
fi

shopt -s extglob

ls !(.keep|*.bash) >/dev/null 2>&1

if [[ $? -eq 0 ]]
then
    rm -r !(.keep|*.bash)
fi

exit 0

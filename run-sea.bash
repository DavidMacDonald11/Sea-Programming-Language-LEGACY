#!/bin/bash

./compile-sea.bash "$@"

echo -e "Running program...\n"

if [[ "$2" == "" ]]
then
    cd bin/bin
else
    cd "$2"/bin
fi

./program

exit 0

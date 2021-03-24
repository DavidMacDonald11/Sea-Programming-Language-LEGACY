#!/bin/bash

./transpile-sea.bash "$@"

if [[ "$2" == "" ]]
then
    cd bin
else
    cd "$2"
fi

./compile-c.bash $(cat files.tmp | tr "\n" " ")

exit 0

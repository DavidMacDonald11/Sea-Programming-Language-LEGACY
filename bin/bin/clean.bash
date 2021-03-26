#!/bin/bash

shopt -s extglob

ls !(.keep|*.bash) >/dev/null 2>&1

if [[ $? -eq 0 ]]
then
    rm -r !(.keep|*.bash)
fi

exit 0

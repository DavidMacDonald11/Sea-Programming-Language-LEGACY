#!/bin/bash

shopt -s extglob

ls !(bin|.keep|*.bash) >/dev/null 2>&1

if [[ $? -eq 0 ]]
then
    rm -r !(bin|.keep|*.bash)
fi

exit 0

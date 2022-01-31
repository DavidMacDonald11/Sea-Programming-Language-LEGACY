#!/bin/bash

printf "This will attempt to automate the installation of Sea onto your system.\n"
printf "If this installer is insufficient for your system, contact the developer.\n"
printf "Changes will always require user input to be performed.\n"
printf "Entering any key other than shown will abort at any stage, "
printf "but will NOT undo any changes already made.\n"
printf "Enter 1 to proceed: "
read -r key_press

if [[ "$key_press" != "1" ]]
then
    printf "Aborting installation.\n"
    exit 1
fi

printf "\nThe installer is going to use git to clone the Sea repository. "
printf "You will be prompted for a location.\n"
printf "If you do not have git or would like to install a custom version, "
printf "place the folder into a permenant location, "
printf "and ensure the folder name contains 'sea_lang'.\n"
printf "Enter 1 to use git to install the latest version of Sea;\n"
printf "Enter 2 to skip this step: "
read -r key_press

if [[ "$key_press" == "1" ]]
then
    printf "\nWhere would you like to install to? (Recommended '/usr/lib')\n"
    printf "Use '\ ' in place of each space.\n"
    printf "Location: "
    read -r location
    location=$(printf "%s/\n" "${location%/}")

    while [[ ! -d "$location" ]]
    do
        printf "\n'%s' is not a valid directory.\n" "$location"
        printf "Perhaps use 'mkdir' in another terminal.\n"
        printf "Enter 1 to change the directory;\n"
        printf "Enter 2 to try again (used mkdir): "
        read -r key_press

        if [[ "$key_press" == "1" ]]
        then
            printf "Location: "
            read -r location
            location=$(printf "%s/\n" "${location%/}")
        elif [[ "$key_press" != "2" ]]
        then
            printf "Aborting installation.\n"
            exit 1
        fi
    done

    printf "\nLocation is a valid directory.\n"
    printf "Enter 1 to proceed with install into Location: "
    read -r key_press

    if [[ "$key_press" != "1" ]]
    then
        printf "Aborting installation.\n"
        exit 1
    fi

    printf "Moving into location... \n"

    eval cd "$location"
    git clone https://github.com/DavidMacDonald11/Sea-Programming-Language.git sea_lang

    if [[ "$?" == "128" ]]
    then
        printf "The location requires sudo permission to write into: \n"
        sudo git clone https://github.com/DavidMacDonald11/Sea-Programming-Language.git sea_lang
    fi

    location=$(printf "%s\n" "${location%/}")/sea_lang

    eval cd "$location"
    make venv

    if [[ "$?" == "128" ]]
    then
        printf "The location requires sudo permission to write into: \n"
        sudo make venv
    fi

    printf "Done.\n"
elif [[ "$key_press" == "2" ]]
then
    printf "\nWhere is your custom Sea installation?\n"
    printf "Location: "
    read -r location
    location=$(printf "%s/\n" "${location%/}")

    condition="$(echo "$location" | grep sea_lang)"

    while [[ ! -d "$location" || "$condition" == "" ]]
    do
        if [[ "$condition" == "" ]]
        then
            printf "\nThe folder name must include 'sea_lang'."
        fi

        printf "\n'%s' is not a valid directory.\n" "$location"
        printf "Perhaps use 'mkdir' in another terminal.\n"
        printf "Enter 1 to change the directory;\n"
        printf "Enter 2 to try again (used mkdir): "
        read -r key_press

        if [[ "$key_press" == "1" ]]
        then
            printf "Location: "
            read -r location
            location=$(printf "%s/\n" "${location%/}")
        elif [[ "$key_press" != "2" ]]
        then
            printf "Aborting installation.\n"
            exit 1
        fi

        condition="$(echo "$location" | grep sea_lang)"
    done

    printf "\nLocation is a valid directory.\n"
else
    printf "Aborting installation.\n"
    exit 1
fi

printf "\nThe installer will now edit '~/.bashrc' to add a global 'sea' command "
printf "linked to the entered location.\n"
printf "This will override any pre-existing 'sea' command.\n"
printf "Enter 1 to proceed: "
read -r key_press

if [[ "$key_press" != "1" ]]
then
    printf "Aborting installation.\n"
    exit 1
fi

location=$(printf "%s\n" "${location%/}")
printf "Writing... "

{ printf "\n# Auto-Generated Sea Language Command\n";
printf "export PATH=\"\$PATH:%s\"\n" "$location";
printf "alias sea='%s/sea.bash'" "$location"; }  >> ~/.bashrc

printf "Done\n"

printf "\nYou may need to restart your terminal to cement these changes.\n"
printf "\nIf the installer did not work, do not attempt to run it again. "
printf "It will proabably only make things worse.\n"
printf "Reach out to the developer to improve this installer.\n"

#!/bin/bash

parse_path_var() {
    paths=("$(printenv PATH | tr ":" "\n")")
    sea_paths=()

    for path in "${paths[@]}"
    do
        check="$(echo "$path" | grep sea_lang)"

        if [[ "$check" != "" ]]
        then
            sea_paths+=("$check")
        fi
    done

    if [[ "${#sea_paths[@]}" -lt "1" ]]
    then
        printf "You must set up your PATH variable for Sea.\n"
        exit 2
    fi

    sea_lang="${sea_paths[0]}"
    eval cd "$sea_lang"

    if [[ ! -f Makefile ]]
    then
        printf "Incorrect directory listed in PATH variable.\n"
        exit 3
    fi

    if [[ ! -d venv ]]
    then
        make venv
        result="$?"

        if [[ "$result" != "2" ]]
        then
            printf "Incorrect directory listed in PATH variable.\n"
            exit 3
        elif [[ "$result" == "2" ]]
        then
            sudo make venv
        fi
    fi
}

working="$(pwd | sed s/' '/'\\ '/g)"

if [[ "$0" != "./sea.bash" ]]
then
    parse_path_var
else
    sea_lang="$working"
fi

eval cd "$working"

print_help() {
    printf "\t--help or -h              "
    printf "\tprints the sea command's usage information.\n\n"
}

print_install() {
    printf "\t--install or -i           "
    printf "\twalks the user through the installation process.\n\n"
}

print_update() {
    printf "\t--update or -u            "
    printf "\tuses git to update sea to the latest version.\n\n"
}

print_debug() {
    printf "\t--debug or -d             "
    printf "\tprints the generated tokens and AST for debugging.\n\n"
}

print_mode() {
    printf "\t--mode=[MODE] or -m=[MODE]"
    printf "\tallows for file transpilation, compilation,\n"
    printf "\t                          "
    printf "\tor interpretation. Excluding this argument will \n"
    printf "\t                          "
    printf "\topen the interpreter's terminal interface.\n"
    printf "\t                          "
    printf "\t[MODE] can be: \n"
    printf "\t                          "
    printf "\t\tt (for transpilation)\n"
    printf "\t                          "
    printf "\t\tc (for compilation)\n"
    printf "\t                          "
    printf "\t\ti (for interpretation)\n\n"
}

print_sea_dir() {
    printf "\t-s [DIR]                  "
    printf "\tspecifies the source directory of Sea files\n"
    printf "\t                          "
    printf "\tto use when using mode t, c, or i.\n\n"
}

print_c_src_dir() {
    printf "\t-c [DIR]                  "
    printf "\tspecifies the directory to place C files\n"
    printf "\t                          "
    printf "\tinto when using mode t or c.\n\n"
}

print_bin_dir() {
    printf "\t-b [DIR]                  "
    printf "\tspecifies the directory to place binary files\n"
    printf "\t                          "
    printf "\tinto when using mode t or c.\n\n"
}

usage() {
    printf "Usage: sea [options...] [files|dirs...]\n"
    printf "Options:\n"

    print_help
    print_install
    print_update
    print_debug
    print_mode
    print_sea_dir
    print_c_src_dir
    print_bin_dir
}

update() {
    git pull origin main
}

mode="None"
debug="False"
in_dir="input"
out_dir="output"
bin_dir="bin"
paths=()

for (( i=1; i <= "$#"; i++ ))
do
    if [[ "${!i}" == "--help" ||  "${!i}" == "-h" ]]
    then
        usage
        exit 1
    fi

    if [[ "${!i}" == "--install" || "${!i}" == "-i" ]]
    then
        ./installer.bash
        exit $?
    fi

    if [[ "${!i}" == "--update" ||  "${!i}" == "-u" ]]
    then
        update
        exit 0
    fi

    if [[ "${!i}" == "--debug" ||  "${!i}" == "-d" ]]
    then
        debug="True"
        continue
    fi

    if [[ "${!i}" == --mode=* ||  "${!i}" == -m=* ]]
    then
        mode=$(echo "${!i}" | awk -F= '{print tolower($2)}')
        mode=${mode::1}

        if [[ "$mode" != "t" && "$mode" != "c" && "$mode" != "i" ]]
        then
            usage
            exit 1
        fi

        continue
    fi

    if [[ "${!i}" == "-s" ]]
    then
        (( i++ ))
        in_dir="${!i}"
        continue
    fi

    if [[ "${!i}" == "-c" ]]
    then
        (( i++ ))
        out_dir="${!i}"
        continue
    fi

    if [[ "${!i}" == "-b" ]]
    then
        (( i++ ))
        bin_dir="${!i}"
        continue
    fi

    if [[ "${!i}" == -* || "${!i}" == --* ]]
    then
        usage
        exit 1
    fi

    paths+=("${!i}")
done

eval cd "$sea_lang"
source venv/bin/activate
eval cd "$working"

python=$(printf '%s/venv/bin/python3' "$sea_lang")
main=$(printf '%s/modules/main.py' "$sea_lang")

case "$mode" in
    "None"|"t"|"c"|"i")
        eval "$python" "$main" "$mode" "$debug" "$in_dir" "$out_dir" "$bin_dir" "${paths[@]}"
        ;;
    *)
        usage
        exit 1
        ;;
esac

exit 0

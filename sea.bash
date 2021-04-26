#!/bin/bash

paths=("$(printenv PATH | tr ":" "\n")")
sea_lang_paths=()

for path in "${paths[@]}"
do
    check="$(echo "$path" | grep Sea)"

    if [[ "$check" != "" ]]
    then
        sea_lang_paths+=("$check")
    fi
done

if [[ "${#sea_lang_paths[@]}" -lt "1" ]]
then
    printf "You must set up your PATH variable for Sea.\n"
    exit 2
fi

sea_lang="${sea_lang_paths[0]}"
working="$(pwd | sed s/' '/'\\ '/g)"

eval cd "$sea_lang"

if [[ ! -f Makefile ]]
then
    printf "Incorrect directory listed in PATH variable.\n"
    exit 3
fi

if [[ ! -d venv ]]
then
    if make venv
    then
        printf "Incorrect directory listed in PATH variable.\n"
        exit 3
    fi
fi

eval cd "$working"

print_help() {
    printf "\t--help or -h              "
    printf "\tprints the sea command's usage information.\n\n"
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
    printf "\tSpecifies the source directory of Sea files\n"
    printf "\t                          "
    printf "\tto use when using mode t, c, or i.\n\n"
}

print_c_src_dir() {
    printf "\t-c [DIR]                  "
    printf "\tSpecifies the directory to place C files\n"
    printf "\t                          "
    printf "\tinto when using mode t or c.\n\n"
}

print_bin_dir() {
    printf "\t-b [DIR]                  "
    printf "\tSpecifies the directory to place binary files\n"
    printf "\t                          "
    printf "\tinto when using mode t or c.\n\n"
}

usage() {
    printf "Usage: sea [options...] [files|dirs...]\n"
    printf "Options:\n"

    print_help
    print_debug
    print_mode
    print_sea_dir
    print_c_src_dir
    print_bin_dir
}

mode="None"
debug="False"
input_dir="input"
output_dir="output"
bin_dir="bin"
paths=()

for (( i=1; i <= "$#"; i++ ))
do
    if [[ "${!i}" == "--help" ||  "${!i}" == "-h" ]]
    then
        usage
        exit 1
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
        input_dir="${!i}"
        continue
    fi

    if [[ "${!i}" == "-c" ]]
    then
        (( i++ ))
        output_dir="${!i}"
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

python=$(printf '%s' "$sea_lang"; printf "venv/bin/python3")
main=$(printf '%s' "$sea_lang"; printf "modules/main.py")

case "$mode" in
    "None"|"t"|"c"|"i")
        eval "$python" "$main" "$mode" "$debug" "$input_dir" "$output_dir" "$bin_dir" "${paths[@]}"
        ;;
    *)
        usage
        exit 1
        ;;
esac

exit 0
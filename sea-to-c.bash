src_dir="src"
bin_dir="bin"

for (( i=1; i <= "$#"; i++ ))
do
    if [[ "$i" -eq "1" ]]
    then
        src_dir="${!i}"
    fi

    if [[ "$i" -eq "2" ]]
    then
        bin_dir="${!i}"
    fi
done

if [[ ! -d venv ]]
then
    make venv
fi

source venv/bin/activate

./venv/bin/python3 main.py "$src_dir" "$bin_dir"

exit 0

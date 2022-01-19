for file in $(ls Experiments | grep \.py$ | sed -e 's/\.py$//')
do
    python3 -m Experiments.$file
    echo "$file have done"
done
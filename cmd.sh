python3 -m unzip
echo 'unzip done'
python3 -m preprocess
echo 'preprocess done'
python3 -m integrate
echo 'integrate done'
python3 -m make_bout
echo 'bouts done'

for file in $(ls Exp | grep \.py$ | sed -e 's/\.py$//')
do
    python3 -m Exp.$file > Log/$file.out
    echo "$file have processed"
done
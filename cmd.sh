python3 -m Refactoring.unzip
echo 'unzip done'
python3 -m Refactoring.preprocess
echo 'preprocess done'
python3 -m Refactoring.integrate
echo 'integrate done'
python3 -m Refactoring.make_bout
echo 'bouts done'

for file in $(ls Refactoring/Exp | grep \.py$ | sed -e 's/\.py$//')
do
    python3 -m Refactoring.Exp.$file > Refactoring/Log/$file.out
    echo "$file have processed"
done
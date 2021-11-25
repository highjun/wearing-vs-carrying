python3 -m Preprocess.unzip
echo 'unzip done'
python3 -m Preprocess.preprocess
echo 'preprocess done'
python3 -m Preprocess.integrate
echo 'integrate done'
python3 -m Preprocess.bout
echo 'bouts done'

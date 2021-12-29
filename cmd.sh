# python3 -m Preprocess.unzip
# python3 -m Preprocess.preprocess
# python3 -m Preprocess.integrate
# python3 -m Preprocess.bout
for idx in {2..15}
do
    num=$(printf %02d $idx)
    python3 -m Experiments.$num
done
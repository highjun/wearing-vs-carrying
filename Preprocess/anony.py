import glob
import os, shutil
from tqdm import tqdm

cwd = os.getcwd()
print(cwd)

for name in tqdm(sorted(os.listdir("Raws"))):
    folder = os.path.join("Raws",name)
    while len(os.listdir(folder))== 1:
        folder = os.path.join(folder, os.listdir(folder)[0])
    csvs = set(glob.glob(os.path.join(folder,"*.csv")))
    all = set(glob.glob(os.path.join(folder,"*")))
    for other in all.difference(csvs):
        if os.path.isdir(other):
            shutil.rmtree(other)
        else:
            os.remove(other)     
    shutil.make_archive(f"AnonyZips/{name}", 'zip', folder)
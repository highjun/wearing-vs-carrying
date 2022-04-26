import glob
import os, shutil
import zipfile
from tqdm import tqdm
cwd = os.getcwd()
print(cwd)
target = os.path.join(cwd, "Raws")
if os.path.exists(target):
    shutil.rmtree(target)
os.mkdir(target)

for name in tqdm(sorted(glob.glob(os.path.join(cwd, "Zips/*.zip")))):
    with zipfile.ZipFile(name, 'r') as zip_ref:
        file = os.path.splitext(os.path.basename(name))[0]
        zip_ref.extractall(os.path.join(cwd, f"Raws/{file}"))
import glob
import os
import zipfile
cwd = os.getcwd()
for idx,name in enumerate(sorted(glob.glob(os.path.join(cwd, "Zips/*.zip")))):
    with zipfile.ZipFile(name, 'r') as zip_ref:
        file = os.path.splitext(os.path.basename(name))[0]
        zip_ref.extractall(f"Raws/{file}")
        print(f"{file} zip is done")
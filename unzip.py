import glob
import os, shutil
import zipfile
cwd = os.getcwd()
print(cwd)
# shutil.rmtree(os.path.join(cwd, "Raws"))
# os.mkdir(os.path.join(cwd, "Raws"))

for idx,name in enumerate(sorted(glob.glob(os.path.join(cwd, "Zips/*.zip")))):
    name ="Zips/P32.zip"
    with zipfile.ZipFile(name, 'r') as zip_ref:
        file = os.path.splitext(os.path.basename(name))[0]
        zip_ref.extractall(os.path.join(cwd, f"Raws/{file}"))
        print(f"{file} zip is done")
    break
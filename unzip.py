import glob
import zipfile
for idx,name in enumerate(sorted(glob.glob("Zips/*.zip"))):
    with zipfile.ZipFile(name, 'r') as zip_ref:
        zip_ref.extractall(f"Raws/{str(idx+1).zfill(3)}")
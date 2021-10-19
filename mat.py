import glob
import zipfile
for idx,name in enumerate(sorted(glob.glob("Raws/*.zip"))):
    with zipfile.ZipFile(name, 'r') as zip_ref:
        zip_ref.extractall(f"Datas/{str(idx).zfill(3)}")
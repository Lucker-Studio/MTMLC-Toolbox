import os
import zipfile


def unpack_zip(zip_path: str, target_path: str) -> None:
    if not os.path.isdir(target_path):
        os.makedirs(target_path)
    zipfile.ZipFile(zip_path).extractall(target_path)
    for dirpath, dirnames, filenames in os.walk(target_path):
        for name in dirnames+filenames:
            try:
                newname = name.encode('cp437').decode('utf-8')
                os.rename(os.path.join(target_path, dirpath, name), os.path.join(target_path, dirpath, newname))
            except:
                pass

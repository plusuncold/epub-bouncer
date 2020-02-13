import os
import shutil


# Delete the folder at folder, or if folder does not exist, raise an exception
def delete_folder(folder: str):
    if not isinstance(folder, str) or not folder:
        print('Folder to delete is invalid, so will not be deleted')
        raise TypeError

    if not os.path.exists(folder):
        raise Exception(f'folder {folder} does not exist!')

    try:
        shutil.rmtree(folder)
    except OSError as ex:
        print(f'Error deleting temp folder: {ex.filename} {ex.strerror}')

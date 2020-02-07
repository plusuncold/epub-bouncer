import pytest
import os
import sys
import shutil

DIR = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(DIR, '../bouncer')
print(path)
sys.path.append(path)
from bouncer.bouncer import delete_folder # noqa E402

TEST_TEMP_FOLDER = 'test_temp'


# delete folder
def test_delete_folder_no_folder_provided():
    with pytest.raises(TypeError):
        delete_folder(None)


def test_delete_folder_wrong_type():
    with pytest.raises(TypeError):
        delete_folder(0)


def test_delete_folder_does_not_exist():
    if os.path.exists(TEST_TEMP_FOLDER):
        shutil.rmtree(TEST_TEMP_FOLDER)
    if os.path.exists(TEST_TEMP_FOLDER):
        raise Exception('''test function was unable to remove folder
                            {TEST_TEMP_FOLDER}''')

    with pytest.raises(Exception):
        delete_folder(TEST_TEMP_FOLDER)


def test_delete_folder():
    if not os.path.exists(TEST_TEMP_FOLDER):
        os.makedirs(TEST_TEMP_FOLDER)
    if not os.path.exists(TEST_TEMP_FOLDER):
        raise Exception('''test function was unable to create folder
                            {TEST_TEMP_FOLDER}''')

    delete_folder(TEST_TEMP_FOLDER)

    if not os.path.exists(TEST_TEMP_FOLDER):
        assert True
    else:
        assert False

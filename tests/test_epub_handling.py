import os
import sys
DIR = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(DIR, '../bouncer')
sys.path.append(path)
from bouncer.epub_handling import extract_from_epub_file # noqa E402

TEST_PATH = 'temp_test'


def test_extract_from_epub_file_folder_non_empty():
    # make the temp folder ahead of time and check that
    # only the files from the epub are in that folder

    # make temp folder
    if not os.path.exists(TEST_PATH):
        os.makedirs(TEST_PATH)

    # add test file
    test_file = TEST_PATH + '/test_file_for_extracting'
    open(test_file, 'w').close()

    # extract an epub to the folder
    epub_name = 'tests/test_data/valid_epubs/eng-web.epub'
    extract_from_epub_file(epub_name, TEST_PATH)

    # assert test file is not in the folder
    assert not os.path.exists(test_file)

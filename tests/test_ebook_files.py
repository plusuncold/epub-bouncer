import os
import sys
DIR = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(DIR, '../bouncer')
sys.path.append(path)
from bouncer.bouncer import correct_ebook # noqa E402
from bouncer.file_utils import delete_folder # noqa E402
from bouncer.epub_handling import extract_from_epub_file, write_epub_file # noqa E402
import bouncer.xml_handling as xh # noqa E402


def is_empty(folder: str):
    if not os.path.exists(folder):
        return True
    list_files = [f for f in os.listdir(folder) if not f.startswith('.')]
    return len(list_files) == 0


class TestOnEPUBS:

    def setup_class(self):
        self.temp_folder = 'temp_testing'

        # delete folder if present
        if os.path.exists(self.temp_folder):
            delete_folder(self.temp_folder)

    # test opening eng-web.epub
    def test_open_non_valid(self):
        temp = self.temp_folder

        for epub_name, text_files_test in non_valid_test_epubs.items():
            assert is_empty(temp)

            extract_from_epub_file(epub_name, temp)
            contents = xh.get_contents_path_from_container_file(temp)
            text_files = xh.get_text_file_paths_from_contents_file(contents,
                                                                   temp)
            _ = xh.get_text_elements_from_text_files(text_files)

            assert text_files == text_files_test

            delete_folder(temp)

    def test_open_valid(self):
        temp = self.temp_folder

        for epub_name, text_files_test in valid_test_epubs.items():
            assert is_empty(temp)

            extract_from_epub_file(epub_name, temp)
            contents = xh.get_contents_path_from_container_file(temp)
            text_files = xh.get_text_file_paths_from_contents_file(contents,
                                                                   temp)
            _ = xh.get_text_elements_from_text_files(text_files)

            assert text_files == text_files_test

            delete_folder(temp)

    def test_whole_process_non_valid(self):
        temp = self.temp_folder

        for epub_name, text_files_test in non_valid_test_epubs.items():
            assert is_empty(temp)

            path_corrected = epub_name[:-5] + '_corrected.epub'

            extract_from_epub_file(epub_name, temp)
            contents = xh.get_contents_path_from_container_file(temp)
            text_files = xh.get_text_file_paths_from_contents_file(contents,
                                                                   temp)
            _ = xh.get_text_elements_from_text_files(text_files)

            assert text_files == text_files_test

            corrections = {}
            xh.apply_corrections(corrections, text_files)
            write_epub_file(path_corrected, temp)
            delete_folder(temp)

    def test_whole_process_valid(self):
        temp = self.temp_folder

        for epub_name, text_files_test in valid_test_epubs.items():
            assert is_empty(temp)

            path_corrected = epub_name[:-5] + '_corrected.epub'

            extract_from_epub_file(epub_name, temp)
            contents = xh.get_contents_path_from_container_file(temp)
            text_files = xh.get_text_file_paths_from_contents_file(contents,
                                                                   temp)
            _ = xh.get_text_elements_from_text_files(text_files)

            assert text_files == text_files_test

            corrections = {}
            xh.apply_corrections(corrections, text_files)
            write_epub_file(path_corrected, temp)
            delete_folder(temp)


# TEST DATA
ENG_WEB_FILES = ['temp_testing/OEBPS/1CH.xhtml',
                 'temp_testing/OEBPS/1CO.xhtml',
                 'temp_testing/OEBPS/1ES.xhtml',
                 'temp_testing/OEBPS/1JN.xhtml',
                 'temp_testing/OEBPS/1KI.xhtml',
                 'temp_testing/OEBPS/1MA.xhtml',
                 'temp_testing/OEBPS/1PE.xhtml',
                 'temp_testing/OEBPS/1SA.xhtml',
                 'temp_testing/OEBPS/1TH.xhtml',
                 'temp_testing/OEBPS/1TI.xhtml',
                 'temp_testing/OEBPS/2CH.xhtml',
                 'temp_testing/OEBPS/2CO.xhtml',
                 'temp_testing/OEBPS/2ES.xhtml',
                 'temp_testing/OEBPS/2JN.xhtml',
                 'temp_testing/OEBPS/2KI.xhtml',
                 'temp_testing/OEBPS/2MA.xhtml',
                 'temp_testing/OEBPS/2PE.xhtml',
                 'temp_testing/OEBPS/2SA.xhtml',
                 'temp_testing/OEBPS/2TH.xhtml',
                 'temp_testing/OEBPS/2TI.xhtml',
                 'temp_testing/OEBPS/3JN.xhtml',
                 'temp_testing/OEBPS/3MA.xhtml',
                 'temp_testing/OEBPS/4MA.xhtml',
                 'temp_testing/OEBPS/ACT.xhtml',
                 'temp_testing/OEBPS/AMO.xhtml',
                 'temp_testing/OEBPS/BAR.xhtml',
                 'temp_testing/OEBPS/COL.xhtml',
                 'temp_testing/OEBPS/DAG.xhtml',
                 'temp_testing/OEBPS/DAN.xhtml',
                 'temp_testing/OEBPS/DEU.xhtml',
                 'temp_testing/OEBPS/ECC.xhtml',
                 'temp_testing/OEBPS/EPH.xhtml',
                 'temp_testing/OEBPS/ESG.xhtml',
                 'temp_testing/OEBPS/EST.xhtml',
                 'temp_testing/OEBPS/EXO.xhtml',
                 'temp_testing/OEBPS/EZK.xhtml',
                 'temp_testing/OEBPS/EZR.xhtml',
                 'temp_testing/OEBPS/FRT.xhtml',
                 'temp_testing/OEBPS/GAL.xhtml',
                 'temp_testing/OEBPS/GEN.xhtml',
                 'temp_testing/OEBPS/GLO.xhtml',
                 'temp_testing/OEBPS/HAB.xhtml',
                 'temp_testing/OEBPS/HAG.xhtml',
                 'temp_testing/OEBPS/HEB.xhtml',
                 'temp_testing/OEBPS/HOS.xhtml',
                 'temp_testing/OEBPS/ISA.xhtml',
                 'temp_testing/OEBPS/JAS.xhtml',
                 'temp_testing/OEBPS/JDG.xhtml',
                 'temp_testing/OEBPS/JDT.xhtml',
                 'temp_testing/OEBPS/JER.xhtml',
                 'temp_testing/OEBPS/JHN.xhtml',
                 'temp_testing/OEBPS/JOB.xhtml',
                 'temp_testing/OEBPS/JOL.xhtml',
                 'temp_testing/OEBPS/JON.xhtml',
                 'temp_testing/OEBPS/JOS.xhtml',
                 'temp_testing/OEBPS/JUD.xhtml',
                 'temp_testing/OEBPS/LAM.xhtml',
                 'temp_testing/OEBPS/LEV.xhtml',
                 'temp_testing/OEBPS/LUK.xhtml',
                 'temp_testing/OEBPS/MAL.xhtml',
                 'temp_testing/OEBPS/MAN.xhtml',
                 'temp_testing/OEBPS/MAT.xhtml',
                 'temp_testing/OEBPS/MIC.xhtml',
                 'temp_testing/OEBPS/MRK.xhtml',
                 'temp_testing/OEBPS/NAM.xhtml',
                 'temp_testing/OEBPS/NEH.xhtml',
                 'temp_testing/OEBPS/NUM.xhtml',
                 'temp_testing/OEBPS/OBA.xhtml',
                 'temp_testing/OEBPS/PHM.xhtml',
                 'temp_testing/OEBPS/PHP.xhtml',
                 'temp_testing/OEBPS/PRO.xhtml',
                 'temp_testing/OEBPS/PS2.xhtml',
                 'temp_testing/OEBPS/PSA.xhtml',
                 'temp_testing/OEBPS/REV.xhtml',
                 'temp_testing/OEBPS/ROM.xhtml',
                 'temp_testing/OEBPS/RUT.xhtml',
                 'temp_testing/OEBPS/SIR.xhtml',
                 'temp_testing/OEBPS/SNG.xhtml',
                 'temp_testing/OEBPS/TIT.xhtml',
                 'temp_testing/OEBPS/TOB.xhtml',
                 'temp_testing/OEBPS/WIS.xhtml',
                 'temp_testing/OEBPS/ZEC.xhtml',
                 'temp_testing/OEBPS/ZEP.xhtml',
                 'temp_testing/OEBPS/copyright.xhtml',
                 'temp_testing/OEBPS/cover.xhtml',
                 'temp_testing/OEBPS/index.xhtml']

valid_test_epubs = {
    'tests/test_data/valid_epubs/eng-web.epub': ENG_WEB_FILES
}
non_valid_test_epubs = {
    'tests/test_data/non_valid_epubs/eng-web.epub': ENG_WEB_FILES
}

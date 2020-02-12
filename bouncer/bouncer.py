import correct_spellings
import epub_handling
import xml_handling as xh
import argparse
import shutil
import os


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


def correct_ebook(epub_name: str, temp_folder: str, dict_lang: str):
    # set path and path_corrected
    path = epub_name
    if '.epub' not in epub_name[-5:]:
        path = epub_name + '.epub'
    path_corrected = path[:-5] + '_corrected.epub'

    # Only permit currently allowable dictionaries
    if dict_lang != 'en_US':
        print(f'Bouncer does not support {dict_lang} currently only')
        print(' the en_US dictionary is supported')
        quit()

    # Extract the files from the epub into temp_folder
    epub_handling.extract_from_epub_file(path, temp_folder)

    print('Extracted the ePub files')

    # Get the location of all the files with text in
    contents_path = xh.get_contents_path_from_container_file(temp_folder)
    text_files = xh.get_text_file_paths_from_contents_file(contents_path,
                                                           temp_folder)

    # Read list of paragraphs from text files
    text_from_files = xh.get_text_elements_from_text_files(text_files)

    print('All text read from ePub')

    # Get dict of corrections [original,correction] to be applied
    # to all text_files
    corrections = correct_spellings.corrections_for_words(text_from_files,
                                                          dict_lang)

    print(f'Applying corrections to ePub extracted files...')
    xh.apply_corrections(corrections, text_files)

    print(f'Applied corrections, writing extracted files back to .ePub file')
    epub_handling.write_epub_file(path_corrected, temp_folder)

    print('Wrote corrected ePub!')

    delete_folder(temp_folder)


def main():
    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--epub-name', type=str, default='book', metavar='N',
                        help='the file name of the epub to be corrected')
    parser.add_argument('--dict-lang', type=str, default='en_US', metavar='N',
                        help='the language code of the dictionary to use')
    parser.add_argument('--temp-folder', type=str, default='temp', metavar='N',
                        help='name of the temporary folder created')
    args = parser.parse_args()

    correct_ebook(args.epub_name, args.temp_folder, args.dict_lang)


if __name__ == '__main__':
    main()

from typing import Dict
import correct_spellings
import epub_handling
import xml_handling as xh
import argparse
import string
import re

# ---------------------------------------------------------------------------------------------------


# Apply the corrections to the string file_contents
def correct_file_contents(corrections: Dict[str, str], file_contents: str):
    file_contents_corrected = file_contents
    for orig, corr in corrections.items():
        # Replace (orig, corr) with (orig, corr), (Orig, Corr) and (ORIG, CORR)
        file_contents_corrected = file_contents.replace(orig, corr)
        file_contents_corrected = file_contents.replace(string.capwords(orig),
                                                        string.capwords(corr))
        file_contents_corrected = file_contents.replace(orig.upper(),
                                                        corr.upper())

        # Catch-all for MiXeD case words
        file_contents_corrected = re.sub(orig,
                                         corr.upper(),
                                         file_contents_corrected,
                                         re.IGNORECASE)

    return file_contents_corrected


# Apply the corrections to the text_files, opening them, correcting them,
# and saving them
def apply_corrections(corrections, text_files):
    for text_file in text_files:
        file_contents = ''
        with open(text_file, 'r') as file:
            file_contents = file.read()
        file_contents_with_corrections = correct_file_contents(corrections,
                                                               file_contents)
        with open(text_file, 'w') as file:
            file.write(file_contents_with_corrections)


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

    # set path and path_corrected
    path = args.epub_name
    if '.epub' not in args.epub_name[-5:]:
        path = args.epub_name + '.epub'
    path_corrected = path[:-5] + '_corrected.epub'

    # Only permit currently allowable dictionaries
    if args.dict_lang != 'en_US':
        print(f'Bouncer currently only supports the en_US dictionary')
        quit()

    # Extract the files from the epub into temp_folder
    epub_handling.extract_from_epub_file(path, args.temp_folder)

    print('Extracted the ePub files')

    # Get the location of all the files with text in
    contents_path = xh.get_contents_path_from_container_file(args.temp_folder)
    text_files = xh.get_text_file_paths_from_contents_file(contents_path,
                                                           args.temp_folder)

    # Read dict of unique words (with occurance count) from text files
    unique_words = xh.unique_words_from_text_files(text_files)

    print('Read all words from ePub')

    # Get dict of corrections [original,correction] to be applied
    # to all text_files
    corrections = correct_spellings.corrections_for_words(unique_words,
                                                          args.dict_lang)

    print(f'Applying corrections to ePub extracted files')
    apply_corrections(corrections, text_files)

    print(f'Applied corrections, writing extracted files back to .ePub file')
    epub_handling.write_epub_file(path_corrected, args.temp_folder)

    print('Wrote corrected ePub!')


if __name__ == '__main__':
    main()

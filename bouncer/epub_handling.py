#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 10:39:05 2020

@author: plusuncold
"""

from zipfile import ZipFile
import glob
import os

# Extract all the files from the EPUB archive into the dest_folder
def extract_from_epub_file(path, dest_folder):
    # Open the zip file
    try:
        with ZipFile(path) as zip_file:
            # Extract to temp folder
            zip_file.extractall(dest_folder)
    except:
        print(f'Error opening ePub file {path}, does it exist?')
        quit()
        
# Get a list of the files in the folder, with mimetype as the first in the list
def list_of_files_in_folder(folder: str):
    folder_glob = folder + '/**'
    files = glob.glob(folder_glob, recursive=True)
    files = [ file for file in files if os.path.isfile(file)]

    # Put mimetype file as the first in the list
    mimetype_index = files.index(folder + '/mimetype')
    files[0], files[mimetype_index] = files[mimetype_index], files[0]
    
    return files

# Write all the files in the source_folder to an EPUB archive
def write_epub_file(path, source_folder):
    # Zip the temp folder
    with ZipFile(path, 'w') as zip_file:
        # Write the files in source_file (with any corrections) to corrected filename
        # NOTE: standard requires mimetype file be first file in archive
        files_to_write = list_of_files_in_folder(source_folder)

        for file in files_to_write:
            # Remove the temp folder name before writing
            file_name_in_zip = file[len(source_folder)+1:]
            zip_file.write(file, file_name_in_zip)

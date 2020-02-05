#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 10:39:05 2020

@author: plusuncold
"""

from zipfile import ZipFile
import glob
import os

def extract_from_epub_file(path, dest_folder):
    # Open the zip file
    try:
        with ZipFile(path) as zip_file:
            # Extract to temp folder
            zip_file.extractall(dest_folder)
    except:
        print(f'Error opening ePub file {path}, does it exist?')
        quit()
        
# Get a list of the files in the folder, with mimetype the first in the list
def list_of_files_in_folder(folder: str):
    folder_glob = folder + '/**'
    files = glob.glob(folder_glob, recursive=True)
    files = [ file for file in files if os.path.isfile(file)]
    mimetype_index = files.index(folder + '/mimetype')
    files[0], files[mimetype_index] = files[mimetype_index], files[0]
    return files
        
def write_epub_file(path, source_folder):
    # Zip the temp folder
    with ZipFile(path, 'w') as zip_file:
        # Write the files in temp (with any corrections) to corrected filename
        # NOTE: standard requires mimetype file be first
        files_to_write = list_of_files_in_folder(source_folder)
        for file in files_to_write:
            zip_file.write(file)
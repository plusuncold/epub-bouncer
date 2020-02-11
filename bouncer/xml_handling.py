#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 10:43:24 2020

@author: plusuncold
"""

import xml.etree.ElementTree as ET
from typing import List
import string
import re


# Read META-INF/container.xml for the location of the OPF contents file
def get_contents_path_from_container_file(temp_folder):
    container_file = temp_folder + '/META-INF/container.xml'
    tree = ET.parse(container_file)
    root = tree.getroot()

    # navigate the tree to get <rootfile>
    for rootfiles in root:
        for rootfile in rootfiles:
            # path is at attribute 'full-path'
            opt_contents_path = rootfile.attrib['full-path']
            assert(len(opt_contents_path) != 0)
            opt_contents_path = temp_folder + '/' + opt_contents_path
            return opt_contents_path


# Get list of text files from OPF contents file
def get_text_file_paths_from_contents_file(contents_file_path, temp_folder):
    text_files = []
    root = ET.parse(contents_file_path).getroot()

    # find all xhtml/xml elements in the manifest
    for child in root.findall('{http://www.idpf.org/2007/opf}manifest'):
        text_files = [item.attrib['href']
                      for item in child
                      if item.attrib['media-type'] == 'application/xhtml+xml']

    # place in reference to temp_folder directory
    text_files = [str(temp_folder + '/' + f) for f in text_files]
    return text_files


# Traverse the document tree and add words to the list of text elements
def add_words_from_node_to_text_list(node, text):
    for child in node:
        if child.text:
            text.append(child.text)
        for submember in child:
            # Recursively call function for submember of child
            add_words_from_node_to_text_list(submember, text)


# Returns a dict with unique words and occurances
def get_text_elements_from_text_files(text_file_paths: List[str]):
    text = []
    for text_file_path in text_file_paths:
        root = ET.parse(text_file_path).getroot()
        for body in root.findall('{http://www.w3.org/1999/xhtml}body'):
            add_words_from_node_to_text_list(body, text)
    return text


# Apply the corrections to the string text
def apply_corrections_to_string(corrections, text: str):
    text_corrected = text
    for orig, corr in corrections.items():
        # Replace (orig, corr) with (orig, corr), (Orig, Corr) and (ORIG, CORR)
        text_corrected = text.replace(orig, corr)
        text_corrected = text.replace(string.capwords(orig),
                                      string.capwords(corr))
        text_corrected = text.replace(orig.upper(),
                                      corr.upper())

        # Catch-all for MiXeD case words
        text_corrected = re.sub(orig,
                                corr.upper(),
                                text_corrected,
                                re.IGNORECASE)

    return text_corrected


# Traverse the document tree and apply corrections to each text element
def add_corrections_to_node(corrections, node):
    for child in node:
        if child.text:
            child.text = apply_corrections_to_string(corrections, child.text)
        for submember in child:
            add_corrections_to_node(corrections, submember)


# Apply the corrections to the text_files, opening them, correcting them,
# and saving them
def apply_corrections(corrections, text_files):
    for text_file in text_files:
        root = ET.parse(text_file).getroot()
        for body in root.findall('{http://www.w3.org/1999/xhtml}body'):
            add_corrections_to_node(corrections, body)
        tree = ET.ElementTree(root)
        with open(text_file, 'w') as file:
            tree.write(file)

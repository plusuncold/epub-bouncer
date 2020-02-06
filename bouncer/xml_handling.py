#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 10:43:24 2020

@author: plusuncold
"""

import xml.etree.ElementTree as ET
from typing import List
import re
import contractions


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


# Traverse the document tree and add words to the word_list
def add_words_from_text_to_word_list(body, word_list):
    for child in body:
        if child.text:
            # split the text into words
            text_split = re.findall(r"[\w']+", child.text)

            for word in text_split:
                # check 'word' is not just a ' char
                if not word == '\'':
                    word_list.append(word)
        for submember in child:
            # Recursively call function for submember of child
            add_words_from_text_to_word_list(submember, word_list)


# Strip out non-alphanumeric characters from the beginning and ending of word
def strip_non_alphanum(word):
    if not word:
        return word  # nothing to strip
    for start, ch in enumerate(word):
        if ch.isalnum():
            break
    for end, ch in enumerate(word[::-1]):
        if ch.isalnum():
            break
    return word[start:len(word) - end]


# Strip out common English contractions from word (e.g. they'll)
# leaving just the first part (e.g. they)
def strip_contractions(word):
    word_list = contractions.fix(word).split()
    return word_list[0]


# Remove any saxon genitives (e.g. David's)
def strip_saxon_genitive(word):
    if word[-1] == 's':
        if word[-2] == '\'':
            word = word[:-2]
    return word


# Strip out unnecessary characters
def clean_word(word):
    word = strip_non_alphanum(word)
    word = strip_contractions(word)
    word = strip_saxon_genitive(word)
    return word


# Returns a dict with unique words and occurances
def unique_words_from_text_files(text_file_paths: List[str]):
    all_unique_words = {}
    for text_file_path in text_file_paths:
        root = ET.parse(text_file_path).getroot()
        words = []
        for body in root.findall('{http://www.w3.org/1999/xhtml}body'):
            add_words_from_text_to_word_list(body, words)
        add_list_to_unique_words(all_unique_words, words)
    return all_unique_words


# Merge word_list into unique_words, generating associated count data
def add_list_to_unique_words(unique_words, word_list):
    clean_word_list = [clean_word(word) for word in word_list]
    words_list_set = set(clean_word_list)
    for word in words_list_set:
        if word:

            # set or increment value for word key in unique words
            # key: word
            # value: (count, count_capitalized)
            is_capitalized = True if word[0].isupper() else False
            word_lower = word.lower()
            if unique_words.get(word_lower):
                count, count_capitalized = unique_words.get(word_lower)
                count += 1
                if is_capitalized:
                    count_capitalized += 1
                unique_words[word_lower] = (count, count_capitalized)
            else:
                count_capitalized = 1 if is_capitalized else 0
                unique_words[word_lower] = (1, count_capitalized)
    return unique_words

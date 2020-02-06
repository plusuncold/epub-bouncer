#!/usr/bin/env python3
"""
Created on Tue Feb  4 13:33:27 2020

@author: plusuncold
"""

from typing import Dict
import enchant
import string


def get_user_inputted_word():
    print(f'Input word for correction: (or \'!\' to cancel, or \'@\' to quit) ', end='')
    user_input = input()
    
    if user_input == '!':
        return (None, False)
    elif user_input == '@':
        print('Quitting program')
        quit()
    
    return (user_input, False)
    

def get_correction_for_word(word : str, count : int, count_capitalized : int, dictionary, index : int, total : int):
    if count == count_capitalized:
        word = string.capwords(word)
        print(f'Correct \'{word}\'? (all {count} occurances are capitalized, correction {index} of {total})')
    else:
        print(f'Correct \'{word}\'? ({count} occurances, {count_capitalized} are capitalized, correction {index} of {total})')
        
    print(f'0 - No', end='')
    suggestions = dictionary.suggest(word)
    for key_number, suggestion in enumerate(suggestions):
        if key_number > 9:
            break
        print(f', {key_number+1} - \'{suggestion}\'', end='')
    print('')
    user_input = input()
    if user_input == 'd':
        return (None, True)
    elif user_input == 'e':
        user_input, _ = get_user_inputted_word()
        if user_input:
            return (user_input, False)
    elif user_input == 'q':
        print('Quitting program')
        quit()
    try:
        key_number = int(user_input)
        if key_number == 0:
            return (None, False)
        elif key_number >= 1 and key_number <= 9:
            return (suggestions[key_number-1], False)
    except:
        print(f'Input {user_input} is not valid. Please input \'d\', \'e\' or a number between 0 and 9')
        return get_correction_for_word(word, count, dictionary, index, total)
        


def corrections_for_words(unique_words, dict_lang):
    count_unique_words = len(unique_words)
    d = enchant.Dict(dict_lang)
    misspelled_words = { k: (c, cc) for k, (c, cc) in unique_words.items() if not d.check(k)}
    misspelled_words = sorted(misspelled_words.items(),
                          key=lambda kv: kv[1],
                          reverse=True)
    count_misspelled_words = len(misspelled_words)
    print(f'Of {count_unique_words} unique words in the ePub, {count_misspelled_words} were not found in dictionary \'{dict_lang}\'')
    print('\nCorrect any misspelled words')
    print('Enter:\n\ta number 1-9 to select a correction')
    print('\t\'0\' to leave the word as is')
    print('\t\'e\' to enter the correct word')
    print('\t\'d\' to finish correcting words or')
    print('\t\'q\' to quit\n')
    
    print('Unique misspelled words')
    for word, (_, _) in misspelled_words:
        print(word, end=' ')
    print('')
        
    corrections = {}
    index = 1
    for word, (count, count_capitalized) in misspelled_words:
        correction, finished = get_correction_for_word(word, count, count_capitalized, d, index, count_misspelled_words)
        if finished:
            break
        if correction:
            corrections[word] = correction
        print('')
        index += 1
    return corrections
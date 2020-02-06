#!/usr/bin/env python3
"""
Created on Tue Feb  4 13:33:27 2020

@author: plusuncold
"""
import enchant
import string


# Read word from console, with special control characters
def get_user_inputted_word():
    print(f'Input word for correction: (or \'!\' to cancel) ', end='')
    user_input = input()

    if user_input == '!':
        # cancel word input
        return None

    return user_input


# Get a correction for word with associated data count and count_capitalized
# Return: (word_corrected, is_finished_correcting)
def get_correction_for_word(word: str, count: int, count_capitalized: int,
                            dictionary, index: int, total: int):
    if count == count_capitalized:
        word = string.capwords(word)
        print(f'''Correct \'{word}\'? (all {count} occurances are capitalized,
                   correction {index} of {total})''')
    else:
        print(f'''Correct \'{word}\'? ({count} occurances, {count_capitalized}
                   are capitalized, correction {index} of {total})''')

    print(f'''0 - No correction, e - end correct word, f - finish correcting
               words, q - quit''')
    print('Suggestions: ', end='')

    # Get the suggestions from the dictionary
    suggestions = dictionary.suggest(word)
    for key_number, suggestion in enumerate(suggestions):
        if key_number > 9:
            break
        if key_number == 0:
            print(f'{key_number+1} - \'{suggestion}\'', end='')
        else:
            print(f', {key_number+1} - \'{suggestion}\'', end='')
    print('')

    user_input = input()

    # Check control characters
    if user_input == 'f':
        return (None, True)
    elif user_input == 'e':
        user_input = get_user_inputted_word()
        if user_input:
            return (user_input, False)
    elif user_input == 'q':
        print('Quitting program')
        quit()

    # Get selection from suggestions or no selection
    try:
        key_number = int(user_input)
        if key_number == 0:
            return (None, False)
        elif key_number >= 1 and key_number <= 9:
            return (suggestions[key_number-1], False)
    except ValueError:
        print(f'''Input {user_input} is not valid. Please input \'f\', \'e\',
                   \'q\' or a number between 0 and 9''')
        return get_correction_for_word(word, count, count_capitalized,
                                       dictionary, index, total)


# Interface to get corrections from user
def corrections_for_words(unique_words, dict_lang):
    count_unique_words = len(unique_words)

    # Get a dictionary object for language dict_lang
    d = enchant.Dict(dict_lang)

    # Get misspelled_words by checking against dictionary,
    # then sort by occurance (greatest to least)
    misspelled_words = {k: (c, cc) for k, (c, cc) in unique_words.items()
                        if not d.check(k)}
    misspelled_words = sorted(misspelled_words.items(),
                              key=lambda kv: kv[1],
                              reverse=True)
    count_misspelled_words = len(misspelled_words)

    print(f'''Of {count_unique_words} unique words in the ePub,
               {count_misspelled_words} were not found in dictionary
               \'{dict_lang}\'''')
    print('\nCorrect any misspelled words')
    print('Enter:\n\ta number 1-9 to select a correction')
    print('\t\'0\' to leave the word as is')
    print('\t\'e\' to enter the correct word')
    print('\t\'f\' to finish correcting words or')
    print('\t\'q\' to quit\n')

    print('Unique misspelled words')
    for word, (_, _) in misspelled_words:
        print(word, end=' ')
    print('')

    corrections = {}
    index = 1

    # Iterate through the words that aren't found in the dictionary,
    # getting any corrections
    for word, (count, count_capitalized) in misspelled_words:
        correction, finished = get_correction_for_word(word,
                                                       count,
                                                       count_capitalized,
                                                       d, index,
                                                       count_misspelled_words)
        if finished:
            break
        if correction:
            corrections[word] = correction
        print('')
        index += 1

    return corrections

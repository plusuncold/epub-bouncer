#!/usr/bin/env python3
"""
Created on Tue Feb  4 13:33:27 2020

@author: plusuncold
"""
import enchant
import re
import contractions
from itertools import islice

CONTEXT_LENGTH = 5
CHUNK_SIZE = 5
SPACES_TO_SEARCH = CONTEXT_LENGTH // 2 + 1
ENGLISH_WORD_SPLIT_REGEX = r"[\w']+"
PROPER_NOUN_THRESHOLD = 2


class Unique_Word_Data:
    def __init__(self, word: str, context: str):
        self.count = 1
        self.unique_capitalizations = {word: 1}
        self.contexts = [context]
        self.word_length = len(word)

    def update(self, word: str, context: str):
        self.count += 1
        self.contexts.append(context)
        # self.unique_capitalizations.add(word)
        count = self.unique_capitalizations.get(word, 0) + 1
        self.unique_capitalizations[word] = count

    def are_all_occurences_capitalized(self):
        for unique_capitalization in self.unique_capitalizations:
            if not unique_capitalization[0].isupper():
                return False
        return True

    def get_capitalized(self):
        return list(self.unique_capitalizations)[0]

    def get_display_version_of_word(self):
        return max(self.unique_capitalizations,
                   key=self.unique_capitalizations.get)

    def get_context_example(self):
        for context in self.contexts:
            if len(context) > self.word_length:
                return context
        return self.contexts[0]

    def __str__(self):
        retStr = ''
        retStr += '\tCount ' + str(self.count) + '\n'
        retStr += '\tUnique Capitalizations '
        retStr += str(self.unique_capitalizations) + '\n'
        retStr += '\tContexts ' + str(self.contexts)
        return retStr

    def __lt__(self, other):
        return self.count < other.count


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
def get_correction_for_word(word: str, data: Unique_Word_Data,
                            dictionary, index: int, total: int):
    if data.are_all_occurences_capitalized():
        cap_word = data.get_capitalized()
        output = f'Correct \'{cap_word}\'? (all {data.count} occurances'
        output += f' are capitalized, correction {index} of {total})'
        print(output)
    else:
        output = f'Correct \'{word}\'? ({data.count} occurances, '
        output += f'correction {index} of {total})'
        print(output)

    print(f'Example: "{data.get_context_example()}"')

    output = f'0 - No correction, e - enter correct word, f - finish '
    output += 'correcting words, q - quit'
    print(output)
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
        else:
            return get_context_for_word(word, data, dictionary, index, total)
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
        else:
            print(f'{key_number} is not a valid number for input')
            return get_correction_for_word(word, data, dictionary,
                                           index, total)
    except ValueError:
        output = f'Input {user_input} is not valid. Please input \'f\', \'e\''
        output += ',\'q\' or a number between 0 and 9'
        print(output)
        return get_correction_for_word(word, data, dictionary, index, total)


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
    if not isinstance(word, str):
        raise TypeError

    # Catch some contractions that the contractions package doesn't get
    if word[-3:] == '\'ll':
        return word[:-3]

    # Get list of constituent words
    word_list = contractions.fix(word).split()

    # Return only the original length of the word (bug in contractions
    # doesn't preserve capitalization)
    return word[:len(word_list[0])]


# Remove any saxon genitives (e.g. David's)
def strip_saxon_genitive(word):
    if word[-2:] == '\'s':
        word = word[:-2]
    return word


# Strip out unnecessary characters
def clean_word(word: str, lang: str):
    word = strip_non_alphanum(word)

    if lang[:2] == 'en':
        word = strip_contractions(word)
        word = strip_saxon_genitive(word)

    word = strip_non_alphanum(word)

    return word


def get_full(index, text, lang):
    # if there is an alphanumeric character before a space character
    # either before or after the index is not for a full word
    if not lang[:2] == 'en':
        print(f'Cannot match for language {lang}')
        quit()

    start = index
    space_found = False

    while not space_found:
        if start == 0:
            break
        start -= 1
        if not re.match(ENGLISH_WORD_SPLIT_REGEX, text[start:start+1]):
            space_found = True
            start += 1

    space_found = False
    end = index

    while not space_found:
        if end >= len(text):
            break
        end += 1
        if not re.match(ENGLISH_WORD_SPLIT_REGEX, text[end:end+1]):
            space_found = True
            end -= 1

    return text[start:end+1]


def get_context_for_word(index, text, word, text_split, lang):
    # Find the indices that word appears in text
    # Find the which occurance index of text_split corresponds to

    positions_word_found_in_text = [m.start() for m in re.finditer(word, text)
                                    if get_full(m.start(), text, lang) == word]
    positions_word_found_in_split = [i
                                     for i, x in enumerate(text_split)
                                     if x == word]
    index_of_this_occurance = 0
    while not positions_word_found_in_split[index_of_this_occurance] == index:
        index_of_this_occurance += 1

    string_index = positions_word_found_in_text[index_of_this_occurance]
    spaces_found = 0
    prior_index = string_index

    while spaces_found < SPACES_TO_SEARCH:
        if prior_index == 0:
            break
        prior_index -= 1
        if text[prior_index] == ' ':
            spaces_found += 1

    if not prior_index == 0:
        prior_index += 1

    spaces_found = 0
    posterior_index = string_index

    while spaces_found < SPACES_TO_SEARCH:
        if posterior_index >= len(text) - 1:
            posterior_index = len(text)
            break
        posterior_index += 1
        if text[posterior_index] == ' ':
            spaces_found += 1

    return text[prior_index:posterior_index]


# Merge word_list into unique_words, generating associated count data
def add_word_to_unique_words(word, index_of_word_in_split, text_element_split,
                             text_element, unique_words, lang):
    word_clean = clean_word(word, lang)

    if word_clean:
        if word_clean == '\'':
            return

        context = get_context_for_word(index_of_word_in_split,
                                       text_element, word,
                                       text_element_split, lang)

        word_lower = word_clean.lower()

        if unique_words.get(word_lower):
            unique_words[word_lower].update(word_clean, context)
        else:
            unique_words[word_lower] = Unique_Word_Data(word_clean, context)


# Split a text string according to language rules
def split_element_for_lang(text: str, lang: str):
    if lang[:2] == 'en':
        # split the text into words
        text_split = re.findall(ENGLISH_WORD_SPLIT_REGEX, text)
        return text_split
    else:
        output = f'Cannot split text element for {lang} '
        output += '(Not currently supported)'
        print(output)

    # Only reached if no valid lang is given
    quit()


# Make a dict of unique words with associated data, using lang
def get_unique_words_and_data(text_list, lang):

    # Can only deal with English for the moment
    assert lang[:2] == 'en'

    unique_words = {}

    # Iterate through the text lists
    for text_element in text_list:
        # text_element is a continuous string from the epub
        text_element_split = split_element_for_lang(text_element, lang)
        for index, word in enumerate(text_element_split):
            add_word_to_unique_words(word, index, text_element_split,
                                     text_element, unique_words, lang)

    return unique_words


def chunker(chunk_size, iterable):
    it = iter(iterable)
    for i in range(0, len(iterable), chunk_size):
        yield {k: iterable[k] for k in islice(it, chunk_size)}


def exclude_proper_nouns(words):
    excluded_words = []

    possible_proper_nouns = {k: v
                             for k, v in words.items()
                             if v.are_all_occurences_capitalized() and
                             v.count >= PROPER_NOUN_THRESHOLD}

    print(f'There are {len(possible_proper_nouns)} possible ', end='')
    print('proper nouns not found in the dictionary (e.g. names). ', end='')
    print('Accept any that are not misspellings.\n')
    set_count = 1
    total_sets = len(possible_proper_nouns) // CHUNK_SIZE + 1

    for chunk in chunker(CHUNK_SIZE, possible_proper_nouns):
        print(f'Set {set_count} of {total_sets}')

        for word, data in chunk.items():
            print('\t', data.get_display_version_of_word(), end='\t')
            print(f' e.g. "{data.get_context_example()}"')
        print('')

        user_input = ''
        while user_input not in ['y', 'Y', 'n', 'N']:
            print('y - accept all, ', end='')
            print('n - some are not proper nouns or have errors')
            user_input = input()

        if user_input in ['y', 'Y']:
            for word in chunk:
                excluded_words.append(word)

        set_count += 1
        print('')

    print(f'\n\nExcluded {len(excluded_words)} words from corrections')

    misspelled_words = {k: v
                        for k, v in words.items()
                        if k not in excluded_words}

    print(f'{len(misspelled_words)} words to correct')

    return misspelled_words


def proper_nouns_are_capitalized_with_language(dict_lang: str):
    if dict_lang[:2] == 'en':
        return True

    print(f'Dictionary {dict_lang} is unsupported')
    quit()


# Interface to get corrections from user
def corrections_for_words(text, dict_lang):
    # Start by obtaining unique words and associated data
    print('Extracting word data...')
    unique_words = get_unique_words_and_data(text, dict_lang)
    print('Word data extracted!')

    count_unique_words = len(unique_words)

    # Get a dictionary object for language dict_lang
    d = enchant.Dict(dict_lang)

    # Get misspelled_words by checking against dictionary,
    # then sort by occurance (greatest to least)
    misspelled_words = {k: data for k, data in unique_words.items()
                        if not d.check(k)}

    count_misspelled_words = len(misspelled_words)

    unique_word_info = f'\nOf {count_unique_words} unique words in the ePub, '
    unique_word_info += f'{count_misspelled_words} were not found in '
    unique_word_info += f'dictionary \'{dict_lang}\''
    print(unique_word_info)

    misspelled_words = {k: v for k, v in sorted(misspelled_words.items(),
                                                key=lambda kv: kv[1],
                                                reverse=True)}

    print('\nUnique words not found in dictionary:')
    for v, data in misspelled_words.items():
        print(data.get_display_version_of_word(), end=' ')
    print('')

    corrections = {}
    index = 1

    # Exclusion of proper nouns
    if proper_nouns_are_capitalized_with_language(dict_lang):
        print('\n\n-----------------------------------------------------')
        print('Correct words - Stage 1 of 2 - Filter out names, etc.')
        print('-----------------------------------------------------\n\n')
        misspelled_words = exclude_proper_nouns(misspelled_words)
        count_misspelled_words = len(misspelled_words)
    else:
        print('\n\n------------------------------------')
        print('Correct words - Skipped Stage 1 of 2')
        print('------------------------------------\n\n')

    print('\n\n-------------------------------------------------------------')
    print('Correct words - Stage 2 of 2 - Search and replace wrong words')
    print('-------------------------------------------------------------\n')

    print('Correct any misspelled words')
    print('Enter:\n\ta number 1-9 to select a correction')
    print('\t\'0\' to leave the word as is')
    print('\t\'e\' to enter the correct word')
    print('\t\'f\' to finish correcting words or')
    print('\t\'q\' to quit\n')

    # Iterate through the words that aren't found in the dictionary,
    # getting any corrections
    for word, data in misspelled_words.items():
        correction, finished = get_correction_for_word(word,
                                                       data,
                                                       d, index,
                                                       count_misspelled_words)
        if finished:
            break
        if correction:
            corrections[word] = correction
        print('')
        index += 1

    return corrections

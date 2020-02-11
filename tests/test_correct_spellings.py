import pytest
import os
import sys
DIR = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(DIR, '../bouncer')
sys.path.append(path)
from bouncer.correct_spellings import strip_non_alphanum, strip_contractions, strip_saxon_genitive, clean_word # noqa E402


COMMON_CONTRACTIONS = {
    'Dave\'ll': 'Dave',
    'I\'m': 'I',
    'i\'m': 'i',
    'i\'ll': 'i',
    'i\'ve': 'i',
    'he\'ll': 'he',
    'it\'d': 'it',
    'it\'s': 'it',
    'hasn\'t': 'has',
    'mightn\'t': 'might',
    'You\'re': 'You',
}


# strip_non_alphanum
def test_strip_non_alphanum_non_string():
    with pytest.raises(TypeError):
        strip_non_alphanum(1)


def test_strip_non_alphanum_just_alphanum():
    assert strip_non_alphanum('bob') == 'bob'


def test_strip_non_alphanum_non_alphanum_before():
    assert strip_non_alphanum('#jane') == 'jane'


def test_strip_non_alphanum_non_alphanum_after():
    assert strip_non_alphanum('janet-') == 'janet'


def test_strip_non_alphanum_non_alphanum_before_and_after():
    assert strip_non_alphanum('@Callum-') == 'Callum'


# strip_contractions
def test_strip_contractions_non_string():
    with pytest.raises(TypeError):
        strip_contractions(585)


def test_strip_contractions_non_contracted():
    assert strip_contractions('bob') == 'bob'


def test_strip_contractions_common_contractions():
    for key, value in COMMON_CONTRACTIONS.items():
        assert strip_contractions(key) == value


# strip saxon genitive (posessive)
def test_strip_saxon_genitive_non_string():
    with pytest.raises(TypeError):
        strip_saxon_genitive(6)


def test_strip_saxon_genitive_non_genitive():
    assert strip_saxon_genitive('bob') == 'bob'


def test_strip_saxon_genitive_genitive():
    assert strip_saxon_genitive('kate\'s') == 'kate'


# clean word
def test_clean_word_saxon_gen_contractions_non_alphanum():
    assert clean_word('-Vin\'s,"', 'en-US') == 'Vin'


def test_clean_word_saxon_genitive_only():
    assert clean_word('bob\'s', 'en-US') == 'bob'


def test_clean_word_non_alphanum():
    assert clean_word('"life-', 'en-US') == 'life'


def test_clean_word_contractions():
    for key, value in COMMON_CONTRACTIONS.items():
        assert clean_word(key, 'en-US') == value

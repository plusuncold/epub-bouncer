import pytest
from bouncer.xml_handling import strip_non_alphanum, strip_contractions


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
    common_contractions = {
        'Dave\'ll': 'Dave',
        'I\'m': 'I',
        'he\'ll': 'he',
        'it\'d': 'it',
        'it\'s': 'it',
        'hasn\'t': 'has',
        'mightn\'t': 'might',
        'You\'re': 'You',
    }
    for key, value in common_contractions.items():
        print(key, value, strip_contractions(key))
        assert strip_contractions(key) == value

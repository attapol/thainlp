# -*- coding: utf8 -*-

#TODO: make it python3 compatible by using chr instead of unichr

CONSONANTS = set([unichr(ord(u'ก') + i) for i in range(46)])
VOWELS = set([unichr(ord(u'ฯ') + i) for i in range(12)])
VOWEL_TONE_NUMBERS = set([unichr(ord(u'฿') + i) for i in range(29)])

THAI_CHAR_SET = CONSONANTS.union(VOWELS).union(VOWEL_TONE_NUMBERS)

def is_thai_char(character):
    return character in THAI_CHAR_SET

def is_consonant(character):
    return character in CONSONANTS

def is_vowel(character):
    return character in VOWELS

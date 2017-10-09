# -*- coding: utf8 -*-
import nltk

CONSONANTS = [unichr(ord(u'ก') + i) for i in range(46)]
SINGLE_PREFIX_VOWEL = [u'เ', u'แ', u'โ']
SINGLE_SUFFIX_VOWEL = [u'ะ', u'า', u' ิ', u' ี', u' ึ', u' ื' ]
SINGLE_SUFFIX_WITH_FINAL_VOWEL = [u' ื', u' ั']
TONE_MARKERS = [u' ่', u' ้', u' ๊', u' ๋']

def terminalize(char_set):
    stripped_char_set = [x.strip() for x in char_set]
    return u"'" + u"' | '".join(stripped_char_set) + u"'"

#vowel_set1 = [unichr(ord(u'ฯ') + i) for i in range(12)]
#vowel_tone_numbers =[unichr(ord(u'฿') + i) for i in range(29)]
#thai_char_list = consonants + vowel_set1 + vowel_tone_numbers
#THAI_CHAR_SET = set(thai_char_list)

MAIN_GRAMMAR_STR = u"""
S -> A S 
S -> A
A -> C V
C -> {}
V -> 'า'
T -> {} 
""".format(terminalize(CONSONANTS), terminalize(TONE_MARKERS))

SPV_RULES = u"""
A -> SPV C | SPV C SPV_FINAL | SPV C T | SPV C T SPV_FINAL
SPV -> {}
SPV_FINAL -> 'ะ' | C
""".format(terminalize(SINGLE_PREFIX_VOWEL))

SSV_RULES = u"""
A -> C SSV | C SSV C | C T SSV | C T SSV C
SSV -> {}
""".format(terminalize(SINGLE_SUFFIX_VOWEL))


GRAMMAR_STR = MAIN_GRAMMAR_STR + SPV_RULES + SSV_RULES

ATOMIC_ROOT_SYMBOL_SET = set([u'A'])

GRAMMAR = nltk.CFG.fromstring(GRAMMAR_STR)
PARSER = nltk.ChartParser(GRAMMAR)


def parse_syllables(text):
    results = PARSER.parse_all(text)
    if len(results) == 0:
        return []
    syllables = []
    extract_syllables_from_tree(results[0], syllables)
    return syllables

def extract_syllables_from_tree(root, so_far):
    if root.label() in ATOMIC_ROOT_SYMBOL_SET:
        so_far.append(u''.join(root.leaves()))
        return
    for subtree in root:
        extract_syllables_from_tree(subtree, so_far)
    

if __name__ == '__main__':
    print '|'.join(parse_syllables(u'กากา'))
    print '|'.join(parse_syllables(u'เจ'))
    print '|'.join(parse_syllables(u'เตะ'))
    print '|'.join(parse_syllables(u'เต้น'))
    print '|'.join(parse_syllables(u'เต๊ะ'))
    print '|'.join(parse_syllables(u'ก้าม'))
    print '|'.join(parse_syllables(u'กาก'))

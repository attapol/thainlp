# -*- coding: utf8 -*-
import nltk

CONSONANTS = [unichr(ord(u'ก') + i) for i in range(46)]
SINGLE_PREFIX_VOWEL = [u'เ', u'แ', u'โ']
SINGLE_SUFFIX_VOWEL = [u'ะ', u'า']
SINGLE_TOP_VOWEL = [u' ิ', u' ี', u' ึ', u' ื' ]
SINGLE_TOP_VOWEL_WITH_FINAL = [u' ื', u' ั']
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
CT -> C T | C
TC -> T C | C
""".format(terminalize(CONSONANTS), terminalize(TONE_MARKERS))

SPV_RULES = u"""
A -> SPV CT | SPV CT SPV_FINAL 
SPV -> {}
SPV_FINAL -> 'ะ' | C
""".format(terminalize(SINGLE_PREFIX_VOWEL))

SSV_RULES = u"""
A -> CT SSV | CT SSV C | C STV | C STV T | C STV TC | CT STV_F TC 
SSV -> {}
STV -> {}
STV_F -> {}
""".format(terminalize(SINGLE_SUFFIX_VOWEL), 
        terminalize(SINGLE_TOP_VOWEL),
        terminalize(SINGLE_TOP_VOWEL_WITH_FINAL))

DIPHTHONG_RULES = u"""
A -> 'เ' C DIPH | C UA
DIPH -> IA | UEA 
IA -> 'ี' 'ย' | 'ี' T 'ย' | 'ี' 'ย' SPV_FINAL | 'ี' T 'ย' SPV_FINAL
UEA -> 'ื' 'อ' | 'ื' T 'อ' |  'ื' 'อ' SPV_FINAL | 'ื' T 'อ' SPV_FINAL
UA -> 'ั' 'ว' | 'ั' T 'ว' | 'ั' 'ว' 'ะ' | 'ั' T 'ว' 'ะ' | 'ว' C | T 'ว' C
"""

GRAMMAR_STR = MAIN_GRAMMAR_STR + SPV_RULES + SSV_RULES + DIPHTHONG_RULES

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
    test_cases = [u'วัน',u'นี้', u'กิน', u'ข้าว', u'มา', u'แล้ว',
            u'วันนี้',
            u'กินข้าว',
            u'วันนี้กินข้าว',
            u'วันนี้กินข้าวมาแล้ว']
    for test_case in test_cases:
        print '|'.join(parse_syllables(test_case))
    
    print '|'.join(parse_syllables(u'กากา'))
    print '|'.join(parse_syllables(u'เจ'))
    print '|'.join(parse_syllables(u'จี้'))
    print '|'.join(parse_syllables(u'เตะ'))
    print '|'.join(parse_syllables(u'เต้น'))
    print '|'.join(parse_syllables(u'เต๊ะ'))
    print '|'.join(parse_syllables(u'ก้าม'))
    print '|'.join(parse_syllables(u'กาก'))
    print '|'.join(parse_syllables(u'เสีย'))
    print '|'.join(parse_syllables(u'เสือ'))
    print '|'.join(parse_syllables(u'เสียง'))
    print '|'.join(parse_syllables(u'เสี่ยง'))
    print '|'.join(parse_syllables(u'ดวง'))
    print '|'.join(parse_syllables(u'ด้วง'))
    print '|'.join(parse_syllables(u'ตัว'))

    #print '|'.join(parse_syllables(u'วันนี้เป็นวันสงกรานต์'))

# -*- coding: utf8 -*-
import nltk

CONSONANTS = [unichr(ord(u'ก') + i) for i in range(46)]
SINGLE_PREFIX_VOWEL = [u'เ', u'แ', u'โ']
SINGLE_SUFFIX_VOWEL_OPT_FINAL = [u'า', u'อ', u' ุ', u' ู']
SINGLE_TOP_VOWEL = [u' ิ', u' ี', u' ึ' ]
SINGLE_TOP_VOWEL_WITH_FINAL = [u' ื', u' ั']
TONE_MARKERS = [u' ่', u' ้', u' ๊', u' ๋']

HIGH_CONSONANTS = [x for x in u'ขฃฉผฝถฐสศษห']
MID_CONSONANTS = [x for x in u'กจฎฏดตบปอ']
LOW_SINGLE_CONSONANTS  = [x for x in u'งญณนมยรลวฬ']

STOP_CONSONANTS = [x for x in u'บปพฟภจชซฌฎฏฐฑฒดตถทธศษสกขคฆ']
NON_APPROXIMANT_FINALS = [x for x in u'มญณนรลฬงบปพฟภจชซฌฎฏฐฑฒดตถทธศษสกขคฆ']
APPROXIMANT_FINALS = [u'ว', u'ย']
CONSONANTS_FINALS = APPROXIMANT_FINALS + NON_APPROXIMANT_FINALS


def terminalize(char_set):
    stripped_char_set = [x.strip() for x in char_set]
    return u"'" + u"' | '".join(stripped_char_set) + u"'"

#vowel_set1 = [unichr(ord(u'ฯ') + i) for i in range(12)]
#vowel_tone_numbers =[unichr(ord(u'฿') + i) for i in range(29)]
#thai_char_list = consonants + vowel_set1 + vowel_tone_numbers
#THAI_CHAR_SET = set(thai_char_list)

MAIN_GRAMMAR_STR = u"""
S -> SYLLABLE | SYLLABLE S
SYLLABLE -> A SILENT
C -> {}
HC -> {}
MC -> {}
LC -> {}
T -> {} | 
""".format(
        terminalize(CONSONANTS), 
        terminalize(HIGH_CONSONANTS), 
        terminalize(MID_CONSONANTS), 
        terminalize(LOW_SINGLE_CONSONANTS), 
        terminalize(TONE_MARKERS)
        )

CONSONANT_CLUSTER = u"""
CC -> C_LIQUID | C_LEAD
C_LIQUID -> STOP LIQUID | 'ฟ' LIQUID
LIQUID -> 'ร' | 'ล' | 'ว'
C_LEAD -> HC LC | MC LC | 'อ' 'ย'

IC -> CC T | C T
FC -> FINALS | FINALS 'ร'
SILENT -> C '์' | C C '์' | C 'ิ' '์' | C 'ุ' '์' |
STOP -> {}
NON_APPROXIMANT_FINALS -> {}
FINALS -> {}
""".format(terminalize(STOP_CONSONANTS),
        terminalize(NON_APPROXIMANT_FINALS),
        terminalize(CONSONANTS_FINALS))

SPV_RULES = u"""
A -> C T NON_APPROXIMANT_FINALS | STOP 'ล' T NON_APPROXIMANT_FINALS
A -> STOP 'ร' T NON_APPROXIMANT_FINALS | C_LEAD T NON_APPROXIMANT_FINALS  
A -> SPV IC | SPV IC SPV_FINAL | SPV IC '็' SPV_FINAL | 'ก' '็' 
SPV -> {}
SPV_FINAL -> 'ะ' | FC
""".format(terminalize(SINGLE_PREFIX_VOWEL))

SSV_RULES = u"""
A -> IC SSV_O_F T | IC SSV_O_F T FC | IC STV T | IC STV T FC | IC STV_F T FC | IC 'ื' T 'อ' 
A -> IC 'ะ' | IC '็' 'อ' FC
A -> C 'ร' 'ร' NON_APPROXIMANT_FINALS | C 'ร' 'ร'
SSV_O_F -> {}
STV -> {}
STV_F -> {}
""".format(terminalize(SINGLE_SUFFIX_VOWEL_OPT_FINAL), 
        terminalize(SINGLE_TOP_VOWEL),
        terminalize(SINGLE_TOP_VOWEL_WITH_FINAL))

DIPHTHONG_RULES = u"""
A -> 'เ' IC DIPH | IC UA
DIPH -> IA | UEA 
IA ->  'ี' T 'ย' | 'ี' T 'ย' SPV_FINAL
UEA -> 'ื' T 'อ' | 'ื' T 'อ' SPV_FINAL
UA ->  'ั' T 'ว' | 'ั' T 'ว' 'ะ' | 'ว' FC 
"""

EXTRA_RULES = u"""
A -> IC 'ำ' | 'ไ' IC | 'ไ' IC C |'ใ' IC | C 'ฤ' C | 'เ' IC 'า' | 'ฤ' 'ๅ' | 'ฦ' 'ๅ'
"""
GRAMMAR_STR = MAIN_GRAMMAR_STR + SPV_RULES + SSV_RULES + DIPHTHONG_RULES + EXTRA_RULES + CONSONANT_CLUSTER

ATOMIC_ROOT_SYMBOL_SET = set([u'SYLLABLE'])

GRAMMAR = nltk.CFG.fromstring(GRAMMAR_STR)
PARSER = nltk.ChartParser(GRAMMAR)


def parse_syllables(text, draw=False):
    results = PARSER.parse_all(text)
    if len(results) == 0:
        return []
    syllables = []
    if len(results) > 1:
        #print 'Ambiguous'
        for x in results:
            syll = []
            extract_syllables_from_tree(x, syll)
            if draw:
                print '|'.join(syll)
                x.draw()
        
    extract_syllables_from_tree(results[0], syllables)
    return syllables

def extract_syllables_from_tree(root, so_far):
    if root.label() in ATOMIC_ROOT_SYMBOL_SET:
        so_far.append(u''.join(root.leaves()))
        return
    for subtree in root:
        extract_syllables_from_tree(subtree, so_far)
    

if __name__ == '__main__':
    #parse_syllables(u'ดวง', True)
    #parse_syllables(u'วัน', True)
    test_cases = [u'วัน',u'นี้', u'กิน', u'ข้าว', u'มา', u'แล้ว',
            u'วันนี้',
            u'กินข้าว',
            u'วันนี้กินข้าว',
            u'วันนี้กินข้าวมาแล้ว',
            u'ปะทะ',
            u'เป็น',
            u'แน็ต',
            u'โก๊ะตี๋',
            u'น็อก',
            u'มือถือ',
            u'เสียงลือเสียงเล่าอ้าง', u'อันใดพี่เอย',
            u'เสียงย่อมยอยศใคร', u'ทั่วหล้า',
            u'สองเผือพี่หลับใหล', u'ลืมตื่นฤาพี่',
            u'สองพี่คิดเองอ้า', u'อย่าได้ถามเผือ',
            u'ฉันตายโดยปราศจากคนที่รักฉัน',u'แต่ฉันก็อิ่มใจว่าฉันมีคนที่ฉันรัก',
            u'เดือนช่วงดวงเด่นฟ้าดาดาว',u'หม่อมราชวงศ์กีรติ',
            u'สุพรรณหงส์ทรงพู่ห้อย', u'งามชดช้อยลอยหลังสินธุ์', 
            u'เพียงหงส์ทรงพรมมินทร์', u'ลินลาศเลื่อนเตือนตาชม',
            u'ยำใหญ่ใส่สารพัด', u'งามจานจัดหลายเหลือตรา',
			u'รสดีด้วยน้ำปลา', u'ญี่ปุ่นล้ำเย้ายวนใจ',
            u'ว่าพลางทางชมคณานก', u'โผนผกจับไม้อึงมี่',
 			u'เบญจวรรณจับวัลย์ชาลี', u'เหมือนวันพี่ไกลสามสุดามา', 
			u'นางนวลจับนางนวลนอน', u'เหมือนพี่แนบนวลสมรจินตะหรา', 
			u'จากพรากจับจากจำนรรจา', u'เหมือนจากนางสการะวาตี',
			u'ปางนั้นสมเด็จพระบรมโพธิสัตว์', u'ตรัสได้ทรงฟังพระลูกน้อย', u'ทรงกันแสงทูลละห้อยวันนั้น'] 
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

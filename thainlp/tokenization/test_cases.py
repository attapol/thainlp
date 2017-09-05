# -*- coding: utf8 -*-
CHAR_CLUSTER = [
        (u'เล็ก', [u'เล็ก']),
        (u'เหม็น', [u'เหม็น']),
        (u'เรื่อง', [u'เรื่อง']),
        (u'ร่วง', [u'ร่วง']),
        ]

SIMPLE_SENTENCES = [
        (u'รองเท้าสวย', [u'รองเท้า',u'สวย']),
        (u'ขัดหม้อ', [u'ขัด', u'หม้อ']),
        (u'อ่านข่าว', [u'อ่าน', u'ข่าว']),
        (u'ฟังเพลง', [u'ฟัง', u'เพลง'])
        ]

SIMPLE_CASES = [
        (u'ตาขับรถมา', [u'ตา',u'ขับ', u'รถ', u'มา']),
        (u'ผู้ใหญ่หาผ้าใหม่', [u'ผู้ใหญ่', u'หา', u'ผ้า', u'ใหม่']),
        (u'ให้สะใภ้ใช้คล้องคอ', [u'ให้', u'สะใภ้', u'ใช้', u'คล้อง',u'คอ'])
        ]

NAME_CASES = [
        (u'ณเดชพบกับธนาธรทุกวัน', [u'ณเดช',u'พบ', u'กับ', u'ธนาธร', u'ทุก',u'วัน']),
        (u'เดือนนี้ณัฐพลได้งานใหม่', [u'เดือน',u'นี้',u'ณัฐพล',u'ได้',u'งาน',u'ใหม่']),
        (u'บ้านหลังนี้อาจารย์ซื้อจากศรัณย์', [u'บ้าน', u'หลัง',u'นี้', u'อาจารย์', u'ซื้อ', u'จาก', u'ศรัณย์'])
        ]

def analyze_tokenizer(tokenizer):
    print 'Character cluster'
    _run_on_test_cases(tokenizer, CHAR_CLUSTER)
    print 'Simple sentences'
    _run_on_test_cases(tokenizer, SIMPLE_SENTENCES)
    print 'Simple test cases'
    _run_on_test_cases(tokenizer, SIMPLE_CASES)
    print 'Cases with Thai names'
    _run_on_test_cases(tokenizer, NAME_CASES)

def _run_on_test_cases(tokenizer, test_cases):
    for string, tokens in test_cases:
        auto_tokens = tokenizer.tokenize(string)
        if auto_tokens == tokens:
            print u'CORRECT   - Predicted : {}'.format('|'.join(auto_tokens))
        else:
            print u'INCORRECT - Predicted : {}'.format('|'.join(auto_tokens))
            print u'          - Gold      : {}'.format('|'.join(tokens))


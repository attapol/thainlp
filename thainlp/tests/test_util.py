# -*- coding: utf8 -*-
from unittest import TestCase
import thainlp.util

class TestUtil(TestCase):

    def test_is_thai_char(self):
        assert thainlp.is_thai_char(u'ฟ')
        assert thainlp.util.is_thai_char(u'ฟ')
        assert not thainlp.util.is_thai_char(u'd')

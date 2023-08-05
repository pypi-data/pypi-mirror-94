# -*- coding: utf-8 -*-

import pykakasi


def test_issues60():
    TESTS = [
        (u"市立", u"しりつ")
    ]
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", None)
    kakasi.setMode("K", None)
    kakasi.setMode("J", "H")
    kakasi.setMode("s", False)
    kakasi.setMode("C", True)
    kakasi.setMode("E", None)
    kakasi.setMode("a", None)
    converter = kakasi.getConverter()
    for case, result in TESTS:
        assert converter.do(case) == result


def test_issues59():
    TESTS = [
        (u"じゃーん", u"じゃーん"),
        (u"ヷヸヹヺ", u"ヷヸヹヺ")
    ]
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", None)
    kakasi.setMode("K", "H")
    kakasi.setMode("J", None)
    kakasi.setMode("s", False)
    kakasi.setMode("C", True)
    kakasi.setMode("E", None)
    kakasi.setMode("a", None)
    converter = kakasi.getConverter()
    for case, result in TESTS:
        assert converter.do(case) == result


def test_issue66():
    TESTS = [
        (u"月々", "tukizuki"),
        (u"毎月々", "maitukizuki"),
        (u"佐々木", "sasaki"),
        (u"中佐々木", "nakasasaki"),
        (u"代々木", "yoyogi"),
        (u"次代々木", "tugiyoyogi")
    ]
    kakasi = pykakasi.kakasi()
    kakasi.setMode("J", "a")
    kakasi.setMode("r", "Kunrei")
    conv = kakasi.getConverter()
    for case, result in TESTS:
        assert conv.do(case) == result


def test_issues68():
    TESTS = [
        (u"", u""),
        (u"埇", u"よう")
    ]
    kks = pykakasi.kakasi()
    kks.setMode("J", "H")
    convert = kks.getConverter()
    for case, result in TESTS:
        assert convert.do(case) == result


def test_issue68_2():
    kks = pykakasi.kakasi()
    kks.setMode("J", "H")
    convert = kks.getConverter()
    for case in range(0x3400, 0xdfff):
        assert convert.do(chr(case)) is not None
    for case in range(0xf900, 0xfa2e):
        assert convert.do(chr(case)) is not None


def test_issue72():
    TESTS = [
        (u"㐂", u"き")
    ]
    kks = pykakasi.kakasi()
    kks.setMode("J", "H")
    convert = kks.getConverter()
    for case, result in TESTS:
        assert convert.do(case) == result


def test_issue78():
    TESTS = [
        (u"由来し、この", u"ゆらい し、 この"),
        (u"これは人類普遍であり、かかる原理に",
         u"これは じんるいふへん であり、 かかる げんり に")
    ]
    kks = pykakasi.kakasi()
    kks.setMode("J", "H")
    kks.setMode("s", True)
    convert = kks.getConverter()
    for case, result in TESTS:
        assert convert.do(case) == result


def test_issue90():
    TESTS = [
        (u'私がこの子を助けなきゃいけないってことだよね', u'ワタシガコノコヲタスケナキャイケナイッテコトダヨネ')
    ]
    kks = pykakasi.kakasi()
    kks.setMode("J", "K")
    kks.setMode("H", "K")
    convert = kks.getConverter()
    for case, result in TESTS:
        assert convert.do(case) == result


def test_issue105():
    text = 'ｿｳｿﾞｸﾆﾝ'
    kks = pykakasi.kakasi()
    result = kks.convert(text)
    assert result[0]['kana'] == 'ｿｳｿﾞｸﾆﾝ'
    assert result[0]['hepburn'] == 'souzokunin'
    assert result[0]['hira'] == 'そうぞくにん'


def test_issue105_legacy():
    text = 'ｿｳｿﾞｸﾆﾝ'
    kks = pykakasi.kakasi()
    kks.setMode("K", "H")
    converter = kks.getConverter()
    result = converter.do(text)
    assert result == 'そうぞくにん'


def test_issue114():
    text = '思った 言った 行った'
    kks = pykakasi.kakasi()
    result = kks.convert(text)
    assert result[0]['hepburn'] == 'omotta'
    assert result[2]['hepburn'] == 'itta'
    assert result[4]['hepburn'] == 'itta'

from .. import *

from .constants import extractIntValue, extractBytesValue, extractAddrValue, createConstantBlocks

def test_extractIntValue():
    tests = [
        (TealOp(None, Op.int, 0), 0),
        (TealOp(None, Op.int, 5), 5),
        (TealOp(None, Op.int, "pay"), 1),
        (TealOp(None, Op.int, "NoOp"), 0),
        (TealOp(None, Op.int, "UpdateApplication"), 4),
        (TealOp(None, Op.int, "TMPL_NAME"), "TMPL_NAME"),
    ]

    for op, expected in tests:
        actual = extractIntValue(op)
        assert actual == expected

def test_extractBytesValue():
    tests = [
        (TealOp(None, Op.byte, "\"\""), b''),
        (TealOp(None, Op.byte, "\"test\""), b'test'),
        (TealOp(None, Op.byte, "\"\\t\\n\\\\\\\"\""), b'\t\n\\"'),
        (TealOp(None, Op.byte, "0x"), b''),
        (TealOp(None, Op.byte, "0x00"), b'\x00'),
        (TealOp(None, Op.byte, "0xFF00"), b'\xff\x00'),
        (TealOp(None, Op.byte, "0xff00"), b'\xff\x00'),
        (TealOp(None, Op.byte, "base32()"), b''),
        (TealOp(None, Op.byte, "base32(ORSXG5A)"), b'test'),
        (TealOp(None, Op.byte, "base32(ORSXG5A=)"), b'test'),
        (TealOp(None, Op.byte, "base64()"), b''),
        (TealOp(None, Op.byte, "base64(dGVzdA==)"), b'test'),
        (TealOp(None, Op.byte, "TMPL_NAME"), "TMPL_NAME"),
    ]

    for op, expected in tests:
        actual = extractBytesValue(op)
        assert actual == expected

def test_extractAddrValue():
    tests = [
        (TealOp(None, Op.byte, "WSJHNPJ6YCLX5K4GUMQ4ISPK3ABMS3AL3F6CSVQTCUI5F4I65PWEMCWT3M"), b'\xb4\x92v\xbd>\xc0\x97~\xab\x86\xa3!\xc4I\xea\xd8\x02\xc9l\x0b\xd9|)V\x13\x15\x11\xd2\xf1\x1e\xeb\xec'),
        (TealOp(None, Op.addr, "TMPL_NAME"), "TMPL_NAME"),
    ]

    for op, expected in tests:
        actual = extractAddrValue(op)
        assert actual == expected

def test_createConstantBlocks_empty():
    ops = []

    expected = ops[:]

    actual = createConstantBlocks(ops)
    assert actual == expected


def test_createConstantBlocks_no_consts():
    ops = [
        TealOp(None, Op.txn, "Sender"),
        TealOp(None, Op.txn, "Receiver"),
        TealOp(None, Op.eq),
    ]

    expected = ops[:]

    actual = createConstantBlocks(ops)
    assert actual == expected

def test_createConstantBlocks_pushint():
    ops = [
        TealOp(None, Op.int, 0),
        TealOp(None, Op.int, "OptIn"),
        TealOp(None, Op.add),
    ]

    expected = [
        TealOp(None, Op.pushint, 0, "//", 0),
        TealOp(None, Op.pushint, 1, "//", "OptIn"),
        TealOp(None, Op.add),
    ]

    actual = createConstantBlocks(ops)
    assert actual == expected

def test_createConstantBlocks_intblock_single():
    ops = [
        TealOp(None, Op.int, 1),
        TealOp(None, Op.int, "OptIn"),
        TealOp(None, Op.add),
    ]

    expected = [
        TealOp(None, Op.intcblock, 1),
        TealOp(None, Op.intc_0, "//", 1),
        TealOp(None, Op.intc_0, "//", "OptIn"),
        TealOp(None, Op.add),
    ]

    actual = createConstantBlocks(ops)
    assert actual == expected

def test_createConstantBlocks_intblock_multiple():
    ops = [
        TealOp(None, Op.int, 1),
        TealOp(None, Op.int, "OptIn"),
        TealOp(None, Op.add),
        TealOp(None, Op.int, 2),
        TealOp(None, Op.int, "keyreg"),
        TealOp(None, Op.add),
        TealOp(None, Op.int, 3),
        TealOp(None, Op.int, "ClearState"),
        TealOp(None, Op.add),
    ]

    expected = [
        TealOp(None, Op.intcblock, 3, 2, 1),
        TealOp(None, Op.intc_2, "//", 1),
        TealOp(None, Op.intc_2, "//", "OptIn"),
        TealOp(None, Op.add),
        TealOp(None, Op.intc_1, "//", 2),
        TealOp(None, Op.intc_1, "//", "keyreg"),
        TealOp(None, Op.add),
        TealOp(None, Op.intc_0, "//", 3),
        TealOp(None, Op.intc_0, "//", "ClearState"),
        TealOp(None, Op.add),
    ]

    actual = createConstantBlocks(ops)
    assert actual == expected

def test_createConstantBlocks_intblock_pushint():
    ops = [
        TealOp(None, Op.int, 1),
        TealOp(None, Op.int, "OptIn"),
        TealOp(None, Op.add),
        TealOp(None, Op.int, 2),
        TealOp(None, Op.int, 3),
        TealOp(None, Op.add),
        TealOp(None, Op.int, 3),
        TealOp(None, Op.int, "ClearState"),
        TealOp(None, Op.add),
    ]

    expected = [
        TealOp(None, Op.intcblock, 3, 1),
        TealOp(None, Op.intc_1, "//", 1),
        TealOp(None, Op.intc_1, "//", "OptIn"),
        TealOp(None, Op.add),
        TealOp(None, Op.pushint, 2, "//", 2),
        TealOp(None, Op.intc_0, "//", 3),
        TealOp(None, Op.add),
        TealOp(None, Op.intc_0, "//", 3),
        TealOp(None, Op.intc_0, "//", "ClearState"),
        TealOp(None, Op.add),
    ]

    actual = createConstantBlocks(ops)
    assert actual == expected

def test_createConstantBlocks_pushbytes():
    ops = [
        TealOp(None, Op.byte, "0x0102"),
        TealOp(None, Op.byte, "0x0103"),
        TealOp(None, Op.concat),
    ]

    expected = [
        TealOp(None, Op.pushbytes, "0x0102", "//", "0x0102"),
        TealOp(None, Op.pushbytes, "0x0103", "//", "0x0103"),
        TealOp(None, Op.concat),
    ]

    actual = createConstantBlocks(ops)
    assert actual == expected

def test_createConstantBlocks_byteblock_single():
    ops = [
        TealOp(None, Op.byte, "0x0102"),
        TealOp(None, Op.byte, "base64(AQI=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "base32(AEBA====)"),
        TealOp(None, Op.concat),
    ]

    expected = [
        TealOp(None, Op.bytecblock, "0x0102"),
        TealOp(None, Op.bytec_0, "//", "0x0102"),
        TealOp(None, Op.bytec_0, "//", "base64(AQI=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_0, "//", "base32(AEBA====)"),
        TealOp(None, Op.concat),
    ]

    actual = createConstantBlocks(ops)
    assert actual == expected

def test_createConstantBlocks_byteblock_multiple():
    ops = [
        TealOp(None, Op.byte, "0x0102"),
        TealOp(None, Op.byte, "base64(AQI=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "base32(AEBA====)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "\"test\""),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "base32(ORSXG5A=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "0xb49276bd3ec0977eab86a321c449ead802c96c0bd97c2956131511d2f11eebec"),
        TealOp(None, Op.concat),
        TealOp(None, Op.addr, "WSJHNPJ6YCLX5K4GUMQ4ISPK3ABMS3AL3F6CSVQTCUI5F4I65PWEMCWT3M"),
        TealOp(None, Op.concat),
    ]

    expected = [
        TealOp(None, Op.bytecblock, "0x0102", "0xb49276bd3ec0977eab86a321c449ead802c96c0bd97c2956131511d2f11eebec", "0x74657374"),
        TealOp(None, Op.bytec_0, "//", "0x0102"),
        TealOp(None, Op.bytec_0, "//", "base64(AQI=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_0, "//", "base32(AEBA====)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_2, "//", "\"test\""),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_2, "//", "base32(ORSXG5A=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_1, "//", "0xb49276bd3ec0977eab86a321c449ead802c96c0bd97c2956131511d2f11eebec"),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_1, "//", "WSJHNPJ6YCLX5K4GUMQ4ISPK3ABMS3AL3F6CSVQTCUI5F4I65PWEMCWT3M"),
        TealOp(None, Op.concat),
    ]

    actual = createConstantBlocks(ops)
    assert actual == expected

def test_createConstantBlocks_byteblock_pushbytes():
    ops = [
        TealOp(None, Op.byte, "0x0102"),
        TealOp(None, Op.byte, "base64(AQI=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "base32(AEBA====)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "\"test\""),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "base32(ORSXG5A=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.addr, "WSJHNPJ6YCLX5K4GUMQ4ISPK3ABMS3AL3F6CSVQTCUI5F4I65PWEMCWT3M"),
        TealOp(None, Op.concat),
    ]

    expected = [
        TealOp(None, Op.bytecblock, "0x0102", "0x74657374"),
        TealOp(None, Op.bytec_0, "//", "0x0102"),
        TealOp(None, Op.bytec_0, "//", "base64(AQI=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_0, "//", "base32(AEBA====)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_1, "//", "\"test\""),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_1, "//", "base32(ORSXG5A=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.pushbytes, "0xb49276bd3ec0977eab86a321c449ead802c96c0bd97c2956131511d2f11eebec", "//", "WSJHNPJ6YCLX5K4GUMQ4ISPK3ABMS3AL3F6CSVQTCUI5F4I65PWEMCWT3M"),
        TealOp(None, Op.concat),
    ]

    actual = createConstantBlocks(ops)
    assert actual == expected

def test_createConstantBlocks_all():
    ops = [
        TealOp(None, Op.byte, "0x0102"),
        TealOp(None, Op.byte, "base64(AQI=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "base32(AEBA====)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "\"test\""),
        TealOp(None, Op.concat),
        TealOp(None, Op.byte, "base32(ORSXG5A=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.addr, "WSJHNPJ6YCLX5K4GUMQ4ISPK3ABMS3AL3F6CSVQTCUI5F4I65PWEMCWT3M"),
        TealOp(None, Op.concat),
        TealOp(None, Op.int, 1),
        TealOp(None, Op.int, "OptIn"),
        TealOp(None, Op.add),
        TealOp(None, Op.int, 2),
        TealOp(None, Op.int, 3),
        TealOp(None, Op.add),
        TealOp(None, Op.int, 3),
        TealOp(None, Op.int, "ClearState"),
        TealOp(None, Op.add),
    ]

    expected = [
        TealOp(None, Op.intcblock, 3, 1),
        TealOp(None, Op.bytecblock, "0x0102", "0x74657374"),
        TealOp(None, Op.bytec_0, "//", "0x0102"),
        TealOp(None, Op.bytec_0, "//", "base64(AQI=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_0, "//", "base32(AEBA====)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_1, "//", "\"test\""),
        TealOp(None, Op.concat),
        TealOp(None, Op.bytec_1, "//", "base32(ORSXG5A=)"),
        TealOp(None, Op.concat),
        TealOp(None, Op.pushbytes, "0xb49276bd3ec0977eab86a321c449ead802c96c0bd97c2956131511d2f11eebec", "//", "WSJHNPJ6YCLX5K4GUMQ4ISPK3ABMS3AL3F6CSVQTCUI5F4I65PWEMCWT3M"),
        TealOp(None, Op.concat),
        TealOp(None, Op.intc_1, "//", 1),
        TealOp(None, Op.intc_1, "//", "OptIn"),
        TealOp(None, Op.add),
        TealOp(None, Op.pushint, 2, "//", 2),
        TealOp(None, Op.intc_0, "//", 3),
        TealOp(None, Op.add),
        TealOp(None, Op.intc_0, "//", 3),
        TealOp(None, Op.intc_0, "//", "ClearState"),
        TealOp(None, Op.add),
    ]

    actual = createConstantBlocks(ops)
    assert actual == expected

# -*- coding: utf-8 -*-g
import pytest
from antlr4 import *

from antelope import YAMLLexer
from antelope.yaml_input_stream import StringInputStream


@pytest.mark.parametrize('input_str', [
    u'abcdé',
    u'אבג',
    'abcde',
])
@pytest.mark.parametrize('bom,input_encoding', [
    # with bom
    (b'\xef\xbb\xbf', None),
    (b'\xef\xbb\xbf', 'utf-8'),
    (b'\xfe\xff', 'utf-16-be'),
    (b'\xff\xfe', 'utf-16-le'),
    (b'\x00\x00\xfe\xff', 'utf-32-be'),
    (b'\xff\xfe\x00\x00', 'utf-32-le'),

    # without bom, correctly identifies only if first character is ascii
    (None, None),
    (None, 'utf-8'),
    (None, 'utf-16-be'),
    (None, 'utf-16-le'),
    (None, 'utf-32-be'),
    (None, 'utf-32-le'),
])
def test_string_input_stream(bom, input_encoding, input_str):
    if input_encoding is None:
        input_encoding = 'utf-8'
    s = input_str.encode(encoding=input_encoding)
    bom_len = 0
    if bom is None:
        # non ascii first character and no bom.
        # this is not expected to work correctly.
        if ord(input_str[0]) >= 128:
            return
    else:
        s = bom + s
        bom_len = len(bom)
    stream = StringInputStream(s)
    assert stream.index == 0
    assert stream.size == len(input_str) + bom_len
    for _ in range(bom_len):
        # consume bom
        stream.consume()
    assert stream.size - stream.index == len(input_str)
    assert stream.LA(1) == ord(input_str[0])
    stream.consume()
    assert stream.index == bom_len + 1
    stream.seek(bom_len + len(input_str))
    assert stream.LA(1) == Token.EOF
    for i in range(len(input_str)):
        for j in range(len(input_str)):
            assert stream.getText(bom_len + i, bom_len + j) == input_str[i:j + 1]
    stream.reset()
    assert stream.index == 0


@pytest.mark.parametrize('bom_str,token', [
    (b'\xef\xbb\xbf', YAMLLexer.BOM_UTF8),
    (b'\xfe\xff', YAMLLexer.BOM_UTF16_BE),
    (b'\xff\xfe', YAMLLexer.BOM_UTF16_LE),
    (b'\x00\x00\xfe\xff', YAMLLexer.BOM_UTF32_BE),
    (b'\xff\xfe\x00\x00', YAMLLexer.BOM_UTF32_LE),
])
def test_lexer_bom(bom_str, token):
    inp = StringInputStream(bom_str)
    lexer = YAMLLexer(inp)
    tokens = lexer.getAllTokens()
    assert len(tokens) == 1
    assert tokens[0].type == token


@pytest.mark.parametrize('s, token', [
    (b'-', YAMLLexer.C_SEQUENCE_ENTRY),
    (b'?', YAMLLexer.C_MAPPING_KEY),
    (b':', YAMLLexer.C_MAPPING_VALUE),
    (b',', YAMLLexer.C_COLLECT_ENTRY),
    (b'[', YAMLLexer.C_SEQUENCE_START),
    (b']', YAMLLexer.C_SEQUENCE_END),
    (b'{', YAMLLexer.C_MAPPING_START),
    (b'}', YAMLLexer.C_MAPPING_END),
    (b'#', YAMLLexer.C_COMMENT),
    (b'&', YAMLLexer.C_ANCHOR),
    (b'*', YAMLLexer.C_ALIAS),
    (b'!', YAMLLexer.C_TAG),
    (b'|', YAMLLexer.C_LITERAL),
    (b'>', YAMLLexer.C_FOLDED),
    (b'\'', YAMLLexer.C_SINGLE_QUOTE),
    (b'"', YAMLLexer.C_DOUBLE_QUOTE),
    (b'%', YAMLLexer.C_DIRECTIVE),
    (b'@', YAMLLexer.C_RESERVED),
    (b'`', YAMLLexer.C_RESERVED),
])
def test_indicators(s, token):
    inp = StringInputStream(s)
    lexer = YAMLLexer(inp)
    tokens = lexer.getAllTokens()
    assert tokens[0].type == token, "Expected {}, matched {}".format(YAMLLexer.symbolicNames[token],
                                                                     YAMLLexer.symbolicNames[tokens[0].type])

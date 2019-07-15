from antelope import Antelope
import pytest

from antelope import YAMLLexer
from antlr4 import *
from antelope.yaml_input_stream import StringInputStream


# def get_test_files():
#     return [
#         ('a', 1),
#         ('b', 2),
#         ('c', 3),
#         ('d', 4),
#     ]
#
#
# @pytest.mark.parametrize('test_name,file', get_test_files())
# def test_foo(test_name, file):
#   pass


@pytest.mark.parametrize('bom,encoding', [
    (b'\xef\xbb\xbf', None),
    (b'\xef\xbb\xbf', 'utf-8'),
    (b'\xfe\xff', 'utf-16-be'),
    (b'\xff\xfe', 'utf-16-le'),
    (b'\x00\x00\xfe\xff', 'utf-32-be'),
    (b'\xff\xfe\x00\x00', 'utf-32-le'),

    (None, None),
    (None, 'utf-8'),
    (None, 'utf-16-be'),
    (None, 'utf-16-le'),
    (None, 'utf-32-be'),
    (None, 'utf-32-le'),
])
def test_string_input_stream(bom, encoding):
    input_str = "abcde"
    if encoding is None:
        encoding = 'utf-8'
    s = input_str.encode(encoding=encoding)

    bom_len = 0
    if bom is not None:
        s = bom + s
        bom_len = len(bom)
    stream = StringInputStream(s)
    assert stream.index == 0
    assert stream.size == len(input_str) + bom_len
    for _ in range(bom_len):
        # consume bom
        stream.consume()
    assert stream.size - stream.index == len(input_str)
    assert stream.LA(1) == ord("a")
    stream.consume()
    assert stream.index == bom_len + 1
    stream.seek(bom_len + len(input_str))
    assert stream.LA(1) == Token.EOF
    assert stream.getText(bom_len + 1, bom_len + 3) == 'bcd'
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

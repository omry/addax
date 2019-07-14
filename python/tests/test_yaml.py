from antelope import Antelope
import pytest

from antelope import YAMLLexer
from antlr4 import *


def test_basic():
    s = "{99, 3, 451}"
    antelope = Antelope(s)
    print(antelope)


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

@pytest.mark.parametrize('input_, tokens_str', [
    ('\x00\x00\xfe\xff', 'BOM_UTF32_BE=\x00\x00\xfe\xff'),
    ('\xff\xfe\x00\x00', 'BOM_UTF32_LE=\xff\xfe\x00\x00'),
    ('\xfe\xff', 'BOM_UTF16_BE=\xfe\xff'),
    ('\xff\xfe', 'BOM_UTF16_LE=\xff\xfe'),
    ('\xff\xbb\xbf', 'BOM_UTF8=\xff\xbb\xbf'),
    # no BOM
    ('word', 'WORD=word'),
    # with bom
    ('\xfe\xffword', 'BOM_UTF16_BE=\xfe\xff,WORD=word'),
])
def test_lexer_bom(input_, tokens_str):
    lexer = YAMLLexer(InputStream(input_))
    tokens = lexer.getAllTokens()
    assert ','.join(["{}={}".format(lexer.ruleNames[t.type - 1], t.text) for t in tokens]) == tokens_str

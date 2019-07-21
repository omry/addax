# -*- coding: utf-8 -*-g
import pytest
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antelope import YAMLLexer, YAMLParser
from antelope.yaml_input_stream import StringInputStream
from antelope.yaml_lexer_wrapper import YAMLLexerWrapper
import os
from os import path
import glob


def validate_token(token, expected_type):
    assert token.type == expected_type, "Expected {}, matched {}".format(
        YAMLLexer.symbolicNames[expected_type],
        YAMLLexer.symbolicNames[token.type])


def validate_token_list(tokens, expected_types):
    def to_str(in_tokens):
        s = ''
        for t in in_tokens:
            token_type = t if type(t) == int else t.type
            if s == '':
                s = 'YAMLParser.{}'.format(YAMLParser.symbolicNames[token_type])
            else:
                s += "," + 'YAMLParser.{}'.format(YAMLParser.symbolicNames[token_type])

        return '[{}]'.format(s)

    assert len(tokens) == len(expected_types), "mismatch number of tokens\nreceived=\n\t{}\nexpected=\n\t{}\n".format(
        to_str(tokens),
        to_str(expected_types),
    )

    for i in range(len(tokens)):
        actual_type = tokens[i].type
        expected_type = expected_types[i]
        assert actual_type == expected_type, "Token #{}: Expected {}, matched {}".format(
            i,
            YAMLParser.symbolicNames[expected_type],
            YAMLParser.symbolicNames[actual_type])


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


@pytest.mark.parametrize('bom_str', [
    b'\xef\xbb\xbf',
    b'\xfe\xff',
    b'\xff\xfe',
    b'\x00\x00\xfe\xff',
    b'\xff\xfe\x00\x00',
])
def test_lexer_illegal_bom(bom_str):
    bom_str = b'\xef\xbb\xbf'
    s = b'[]' + bom_str + b'[]'
    inp = StringInputStream(s)
    lexer = YAMLLexer(inp)
    lexer.removeErrorListeners()

    class MyErrorListener(ErrorListener):
        def __init__(self):
            self.errors = []

        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            self.errors.append(column)

    listener = MyErrorListener()
    lexer.addErrorListener(listener)
    tokens = lexer.getAllTokens()

    validate_token_list(tokens, [YAMLLexer.C_SEQUENCE_START, YAMLLexer.C_SEQUENCE_END,
                                 YAMLLexer.C_SEQUENCE_START, YAMLLexer.C_SEQUENCE_END])
    assert len(listener.errors) == 1
    # error in column 2
    assert listener.errors[0] == 2


@pytest.mark.parametrize('input_str, expected_tokens', [
    (b'\xef\xbb\xbf', YAMLLexer.BOM_MARKER),
    (b'\xfe\xff', YAMLLexer.BOM_MARKER),
    (b'\xff\xfe', YAMLLexer.BOM_MARKER),
    (b'\x00\x00\xfe\xff', YAMLLexer.BOM_MARKER),
    (b'\xff\xfe\x00\x00', YAMLLexer.BOM_MARKER),
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
    (b'\x0d\x0a', YAMLLexer.B_BREAK),
    (b'\x0d', YAMLLexer.B_BREAK),
    (b'\x0a', YAMLLexer.B_BREAK),
])
def test_tokens(input_str, expected_tokens):
    if not isinstance(expected_tokens, list):
        expected_tokens = [expected_tokens]
    inp = StringInputStream(input_str)
    lexer = YAMLLexerWrapper(inp)
    tokens = lexer.getAllTokens()
    validate_token_list(tokens, expected_tokens)


def get_lexer_tests():
    tests_dir = path.join(path.dirname(__file__), 'lexer_tests_data')
    assert path.exists(tests_dir)
    tests = [(tests_dir, path.splitext(path.basename(x))[0]) for x in glob.glob(tests_dir + '/*.meta')]
    return tests


@pytest.mark.parametrize('test_dir, test_name', get_lexer_tests())
def test_lexer_data_dir(test_dir, test_name):
    with open(path.join(test_dir, test_name + '.in'), mode='rb') as file:  # b is important -> binary
        test_input = file.read()
    with open(path.join(test_dir, test_name + '.tokens'), 'r') as f:
        expected_tokens = []
        for t in f.readlines():
            t = t.strip('\n')
            try:
                t = getattr(YAMLLexer, t)
            except AttributeError:
                try:
                    t = getattr(YAMLParser, t)
                except AttributeError:
                    raise RuntimeError("{} was not found in both YAMLLexer and YAMLParser".format(t))

            expected_tokens.append(t)

    test_tokens(test_input, expected_tokens)


def get_reference_yeast_tests():
    return get_yeast_tests('yaml-reference-tests')


def get_my_yeast_tests():
    return get_yeast_tests('supported-yaml-reference-tests')


def get_yeast_tests(directory):
    tests_dir = path.join(path.dirname(__file__), directory)
    assert path.exists(tests_dir)
    tests = [(tests_dir, path.splitext(path.basename(x))[0]) for x in glob.glob(tests_dir + '/*.input')]
    return tests


def tokens_to_yeast(tokens):
    """
    --  [@U@] BOM, contains \"@TF8@\", \"@TF16LE@\" or \"@TF16BE@\"
    --  [@T@] Contains preserved content text characters
    --  [@t@] Contains non-content (meta) text characters
    --  [@b@] Contains separation line break
    --  [@L@] Contains line break normalized to content line feed
    --  [@l@] Contains line break folded to content space
    --  [@I@] Contains character indicating structure
    --  [@w@] Contains separation white space
    --  [@i@] Contains indentation spaces
    --  [@K@] Directives end marker
    --  [@k@] Document end marker
    --  [@E@] Begins escape sequence
    --  [@e@] Ends escape sequence
    --  [@C@] Begins comment
    --  [@c@] Ends comment
    --  [@D@] Begins directive
    --  [@d@] Ends directive
    --  [@G@] Begins tag
    --  [@g@] Ends tag
    --  [@H@] Begins tag handle
    --  [@h@] Ends tag handle
    --  [@A@] Begins anchor
    --  [@a@] Ends anchor
    --  [@P@] Begins node properties
    --  [@p@] Ends node properties
    --  [@R@] Begins alias (reference)
    --  [@r@] Ends alias (reference)
    --  [@S@] Begins scalar content
    --  [@s@] Ends scalar content
    --  [@Q@] Begins sequence content
    --  [@q@] Ends sequence content
    --  [@M@] Begins mapping content
    --  [@m@] Ends mapping content
    --  [@N@] Begins complete node
    --  [@n@] Ends complete node
    --  [@X@] Begins mapping key:value pair
    --  [@x@] Ends mapping key:value pair
    --  [@O@] Begins document
    --  [@o@] Ends document
    --  [@!@] Parsing error at this point.
    --  [@-@] Unparsed text following error point.
    :param tokens:
    :return:
    """
    res = []
    for t in tokens:
        s = ''
        if t.type == YAMLLexer.BOM_MARKER:
            if t.text == u'\x00\x00\xfe\xff':
                s = "UTF-32BE"
            elif t.text == u'\xff\xfe\x00\x00':
                s = "UTF-32LE"
            elif t.text == u'\xfe\xff':
                s = "UTF-16BE"
            elif t.text == u'\xff\xfe':
                s = "UTF-16LE"
            elif t.text == u'\xef\xbb\xbf':
                s = "UTF-8"
            else:
                assert False, "Invalid bom data : {}".format([hex(ord(c)) for c in t.text])

        res.append(s)

    return res


@pytest.mark.parametrize('test_dir, test_name', get_my_yeast_tests())
def test_lexer_data_dir(test_dir, test_name):
    yeast_test_impl(test_dir, test_name)


# TODO: enable later
# @pytest.mark.parametrize('test_dir, test_name', get_reference_yeast_tests())
# def test_lexer_data_dir(test_dir, test_name):
#     yeast_test_impl(test_dir, test_name)


def yeast_test_impl(test_dir, test_name):
    with open(path.join(test_dir, test_name + '.input'), mode='rb') as file:  # b is important -> binary
        test_input = file.read()
    with open(path.join(test_dir, test_name + '.output'), 'r') as f:
        expected_yeast_tokens = []
        for t in f.readlines():
            t = t.strip('\n\r')
            if t.startswith("#"):
                continue
            expected_yeast_tokens.append(t)

    inp = StringInputStream(test_input)
    lexer = YAMLLexerWrapper(inp)
    produced_tokens = lexer.getAllTokens()
    produced_yeast_tokens = tokens_to_yeast(produced_tokens)
    for idx in range(min(len(expected_yeast_tokens), len(produced_yeast_tokens))):
        assert produced_yeast_tokens[idx] == expected_yeast_tokens[idx]
    assert len(expected_yeast_tokens) == len(produced_yeast_tokens)

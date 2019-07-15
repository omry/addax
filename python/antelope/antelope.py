from antlr4 import *

from . import YAMLLexer
from . import YAMLParser
from . import yaml_input_stream

class Antelope(object):
    def __init__(self, s):
        istream = yaml_input_stream.StringInputStream(s)
        self.parse(istream)

    def parse(self, istream):
        lexer = YAMLLexer(istream)
        stream = CommonTokenStream(lexer)
        parser = YAMLParser(stream)
        self.tree = parser.document()
        print(self.tree.toStringTree(recog=parser))


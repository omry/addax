from antlr4 import *

from . import YAMLLexer
from . import YAMLParser


class Antelope(object):
    def __init__(self, s):
        istream = InputStream(s)
        lexer = YAMLLexer(istream)
        stream = CommonTokenStream(lexer)
        parser = YAMLParser(stream)
        self.tree = parser.init()
        print(self.tree.toStringTree(recog=parser))

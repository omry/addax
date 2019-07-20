from . import YAMLLexer
from . import YAMLParser


class YAMLLexerWrapper(YAMLLexer):
    """
    A wrapper of the lexer that handles the the indentation logic.
    """
    def __init__(self, input_stream):
        super(YAMLLexerWrapper, self).__init__(input_stream)
        self.indentation = 0
        self.last_num_spaces = 0

    def nextToken(self):
        t = super(YAMLLexerWrapper, self).nextToken()
        if t.type == YAMLLexer.S_INDENT:
            num_spaces = len(t.text)
            if num_spaces == self.last_num_spaces:
                # skip to next token
                t = self.nextToken()
            elif num_spaces < self.last_num_spaces:
                t.type = YAMLParser.DEDENT
            elif num_spaces > self.last_num_spaces:
                t.type = YAMLParser.INDENT
            else:
                assert False
            self.last_num_spaces = num_spaces
        return t

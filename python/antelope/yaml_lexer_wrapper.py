from . import YAMLLexer
from . import YAMLParser
from antlr4.Token import Token, CommonToken


class YAMLLexerWrapper(YAMLLexer):
    """
    A wrapper of the lexer that handles the the indentation logic.
    """

    def __init__(self, input_stream):
        super(YAMLLexerWrapper, self).__init__(input_stream)
        self.last_token = None
        self.last_num_spaces = 0
        # a token that should be returned on next call to getToken()
        self.pending_token = None

    def nextToken(self):
        # consume pending token if it's there.
        if self.pending_token is not None:
            t = self.pending_token
            self.pending_token = None
        else:
            t = super(YAMLLexerWrapper, self).nextToken()
            if t.type == YAMLLexer.S_INDENT:
                num_spaces = len(t.text)
                if num_spaces == self.last_num_spaces:
                    # skip to next token
                    t = self.nextToken()
                elif num_spaces < self.last_num_spaces:
                    self.pending_token = t
                    t = CommonToken(type=YAMLParser.DEDENT)
                elif num_spaces > self.last_num_spaces:
                    t = CommonToken(type=YAMLParser.INDENT)
                else:
                    assert False
                self.last_num_spaces = num_spaces
            elif t.type == Token.EOF:
                if self.last_token.type == YAMLLexer.B_BREAK:
                    if self.last_num_spaces > 0:
                        self.pending_token = t
                        t = CommonToken(type=YAMLParser.DEDENT)

        self.last_token = t
        return t

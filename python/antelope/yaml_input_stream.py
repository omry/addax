import six
from . import utils

from antlr4.Token import Token

if six.PY2:
    from antlr4.CodePoints import to_unicode


class StringInputStream(object):

    def __init__(self, input_str, input_encoding=None):
        """
        :param input_str:
        :param input_encoding: by default auto detects based on bom rules. if specified bom is ignored.
        """
        bom, self.encoding = utils.get_bom_from_string(input_str, input_encoding)
        self.data = [c for c in bom] + [ord(c) for c in (input_str[len(bom):].decode(encoding=self.encoding))]
        self._index = 0
        self._size = len(self.data)

    @property
    def index(self):
        return self._index

    @property
    def size(self):
        return self._size

    # Reset the stream so that it's in the same state it was
    #  when the object was created *except* the data array is not
    #  touched.
    #
    def reset(self):
        self._index = 0

    def consume(self):
        if self._index >= self._size:
            assert self.LA(1) == Token.EOF
            raise Exception("cannot consume EOF")
        self._index += 1

    def LA(self, offset):
        if offset == 0:
            return 0  # undefined
        if offset < 0:
            offset += 1  # e.g., translate LA(-1) to use offset=0
        pos = self._index + offset - 1
        if pos < 0 or pos >= self._size:  # invalid
            return Token.EOF
        return self.data[pos]

    def LT(self, offset):
        return self.LA(offset)

    # mark/release do nothing; we have entire buffer
    def mark(self):
        return -1

    def release(self, marker):
        pass

    # consume() ahead until p==_index; can't just set p=_index as we must
    # update line and column. If we seek backwards, just set p
    #
    def seek(self, _index):
        if _index <= self._index:
            self._index = _index  # just jump; don't update stream state (line, ...)
            return
        # seek forward
        self._index = min(_index, self._size)

    def getText(self, start, stop):
        if stop >= self._size:
            stop = self._size - 1
        if start >= self._size:
            return ""
        else:
            if six.PY2:
                return to_unicode(self.data[start:stop + 1])
            else:
                r = ''
                r = r.join([chr(c) for c in self.data[start:stop + 1]])
                return r

    def __str__(self):
        return self.data

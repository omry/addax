import six

# Copyright (c) 2012-2017 The ANTLR Project. All rights reserved.
# Use of this file is governed by the BSD 3-clause license that
# can be found in the LICENSE.txt file in the project root.
#
import unittest

#
#  Vacuum all input from a string and then treat it like a buffer.
#
from antlr4.Token import Token
from antlr4.CodePoints import to_unicode


class StringInputStream(object):

    def __init__(self, d):
        self.name = "<empty>"
        """
                                    Byte0    Byte1   Byte2   Byte3   Encoding
            Explicit BOM            #x00 	 #x00 	 #xFE 	 #xFF 	 UTF-32BE
            ASCII first character 	#x00 	 #x00 	 #x00 	 any 	 UTF-32BE
            Explicit BOM 	        #xFF 	 #xFE 	 #x00 	 #x00 	 UTF-32LE
            ASCII first character 	any 	 #x00 	 #x00 	 #x00 	 UTF-32LE
            Explicit BOM 	        #xFE 	 #xFF       	  	  	 UTF-16BE
            ASCII first character 	#x00 	 any 	  	          	 UTF-16BE
            Explicit BOM 	        #xFF 	 #xFE 	  	  	         UTF-16LE
            ASCII first character 	any 	 #x00 	  	  	         UTF-16LE
            Explicit BOM 	        #xEF 	 #xBB 	 #xBF 	  	     UTF-8
            Default 	  	  	    UTF-8
        """
        bom = ''
        if len(d) >= 4 and d[0] == '\x00' and d[1] == '\x00' and d[2] == '\xFE' and d[3] == '\xFF':
            encoding = 'utf-32-be'
            bom = d[0:4]
        elif len(d) >= 4 and d[0] == '\x00' and d[1] == '\x00' and d[2] == '\x00':
            encoding = 'utf-32-be'
        elif len(d) >= 4 and d[0] == '\xFF' and d[1] == '\xFE' and d[2] == '\x00' and d[3] == '\x00':
            encoding = 'utf-32-le'
            bom = d[0:4]
        elif len(d) >= 2 and d[1] == '\x00' and d[2] == '\x00' and d[3] == '\x00':
            encoding = 'utf-32-le'
        elif len(d) >= 2 and d[0] == '\xFE' and d[1] == '\xFF':
            encoding = 'utf-16-be'
            bom = d[0:2]
        elif d[0] == '\x00':
            encoding = 'utf-16-be'
        elif len(d) >= 2 and d[0] == '\xFF' and d[1] == '\xFE':
            encoding = 'utf-16-le'
            bom = d[0:2]
        elif len(d) >= 2 and d[1] == '\x00':
            encoding = 'utf-16-le'
        elif len(d) >= 3 and d[0] == '\xEF' and d[1] == '\xBB' and d[2] == '\xBF':
            encoding = 'utf-8'
            bom = d[0:3]
        else:
            encoding = 'utf-8'

        self.data = []
        if len(bom) > 0:
            bom_int = 0
            for i in range(len(bom)):
                bom_int = bom_int << 8
                bom_int = bom_int | ord(bom[i])
            self.data.append(bom_int)

        if six.PY2:
            self.data.extend([ord(c) for c in d[len(bom):].decode(encoding=encoding)])
        else:
            self.data.extend(d[len(bom):].decode(encoding=encoding))

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
            return u""
        else:
            return to_unicode(self.data[start:stop + 1])

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        return self.strdata
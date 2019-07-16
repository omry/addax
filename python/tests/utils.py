import six
import struct


def bytes_to_unsigned(c):
    if len(c) == 1:
        t = 'B'
    elif len(c) == 2:
        t = 'H'
    elif len(c) == 4:
        t = 'I'

    return struct.unpack(t, c)[0]


def char_range(c1, c2):
    if six.PY2:
        """Generates the characters from `c1` to `c2`, inclusive."""
        for c in xrange(bytes_to_unsigned(c1), bytes_to_unsigned(c2) + 1):
            yield chr(c)
    else:
        for c in range(bytes_to_unsigned(c1), bytes_to_unsigned(c2) + 1):
            yield chr(c)

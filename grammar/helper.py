"""
A small utility hat help generates some fragments for YAML.g4
"""
import struct


def create_segments(range_start, range_end, excluded):
    ordinals = []
    for c in excluded:
        if len(c) == 1:
            n = ord(c)
        elif len(c) == 2:
            n = struct.unpack('>H', c)[0]
        elif len(c) == 3:
            n = struct.unpack('>I', b'\x00' + c)[0]
        elif len(c) == 4:
            n = struct.unpack('>I', c)[0]
        else:
            assert False
        ordinals.append(n)

    excluded = sorted(ordinals)

    segments = []
    seg_start = range_start
    for i in range(len(excluded)):
        ex = excluded[i]
        if ex < seg_start or ex >= range_end:
            continue
        skip = ex == seg_start
        if not skip:
            segments.append((seg_start, ex - 1))
        seg_start = ex + 1
    # close the last segment
    segments.append((seg_start, range_end))
    return segments


def print_8bit_segments(segments):
    s = "fragment PRINTABLE_8BIT: '\\u0009' | '\\u000A' | '\\u000D'"
    for segment in segments:
        s0 = hex(segment[0])[2:]
        s1 = hex(segment[1])[2:]
        if s0 == s1:
            s += " | '\\u00{}'".format(s0)
        else:
            s += " | '\\u00{}'..'\\u00{}'".format(s0, s1)
    s += ";"
    print(s)


def main():
    excluded = [
        # indicators
        '-',
        '?',
        ':',
        ',',
        '[',
        ']',
        '{',
        '}',
        '#',
        '&',
        '*',
        '!',
        '|',
        '>',
        '\'',
        '"',
        '%',
        '@',
        '`',
        b'\xef\xbb\xbf',
        b'\xfe\xff',
        b'\xff\xfe',
        b'\x00\x00\xfe\xff',
        b'\xff\xfe\x00\x00',
    ]
    seg_8bit = create_segments(range_start=0x20, range_end=0x7e, excluded=excluded)
    print_8bit_segments(seg_8bit)
    seg_16bit_1 = create_segments(range_start=0x00A0, range_end=0xD7FF, excluded=excluded)
    seg_16bit_2 = create_segments(range_start=0xE000, range_end=0xFFFD, excluded=excluded)
    # print_16bit_segments(seg_16bit_1, seg_16bit_2)


if __name__ == '__main__':
    main()

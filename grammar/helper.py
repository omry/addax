"""
A small utility hat help generates some fragments for YAML.g4
"""


def create_segments(range_start, range_end, excluded):
    # fragment PRINTABLE_8BIT: '\u0009' | '\u000A' | '\u000D' | '\u0020'..'\u007E'
    s = "fragment PRINTABLE_8BIT: '\\u0009' | '\\u000A' | '\\u000D'"

    excluded = [ord(c) for c in excluded]
    excluded = sorted(excluded)

    segments = []
    seg_start = range_start
    for i in range(len(excluded)):
        ex_8bit = excluded[i]
        skip = ex_8bit == seg_start
        if not skip:
            segments.append((seg_start, ex_8bit - 1))
        seg_start = ex_8bit + 1
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


if __name__ == '__main__':
    segments = create_segments(
        range_start=0x20,
        range_end=0x7e,
        excluded=[
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
        ])
    print_8bit_segments(segments)

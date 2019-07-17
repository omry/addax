"""
A small utility hat help generates some fragments for YAML.g4
"""

def create_8bit_printable_fragment():
    # fragment PRINTABLE_8BIT: '\u0009' | '\u000A' | '\u000D' | '\u0020'..'\u007E'
    s = "fragment PRINTABLE_8BIT: '\\u0009' | '\\u000A' | '\\u000D'"

    excluded = dict(
        C_SEQUENCE_ENTRY='-',
        C_MAPPING_KEY='?',
        C_MAPPING_VALUE=':',
        C_COLLECT_ENTRY=',',
        C_SEQUENCE_START='[',
        C_SEQUENCE_END=']',
        C_MAPPING_START='{',
        C_MAPPING_END='}',
        C_COMMENT='#',
        C_ANCHOR='&',
        C_ALIAS='*',
        C_TAG='!',
        C_LITERAL='|',
        C_FOLDED='>',
        C_SINGLE_QUOTE='\'',
        C_DOUBLE_QUOTE='"',
        C_DIRECTIVE='%',
        C_RESERVED_1='@',
        C_RESERVED_2='`',
    )

    ex = set(excluded.values())
    values = []
    for c in range(0x20, 0x7e):
        if chr(c) not in ex:
            values.append(c)

    segments = []
    seg_start = None
    for i in range(len(values)):
        v = values[i]
        if seg_start is None:
            seg_start = v
        else:
            if v - 1 != values[i - 1]:
                # new segment:
                segments.append((seg_start, values[i - 1]))
                seg_start = v
    # close the last segment
    if seg_start != values[-1]:
        segments.append((seg_start, values[-1]))

    for segment in segments:
        s0 = hex(segment[0])[2:]
        s1 = hex(segment[1])[2:]
        if s0 == s1:
            s += " | '\\u00{}'".format(s0)
        else:
            s += " | '\\u00{}'..'\\u00{}'".format(s0, s1)
    s += ";"
    return s


if __name__ == '__main__':
    print(create_8bit_printable_fragment())

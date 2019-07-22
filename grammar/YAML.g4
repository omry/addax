/** Grammars always start with a grammar header. This grammar is called
 *  ArrayInit and must match the filename: ArrayInit.g4
 */
grammar YAML;
// Comments starting with /// are copied from the YAML 1.2 reference https://yaml.org/spec/1.2/spec.htm.

tokens {
    INDENT,
    DEDENT
}

//=============== Parser ===============
document:;

//=============== LEXER ===============
fragment BOM_UTF32_BE: '\u0000' '\u0000' '\u00fe' '\u00ff';
fragment BOM_UTF32_LE: '\u00ff' '\u00fe' '\u0000' '\u0000';
fragment BOM_UTF16_BE: '\u00fe' '\u00ff';
fragment BOM_UTF16_LE: '\u00ff' '\u00fe';
fragment BOM_UTF8    : '\u00ef' '\u00bb' '\u00bf';
BOM_MARKER: BOM_UTF32_BE | BOM_UTF32_LE | BOM_UTF16_BE | BOM_UTF16_LE | BOM_UTF8;

// Character Set
// with all other tokens removed from it to prevent conflicts
/// 8 bit : #x9 | #xA | #xD | [#x20-#x7E]
fragment PRINTABLE_8BIT: '\u0024' | '\u0028'..'\u0029' | '\u002B' | '\u002E'..'\u0039' | '\u003B'..'\u003D' | '\u0041'..'\u005A' | '\u005C' | '\u005E'..'\u005F' | '\u0061'..'\u007A' | '\u007E';
/// 16 bit: #x85 | [#xA0-#xD7FF] | [#xE000-#xFFFD]
fragment PRINTABLE_16BIT: '\u0085' | '\u00A0'..'\u0D09' | '\u0D0B'..'\uD7FF' | '\uE000'..'\uFEFE' | '\uFF00'..'\uFFFD';
/// 32 bit: [#x10000-#x10FFFF]
fragment PRINTABLE_32BIT: '\u{010000}'..'\u{10FFFF}';

// None space char
NS_CHAR: PRINTABLE_8BIT | PRINTABLE_16BIT | PRINTABLE_32BIT;

// TODO: this should only be allowed inside quoted strings.
/// nb-json 	::= 	#x9 | [#x20-#x10FFFF]
//fragment NB_JSON: '\u{000020}'..'\u{10FFFF}';

// Indicator Characters
C_SEQUENCE_ENTRY: '-';
C_MAPPING_KEY : '?';
C_MAPPING_VALUE : ':';
C_COLLECT_ENTRY : ',';
C_SEQUENCE_START : '[';
C_SEQUENCE_END : ']';
C_MAPPING_START : '{';
C_MAPPING_END : '}';
C_COMMENT : '#';
C_ANCHOR : '&';
C_ALIAS : '*';
C_TAG : '!';
C_LITERAL : '|';
C_FOLDED : '>';
C_SINGLE_QUOTE : '\'';
C_DOUBLE_QUOTE : '"';
C_DIRECTIVE : '%';
C_RESERVED : '@'  | '`';

fragment
C_INDICATOR : C_SEQUENCE_ENTRY | C_MAPPING_KEY| C_MAPPING_VALUE | C_COLLECT_ENTRY |
              C_SEQUENCE_START | C_SEQUENCE_END | C_MAPPING_START | C_MAPPING_END |
              C_COMMENT | C_ANCHOR | C_ALIAS | C_TAG | C_LITERAL | C_FOLDED |
              C_SINGLE_QUOTE | C_DOUBLE_QUOTE | C_DIRECTIVE | C_RESERVED;

fragment
C_FLOW_INDICATOR : C_COLLECT_ENTRY | C_SEQUENCE_START | C_SEQUENCE_END | C_MAPPING_START | C_MAPPING_END;


/// Line Break Characters
/// [24] 	b-line-feed 	::= 	#xA    /* LF */
/// [25] 	b-carriage-return 	::= 	#xD    /* CR */
/// [26] 	b-char 	::= 	b-line-feed | b-carriage-return
fragment B_LINE_FEED: '\u000a';       /* LF */
fragment B_CARRIAGE_RETURN: '\u000d'; /* CR */
fragment B_CHAR:  B_LINE_FEED | B_CARRIAGE_RETURN;

/// [28] 	b-break 	::= 	 ( b-carriage-return b-line-feed ) /* DOS, Windows */
///                           | b-carriage-return               /* MacOS upto 9.x */
///                           | b-line-feed                     /* UNIX, MacOS X */
B_BREAK: (B_CARRIAGE_RETURN B_LINE_FEED |
         B_CARRIAGE_RETURN |
         B_LINE_FEED);
/// [29] 	b-as-line-feed 	::= 	b-break
fragment B_AS_LINE_FEED: B_BREAK;
//. [30] 	b-non-content 	::= 	b-break
fragment B_NON_CONTENT: B_BREAK;

/// Whitespace characters
/// [31] 	s-space	 ::= 	#x20            /* SP */
/// [32] 	s-tab    ::= 	#x9             /* TAB */
/// [33] 	s-white  ::= 	s-space | s-tab
fragment S_SPACE: ' ';
fragment S_TAB: '\t';
fragment S_WHITE: S_SPACE | S_TAB;

/// [35] 	ns-dec-digit 	::= 	[#x30-#x39] /* 0-9 */
fragment NS_DEC_DIGIT: '0'..'9';

/// [36] 	ns-hex-digit 	::= 	  ns-dec-digit
///                             | [#x41-#x46] /* A-F */ | [#x61-#x66] /* a-f */
fragment NS_HEX_DIGIT: NS_DEC_DIGIT | 'A'..'F' | 'a'..'f';

/// [37] 	ns-ascii-letter 	::= 	[#x41-#x5A] /* A-Z */ | [#x61-#x7A] /* a-z */
fragment NS_ASCII_LETTER: 'A'..'Z' | 'a'..'z';

/// [38] 	ns-word-char 	::= 	ns-dec-digit | ns-ascii-letter | “-”
fragment NS_WORD_CHAR: NS_DEC_DIGIT | NS_ASCII_LETTER | '-';

/// [39] 	ns-uri-char 	::= 	  “%” ns-hex-digit ns-hex-digit | ns-word-char | “#”
///                              | “;” | “/” | “?” | “:” | “@” | “&” | “=” | “+” | “$” | “,”
///                              | “_” | “.” | “!” | “~” | “*” | “'” | “(” | “)” | “[” | “]”
fragment NS_URI_CHAR:    '%' NS_HEX_DIGIT NS_HEX_DIGIT | NS_WORD_CHAR
                       | '#' | ';' | '/' | '?' | ':' | '@' | '&' | '=' | '+' | '$'
                       | ',' | '_' | '.' | '!' | '~' | '*' | '\''| '(' | ')' | '[' | ']';

/// [40] 	ns-tag-char 	::= 	ns-uri-char - “!” - c-flow-indicator
fragment NS_TAG_CHAR:  '%' NS_HEX_DIGIT NS_HEX_DIGIT | NS_WORD_CHAR
                     | '#' | ';' | '/' | '?' | ':' | '@' | '&' | '=' | '+'
                     | '$' | '_' | '.' | '~' | '*' | '\''| '(' | ')' |;

/// Escaped characters
/// [41] 	c-escape 	::= 	“\”
fragment C_ESCAPE: '\\';

/// [42]	ns-esc-null	::=	“0”
///	Escaped ASCII null (#x0) character.
fragment NS_ESC_NULL: '0';

/// [43]	ns-esc-bell	::=	“a”
///	Escaped ASCII bell (#x7) character.
fragment NS_ESC_BELL: 'a';

/// [44]	ns-esc-backspace	::=	“b”
///	Escaped ASCII backspace (#x8) character.
fragment NS_ESC_BAKSPACE: 'b';

/// [45]	ns-esc-horizontal-tab	::=	“t” | #x9
///	Escaped ASCII horizontal tab (#x9) character. This is useful at the start or the end of a line to force a leading or trailing tab to become part of the content.
fragment NS_ESC_HORIZONTAL_TAB: 't';

/// [46]	ns-esc-line-feed	::=	“n”
///	Escaped ASCII line feed (#xA) character.
fragment NS_ESC_LINE_FEED: 'n';

/// [47]	ns-esc-vertical-tab	::=	“v”
///	Escaped ASCII vertical tab (#xB) character.
fragment NS_ESC_VERTICAL_TAB : 'v';

/// [48]	ns-esc-form-feed	::=	“f”
///	Escaped ASCII form feed (#xC) character.
fragment NS_ESC_FORM_FEED: 'f';

/// [49]	ns-esc-carriage-return	::=	“r”
///	Escaped ASCII carriage return (#xD) character.
fragment NS_ESC_CARRIAGE_RETURN: 'r';

/// [50]	ns-esc-escape	::=	“e”
///	Escaped ASCII escape (#x1B) character.
fragment NS_ESC_ESCAPE: 'e';

/// [51]	ns-esc-space	::=	#x20
///	Escaped ASCII space (#x20) character. This is useful at the start or the end of a line to force a leading or trailing space to become part of the content.
fragment NS_ESC_SPACE: ' ';

/// [52]	ns-esc-double-quote	::=	“"”
///	Escaped ASCII double quote (#x22).
fragment NS_ESC_DOUBLE_QUOTE: '"';

/// [53]	ns-esc-slash	::=	“/”
///	Escaped ASCII slash (#x2F), for JSON compatibility.
fragment NS_ESC_SLASH: '/';

/// [54]	ns-esc-backslash	::=	“\”
///	Escaped ASCII back slash (#x5C).
fragment NS_ESC_BACKSLASH: '\\';

/// [55]	ns-esc-next-line	::=	“N”
///	Escaped Unicode next line (#x85) character.
fragment NS_ESC_NEXT_LINE: 'N';

/// [56]	ns-esc-non-breaking-space	::=	“_”
///	Escaped Unicode non-breaking space (#xA0) character.
fragment NS_ESC_NON_BREAKING_SPACE: '_';

/// [57]	ns-esc-line-separator	::=	“L”
///	Escaped Unicode line separator (#x2028) character.
fragment NS_ESC_LINE_SEPARATOR: 'L';

/// [58]	ns-esc-paragraph-separator	::=	“P”
///	Escaped Unicode paragraph separator (#x2029) character.
fragment NS_ESC_PARAGRAPH_SEPARATOR: 'P';

/// [59]	ns-esc-8-bit	::=	“x” ( ns-hex-digit × 2 )
///	Escaped 8-bit Unicode character.
fragment NS_ESC_8_BIT: 'x' NS_HEX_DIGIT NS_HEX_DIGIT;

/// [60]	ns-esc-16-bit	::=	“u” ( ns-hex-digit × 4 )
///	Escaped 16-bit Unicode character.
fragment NS_ESC_16_BIT: 'u' NS_HEX_DIGIT NS_HEX_DIGIT NS_HEX_DIGIT NS_HEX_DIGIT;

//[61]	ns-esc-32-bit	::=	“U” ( ns-hex-digit × 8 )
//	Escaped 32-bit Unicode character.
fragment NS_ESC_32_BIT: 'U' NS_HEX_DIGIT NS_HEX_DIGIT NS_HEX_DIGIT NS_HEX_DIGIT
                            NS_HEX_DIGIT NS_HEX_DIGIT NS_HEX_DIGIT NS_HEX_DIGIT;

/// [62] 	c-ns-esc-char 	::= 	“\”
///                        ( ns-esc-null | ns-esc-bell | ns-esc-backspace
///                        | ns-esc-horizontal-tab | ns-esc-line-feed
///                        | ns-esc-vertical-tab | ns-esc-form-feed
///                        | ns-esc-carriage-return | ns-esc-escape | ns-esc-space
///                        | ns-esc-double-quote | ns-esc-slash | ns-esc-backslash
///                        | ns-esc-next-line | ns-esc-non-breaking-space
///                        | ns-esc-line-separator | ns-esc-paragraph-separator
///                        | ns-esc-8-bit | ns-esc-16-bit | ns-esc-32-bit )
fragment C_NS_ESC_CHAR: C_ESCAPE (
    | NS_ESC_NULL                   | NS_ESC_BELL
    | NS_ESC_BAKSPACE               | NS_ESC_HORIZONTAL_TAB
    | NS_ESC_LINE_FEED              | NS_ESC_VERTICAL_TAB
    | NS_ESC_FORM_FEED              | NS_ESC_CARRIAGE_RETURN
    | NS_ESC_ESCAPE                 | NS_ESC_SPACE
    | NS_ESC_DOUBLE_QUOTE           | NS_ESC_SLASH
    | NS_ESC_BACKSLASH              | NS_ESC_NEXT_LINE
    | NS_ESC_NON_BREAKING_SPACE     | NS_ESC_LINE_SEPARATOR
    | NS_ESC_PARAGRAPH_SEPARATOR    | NS_ESC_8_BIT
    | NS_ESC_16_BIT                 | NS_ESC_32_BIT
);
// TODO:  test escape characters once double quoted string is implemented

/// [63] 	s-indent(n) 	::= 	s-space × n
/// [64] 	s-indent(<n) 	::= 	s-space × m /* Where m < n */
/// [65] 	s-indent(≤n) 	::= 	s-space × m /* Where m ≤ n */
S_INDENT: S_SPACE+;


/// [66] 	s-separate-in-line  	::= 	s-white+ | /* Start of line *//
fragment S_SEPARATE_IN_LINE : S_WHITE+;

// TODO: for now this captures only block_in. this should probably be using lexer modes
/// [67] 	s-line-prefix(n,c) 	::= 	c = block-out ⇒ s-block-line-prefix(n)
///                                     c = block-in  ⇒ s-block-line-prefix(n)
///                                     c = flow-out  ⇒ s-flow-line-prefix(n)
///                                     c = flow-in   ⇒ s-flow-line-prefix(n)
fragment S_LINE_PREFIX: S_BLOCK_LINE_PREFIX;


/// [68] 	s-block-line-prefix(n) 	::= 	s-indent(n)
fragment S_BLOCK_LINE_PREFIX: S_INDENT;

/// [69] 	s-flow-line-prefix(n) 	::= 	s-indent(n) s-separate-in-line?
fragment S_FLOW_LINE_PREFIX: S_INDENT S_SEPARATE_IN_LINE?;

/// [70] 	l-empty(n,c) 	::= 	( s-line-prefix(n,c) | s-indent(<n) )
///                                 b-as-line-feed
fragment L_EMPTY: (S_LINE_PREFIX | S_INDENT) B_AS_LINE_FEED;

/// [71] 	b-l-trimmed(n,c) 	::= 	b-non-content l-empty(n,c)+
fragment B_L_TRIMMED: B_NON_CONTENT L_EMPTY+;

/// [72] 	b-as-space 	::= 	b-break
fragment B_AS_SPACE: B_BREAK;

/// [73] 	b-l-folded(n,c) 	::= 	b-l-trimmed(n,c) | b-as-space
fragment B_L_FOLDED: B_L_TRIMMED | B_AS_SPACE;


// TODO: flow not supported yet
/// [74] 	s-flow-folded(n) 	::= 	s-separate-in-line? b-l-folded(n,flow-in)
///                                     s-flow-line-prefix(n)



// TODO: work in progress to support some early testing
/// [126] 	ns-plain-first(c) 	::= 	  ( ns-char - c-indicator )
///                                     | ( ( “?” | “:” | “-” )
///                                        /* Followed by an ns-plain-safe(c)) */ )
fragment NS_PLAIN_FIRST: NS_CHAR | (C_MAPPING_KEY | C_MAPPING_VALUE | C_SEQUENCE_ENTRY );

///    /* Followed by an ns-plain-safe(c)) */ )
/// [127] 	ns-plain-safe(c) 	::= 	c = flow-out  ⇒ ns-plain-safe-out
///                                     c = flow-in   ⇒ ns-plain-safe-in
///                                     c = block-key ⇒ ns-plain-safe-out
///                                     c = flow-key  ⇒ ns-plain-safe-in
fragment NS_PLAIN_SAFE: NS_PLAIN_SAFE_IN;

/// [128] 	ns-plain-safe-out 	::= 	ns-char
/// [129] 	ns-plain-safe-in 	::= 	ns-char - c-flow-indicator
fragment NS_PLAIN_SAFE_IN: NS_CHAR;
/// [130] 	ns-plain-char(c) 	::= 	  ( ns-plain-safe(c) - “:” - “#” )
///                                    | ( /* An ns-char preceding */ “#” )
///                                    | ( “:” /* Followed by an ns-plain-safe(c) */ )
fragment NS_PLAIN_CHAR: NS_PLAIN_SAFE | C_COMMENT | C_MAPPING_VALUE NS_PLAIN_SAFE;
/// [131] 	ns-plain(n,c) 	::= 	c = flow-out  ⇒ ns-plain-multi-line(n,c)
///                                c = flow-in   ⇒ ns-plain-multi-line(n,c)
///                                c = block-key ⇒ ns-plain-one-line(c)
///                                c = flow-key  ⇒ ns-plain-one-line(c)
/// [132] 	nb-ns-plain-in-line(c) 	::= 	( s-white* ns-plain-char(c) )*
// TODO not following spec
NB_NS_PLAIN_IN_LINE: (NS_PLAIN_CHAR)+;
/// [133]     	ns-plain-one-line(c) 	::= 	ns-plain-first(c) nb-ns-plain-in-line(c)
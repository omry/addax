/** Grammars always start with a grammar header. This grammar is called
 *  ArrayInit and must match the filename: ArrayInit.g4
 */
grammar YAML;

yaml_stream: ;
//document  : YAML_HEADER? bom_marker? WORD+;
//bom_marker: BOM_UTF32_LE | BOM_UTF32_LE | BOM_UTF16_BE | BOM_UTF16_LE | BOM_UTF8;

BOM_UTF32_BE: '\u0000' '\u0000' '\u00fe' '\u00ff';
BOM_UTF32_LE: '\u00ff' '\u00fe' '\u0000' '\u0000';
BOM_UTF16_BE: '\u00fe' '\u00ff';
BOM_UTF16_LE: '\u00ff' '\u00fe';
BOM_UTF8    : '\u00ef' '\u00bb' '\u00bf';

// Character Set
// with all other tokens removed from it to prevent conflicts
// 8 bit : #x9 | #xA | #xD | [#x20-#x7E]
fragment PRINTABLE_8BIT: '\u0009' | '\u0020' | '\u0024' | '\u0028'..'\u0029' | '\u002B' | '\u002E'..'\u0039' | '\u003B'..'\u003D' | '\u0041'..'\u005A' | '\u005C' | '\u005E'..'\u005F' | '\u0061'..'\u007A' | '\u007E';
// 16 bit: #x85 | [#xA0-#xD7FF] | [#xE000-#xFFFD]
fragment PRINTABLE_16BIT: '\u0085' | '\u00A0'..'\uD7FF' | '\uE000'..'\uFEFE' | '\uFF00'..'\uFFFD';
//
// 32 bit: [#x10000-#x10FFFF]
fragment PRINTABLE_32BIT: '\u{010000}'..'\u{10FFFF}';

// [27] 	nb-char 	::= 	c-printable - b-char - c-byte-order-mark
NB_CHAR: PRINTABLE_8BIT | PRINTABLE_16BIT | PRINTABLE_32BIT;

// TODO: this should only be allowed inside quoted strings.
// nb-json 	::= 	#x9 | [#x20-#x10FFFF]
fragment NB_JSON: '\u{000020}'..'\u{10FFFF}';

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

//fragment
//C_INDICATOR : C_SEQUENCE_ENTRY | C_MAPPING_KEY| C_MAPPING_VALUE | C_COLLECT_ENTRY |
//              C_SEQUENCE_START | C_SEQUENCE_END | C_MAPPING_START | C_MAPPING_END |
//              C_COMMENT | C_ANCHOR | C_ALIAS | C_TAG | C_LITERAL | C_FOLDED |
//              C_SINGLE_QUOTE | C_DOUBLE_QUOTE | C_DIRECTIVE | C_RESERVED;
//
//fragment
//C_FLOW_INDICATOR : C_COLLECT_ENTRY | C_SEQUENCE_START | C_SEQUENCE_END | C_MAPPING_START | C_MAPPING_END;


// Line Break Characters
//[24] 	b-line-feed 	::= 	#xA    /* LF */
//[25] 	b-carriage-return 	::= 	#xD    /* CR */
//[26] 	b-char 	::= 	b-line-feed | b-carriage-return
fragment B_LINE_FEED: '\u000a';       /* LF */
fragment B_CARRIAGE_RETURN: '\u000d'; /* CR */
fragment B_CHAR:  B_LINE_FEED | B_CARRIAGE_RETURN;

//[28] 	b-break 	::= 	 ( b-carriage-return b-line-feed ) /* DOS, Windows */
//                           | b-carriage-return               /* MacOS upto 9.x */
//                           | b-line-feed                     /* UNIX, MacOS X */
B_BREAK: B_CARRIAGE_RETURN B_LINE_FEED |
         B_CARRIAGE_RETURN |
         B_LINE_FEED;


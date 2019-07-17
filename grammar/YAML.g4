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
//
// 8 bit : #x9 | #xA | #xD | [#x20-#x7E]
PRINTABLE_8BIT: '\u0009' | '\u000A' | '\u000D' | '\u0020' | '\u0024' | '\u0028'..'\u0029' | '\u002b' | '\u002e'..'\u0039' | '\u003b'..'\u003d' | '\u0041'..'\u005a' | '\u005c' | '\u005e'..'\u005f' | '\u0061'..'\u007a' | '\u007e';
// 16 bit: #x85 | [#xA0-#xD7FF] | [#xE000-#xFFFD]
PRINTABLE_16BIT: '\u0085' | '\u00A0'..'\uD7FF' | '\uE000'..'\uFFFD';
//
// 32 bit: [#x10000-#x10FFFF]
// split into two segments:
// 0x010000 - 0x0FFFFF
// 0x100000 - 0x10FFFF
PRINTABLE_32BIT: '\u0001'..'\u000f' '\u0000'..'\uffff' | '\u0010' '\u0000'..'\uffff';

//C_PRINTABLE: PRINTABLE_8BIT | PRINTABLE_16BIT | PRINTABLE_32BIT;
C_PRINTABLE: PRINTABLE_8BIT | PRINTABLE_16BIT ;

//
//// nb-json 	::= 	#x9 | [#x20-#x10FFFF]
//fragment NB_JSON_1: '\u00009';
//fragment NB_JSON_2: '\u0020'..'\uffff';
//fragment NB_JSON_3: '\u0001'..'\u0010' '\u0000'..'\uffff';
//NB_JSON: NB_JSON_1 | NB_JSON_2 | NB_JSON_3;

// Indicator Characters
C_SEQUENCE_ENTRY : '-';
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

// Line Break Characters
fragment B_LINE_FEED: '\u000a';       /* LF */
fragment B_CARRIAGE_RETURN: '\u000d'; /* CR */
fragment B_CHAR:  B_LINE_FEED | B_CARRIAGE_RETURN;





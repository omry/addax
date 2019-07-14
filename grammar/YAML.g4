/** Grammars always start with a grammar header. This grammar is called
 *  ArrayInit and must match the filename: ArrayInit.g4
 */
grammar YAML;

document  : bom_marker? WORD*;
bom_marker: BOM_UTF32_LE | BOM_UTF32_LE | BOM_UTF16_BE | BOM_UTF16_LE | BOM_UTF8;

BOM_UTF32_BE: '\u0000' '\u0000' '\u00fe' '\u00ff';
BOM_UTF32_LE: '\u00ff' '\u00fe' '\u0000' '\u0000';
BOM_UTF16_BE: '\u00fe' '\u00ff';
BOM_UTF16_LE: '\u00ff' '\u00fe';
BOM_UTF8    : '\u00ff' '\u00bb' '\u00bf';

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

// From  spec, unclear if needed
//C_INDICATOR : C_SEQUENCE_ENTRY | C_MAPPING_KEY| C_MAPPING_VALUE | C_COLLECT_ENTRY |
//              C_SEQUENCE_START | C_SEQUENCE_END | C_MAPPING_START | C_MAPPING_END |
//              C_COMMENT | C_ANCHOR | C_ALIAS | C_TAG | C_LITERAL | C_FOLDED |
//              C_SINGLE_QUOTE | C_DOUBLE_QUOTE | C_DIRECTIVE | C_RESERVED;
//
//C_FLOW_INDICATOR : C_COLLECT_ENTRY | C_SEQUENCE_START | C_SEQUENCE_END | C_MAPPING_START | C_MAPPING_END;

// temporary, not from the spec.
CHAR: [0-9a-zA-Z_\-];
WORD: CHAR+;
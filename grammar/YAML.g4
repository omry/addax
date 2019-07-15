/** Grammars always start with a grammar header. This grammar is called
 *  ArrayInit and must match the filename: ArrayInit.g4
 */
grammar YAML;

yaml_stream: ;
//document  : YAML_HEADER? bom_marker? WORD+;
//bom_marker: BOM_UTF32_LE | BOM_UTF32_LE | BOM_UTF16_BE | BOM_UTF16_LE | BOM_UTF8;

//FOO: '\u0001' '\u0000' '\u0001' '\u0000';
//YAML_HEADER: '%YAML' FLOAT;
BOM_UTF32_BE: '\u0000' '\u0000' '\u00fe' '\u00ff';
BOM_UTF32_LE: '\u00ff' '\u00fe' '\u0000' '\u0000';
BOM_UTF16_BE: '\u00fe' '\u00ff';
BOM_UTF16_LE: '\u00ff' '\u00fe';
BOM_UTF8    : '\u00ef' '\u00bb' '\u00bf';

//C_SEQUENCE_ENTRY : '-';
//C_MAPPING_KEY : '?';
//C_MAPPING_VALUE : ':';
//C_COLLECT_ENTRY : ',';
//C_SEQUENCE_START : '[';
//C_SEQUENCE_END : ']';
//C_MAPPING_START : '{';
//C_MAPPING_END : '}';
//C_COMMENT : '#';
//C_ANCHOR : '&';
//C_ALIAS : '*';
//C_TAG : '!';
//C_LITERAL : '|';
//C_FOLDED : '>';
//C_SINGLE_QUOTE : '\'';
//C_DOUBLE_QUOTE : '"';
//C_DIRECTIVE : '%';
//C_RESERVED : '@'  | '`';
//
//// From  spec, unclear if needed
//C_INDICATOR : C_SEQUENCE_ENTRY | C_MAPPING_KEY| C_MAPPING_VALUE | C_COLLECT_ENTRY |
//              C_SEQUENCE_START | C_SEQUENCE_END | C_MAPPING_START | C_MAPPING_END |
//              C_COMMENT | C_ANCHOR | C_ALIAS | C_TAG | C_LITERAL | C_FOLDED |
//              C_SINGLE_QUOTE | C_DOUBLE_QUOTE | C_DIRECTIVE | C_RESERVED;
//
//C_FLOW_INDICATOR : C_COLLECT_ENTRY | C_SEQUENCE_START | C_SEQUENCE_END | C_MAPPING_START | C_MAPPING_END;

//C_PRINTABLE: '\u0009' |  '\u000A' |  '\u000A' | ['\u0020' - '\u007E'] | // 8 bit
//             '\u0085' | ['\u00A0'-'\uD7FF'] | ['\uE000'-'\uFFFD'] |     // 16 bit
//             ['\u10000'-'\u10FFFF'];                                    // 32 bit
//
//BB_JSON:   '\u00009' | ['\u0020'-'\u10FFFF'];


// temporary, not from the spec.
CHAR: [0-9a-zA-Z_\-];
WORD: CHAR+;

//DIGIT: [0-9];
//NZ_DIGIT: [1-9];
//FLOAT: NZ_DIGIT DIGIT* . DIGIT*;


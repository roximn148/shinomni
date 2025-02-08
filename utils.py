# ******************************************************************************
# Copyright (c) 2024. All rights reserved.
# # This work is licensed under the Creative Commons Attribution 4.0
# International License. To view a copy of this license,
# visit # http://creativecommons.org/licenses/by/4.0/.
#
# Author: roximn <roximn148@gmail.com>
# ******************************************************************************
from dataclasses import dataclass

# CATEGORIES *******************************************************************
CATEGORIES = ('Cc|Cf|Cs|Co|Cn|'
              'Ll|Lu|Lt|Lm|Lo|'
              'Mn|Mc|Me|'
              'Nd|Nl|No|'
              'Pc|Pd|Ps|Pe|Pf|Pi|Po|'
              'Sm|Sc|Sk|So|'
              'Zs|Zl|Zp').split('|')
CATEGORIES.sort()

# BLOCKS ***********************************************************************
@dataclass
class UnicodeBlock:
    name: str
    start: int
    end: int
    
BLOCKS = [
    UnicodeBlock('Basic Latin', 0x0000, 0x007F),
    UnicodeBlock('Latin-1 Supplement', 0x0080, 0x00FF),
    UnicodeBlock('Latin Extended-A', 0x0100, 0x017F),
    UnicodeBlock('Latin Extended-B', 0x0180, 0x024F),
    UnicodeBlock('IPA Extensions', 0x0250, 0x02AF),
    UnicodeBlock('Spacing Modifier Letters', 0x02B0, 0x02FF),
    UnicodeBlock('Combining Diacritical Marks', 0x0300, 0x036F),
    UnicodeBlock('Greek and Coptic', 0x0370, 0x03FF),
    UnicodeBlock('Cyrillic', 0x0400, 0x04FF),
    UnicodeBlock('Cyrillic Supplement', 0x0500, 0x052F),
    UnicodeBlock('Armenian', 0x0530, 0x058F),
    UnicodeBlock('Hebrew', 0x0590, 0x05FF),
    UnicodeBlock('Arabic', 0x0600, 0x06FF),
    UnicodeBlock('Syriac', 0x0700, 0x074F),
    UnicodeBlock('Arabic Supplement', 0x0750, 0x077F),
    UnicodeBlock('Thaana', 0x0780, 0x07BF),
    UnicodeBlock('NKo', 0x07C0, 0x07FF),
    UnicodeBlock('Samaritan', 0x0800, 0x083F),
    UnicodeBlock('Mandaic', 0x0840, 0x085F),
    UnicodeBlock('Syriac Supplement', 0x0860, 0x086F),
    UnicodeBlock('Arabic Extended-B', 0x0870, 0x089F),
    UnicodeBlock('Arabic Extended-A', 0x08A0, 0x08FF),
    UnicodeBlock('Devanagari', 0x0900, 0x097F),
    UnicodeBlock('Bengali', 0x0980, 0x09FF),
    UnicodeBlock('Gurmukhi', 0x0A00, 0x0A7F),
    UnicodeBlock('Gujarati', 0x0A80, 0x0AFF),
    UnicodeBlock('Oriya', 0x0B00, 0x0B7F),
    UnicodeBlock('Tamil', 0x0B80, 0x0BFF),
    UnicodeBlock('Telugu', 0x0C00, 0x0C7F),
    UnicodeBlock('Kannada', 0x0C80, 0x0CFF),
    UnicodeBlock('Malayalam', 0x0D00, 0x0D7F),
    UnicodeBlock('Sinhala', 0x0D80, 0x0DFF),
    UnicodeBlock('Thai', 0x0E00, 0x0E7F),
    UnicodeBlock('Lao', 0x0E80, 0x0EFF),
    UnicodeBlock('Tibetan', 0x0F00, 0x0FFF),
    UnicodeBlock('Myanmar', 0x1000, 0x109F),
    UnicodeBlock('Georgian', 0x10A0, 0x10FF),
    UnicodeBlock('Hangul Jamo', 0x1100, 0x11FF),
    UnicodeBlock('Ethiopic', 0x1200, 0x137F),
    UnicodeBlock('Ethiopic Supplement', 0x1380, 0x139F),
    UnicodeBlock('Cherokee', 0x13A0, 0x13FF),
    UnicodeBlock('Unified Canadian Aboriginal Syllabics', 0x1400, 0x167F),
    UnicodeBlock('Ogham', 0x1680, 0x169F),
    UnicodeBlock('Runic', 0x16A0, 0x16FF),
    UnicodeBlock('Tagalog', 0x1700, 0x171F),
    UnicodeBlock('Hanunoo', 0x1720, 0x173F),
    UnicodeBlock('Buhid', 0x1740, 0x175F),
    UnicodeBlock('Tagbanwa', 0x1760, 0x177F),
    UnicodeBlock('Khmer', 0x1780, 0x17FF),
    UnicodeBlock('Mongolian', 0x1800, 0x18AF),
    UnicodeBlock('Unified Canadian Aboriginal Syllabics Extended', 0x18B0, 0x18FF),
    UnicodeBlock('Limbu', 0x1900, 0x194F),
    UnicodeBlock('Tai Le', 0x1950, 0x197F),
    UnicodeBlock('New Tai Lue', 0x1980, 0x19DF),
    UnicodeBlock('Khmer Symbols', 0x19E0, 0x19FF),
    UnicodeBlock('Buginese', 0x1A00, 0x1A1F),
    UnicodeBlock('Tai Tham', 0x1A20, 0x1AAF),
    UnicodeBlock('Combining Diacritical Marks Extended', 0x1AB0, 0x1AFF),
    UnicodeBlock('Balinese', 0x1B00, 0x1B7F),
    UnicodeBlock('Sundanese', 0x1B80, 0x1BBF),
    UnicodeBlock('Batak', 0x1BC0, 0x1BFF),
    UnicodeBlock('Lepcha', 0x1C00, 0x1C4F),
    UnicodeBlock('Ol Chiki', 0x1C50, 0x1C7F),
    UnicodeBlock('Cyrillic Extended-C', 0x1C80, 0x1C8F),
    UnicodeBlock('Georgian Extended', 0x1C90, 0x1CBF),
    UnicodeBlock('Sundanese Supplement', 0x1CC0, 0x1CCF),
    UnicodeBlock('Vedic Extensions', 0x1CD0, 0x1CFF),
    UnicodeBlock('Phonetic Extensions', 0x1D00, 0x1D7F),
    UnicodeBlock('Phonetic Extensions Supplement', 0x1D80, 0x1DBF),
    UnicodeBlock('Combining Diacritical Marks Supplement', 0x1DC0, 0x1DFF),
    UnicodeBlock('Latin Extended Additional', 0x1E00, 0x1EFF),
    UnicodeBlock('Greek Extended', 0x1F00, 0x1FFF),
    UnicodeBlock('General Punctuation', 0x2000, 0x206F),
    UnicodeBlock('Superscripts and Subscripts', 0x2070, 0x209F),
    UnicodeBlock('Currency Symbols', 0x20A0, 0x20CF),
    UnicodeBlock('Combining Diacritical Marks for Symbols', 0x20D0, 0x20FF),
    UnicodeBlock('Letterlike Symbols', 0x2100, 0x214F),
    UnicodeBlock('Number Forms', 0x2150, 0x218F),
    UnicodeBlock('Arrows', 0x2190, 0x21FF),
    UnicodeBlock('Mathematical Operators', 0x2200, 0x22FF),
    UnicodeBlock('Miscellaneous Technical', 0x2300, 0x23FF),
    UnicodeBlock('Control Pictures', 0x2400, 0x243F),
    UnicodeBlock('Optical Character Recognition', 0x2440, 0x245F),
    UnicodeBlock('Enclosed Alphanumerics', 0x2460, 0x24FF),
    UnicodeBlock('Box Drawing', 0x2500, 0x257F),
    UnicodeBlock('Block Elements', 0x2580, 0x259F),
    UnicodeBlock('Geometric Shapes', 0x25A0, 0x25FF),
    UnicodeBlock('Miscellaneous Symbols', 0x2600, 0x26FF),
    UnicodeBlock('Dingbats', 0x2700, 0x27BF),
    UnicodeBlock('Miscellaneous Mathematical Symbols-A', 0x27C0, 0x27EF),
    UnicodeBlock('Supplemental Arrows-A', 0x27F0, 0x27FF),
    UnicodeBlock('Braille Patterns', 0x2800, 0x28FF),
    UnicodeBlock('Supplemental Arrows-B', 0x2900, 0x297F),
    UnicodeBlock('Miscellaneous Mathematical Symbols-B', 0x2980, 0x29FF),
    UnicodeBlock('Supplemental Mathematical Operators', 0x2A00, 0x2AFF),
    UnicodeBlock('Miscellaneous Symbols and Arrows', 0x2B00, 0x2BFF),
    UnicodeBlock('Glagolitic', 0x2C00, 0x2C5F),
    UnicodeBlock('Latin Extended-C', 0x2C60, 0x2C7F),
    UnicodeBlock('Coptic', 0x2C80, 0x2CFF),
    UnicodeBlock('Georgian Supplement', 0x2D00, 0x2D2F),
    UnicodeBlock('Tifinagh', 0x2D30, 0x2D7F),
    UnicodeBlock('Ethiopic Extended', 0x2D80, 0x2DDF),
    UnicodeBlock('Cyrillic Extended-A', 0x2DE0, 0x2DFF),
    UnicodeBlock('Supplemental Punctuation', 0x2E00, 0x2E7F),
    UnicodeBlock('CJK Radicals Supplement', 0x2E80, 0x2EFF),
    UnicodeBlock('Kangxi Radicals', 0x2F00, 0x2FDF),
    UnicodeBlock('Ideographic Description Characters', 0x2FF0, 0x2FFF),
    UnicodeBlock('CJK Symbols and Punctuation', 0x3000, 0x303F),
    UnicodeBlock('Hiragana', 0x3040, 0x309F),
    UnicodeBlock('Katakana', 0x30A0, 0x30FF),
    UnicodeBlock('Bopomofo', 0x3100, 0x312F),
    UnicodeBlock('Hangul Compatibility Jamo', 0x3130, 0x318F),
    UnicodeBlock('Kanbun', 0x3190, 0x319F),
    UnicodeBlock('Bopomofo Extended', 0x31A0, 0x31BF),
    UnicodeBlock('CJK Strokes', 0x31C0, 0x31EF),
    UnicodeBlock('Katakana Phonetic Extensions', 0x31F0, 0x31FF),
    UnicodeBlock('Enclosed CJK Letters and Months', 0x3200, 0x32FF),
    UnicodeBlock('CJK Compatibility', 0x3300, 0x33FF),
    UnicodeBlock('CJK Unified Ideographs Extension A', 0x3400, 0x4DBF),
    UnicodeBlock('Yijing Hexagram Symbols', 0x4DC0, 0x4DFF),
    UnicodeBlock('CJK Unified Ideographs', 0x4E00, 0x9FFF),
    UnicodeBlock('Yi Syllables', 0xA000, 0xA48F),
    UnicodeBlock('Yi Radicals', 0xA490, 0xA4CF),
    UnicodeBlock('Lisu', 0xA4D0, 0xA4FF),
    UnicodeBlock('Vai', 0xA500, 0xA63F),
    UnicodeBlock('Cyrillic Extended-B', 0xA640, 0xA69F),
    UnicodeBlock('Bamum', 0xA6A0, 0xA6FF),
    UnicodeBlock('Modifier Tone Letters', 0xA700, 0xA71F),
    UnicodeBlock('Latin Extended-D', 0xA720, 0xA7FF),
    UnicodeBlock('Syloti Nagri', 0xA800, 0xA82F),
    UnicodeBlock('Common Indic Number Forms', 0xA830, 0xA83F),
    UnicodeBlock('Phags-pa', 0xA840, 0xA87F),
    UnicodeBlock('Saurashtra', 0xA880, 0xA8DF),
    UnicodeBlock('Devanagari Extended', 0xA8E0, 0xA8FF),
    UnicodeBlock('Kayah Li', 0xA900, 0xA92F),
    UnicodeBlock('Rejang', 0xA930, 0xA95F),
    UnicodeBlock('Hangul Jamo Extended-A', 0xA960, 0xA97F),
    UnicodeBlock('Javanese', 0xA980, 0xA9DF),
    UnicodeBlock('Myanmar Extended-B', 0xA9E0, 0xA9FF),
    UnicodeBlock('Cham', 0xAA00, 0xAA5F),
    UnicodeBlock('Myanmar Extended-A', 0xAA60, 0xAA7F),
    UnicodeBlock('Tai Viet', 0xAA80, 0xAADF),
    UnicodeBlock('Meetei Mayek Extensions', 0xAAE0, 0xAAFF),
    UnicodeBlock('Ethiopic Extended-A', 0xAB00, 0xAB2F),
    UnicodeBlock('Latin Extended-E', 0xAB30, 0xAB6F),
    UnicodeBlock('Cherokee Supplement', 0xAB70, 0xABBF),
    UnicodeBlock('Meetei Mayek', 0xABC0, 0xABFF),
    UnicodeBlock('Hangul Syllables', 0xAC00, 0xD7AF),
    UnicodeBlock('Hangul Jamo Extended-B', 0xD7B0, 0xD7FF),
    UnicodeBlock('High Surrogates', 0xD800, 0xDB7F),
    UnicodeBlock('High Private Use Surrogates', 0xDB80, 0xDBFF),
    UnicodeBlock('Low Surrogates', 0xDC00, 0xDFFF),
    UnicodeBlock('Private Use Area', 0xE000, 0xF8FF),
    UnicodeBlock('CJK Compatibility Ideographs', 0xF900, 0xFAFF),
    UnicodeBlock('Alphabetic Presentation Forms', 0xFB00, 0xFB4F),
    UnicodeBlock('Arabic Presentation Forms-A', 0xFB50, 0xFDFF),
    UnicodeBlock('Variation Selectors', 0xFE00, 0xFE0F),
    UnicodeBlock('Vertical Forms', 0xFE10, 0xFE1F),
    UnicodeBlock('Combining Half Marks', 0xFE20, 0xFE2F),
    UnicodeBlock('CJK Compatibility Forms', 0xFE30, 0xFE4F),
    UnicodeBlock('Small Form Variants', 0xFE50, 0xFE6F),
    UnicodeBlock('Arabic Presentation Forms-B', 0xFE70, 0xFEFF),
    UnicodeBlock('Halfwidth and Fullwidth Forms', 0xFF00, 0xFFEF),
    UnicodeBlock('Specials', 0xFFF0, 0xFFFF),
    UnicodeBlock('Linear B Syllabary', 0x10000, 0x1007F),
    UnicodeBlock('Linear B Ideograms', 0x10080, 0x100FF),
    UnicodeBlock('Aegean Numbers', 0x10100, 0x1013F),
    UnicodeBlock('Ancient Greek Numbers', 0x10140, 0x1018F),
    UnicodeBlock('Ancient Symbols', 0x10190, 0x101CF),
    UnicodeBlock('Phaistos Disc', 0x101D0, 0x101FF),
    UnicodeBlock('Lycian', 0x10280, 0x1029F),
    UnicodeBlock('Carian', 0x102A0, 0x102DF),
    UnicodeBlock('Coptic Epact Numbers', 0x102E0, 0x102FF),
    UnicodeBlock('Old Italic', 0x10300, 0x1032F),
    UnicodeBlock('Gothic', 0x10330, 0x1034F),
    UnicodeBlock('Old Permic', 0x10350, 0x1037F),
    UnicodeBlock('Ugaritic', 0x10380, 0x1039F),
    UnicodeBlock('Old Persian', 0x103A0, 0x103DF),
    UnicodeBlock('Deseret', 0x10400, 0x1044F),
    UnicodeBlock('Shavian', 0x10450, 0x1047F),
    UnicodeBlock('Osmanya', 0x10480, 0x104AF),
    UnicodeBlock('Osage', 0x104B0, 0x104FF),
    UnicodeBlock('Elbasan', 0x10500, 0x1052F),
    UnicodeBlock('Caucasian Albanian', 0x10530, 0x1056F),
    UnicodeBlock('Vithkuqi', 0x10570, 0x105BF),
    UnicodeBlock('Todhri', 0x105C0, 0x105FF),
    UnicodeBlock('Linear A', 0x10600, 0x1077F),
    UnicodeBlock('Latin Extended-F', 0x10780, 0x107BF),
    UnicodeBlock('Cypriot Syllabary', 0x10800, 0x1083F),
    UnicodeBlock('Imperial Aramaic', 0x10840, 0x1085F),
    UnicodeBlock('Palmyrene', 0x10860, 0x1087F),
    UnicodeBlock('Nabataean', 0x10880, 0x108AF),
    UnicodeBlock('Hatran', 0x108E0, 0x108FF),
    UnicodeBlock('Phoenician', 0x10900, 0x1091F),
    UnicodeBlock('Lydian', 0x10920, 0x1093F),
    UnicodeBlock('Meroitic Hieroglyphs', 0x10980, 0x1099F),
    UnicodeBlock('Meroitic Cursive', 0x109A0, 0x109FF),
    UnicodeBlock('Kharoshthi', 0x10A00, 0x10A5F),
    UnicodeBlock('Old South Arabian', 0x10A60, 0x10A7F),
    UnicodeBlock('Old North Arabian', 0x10A80, 0x10A9F),
    UnicodeBlock('Manichaean', 0x10AC0, 0x10AFF),
    UnicodeBlock('Avestan', 0x10B00, 0x10B3F),
    UnicodeBlock('Inscriptional Parthian', 0x10B40, 0x10B5F),
    UnicodeBlock('Inscriptional Pahlavi', 0x10B60, 0x10B7F),
    UnicodeBlock('Psalter Pahlavi', 0x10B80, 0x10BAF),
    UnicodeBlock('Old Turkic', 0x10C00, 0x10C4F),
    UnicodeBlock('Old Hungarian', 0x10C80, 0x10CFF),
    UnicodeBlock('Hanifi Rohingya', 0x10D00, 0x10D3F),
    UnicodeBlock('Garay', 0x10D40, 0x10D8F),
    UnicodeBlock('Rumi Numeral Symbols', 0x10E60, 0x10E7F),
    UnicodeBlock('Yezidi', 0x10E80, 0x10EBF),
    UnicodeBlock('Arabic Extended-C', 0x10EC0, 0x10EFF),
    UnicodeBlock('Old Sogdian', 0x10F00, 0x10F2F),
    UnicodeBlock('Sogdian', 0x10F30, 0x10F6F),
    UnicodeBlock('Old Uyghur', 0x10F70, 0x10FAF),
    UnicodeBlock('Chorasmian', 0x10FB0, 0x10FDF),
    UnicodeBlock('Elymaic', 0x10FE0, 0x10FFF),
    UnicodeBlock('Brahmi', 0x11000, 0x1107F),
    UnicodeBlock('Kaithi', 0x11080, 0x110CF),
    UnicodeBlock('Sora Sompeng', 0x110D0, 0x110FF),
    UnicodeBlock('Chakma', 0x11100, 0x1114F),
    UnicodeBlock('Mahajani', 0x11150, 0x1117F),
    UnicodeBlock('Sharada', 0x11180, 0x111DF),
    UnicodeBlock('Sinhala Archaic Numbers', 0x111E0, 0x111FF),
    UnicodeBlock('Khojki', 0x11200, 0x1124F),
    UnicodeBlock('Multani', 0x11280, 0x112AF),
    UnicodeBlock('Khudawadi', 0x112B0, 0x112FF),
    UnicodeBlock('Grantha', 0x11300, 0x1137F),
    UnicodeBlock('Tulu-Tigalari', 0x11380, 0x113FF),
    UnicodeBlock('Newa', 0x11400, 0x1147F),
    UnicodeBlock('Tirhuta', 0x11480, 0x114DF),
    UnicodeBlock('Siddham', 0x11580, 0x115FF),
    UnicodeBlock('Modi', 0x11600, 0x1165F),
    UnicodeBlock('Mongolian Supplement', 0x11660, 0x1167F),
    UnicodeBlock('Takri', 0x11680, 0x116CF),
    UnicodeBlock('Myanmar Extended-C', 0x116D0, 0x116FF),
    UnicodeBlock('Ahom', 0x11700, 0x1174F),
    UnicodeBlock('Dogra', 0x11800, 0x1184F),
    UnicodeBlock('Warang Citi', 0x118A0, 0x118FF),
    UnicodeBlock('Dives Akuru', 0x11900, 0x1195F),
    UnicodeBlock('Nandinagari', 0x119A0, 0x119FF),
    UnicodeBlock('Zanabazar Square', 0x11A00, 0x11A4F),
    UnicodeBlock('Soyombo', 0x11A50, 0x11AAF),
    UnicodeBlock('Unified Canadian Aboriginal Syllabics Extended-A', 0x11AB0, 0x11ABF),
    UnicodeBlock('Pau Cin Hau', 0x11AC0, 0x11AFF),
    UnicodeBlock('Devanagari Extended-A', 0x11B00, 0x11B5F),
    UnicodeBlock('Sunuwar', 0x11BC0, 0x11BFF),
    UnicodeBlock('Bhaiksuki', 0x11C00, 0x11C6F),
    UnicodeBlock('Marchen', 0x11C70, 0x11CBF),
    UnicodeBlock('Masaram Gondi', 0x11D00, 0x11D5F),
    UnicodeBlock('Gunjala Gondi', 0x11D60, 0x11DAF),
    UnicodeBlock('Makasar', 0x11EE0, 0x11EFF),
    UnicodeBlock('Kawi', 0x11F00, 0x11F5F),
    UnicodeBlock('Lisu Supplement', 0x11FB0, 0x11FBF),
    UnicodeBlock('Tamil Supplement', 0x11FC0, 0x11FFF),
    UnicodeBlock('Cuneiform', 0x12000, 0x123FF),
    UnicodeBlock('Cuneiform Numbers and Punctuation', 0x12400, 0x1247F),
    UnicodeBlock('Early Dynastic Cuneiform', 0x12480, 0x1254F),
    UnicodeBlock('Cypro-Minoan', 0x12F90, 0x12FFF),
    UnicodeBlock('Egyptian Hieroglyphs', 0x13000, 0x1342F),
    UnicodeBlock('Egyptian Hieroglyph Format Controls', 0x13430, 0x1345F),
    UnicodeBlock('Egyptian Hieroglyphs Extended-A', 0x13460, 0x143FF),
    UnicodeBlock('Anatolian Hieroglyphs', 0x14400, 0x1467F),
    UnicodeBlock('Gurung Khema', 0x16100, 0x1613F),
    UnicodeBlock('Bamum Supplement', 0x16800, 0x16A3F),
    UnicodeBlock('Mro', 0x16A40, 0x16A6F),
    UnicodeBlock('Tangsa', 0x16A70, 0x16ACF),
    UnicodeBlock('Bassa Vah', 0x16AD0, 0x16AFF),
    UnicodeBlock('Pahawh Hmong', 0x16B00, 0x16B8F),
    UnicodeBlock('Kirat Rai', 0x16D40, 0x16D7F),
    UnicodeBlock('Medefaidrin', 0x16E40, 0x16E9F),
    UnicodeBlock('Miao', 0x16F00, 0x16F9F),
    UnicodeBlock('Ideographic Symbols and Punctuation', 0x16FE0, 0x16FFF),
    UnicodeBlock('Tangut', 0x17000, 0x187FF),
    UnicodeBlock('Tangut Components', 0x18800, 0x18AFF),
    UnicodeBlock('Khitan Small Script', 0x18B00, 0x18CFF),
    UnicodeBlock('Tangut Supplement', 0x18D00, 0x18D7F),
    UnicodeBlock('Kana Extended-B', 0x1AFF0, 0x1AFFF),
    UnicodeBlock('Kana Supplement', 0x1B000, 0x1B0FF),
    UnicodeBlock('Kana Extended-A', 0x1B100, 0x1B12F),
    UnicodeBlock('Small Kana Extension', 0x1B130, 0x1B16F),
    UnicodeBlock('Nushu', 0x1B170, 0x1B2FF),
    UnicodeBlock('Duployan', 0x1BC00, 0x1BC9F),
    UnicodeBlock('Shorthand Format Controls', 0x1BCA0, 0x1BCAF),
    UnicodeBlock('Symbols for Legacy Computing Supplement', 0x1CC00, 0x1CEBF),
    UnicodeBlock('Znamenny Musical Notation', 0x1CF00, 0x1CFCF),
    UnicodeBlock('Byzantine Musical Symbols', 0x1D000, 0x1D0FF),
    UnicodeBlock('Musical Symbols', 0x1D100, 0x1D1FF),
    UnicodeBlock('Ancient Greek Musical Notation', 0x1D200, 0x1D24F),
    UnicodeBlock('Kaktovik Numerals', 0x1D2C0, 0x1D2DF),
    UnicodeBlock('Mayan Numerals', 0x1D2E0, 0x1D2FF),
    UnicodeBlock('Tai Xuan Jing Symbols', 0x1D300, 0x1D35F),
    UnicodeBlock('Counting Rod Numerals', 0x1D360, 0x1D37F),
    UnicodeBlock('Mathematical Alphanumeric Symbols', 0x1D400, 0x1D7FF),
    UnicodeBlock('Sutton SignWriting', 0x1D800, 0x1DAAF),
    UnicodeBlock('Latin Extended-G', 0x1DF00, 0x1DFFF),
    UnicodeBlock('Glagolitic Supplement', 0x1E000, 0x1E02F),
    UnicodeBlock('Cyrillic Extended-D', 0x1E030, 0x1E08F),
    UnicodeBlock('Nyiakeng Puachue Hmong', 0x1E100, 0x1E14F),
    UnicodeBlock('Toto', 0x1E290, 0x1E2BF),
    UnicodeBlock('Wancho', 0x1E2C0, 0x1E2FF),
    UnicodeBlock('Nag Mundari', 0x1E4D0, 0x1E4FF),
    UnicodeBlock('Ol Onal', 0x1E5D0, 0x1E5FF),
    UnicodeBlock('Ethiopic Extended-B', 0x1E7E0, 0x1E7FF),
    UnicodeBlock('Mende Kikakui', 0x1E800, 0x1E8DF),
    UnicodeBlock('Adlam', 0x1E900, 0x1E95F),
    UnicodeBlock('Indic Siyaq Numbers', 0x1EC70, 0x1ECBF),
    UnicodeBlock('Ottoman Siyaq Numbers', 0x1ED00, 0x1ED4F),
    UnicodeBlock('Arabic Mathematical Alphabetic Symbols', 0x1EE00, 0x1EEFF),
    UnicodeBlock('Mahjong Tiles', 0x1F000, 0x1F02F),
    UnicodeBlock('Domino Tiles', 0x1F030, 0x1F09F),
    UnicodeBlock('Playing Cards', 0x1F0A0, 0x1F0FF),
    UnicodeBlock('Enclosed Alphanumeric Supplement', 0x1F100, 0x1F1FF),
    UnicodeBlock('Enclosed Ideographic Supplement', 0x1F200, 0x1F2FF),
    UnicodeBlock('Miscellaneous Symbols and Pictographs', 0x1F300, 0x1F5FF),
    UnicodeBlock('Emoticons', 0x1F600, 0x1F64F),
    UnicodeBlock('Ornamental Dingbats', 0x1F650, 0x1F67F),
    UnicodeBlock('Transport and Map Symbols', 0x1F680, 0x1F6FF),
    UnicodeBlock('Alchemical Symbols', 0x1F700, 0x1F77F),
    UnicodeBlock('Geometric Shapes Extended', 0x1F780, 0x1F7FF),
    UnicodeBlock('Supplemental Arrows-C', 0x1F800, 0x1F8FF),
    UnicodeBlock('Supplemental Symbols and Pictographs', 0x1F900, 0x1F9FF),
    UnicodeBlock('Chess Symbols', 0x1FA00, 0x1FA6F),
    UnicodeBlock('Symbols and Pictographs Extended-A', 0x1FA70, 0x1FAFF),
    UnicodeBlock('Symbols for Legacy Computing', 0x1FB00, 0x1FBFF),
    UnicodeBlock('CJK Unified Ideographs Extension B', 0x20000, 0x2A6DF),
    UnicodeBlock('CJK Unified Ideographs Extension C', 0x2A700, 0x2B73F),
    UnicodeBlock('CJK Unified Ideographs Extension D', 0x2B740, 0x2B81F),
    UnicodeBlock('CJK Unified Ideographs Extension E', 0x2B820, 0x2CEAF),
    UnicodeBlock('CJK Unified Ideographs Extension F', 0x2CEB0, 0x2EBEF),
    UnicodeBlock('CJK Unified Ideographs Extension I', 0x2EBF0, 0x2EE5F),
    UnicodeBlock('CJK Compatibility Ideographs Supplement', 0x2F800, 0x2FA1F),
    UnicodeBlock('CJK Unified Ideographs Extension G', 0x30000, 0x3134F),
    UnicodeBlock('CJK Unified Ideographs Extension H', 0x31350, 0x323AF),
    UnicodeBlock('Tags', 0xE0000, 0xE007F),
    UnicodeBlock('Variation Selectors Supplement', 0xE0100, 0xE01EF),
    UnicodeBlock('Supplementary Private Use Area-A', 0xF0000, 0xFFFFF),
    UnicodeBlock('Supplementary Private Use Area-B', 0x100000, 0x10FFFF),
]

# Helper function to find the block of given character unicode
def findBlock(n: int) -> int:
    """Find the index of the block that contains the given unicode value.

    Parameters:
        n(int): The unicode value to find.

    Returns:
        The index of the block that contains the given unicode value,
        or -1 if it is not found.
    """
    left, right = 0, len(BLOCKS) - 1

    while left <= right:
        mid = (left + right) // 2

        # Check if n is within the current range
        if BLOCKS[mid].start <= n <= BLOCKS[mid].end:
            return mid  # Return the index of the range that contains n

        # Decide which half to search next
        if n < BLOCKS[mid].start:
            right = mid - 1
        else:
            left = mid + 1

    return -1  # Return -1 if n does not fall within a    for b in BLOCKS:

# ******************************************************************************
@dataclass
class BBox:
    x1: float = float('inf')
    y1: float = float('inf')
    x2: float = float('-inf')
    y2: float = float('-inf')

    def update(self, x1, y1, x2, y2):
        self.x1 = min(self.x1, x1)
        self.y1 = min(self.y1, y1)
        self.x2 = max(self.x2, x2)
        self.y2 = max(self.y2, y2)
        return self

    def addMargin(self, margin):
        self.x1 -= margin
        self.y1 -= margin
        self.x2 += margin
        self.y2 += margin
        return self

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    def __str__(self):
        return f'{self.x1:.2f} {self.y1:.2f} {self.x2:.2f} {self.y2:.2f}'

# ******************************************************************************
@dataclass
class GlyphInfo:
    gid: int
    x: int
    y: int
    xAdvance: int
    yAdvance: int
    cluster: int

    def update(self, txt: str) -> 'GlyphInfo':
        v = [int(x) for x in txt.split()]
        if len(v) != 6:
            raise ValueError(f'Invalid glyph info: {txt}')
        self.gid, self.x, self.y, self.xAdvance, self.yAdvance, self.cluster = v
        return self

    def __str__(self):
        return f'{self.gid} ({self.x},{self.y}) +{self.xAdvance}:{self.yAdvance} [{self.cluster}]'

# ******************************************************************************

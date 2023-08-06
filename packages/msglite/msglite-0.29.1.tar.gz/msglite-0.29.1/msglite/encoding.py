import codecs
import ebcdic  # noqa

# Source:
# https://docs.microsoft.com/en-us/windows/win32/intl/code-page-identifiers
DEFAULT_ENCODING = "utf-16-le"

ENCODINGS = {
    37: "cp037",
    # 708: 'ASMO-708',
    708: "arabic",
    709: "arabic",
    710: "arabic",
    932: "shift_jis",
    936: "gb2312",
    949: "ks_c_5601-1987",
    950: "big5",
    1200: "utf_16_le",
    1201: "utf_16_be",
    1361: "Johab",
    10000: "mac-roman",
    10001: "shiftjis",  # not found: 'mac-shift-jis',
    10002: "big5",  # not found: 'mac-big5',
    10003: "x-mac-korean",
    10004: "mac-arabic",
    10005: "hebrew",
    10006: "mac-greek",
    10007: "mac_cyrillic",
    10008: "gb2312",
    10010: "x-mac-romanian",
    10017: "x-mac-ukrainian",
    10021: "thai",
    10029: "mac_latin2",
    10079: "mac_iceland",
    10081: "mac-turkish",
    10082: "x-mac-croatian",
    12000: "utf_32_le",  # Unicode UTF-32, little endian byte order
    12001: "utf_32_be",  # Unicode UTF-32, big endian byte order
    20000: "x-Chinese_CNS",
    20001: "x-cp20001",
    20002: "x_Chinese-Eten",
    20003: "x-cp20003",
    20004: "x-cp20004",
    20005: "x-cp20005",
    20105: "x-IA5",
    20106: "x-IA5-German",
    20107: "x-IA5-Swedish",
    20108: "x-IA5-Norwegian",
    20261: "x-cp20261",
    20269: "x-cp20269",
    20273: "IBM273",
    20277: "IBM277",
    20278: "IBM278",
    20280: "IBM280",
    20284: "IBM284",
    20285: "IBM285",
    20290: "IBM290",
    20297: "IBM297",
    20420: "IBM420",
    20423: "IBM423",
    20424: "IBM424",
    20833: "x-EBCDIC-KoreanExtended",
    20838: "IBM-Thai",
    20866: "koi8-r",
    20871: "IBM871",
    20880: "IBM880",
    20905: "IBM905",
    20924: "IBM00924",
    20932: "EUC-JP",
    20936: "x-cp20936",
    20949: "x-cp20949",
    21025: "cp1025",
    20127: "ascii",
    21866: "koi8-u",
    28591: "iso-8859-1",
    28592: "iso-8859-2",
    28593: "iso-8859-3",
    28594: "iso-8859-4",
    28595: "iso-8859-5",
    28596: "iso-8859-6",
    28597: "iso-8859-7",
    28598: "iso-8859-8",
    28599: "iso-8859-9",
    28603: "iso-8859-13",
    28605: "iso-8859-15",
    29001: "x-Europa",
    38598: "iso-8859-8",
    50220: "iso-2022-jp",
    50221: "csISO2022JP",
    50222: "iso-2022-jp",
    50225: "iso-2022-kr",
    50227: "x-cp50227",
    51932: "euc-jp",
    51936: "EUC-CN",
    51949: "euc-kr",
    52936: "hz-gb-2312",
    54936: "GB18030",
    # 57002: 'x-iscii-de',
    # 57003: 'x-iscii-be',
    # 57004: 'x-iscii-ta',
    # 57005: 'x-iscii-te',
    # 57006: 'x-iscii-as',
    # 57007: 'x-iscii-or',
    # 57008: 'x-iscii-ka',
    # 57009: 'x-iscii-ma',
    # 57010: 'x-iscii-gu',
    # 57011: 'x-iscii-pa',
    65000: "utf-7",
    65001: "utf-8",
}


def get_encoding(num, default=None):
    """Try to turn a number into an encoding."""
    # Straight conversion to a code page:
    codepage = "cp%s" % num
    mapping = ENCODINGS.get(num)
    for encoding in (codepage, mapping):
        try:
            if encoding is None:
                continue
            codecs.lookup(encoding)
            return encoding
        except LookupError:
            pass
    return default

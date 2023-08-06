import struct

FIXED_LENGTH_PROPS = (
    0x0000,
    0x0001,
    0x0002,
    0x0003,
    0x0004,
    0x0005,
    0x0006,
    0x0007,
    0x000A,
    0x000B,
    0x0014,
    0x0040,
    0x0048,
)

VARIABLE_LENGTH_PROPS = (
    0x000D,
    0x001E,
    0x001F,
    0x00FB,
    0x00FD,
    0x00FE,
    0x0102,
    0x1002,
    0x1003,
    0x1004,
    0x1005,
    0x1006,
    0x1007,
    0x1014,
    0x101E,
    0x101F,
    0x1040,
    0x1048,
    0x1102,
)

TYPE_MESSAGE = 0
TYPE_MESSAGE_EMBED = 1
TYPE_ATTACHMENT = 2
TYPE_RECIPIENT = 3

# Sender if `type & 0xf == 0`
RECIPIENT_SENDER = 0
# To if `type & 0xf == 1`
RECIPIENT_TO = 1
# Cc if `type & 0xf == 2`
RECIPIENT_CC = 2
# Bcc if `type & 0xf == 3`
RECIPIENT_BCC = 3

# Define pre-compiled structs to make unpacking slightly faster
# General structs
ST1 = struct.Struct("<8x4I")
ST2 = struct.Struct("<H2xI8x")
ST3 = struct.Struct("<Q")
# Structs used by prop.py
STFIX = struct.Struct("<8x8s")
STVAR = struct.Struct("<8xi4s")
# Structs to help with email type to python type conversions
STI16 = struct.Struct("<h6x")
STI32 = struct.Struct("<i4x")
STI64 = struct.Struct("<q")
STF32 = struct.Struct("<f4x")
STF64 = struct.Struct("<d")

PTYPES = {
    0x0000: "PtypUnspecified",
    0x0001: "PtypNull",
    0x0002: "PtypInteger16",  # Signed short
    0x0003: "PtypInteger32",  # Signed int
    0x0004: "PtypFloating32",  # Float
    0x0005: "PtypFloating64",  # Double
    0x0006: "PtypCurrency",
    0x0007: "PtypFloatingTime",
    0x000A: "PtypErrorCode",
    0x000B: "PtypBoolean",
    0x000D: "PtypObject/PtypEmbeddedTable/Storage",
    0x0014: "PtypInteger64",  # Signed longlong
    0x001E: "PtypString8",
    0x001F: "PtypString",
    0x0040: "PtypTime",  # Use msgEpoch to convert to unix time stamp
    0x0048: "PtypGuid",
    0x00FB: "PtypServerId",
    0x00FD: "PtypRestriction",
    0x00FE: "PtypRuleAction",
    0x0102: "PtypBinary",
    0x1002: "PtypMultipleInteger16",
    0x1003: "PtypMultipleInteger32",
    0x1004: "PtypMultipleFloating32",
    0x1005: "PtypMultipleFloating64",
    0x1006: "PtypMultipleCurrency",
    0x1007: "PtypMultipleFloatingTime",
    0x1014: "PtypMultipleInteger64",
    0x101E: "PtypMultipleString8",
    0x101F: "PtypMultipleString",
    0x1040: "PtypMultipleTime",
    0x1048: "PtypMultipleGuid",
    0x1102: "PtypMultipleBinary",
}

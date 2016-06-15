from ctypes import *

STRING = c_char_p
WSTRING = c_wchar_p


BT_LIST = 5
BT_HASH_INT = 4
MESSAGE_ABRT = 3
BT_STRING = 2
MESSAGE_CTRL_SAVE = 9
BT_IDENTIFIER = 1
MESSAGE_CTRL_REGA = 5
BT_EMPTY = 0
BT_SEQUENCE = 6
STARREC_FILE_ERR_INTERNAL = 5
STARREC_FILE_ERR_NOT_EXIST = 4
STARREC_FILE_ERR_ACCESS_DENIED = 3
PARSE_HDR_NOPARSE = 7
MESSAGE_CTRL_URGC = 4
STARREC_FILE_OK = 0
MESSAGE_CTRL_REGS = 1
PARSE_INCOMPLETE_DATA = 3
MESSAGE_EVNT = 4
STARREC_FILE_ERR_INV_POINTER = 1
STARREC_FILE_ERR_INV_ARG = 2
PARSE_INV_HANDLE = 6
PARSE_NO_MEMORY = 5
MESSAGE_CTRL_REGC = 3
PARSE_ERROR_INV_PARAM = 1
BT_INTEGER = 3
PARSE_OK = 0
PARSE_EOF = 4
PARSE_ERROR_INTERNAL = 2
MESSAGE_CTRL_INFO = 16
MESSAGE_CTRL_ERRO = 15
MESSAGE_INVALID = 0
MESSAGE_CTRL_RACK = 13
MESSAGE_CTRL_RSET = 12
MESSAGE_CTRL_CNFG = 8
MESSAGE_CTRL_REGF = 7
MESSAGE_CTRL_URGA = 6
MESSAGE_CTRL_STRT = 11
MESSAGE_RESP = 2
MESSAGE_CTRL_URGS = 2
MESSAGE_CTRL = 5
MESSAGE_CTRL_SHUT = 10
MESSAGE_CTRL_INVALID = 0
MESSAGE_CTRL_SETC = 14
MESSAGE_CALL = 1
uintptr_t = c_uint
va_list = STRING
size_t = c_uint
rsize_t = size_t
intptr_t = c_int
ptrdiff_t = c_int
wint_t = c_ushort
wctype_t = c_ushort
errcode = c_int
errno_t = c_int
__time32_t = c_long
__time64_t = c_longlong
time_t = __time64_t
class threadmbcinfostruct(Structure):
    pass
threadmbcinfostruct._fields_ = [
]
class threadlocaleinfostruct(Structure):
    pass
pthreadlocinfo = POINTER(threadlocaleinfostruct)
pthreadmbcinfo = POINTER(threadmbcinfostruct)
class __lc_time_data(Structure):
    pass
__lc_time_data._fields_ = [
]
class localeinfo_struct(Structure):
    pass
localeinfo_struct._fields_ = [
    ('locinfo', pthreadlocinfo),
    ('mbcinfo', pthreadmbcinfo),
]
_locale_t = POINTER(localeinfo_struct)
_locale_tstruct = localeinfo_struct
class tagLC_ID(Structure):
    pass
tagLC_ID._fields_ = [
    ('wLanguage', c_ushort),
    ('wCountry', c_ushort),
    ('wCodePage', c_ushort),
]
LC_ID = tagLC_ID
LPLC_ID = POINTER(tagLC_ID)
class N22threadlocaleinfostruct3DOLLAR_0E(Structure):
    pass
N22threadlocaleinfostruct3DOLLAR_0E._fields_ = [
    ('locale', STRING),
    ('wlocale', WSTRING),
    ('refcount', POINTER(c_int)),
    ('wrefcount', POINTER(c_int)),
]
class lconv(Structure):
    pass
threadlocaleinfostruct._fields_ = [
    ('refcount', c_int),
    ('lc_codepage', c_uint),
    ('lc_collate_cp', c_uint),
    ('lc_handle', c_ulong * 6),
    ('lc_id', LC_ID * 6),
    ('lc_category', N22threadlocaleinfostruct3DOLLAR_0E * 6),
    ('lc_clike', c_int),
    ('mb_cur_max', c_int),
    ('lconv_intl_refcount', POINTER(c_int)),
    ('lconv_num_refcount', POINTER(c_int)),
    ('lconv_mon_refcount', POINTER(c_int)),
    ('lconv', POINTER(lconv)),
    ('ctype1_refcount', POINTER(c_int)),
    ('ctype1', POINTER(c_ushort)),
    ('pctype', POINTER(c_ushort)),
    ('pclmap', POINTER(c_ubyte)),
    ('pcumap', POINTER(c_ubyte)),
    ('lc_time_curr', POINTER(__lc_time_data)),
]
lconv._fields_ = [
]
threadlocinfo = threadlocaleinfostruct
class _GCFHandle(Structure):
    pass
_GCFHandle._fields_ = [
]
GCFHandle = _GCFHandle

# values for enumeration 'GCFPARSE_ERROR'
GCFPARSE_ERROR = c_int # enum

# values for enumeration '_GCFMESSAGE_TYPE'
_GCFMESSAGE_TYPE = c_int # enum
GCFMESSAGE_TYPE = _GCFMESSAGE_TYPE

# values for enumeration 'CONTROL_TYPE'
CONTROL_TYPE = c_int # enum

# values for enumeration 'GCFBasicTypeEnum'
GCFBasicTypeEnum = c_int # enum
class _GCFTypeDefinition(Structure):
    pass
GCFTypeDefinition = _GCFTypeDefinition
class _GCFAddr(Structure):
    pass
GCFAddr = _GCFAddr
class _GCFFeatureValue(Structure):
    pass
GCFFeatureValue = _GCFFeatureValue
class _GCFBasicType(Union):
    pass
StarRec_UTF8 = c_ubyte
GCFString = StarRec_UTF8
StarRec_Int = c_int
_GCFBasicType._fields_ = [
    ('identifier', POINTER(GCFString)),
    ('string', POINTER(GCFString)),
    ('integer', StarRec_Int),
    ('list', POINTER(GCFFeatureValue)),
    ('featureValue', POINTER(GCFFeatureValue)),
]
GCFBasicTypeUnion = _GCFBasicType
_GCFTypeDefinition._fields_ = [
    ('basicType', GCFBasicTypeEnum),
    ('dimension', StarRec_Int),
    ('elements', POINTER(GCFFeatureValue)),
    ('listElementType', POINTER(GCFTypeDefinition)),
]
_GCFAddr._fields_ = [
    ('name', POINTER(GCFString)),
    ('subaddr', POINTER(GCFAddr)),
]
_GCFFeatureValue._fields_ = [
    ('next', POINTER(GCFFeatureValue)),
    ('featureName', POINTER(GCFString)),
    ('attributeType', GCFBasicTypeEnum),
    ('attribute', GCFBasicTypeUnion),
    ('valueType', GCFBasicTypeEnum),
    ('value', GCFBasicTypeUnion),
    ('typeDefinition', POINTER(GCFTypeDefinition)),
]
class N9GCFHeader3DOLLAR_5E(Union):
    pass
N9GCFHeader3DOLLAR_5E._fields_ = [
    ('ServiceName', POINTER(GCFString)),
    ('EventName', POINTER(GCFString)),
]
class GCFHeader(Structure):
    pass
GCFHeader._fields_ = [
    ('messageType', GCFMESSAGE_TYPE),
    ('controltype', CONTROL_TYPE),
    ('callid', StarRec_Int),
    ('src_addr', POINTER(GCFAddr)),
    ('dest_addr', POINTER(GCFAddr)),
    ('OptName', N9GCFHeader3DOLLAR_5E),
]
class GCFParameter(Structure):
    pass
GCFParameter._fields_ = [
    ('featureValue', POINTER(GCFFeatureValue)),
]
class GCFStruct(Structure):
    pass
GCFStruct._fields_ = [
    ('gcfheader', GCFHeader),
    ('parameter', GCFParameter),
]

# values for enumeration 'eStarRec_PAL_FileError'
eStarRec_PAL_FileError = c_int # enum
StarRec_PAL_FileError = eStarRec_PAL_FileError
class sStarRec_PAL_FILE(Structure):
    pass
sStarRec_PAL_FILE._fields_ = [
]
StarRec_PAL_FILE = sStarRec_PAL_FILE
StarRec_UTF16 = c_ushort
StarRec_UCS2 = c_ushort
StarRec_Bool = c_int
StarRec_UInt = c_uint
StarRec_UInt64 = c_ulonglong
StarRec_Int64 = c_longlong
StarRec_UInt32 = c_uint
StarRec_Int32 = c_int
StarRec_UInt16 = c_ushort
StarRec_Int16 = c_short
StarRec_UChar = c_ubyte
StarRec_Char = c_byte
StarRec_UByte = c_ubyte
StarRec_Byte = c_byte
StarRec_Size = size_t
StarRec_PtrDiff = ptrdiff_t
__all__ = ['StarRec_UInt32', 'GCFString', 'threadlocinfo',
           'StarRec_PtrDiff', 'MESSAGE_CALL', 'size_t',
           'StarRec_Char', 'StarRec_PAL_FileError',
           '_GCFFeatureValue', 'GCFStruct', 'StarRec_Int64',
           'StarRec_Size', 'rsize_t', 'GCFParameter',
           'GCFFeatureValue', 'STARREC_FILE_OK', 'tagLC_ID',
           '_locale_tstruct', 'intptr_t', 'BT_STRING',
           'MESSAGE_INVALID', 'MESSAGE_CTRL_INVALID', 'BT_INTEGER',
           'StarRec_Byte', 'LC_ID', 'wint_t', '__time32_t',
           'GCFHeader', 'MESSAGE_CTRL_INFO', 'BT_HASH_INT',
           'StarRec_UInt64', 'STARREC_FILE_ERR_INV_ARG',
           'MESSAGE_CTRL_RSET', 'MESSAGE_CTRL_CNFG', 'GCFHandle',
           'StarRec_UInt16', 'MESSAGE_CTRL_SAVE', 'GCFPARSE_ERROR',
           'LPLC_ID', 'BT_LIST', 'StarRec_UCS2', 'StarRec_Int',
           'STARREC_FILE_ERR_INV_POINTER', 'PARSE_INCOMPLETE_DATA',
           '_GCFAddr', 'localeinfo_struct', 'va_list',
           'PARSE_ERROR_INTERNAL', 'MESSAGE_CTRL_RACK',
           'sStarRec_PAL_FILE', 'pthreadlocinfo', 'StarRec_UByte',
           '_GCFBasicType', 'errcode', 'BT_EMPTY', 'ptrdiff_t',
           'StarRec_UInt', 'pthreadmbcinfo', '__time64_t',
           'MESSAGE_CTRL_SHUT', 'PARSE_NO_MEMORY',
           'eStarRec_PAL_FileError', 'STARREC_FILE_ERR_INTERNAL',
           'BT_IDENTIFIER', 'MESSAGE_EVNT',
           'STARREC_FILE_ERR_ACCESS_DENIED', 'errno_t',
           'StarRec_Int16', 'MESSAGE_CTRL_URGC', '_GCFMESSAGE_TYPE',
           'MESSAGE_CTRL_URGA', 'GCFAddr', 'PARSE_HDR_NOPARSE',
           'GCFBasicTypeEnum', 'MESSAGE_CTRL_URGS', 'uintptr_t',
           'PARSE_EOF', '__lc_time_data', 'StarRec_Int32',
           'MESSAGE_ABRT', 'MESSAGE_CTRL_STRT', '_locale_t',
           'MESSAGE_RESP', 'GCFTypeDefinition', 'StarRec_UTF8',
           'N22threadlocaleinfostruct3DOLLAR_0E', 'GCFBasicTypeUnion',
           'time_t', 'PARSE_INV_HANDLE', 'MESSAGE_CTRL_SETC',
           'PARSE_OK', 'GCFMESSAGE_TYPE', 'MESSAGE_CTRL',
           '_GCFHandle', '_GCFTypeDefinition', 'BT_SEQUENCE',
           'threadlocaleinfostruct', 'StarRec_Bool', 'lconv',
           'StarRec_PAL_FILE', 'STARREC_FILE_ERR_NOT_EXIST',
           'StarRec_UTF16', 'PARSE_ERROR_INV_PARAM',
           'MESSAGE_CTRL_REGS', 'CONTROL_TYPE', 'wctype_t',
           'N9GCFHeader3DOLLAR_5E', 'StarRec_UChar',
           'MESSAGE_CTRL_REGA', 'threadmbcinfostruct',
           'MESSAGE_CTRL_REGC', 'MESSAGE_CTRL_ERRO',
           'MESSAGE_CTRL_REGF']

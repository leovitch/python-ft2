# python-ft2
# Copyright (C) 2010 Ryan Coyner
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

"""FreeType simple types definitions."""

import ctypes
import types

# Typedefs
Bool = ctypes.c_ubyte
Error = ctypes.c_int
F26Dot6 = ctypes.c_long
Fixed = ctypes.c_long
GenericFinalizer = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
Int = ctypes.c_int
Int32 = ctypes.c_int32
Long = ctypes.c_long
Short = ctypes.c_short
String = ctypes.c_char
UInt = ctypes.c_uint
UInt32 = ctypes.c_uint32
ULong = ctypes.c_ulong
UShort = ctypes.c_ushort

# Conversion Helpers
def ToFixed(value):
    """ Converts float or int to FT.Fixed """
    if isinstance(value,types.FloatType):
        return int(value*0x10000)
    if isinstance(value,(types.IntType,types.LongType)):
        return value << 16
    return value
def FromFixed(fixed):
    """ Converts FT.Fixed to float """
    return float(fixed)/0x10000
def IFromFixed(fixed):
    """ Converts FT.Fixed to int (truncates) """
    return fixed >> 16
def ToF26Dot6(value):
    """ Converts float or int to FT.F26Dot6 """
    if isinstance(value,types.FloatType):
        return int(value*64)
    if isinstance(value,(types.IntType,types.LongType)):
        return value << 6
    return value
def FromF26Dot6(f26dot6):
    """ Converts F26Dot6 to float """
    return float(f26dot6)/64
def IFromF26Dot6(f26dot6):
    """ Converts F26Dot6 to int (truncates) """
    return f26dot6 >> 6


# Structures
class Matrix(ctypes.Structure):
    """Stores a 2x2 matrix."""
    _fields_ = [
        ('xx', Fixed),
        ('xy', Fixed),
        ('yx', Fixed),
        ('yy', Fixed)
    ]

class Generic(ctypes.Structure):
    """Associates client data to FreeType core objects."""
    _fields_ = [
        ('data', ctypes.c_void_p),
        ('finalizer', GenericFinalizer)
    ]


class ListNodeRec(ctypes.Structure):
    """Holds a single list element."""
    pass


ListNodeRec._fields_ = [
    ('prev', ctypes.POINTER(ListNodeRec)),
    ('next', ctypes.POINTER(ListNodeRec)),
    ('data', ctypes.c_void_p)
]


class ListRec(ctypes.Structure):
    """Holds a simple doubly-linked list used in FreeType."""
    _fields_ = [
        ('head', ctypes.POINTER(ListNodeRec)),
        ('tail', ctypes.POINTER(ListNodeRec))
    ]

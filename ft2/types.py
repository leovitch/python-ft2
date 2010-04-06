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

__all__ = ['Error', 'F26Dot6', 'Fixed', 'GenericFinalizer', 'Int', 'Long',
           'Short', 'String', 'UInt', 'UInt32', 'UShort', 'Generic', 'ListRec',
           'ListNodeRec']


# Typedefs
Error = ctypes.c_int
F26Dot6 = ctypes.c_long
Fixed = ctypes.c_long
GenericFinalizer = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
Int = ctypes.c_int
Long = ctypes.c_long
Short = ctypes.c_short
String = ctypes.c_char
UInt = ctypes.c_uint
UInt32 = ctypes.c_uint32
UShort = ctypes.c_ushort


# Structures
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

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

"""FreeType low-level system interface definition."""

import ctypes

__all__ = ['MemoryRec', 'StreamRec']


# Structures
class MemoryRec(ctypes.Structure):
    """A memory manager object."""
    pass


class StreamDesc(ctypes.Union):
    """Stores a file descriptor in an input stream."""
    _fields_ = [
        ('value', ctypes.c_long),
        ('pointer', ctypes.c_void_p)
    ]


class StreamRec(ctypes.Structure):
    pass


# Callbacks
AllocFunc = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.POINTER(MemoryRec),
                              ctypes.c_long)

FreeFunc = ctypes.CFUNCTYPE(None, ctypes.POINTER(MemoryRec), ctypes.c_void_p)

ReallocFunc = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.POINTER(MemoryRec),
                                ctypes.c_long, ctypes.c_long, ctypes.c_void_p)

StreamIoFunc = ctypes.CFUNCTYPE(ctypes.c_ulong, ctypes.POINTER(StreamRec),
                                 ctypes.c_ulong, ctypes.c_char_p,
                                 ctypes.c_ulong)

StreamCloseFunc = ctypes.CFUNCTYPE(None, ctypes.POINTER(StreamRec))


MemoryRec._fields_ = [
    ('user', ctypes.c_void_p),
    ('alloc', AllocFunc),
    ('free', FreeFunc),
    ('realloc', ReallocFunc)
]

StreamRec._fields_ = [
    ('base', ctypes.c_char_p),
    ('size', ctypes.c_ulong),
    ('pos', ctypes.c_ulong),
    ('descriptor', StreamDesc),
    ('pathname', StreamDesc),
    ('read', StreamIoFunc),
    ('close', StreamCloseFunc),
    ('memory', ctypes.POINTER(MemoryRec)),
    ('cursor', ctypes.c_char_p),
    ('limit', ctypes.c_char_p)
]

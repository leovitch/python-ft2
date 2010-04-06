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

"""FreeType high-level API and common types."""

import ctypes

from ft2 import image, libfreetype, system, types

__all__ = ['BitmapSize', 'GlyphMetrics', 'CharMapRec', 'DriverRec', 'FaceRec',
           'GlyphSlotRec', 'LibraryRec', 'ModuleRec', 'SizeRec']


# Enumerations
ENCODING_NONE = 0
ENCODING_MS_SYMBOL = 1937337698
ENCODING_UNICODE = 1970170211
ENCODING_SJIS = 1936353651
ENCODING_GB2312 = 1734484000
ENCODING_BIG5 = 1651074869
ENCODING_WANSUNG = 2002873971
ENCODING_JOHAB = 1785686113
ENCODING_MS_SJIS = ENCODING_SJIS
ENCODING_MS_GB2312 = ENCODING_GB2312
ENCODING_MS_BIG5 = ENCODING_BIG5
ENCODING_MS_WANSUNG = ENCODING_WANSUNG
ENCODING_MS_JOHAB = ENCODING_JOHAB
ENCODING_ADOBE_STANDARD = 1094995778
ENCODING_ADOBE_EXPERT = 1094992453
ENCODING_ADOBE_CUSTOM = 1094992451
ENCODING_ADOBE_LATIN_1 = 1818326065
ENCODING_OLD_LATIN_2 = 1818326066
ENCODING_APPLE_ROMAN = 1634889070
Encoding = ctypes.c_int


# Face Flags
FACE_FLAG_SCALABLE = 1
FACE_FLAG_FIXED_SIZES = 2
FACE_FLAG_FIXED_WIDTH = 4
FACE_FLAG_SFNT = 8
FACE_FLAG_HORIZONTAL = 16
FACE_FLAG_VERTICAL = 32
FACE_FLAG_KERNING = 64
FACE_FLAG_FAST_GLYPHS = 128
FACE_FLAG_MULTIPLE_MASTERS = 256
FACE_FLAG_GLYPH_NAMES = 512
FACE_FLAG_EXTERNAL_STREAM = 1024
FACE_FLAG_HINTER = 2048
FACE_FLAG_CID_KEYED = 4096
FACE_FLAG_TRICKY = 8192


class BitmapSize(ctypes.Structure):
    """Models the metrics of a bitmap strike in a bitmap font."""
    _fields_ = [
        ('height', types.Short),
        ('width', types.Short),
        ('size', image.Pos),
        ('x_ppem', image.Pos),
        ('y_ppem', image.Pos)
    ]


class GlyphMetrics(ctypes.Structure):
    """Models the metrics of a single glyph."""
    _fields_ = [
        ('width', image.Pos),
        ('height', image.Pos),
        ('horiBearingX', image.Pos),
        ('horiBearingY', image.Pos),
        ('horiAdvance', image.Pos),
        ('vertBearingX', image.Pos),
        ('vertBearingY', image.Pos),
        ('vertAdvance', image.Pos)
    ]


class CharMapRec(ctypes.Structure):
    """
    Translates character codes in a given encoding into glyph indices for its
    parent's face.

    """
    pass


class DriverRec(ctypes.Structure):
    """A special module capable of creating faces from font files."""
    pass


class GlyphSlotRec(ctypes.Structure):
    """
    A container where glyph images are loaded independently of the glyph image
    format.

    """
    pass


class SizeInternalRec(ctypes.Structure):
    """Models private data of a given Size object."""
    pass


class SizeRec(ctypes.Structure):
    """Models a face scaled to a given character size."""
    pass


class FaceInternalRec(ctypes.Structure):
    """Models private data of a given Face object."""
    pass


class FaceRec(ctypes.Structure):
    """Models a given typeface in a given style."""
    _fields_ = [
        ('num_faces', types.Long),
        ('face_index', types.Long),
        ('face_flags', types.Long),
        ('style_flags', types.Long),
        ('num_glyphs', types.Long),
        ('family_name', ctypes.POINTER(types.String)),
        ('style_name', ctypes.POINTER(types.String)),
        ('num_fixed_sizes', types.Int),
        ('charmaps', ctypes.POINTER(ctypes.POINTER(CharMapRec))),
        ('generic', types.Generic),
        ('bbox', image.BBox),
        ('units_per_EM', types.UShort),
        ('ascender', types.Short),
        ('descender', types.Short),
        ('height', types.Short),
        ('max_advance_width', types.Short),
        ('max_advance_height', types.Short),
        ('underline_position', types.Short),
        ('underline_thickness', types.Short),
        ('glyph', ctypes.POINTER(GlyphSlotRec)),
        ('size', ctypes.POINTER(SizeRec)),
        ('charmap', ctypes.POINTER(CharMapRec)),
        ('driver', ctypes.POINTER(DriverRec)),
        ('memory', ctypes.POINTER(system.MemoryRec)),
        ('stream', ctypes.POINTER(system.StreamRec)),
        ('sizes_list', ctypes.POINTER(types.ListRec)),
        ('autohint', types.Generic),
        ('extensions', ctypes.c_void_p),
        ('internal', ctypes.POINTER(FaceInternalRec))
    ]


CharMapRec._fields_ = [
    ('face', ctypes.POINTER(FaceRec)),
    ('encoding', Encoding),
    ('platform_id', types.UShort),
    ('encoding_id', types.UShort)
]


class LibraryRec(ctypes.Structure):
    """Parent of all other objects in FreeType."""
    pass


class ModuleRec(ctypes.Structure):
    """Provides services in FreeType."""
    pass


Init_FreeType = libfreetype.FT_Init_FreeType
Init_FreeType.restype = types.Error
Init_FreeType.argtypes = [ctypes.POINTER(ctypes.POINTER(LibraryRec))]

Done_FreeType = libfreetype.FT_Done_FreeType
Done_FreeType.restype = types.Error
Done_FreeType.argtypes = [ctypes.POINTER(LibraryRec)]

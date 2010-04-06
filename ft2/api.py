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

from ft2 import image, libfreetype, types

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


class FaceRec(ctypes.Structure):
    """Models a given typeface in a given style."""
    pass


CharMapRec._fields_ = [
    ('face', ctypes.POINTER(FaceRec)),
    ('encoding', Encoding),
    ('platform_id', types.UShort),
    ('encoding_id', types.UShort)
]


class GlyphSlotRec(ctypes.Structure):
    """
    A container where glyph images are loaded independently of the glyph image
    format.

    """
    pass


class LibraryRec(ctypes.Structure):
    """Parent of all other objects in FreeType."""
    pass


class ModuleRec(ctypes.Structure):
    """Provides services in FreeType."""
    pass


class SizeRec(ctypes.Structure):
    """Models a face scaled to a given character size."""
    pass


Init_FreeType = libfreetype.FT_Init_FreeType
Init_FreeType.restype = types.Error
Init_FreeType.argtypes = [ctypes.POINTER(ctypes.POINTER(LibraryRec))]

Done_FreeType = libfreetype.FT_Done_FreeType
Done_FreeType.restype = types.Error
Done_FreeType.argtypes = [ctypes.POINTER(LibraryRec)]

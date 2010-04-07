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

"""FreeType convenience functions to handle glyphs."""

import ctypes

from ft2 import api, image, libfreetype, types

__all__ = ['GlyphClass', 'GlyphRec', 'BitmapGlyphRec', 'Get_Glyph',
           'Glyph_To_Bitmap', 'Done_Glyph']


class GlyphClass(ctypes.Structure):
    """Forward declaration to a private type."""
    pass


class GlyphRec(ctypes.Structure):
    """Root glyph structure which contains a glyph image."""
    _fields_ = [
        ('library', ctypes.POINTER(api.LibraryRec)),
        ('clazz', ctypes.POINTER(GlyphClass)),
        ('format', image.GlyphFormat),
        ('advance', image.Vector)
    ]


class BitmapGlyphRec(ctypes.Structure):
    """Contains bitmap glyph images."""
    _fields_ = [
        ('root', ctypes.POINTER(GlyphRec)),
        ('left', types.Int),
        ('top', types.Int),
        ('bitmap', image.Bitmap)
    ]


Get_Glyph = libfreetype.FT_Get_Glyph
Get_Glyph.restype = types.Error
Get_Glyph.argtypes = [ctypes.POINTER(api.GlyphSlotRec),
                      ctypes.POINTER(ctypes.POINTER(GlyphRec))]

Glyph_To_Bitmap = libfreetype.FT_Glyph_To_Bitmap
Glyph_To_Bitmap.restype = types.Error
Glyph_To_Bitmap.argtypes = [ctypes.POINTER(ctypes.POINTER(GlyphRec)), api.RenderMode, ctypes.POINTER(image.Vector), types.Bool]

Done_Glyph = libfreetype.FT_Done_Glyph
Done_Glyph.restype = None
Done_Glyph.argtypes = [ctypes.POINTER(GlyphRec)]

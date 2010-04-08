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

__all__ = ['GLYPH_BBOX_UNSCALED', 'GLYPH_BBOX_SUBPIXELS', 'GLYPH_BBOX_GRIDFIT',
           'GLYPH_BBOX_TRUNCATE', 'GLYPH_BBOX_PIXELS', 'Glyph_BBox_Mode',
           'GlyphClass', 'GlyphRec', 'BitmapGlyphRec', 'OutlineGlyphRec',
           'Get_Glyph', 'Glyph_Copy', 'Glyph_Transform', 'Glyph_Get_CBox',
           'Glyph_To_Bitmap', 'Done_Glyph', 'Matrix_Multiply', 'Matrix_Invert']


# Enumerations
GLYPH_BBOX_UNSCALED = 0
GLYPH_BBOX_SUBPIXELS = 0
GLYPH_BBOX_GRIDFIT = 1
GLYPH_BBOX_TRUNCATE = 2
GLYPH_BBOX_PIXELS = 3
Glyph_BBox_Mode = ctypes.c_int


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
    """Used to model a bitmap glyph image."""
    _fields_ = [
        ('root', ctypes.POINTER(GlyphRec)),
        ('left', types.Int),
        ('top', types.Int),
        ('bitmap', image.Bitmap)
    ]


class OutlineGlyphRec(ctypes.Structure):
    """Used for outline (vectorial) glyph images."""
    _fields_ = [
        ('root', ctypes.POINTER(GlyphRec)),
        ('outline', image.Outline)
    ]


Get_Glyph = libfreetype.FT_Get_Glyph
Get_Glyph.restype = types.Error
Get_Glyph.argtypes = [ctypes.POINTER(api.GlyphSlotRec),
                      ctypes.POINTER(ctypes.POINTER(GlyphRec))]

Glyph_Copy = libfreetype.FT_Glyph_Copy
Glyph_Copy.restype = types.Error
Glyph_Copy.argtypes = [ctypes.POINTER(GlyphRec),
                       ctypes.POINTER(ctypes.POINTER(GlyphRec))]

Glyph_Transform = libfreetype.FT_Glyph_Transform
Glyph_Transform.restype = types.Error
Glyph_Transform.argtypes = [ctypes.POINTER(GlyphRec),
                            ctypes.POINTER(types.Matrix),
                            ctypes.POINTER(image.Vector)]

Glyph_Get_CBox = libfreetype.FT_Glyph_Get_CBox
Glyph_Get_CBox.restype = None
Glyph_Get_CBox.argtypes = [ctypes.POINTER(GlyphRec), types.UInt,
                           ctypes.POINTER(image.BBox)]

# XXX: 3rd argument is either a pointer to a Vector, or a 0.
Glyph_To_Bitmap = libfreetype.FT_Glyph_To_Bitmap
Glyph_To_Bitmap.restype = types.Error
Glyph_To_Bitmap.argtypes = [ctypes.POINTER(ctypes.POINTER(GlyphRec)),
                            api.RenderMode, ctypes.c_void_p, types.Bool]

Done_Glyph = libfreetype.FT_Done_Glyph
Done_Glyph.restype = None
Done_Glyph.argtypes = [ctypes.POINTER(GlyphRec)]

Matrix_Multiply = libfreetype.FT_Matrix_Multiply
Matrix_Multiply.restype = None
Matrix_Multiply.argtypes = [ctypes.POINTER(types.Matrix),
                            ctypes.POINTER(types.Matrix)]

Matrix_Invert = libfreetype.FT_Matrix_Invert
Matrix_Invert.restype = types.Error
Matrix_Invert.argtypes = [ctypes.POINTER(types.Matrix)]

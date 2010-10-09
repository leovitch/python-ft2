# python-ft2
# Copyright (C) 2010 Leo Hourvitz
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

"""FreeType bitmap manipulations."""

import ctypes

from freetype2 import libfreetype, fttypes, ftimage, freetype

Bitmap_Copy = libfreetype.FT_Bitmap_Copy
Bitmap_Copy.restype = fttypes.Error
Bitmap_Copy.argtypes = [
    freetype.Library, 
    ctypes.POINTER(ftimage.Bitmap), # source
    ctypes.POINTER(ftimage.Bitmap), # destination
]

Bitmap_Embolden = libfreetype.FT_Bitmap_Embolden
Bitmap_Embolden.restype = fttypes.Error
Bitmap_Embolden.argtypes = [
    freetype.Library,
    ctypes.POINTER(ftimage.Bitmap), # in/out
    ftimage.Pos,
    ftimage.Pos
]

Bitmap_Convert = libfreetype.FT_Bitmap_Convert
Bitmap_Convert.restype = fttypes.Error
Bitmap_Convert.argtypes = [
    freetype.Library,
    ctypes.POINTER(ftimage.Bitmap), # source
    ctypes.POINTER(ftimage.Bitmap), # dest
    ctypes.c_int            # alignment
]

GlyphSlot_Own_Bitmap = libfreetype.FT_GlyphSlot_Own_Bitmap
GlyphSlot_Own_Bitmap.restype = fttypes.Error
GlyphSlot_Own_Bitmap.argypes = [
    freetype.GlyphSlot
]

Bitmap_Done = libfreetype.FT_Bitmap_Done
Bitmap_Done.restype = fttypes.Error
Bitmap_Done.argtypes = [
    freetype.Library,
    ctypes.POINTER(ftimage.Bitmap)
]






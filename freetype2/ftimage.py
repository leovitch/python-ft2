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

"""FreeType glyph image formats and default raster interface."""

import ctypes
from freetype2.fttypes import *

# Enumerations
GLYPH_FORMAT_NONE = 0
GLYPH_FORMAT_COMPOSITE = 1668246896
GLYPH_FORMAT_BITMAP = 1651078259
GLYPH_FORMAT_OUTLINE = 1869968492
GLYPH_FORMAT_PLOTTER = 1886154612
GlyphFormat = ctypes.c_ulong


# Typedefs
Pos = ctypes.c_long


# Outline Flags
OUTLINE_NONE = 0
OUTLINE_OWNER = 1
OUTLINE_EVEN_ODD_FILL = 2
OUTLINE_REVERSE_FILL = 4
OUTLINE_IGNORE_DROPOUTS = 8
OUTLINE_SMART_DROPOUTS = 16
OUTLINE_INCLUDE_STUBS = 32
OUTLINE_HIGH_PRECISION = 256
OUTLINE_SINGLE_PASS = 512


# Structures
class BBox(ctypes.Structure):
    """
    Holds an outline's coordinates of its extrema in the horizontal and
    vertical directions.

    """
    _fields_ = [
        ('xMin', Pos),
        ('yMin', Pos),
        ('xMax', Pos),
        ('yMax', Pos)
    ]

# Mode for describing the format of pixels in a Bitmap
PIXEL_MODE_NONE = 0
PIXEL_MODE_MONO = 1
PIXEL_MODE_GRAY = 2
PIXEL_MODE_GRAY2 = 3
PIXEL_MODE_GRAY4 = 4
PIXEL_MODE_LCD = 5
PIXEL_MODE_LCD_V = 6

PIXEL_MODE_MAX = 7


class Bitmap(ctypes.Structure):
    """Describes a bitmap or pixmap to the raster."""
    _fields_ = [
        ('rows', ctypes.c_int),
        ('width', ctypes.c_int),
        ('pitch', ctypes.c_int),
        ('buffer', ctypes.POINTER(ctypes.c_ubyte)),
        ('num_grays', ctypes.c_short),
        ('pixel_mode', ctypes.c_byte),
        ('palette_mode', ctypes.c_byte),
        ('palette', ctypes.c_void_p)
    ]


class Vector(ctypes.Structure):
    """Stores a two-dimensional vector."""
    _fields_ = [
        ('x', Pos),
        ('y', Pos)
    ]

class Outline(ctypes.Structure):
    """Describes an outline to the scan-line converter."""
    _fields_ = [
        ('n_contours', ctypes.c_short),
        ('n_points', ctypes.c_short),
        ('points', ctypes.POINTER(Vector)),
        ('tags', ctypes.c_char_p),
        ('contours', ctypes.POINTER(ctypes.c_short)),
        ('flags', ctypes.c_int)
    ]

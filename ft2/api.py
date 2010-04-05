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

from ft2 import image, types

__all__ = ['BitmapSize', 'Driver', 'GlyphMetrics', 'Library', 'Module']


class BitmapSize(ctypes.Structure):
    """Models the metrics of a bitmap strike in a bitmap font."""
    _fields_ = [
        ('height', types.Short),
        ('width', types.Short),
        ('size', image.Pos),
        ('x_ppem', image.Pos),
        ('y_ppem', image.Pos)
    ]


class Driver(ctypes.Structure):
    """Handle to a given FreeType font driver object."""
    pass


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


class Library(ctypes.Structure):
    """Handles a FreeType library instance."""
    pass


class Module(ctypes.Structure):
    """Handle to a given FreeType module object."""
    pass

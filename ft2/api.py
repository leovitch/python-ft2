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

__all__ = ['BitmapSize', 'GlyphMetrics']


class BitmapSize(ctypes.Structure):
    _fields_ = [
        ('height', types.Short),
        ('width', types.Short),
        ('size', image.Pos),
        ('x_ppem', image.Pos),
        ('y_ppem', image.Pos)
    ]


class GlyphMetrics(ctypes.Structure):
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

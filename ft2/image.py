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

__all__ = ['BBox', 'Pos']


# Typedefs
Pos = ctypes.c_long


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

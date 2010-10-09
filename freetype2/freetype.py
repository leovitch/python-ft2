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

from freetype2 import ftimage, libfreetype, ftsystem, fttypes

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
Encoding = ctypes.c_uint32


# Render Mode
RENDER_MODE_NORMAL = 0
RENDER_MODE_LIGHT = 1
RENDER_MODE_MONO = 2
RENDER_MODE_LCD = 3
RENDER_MODELCD_V = 4
RENDER_MODE_MAX = 5
RenderMode = ctypes.c_uint


# Kerning Mode
KERNING_DEFAULT = 0
KERNING_UNFITTED = 1
KERNING_UNSCALED = 2
Kerning_Mode = ctypes.c_uint


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

# Macros for testing face flags are lower down, see IS_SCALABLE

# Load Flags
LOAD_DEFAULT = 0
LOAD_NO_SCALE = 1
LOAD_NO_HINTING = 2
LOAD_RENDER = 4
LOAD_NO_BITMAP = 8
LOAD_VERTICAL_LAYOUT = 16
LOAD_FORCE_AUTOHINT = 32
LOAD_CROP_BITMAP = 64
LOAD_PEDANTIC = 128
LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH = 512
LOAD_NO_RECURSE = 1024
LOAD_IGNORE_TRANSFORM = 2048
LOAD_MONOCHROME = 4096
LOAD_LINEAR_DESIGN = 8192
LOAD_NO_AUTOHINT = 32768


class Bitmap_Size(ctypes.Structure):
    """Models the metrics of a bitmap strike in a bitmap font."""
    _fields_ = [
        ('height', fttypes.Short),
        ('width', fttypes.Short),
        ('size', ftimage.Pos),
        ('x_ppem', ftimage.Pos),
        ('y_ppem', ftimage.Pos)
    ]


class Glyph_Metrics(ctypes.Structure):
    """Models the metrics of a single glyph."""
    _fields_ = [
        ('width', ftimage.Pos),
        ('height', ftimage.Pos),
        ('horiBearingX', ftimage.Pos),
        ('horiBearingY', ftimage.Pos),
        ('horiAdvance', ftimage.Pos),
        ('vertBearingX', ftimage.Pos),
        ('vertBearingY', ftimage.Pos),
        ('vertAdvance', ftimage.Pos)
    ]


class SizeMetricsRec(ctypes.Structure):
    """Models the metrics of a Size object."""
    _fields_ = [
        ('x_ppem', fttypes.UShort),
        ('y_ppem', fttypes.UShort),
        ('x_scale', fttypes.Fixed),
        ('y_scale', fttypes.Fixed),
        ('ascender', ftimage.Pos),
        ('descender', ftimage.Pos),
        ('height', ftimage.Pos),
        ('max_advance', ftimage.Pos)
    ]
SizeMetrics = ctypes.POINTER(SizeMetricsRec)


class CharMapRec(ctypes.Structure):
    """
    Translates character codes in a given encoding into glyph indices for its
    parent's face.

    """
    pass
CharMap = ctypes.POINTER(CharMapRec)


class DriverRec(ctypes.Structure):
    """A special module capable of creating faces from font files."""
    pass
Driver = ctypes.POINTER(DriverRec)


class LibraryRec(ctypes.Structure):
    """Parent of all other objects in FreeType."""
    pass
Library = ctypes.POINTER(LibraryRec)

class SubGlyphRec(ctypes.Structure):
    """Internal object used to describe subglyphs."""
    pass


class SlotInternalRec(ctypes.Structure):
    """Models private data of a given GlyphSlot object."""
    pass


class GlyphSlotRec(ctypes.Structure):
    """
    A container where glyph images are loaded independently of the glyph image
    format.

    """
    pass
GlyphSlot = ctypes.POINTER(GlyphSlotRec)


class SizeInternalRec(ctypes.Structure):
    """Models private data of a given Size object."""
    pass
SizeInternal = ctypes.POINTER(SizeInternalRec)

class SizeRec(ctypes.Structure):
    """Models a face scaled to a given character size."""
    pass
Size = ctypes.POINTER(SizeRec)


class FaceInternalRec(ctypes.Structure):
    """Models private data of a given Face object."""
    pass

class FaceRec(ctypes.Structure):
    """Models a given typeface in a given style."""
    _fields_ = [
        ('num_faces', fttypes.Long),
        ('face_index', fttypes.Long),
        ('face_flags', fttypes.Long),
        ('style_flags', fttypes.Long),
        ('num_glyphs', fttypes.Long),
        ('family_name', ctypes.c_char_p),
        ('style_name', ctypes.c_char_p),
        ('num_fixed_sizes', fttypes.Int),
        ('available_sizes', ctypes.POINTER(Bitmap_Size)),
        ('num_charmaps', fttypes.Int),
        ('charmaps', ctypes.POINTER(CharMap)),
        ('generic', fttypes.Generic),
        ('bbox', ftimage.BBox),
        ('units_per_EM', fttypes.UShort),
        ('ascender', fttypes.Short),
        ('descender', fttypes.Short),
        ('height', fttypes.Short),
        ('max_advance_width', fttypes.Short),
        ('max_advance_height', fttypes.Short),
        ('underline_position', fttypes.Short),
        ('underline_thickness', fttypes.Short),
        ('glyph', GlyphSlot),
        ('size', Size),
        ('charmap', CharMap),
        ('driver', Driver),
        ('memory', ctypes.POINTER(ftsystem.MemoryRec)),
        ('stream', ctypes.POINTER(ftsystem.StreamRec)),
        ('sizes_list', ctypes.POINTER(fttypes.ListRec)),
        ('autohint', fttypes.Generic),
        ('extensions', ctypes.c_void_p),
        ('internal', ctypes.POINTER(FaceInternalRec))
    ]
Face = ctypes.POINTER(FaceRec)

CharMapRec._fields_ = [
    ('face', ctypes.POINTER(FaceRec)),
    ('encoding', Encoding),
    ('platform_id', fttypes.UShort),
    ('encoding_id', fttypes.UShort)
]


GlyphSlotRec._fields_ = [
    ('library', ctypes.POINTER(LibraryRec)),
    ('face', ctypes.POINTER(FaceRec)),
    ('next', ctypes.POINTER(GlyphSlotRec)),
    ('reserved', fttypes.UInt),
    ('generic', fttypes.Generic),
    ('metrics', Glyph_Metrics),
    ('linearHoriAdvance', fttypes.Fixed),
    ('linearVertAdvance', fttypes.Fixed),
    ('advance', ftimage.Vector),
    ('format', ftimage.GlyphFormat),
    ('bitmap', ftimage.Bitmap),
    ('bitmap_left', fttypes.Int),
    ('bitmap_top', fttypes.Int),
    ('outline', ftimage.Outline),
    ('num_subglyphs', fttypes.UInt),
    ('subglyphs', ctypes.POINTER(SubGlyphRec)),
    ('control_data', ctypes.c_void_p),
    ('control_len', ctypes.c_long),
    ('lsb_delta', ftimage.Pos),
    ('rsb_delta', ftimage.Pos),
    ('internal', ctypes.POINTER(SlotInternalRec))
]


SizeRec._fields_ = [
    ('face', Face),
    ('generic', fttypes.Generic),
    ('metrics', SizeMetricsRec),
    ('internal', SizeInternal)
]


class ModuleRec(ctypes.Structure):
    """Provides services in FreeType."""
    pass

# Ports of Macro for testing font flags.  
def _ffunc(face):
    """ Helper that allows the ports of the macros to accept either
        a FaceRec or a pointer to a FaceRec
    """
    if isinstance(face,Face):
        face = face.contents
    return face
def HAS_HORIZONTAL(face):
    """
       Returns true whenever a face object contains
       horizontal metrics (this is true for all font formats though).
    """
    return ( _ffunc(face).face_flags & FACE_FLAG_HORIZONTAL) != 0
def HAS_VERTICAL(face):
    """
        Returns true whenever a face object contains vertical
        metrics.
    """
    return (_ffunc(face).face_flags & FACE_FLAG_VERTICAL) != 0
def HAS_KERNING(face):
    """
        Returns true whenever a face object contains kerning
        data that can be accessed with @FT_Get_Kerning.
    """
    return (_ffunc(face).face_flags & FACE_FLAG_KERNING) != 0
def IS_SCALABLE(face):
    """
        Returns true whenever a face object contains a scalable
        font face (true for TrueType, Type~1, Type~42, CID, OpenType/CFF,
        and PFR font formats.
    """
    return (_ffunc(face).face_flags & FACE_FLAG_SCALABLE) != 0
def IS_SFNT(face):
    """
        Returns true whenever a face object contains a font
        whose format is based on the SFNT storage scheme.  This usually
        means: TrueType fonts, OpenType fonts, as well as SFNT-based embedded
        bitmap fonts.
   
        If this macro is true, all functions defined in @FT_SFNT_NAMES_H and
        @FT_TRUETYPE_TABLES_H are available.
    """
    return (_ffunc(face).face_flags & FACE_FLAG_SFNT) != 0
def IS_FIXED_WIDTH(face):
    """
        Returns true whenever a face object contains a font face
        that contains fixed-width (or `monospace', `fixed-pitch', etc.)
        glyphs.
    """
    return (_ffunc(face).face_flags & FACE_FLAG_FIXED_WIDTH) != 0
def HAS_FIXED_SIZES(face):
    """
        Returns true whenever a face object contains some
        embedded bitmaps.  See the `available_sizes' field of the
    """
    return (_ffunc(face).face_flags & FACE_FLAG_FIXED_SIZES) != 0
def HAS_FAST_GLYPHS(face):
    """
        Deprecated.
    """
    return False
def HAS_GLYPH_NAMES(face):
    """
        Returns true whenever a face object contains some glyph
        names that can be accessed through @FT_Get_Glyph_Name.
    """
    return (_ffunc(face).face_flags & FACE_FLAG_GLYPH_NAMES) != 0
def HAS_MULTIPLE_MASTERS(face):
    """
        Returns true whenever a face object contains some
        multiple masters.  The functions provided by @FT_MULTIPLE_MASTERS_H
        are then available to choose the exact design you want.
    """
    return (_ffunc(face).face_flags & FACE_FLAG_MULTIPLE_MASTERS) != 0
def IS_CID_KEYED(face):
    """
        Returns true whenever a face object contains a CID-keyed
        font.  See the discussion of @FACE_FLAG_CID_KEYED for more
        details.
    """
    return (_ffunc(face).face_flags & FACE_FLAG_CID_KEYED) != 0
def IS_TRICKY(face):
    """
        Returns true whenever a face represents a `tricky' font.
        See the discussion of @FACE_FLAG_TRICKY for more details.
    """
    return (_ffunc(face).face_flags & FACE_FLAG_TRICKY) != 0


Init_FreeType = libfreetype.FT_Init_FreeType
Init_FreeType.restype = fttypes.Error
Init_FreeType.argtypes = [ctypes.POINTER(Library)]

Done_FreeType = libfreetype.FT_Done_FreeType
Done_FreeType.restype = fttypes.Error
Done_FreeType.argtypes = [ctypes.POINTER(LibraryRec)]

New_Face = libfreetype.FT_New_Face
New_Face.restype = fttypes.Error
New_Face.argtypes = [ctypes.POINTER(LibraryRec), ctypes.c_char_p, fttypes.Long,
                     ctypes.POINTER(ctypes.POINTER(FaceRec))]

Done_Face = libfreetype.FT_Done_Face
Done_Face.restype = fttypes.Error
Done_Face.argtypes = [ctypes.POINTER(FaceRec)]

Set_Char_Size = libfreetype.FT_Set_Char_Size
Set_Char_Size.restype = fttypes.Error
Set_Char_Size.argtypes = [ctypes.POINTER(FaceRec), fttypes.F26Dot6,
                          fttypes.F26Dot6, fttypes.UInt, fttypes.UInt]

Set_Pixel_Sizes = libfreetype.FT_Set_Pixel_Sizes
Set_Pixel_Sizes.restype = fttypes.Error
Set_Pixel_Sizes.argtypes = [Face, fttypes.UInt, fttypes.UInt ]

Load_Char = libfreetype.FT_Load_Char
Load_Char.restype = fttypes.Error
Load_Char.argtypes = [Face, fttypes.ULong, fttypes.Int32]

Set_Transform = libfreetype.FT_Set_Transform
Set_Transform.restype = None
Set_Transform.argtypes = [Face, ctypes.POINTER(fttypes.Matrix), ctypes.POINTER(ftimage.Vector) ]

Load_Glyph = libfreetype.FT_Load_Glyph
Load_Glyph.restype = fttypes.Error
Load_Glyph.argtypes = [ctypes.POINTER(FaceRec), fttypes.UInt, fttypes.Int32]

Render_Glyph = libfreetype.FT_Render_Glyph
Render_Glyph.restype = fttypes.Error
Render_Glyph.argtypes = [GlyphSlot, RenderMode]

Get_Char_Index = libfreetype.FT_Get_Char_Index
Get_Char_Index.restype = fttypes.UInt
Get_Char_Index.argtypes = [Face, fttypes.ULong]

Get_Kerning = libfreetype.FT_Get_Kerning
Get_Kerning.restype = fttypes.Error
Get_Kerning.argtypes = [Face, fttypes.UInt, fttypes.UInt,
                        fttypes.UInt, ctypes.POINTER(ftimage.Vector)]

Library_Version = libfreetype.FT_Library_Version
Library_Version.restype = None
Library_Version.argtypes = [ctypes.POINTER(LibraryRec),
                            ctypes.POINTER(fttypes.Int),
                            ctypes.POINTER(fttypes.Int),
                            ctypes.POINTER(fttypes.Int)]

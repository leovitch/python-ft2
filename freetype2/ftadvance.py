

"""
    ftadvance.py
    Quick retrieval of advance values
    Interface to ftadvanc.h
"""


import ctypes
import fttypes

from freetype2 import libfreetype, freetype

ADVANCE_FLAG_FAST_ONLY = 0x20000000

Get_Advance = libfreetype.FT_Get_Advance
Get_Advance.restype = fttypes.Error
Get_Advance.argtypes = [freetype.Face, 
                        fttypes.UInt,               # glyph index
                        fttypes.Int32,              # load_flags
                        ctypes.POINTER(fttypes.Fixed) # pointer to result
                        ]

Get_Advances = libfreetype.FT_Get_Advances
Get_Advances.restype = fttypes.Error
Get_Advances.argtypes = [freetype.Face, 
                         fttypes.UInt,                  # first glyph index
                         fttypes.UInt,                  # count of glyph indices to retrieve
                         fttypes.Int32,                  # load flags
                         ctypes.POINTER(fttypes.Fixed)  # Pointer to result array, must contain count elements
                        ]





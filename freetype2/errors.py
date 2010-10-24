

""" This module will contain definitions for each error symbol
    listed below which will be equal to the integer value
    of the error message.
    
    You can directly compare errors code to those objects.
    
    To look up an error by code, use the Errors_by_code dictionary.
    
    Example usage:
    
        import freetype2 as FT
        
        error = FT.Some_Routine(library,*args)
        if error != FT.Ok:
            if error != FT.errors.Too_Many_Hints:
                print "They were at it again"
            else:
                print "Encountered freetype2 error %s"%FT.Errors_by_code[error]
"""



# generic errors

Errors_by_code = { }

class ERRORDEF_(int):
    def __new__(cls,name,code,msg):
        global Errors_by_code
    
        self = int.__new__(cls,code)
        self.name = name
        globals()[name] = self
        Errors_by_code[code] = self
        self.msg = msg
        return self
    def __str__(self):
        return self.msg

ERRORDEF_( 'Ok',                                        0x00, \
                  "no error" )

ERRORDEF_( 'Cannot_Open_Resource',                      0x01, \
                "cannot open resource" )
ERRORDEF_( 'Unknown_File_Format',                       0x02, \
                "unknown file format" )
ERRORDEF_( 'Invalid_File_Format',                       0x03, \
                "broken file" )
ERRORDEF_( 'Invalid_Version',                           0x04, \
                "invalid FreeType version" )
ERRORDEF_( 'Lower_Module_Version',                      0x05, \
                "module version is too low" )
ERRORDEF_( 'Invalid_Argument',                          0x06, \
                "invalid argument" )
ERRORDEF_( 'Unimplemented_Feature',                     0x07, \
                "unimplemented feature" )
ERRORDEF_( 'Invalid_Table',                             0x08, \
                "broken table" )
ERRORDEF_( 'Invalid_Offset',                            0x09, \
                "broken offset within table" )
ERRORDEF_( 'Array_Too_Large',                           0x0A, \
                "array allocation size too large" )

# glyph/character errors

ERRORDEF_( 'Invalid_Glyph_Index',                       0x10, \
                "invalid glyph index" )
ERRORDEF_( 'Invalid_Character_Code',                    0x11, \
                "invalid character code" )
ERRORDEF_( 'Invalid_Glyph_Format',                      0x12, \
                "unsupported glyph image format" )
ERRORDEF_( 'Cannot_Render_Glyph',                       0x13, \
                "cannot render this glyph format" )
ERRORDEF_( 'Invalid_Outline',                           0x14, \
                "invalid outline" )
ERRORDEF_( 'Invalid_Composite',                         0x15, \
                "invalid composite glyph" )
ERRORDEF_( 'Too_Many_Hints',                            0x16, \
                "too many hints" )
ERRORDEF_( 'Invalid_Pixel_Size',                        0x17, \
                "invalid pixel size" )

# handle errors

ERRORDEF_( 'Invalid_Handle',                            0x20, \
                "invalid object handle" )
ERRORDEF_( 'Invalid_Library_Handle',                    0x21, \
                "invalid library handle" )
ERRORDEF_( 'Invalid_Driver_Handle',                     0x22, \
                "invalid module handle" )
ERRORDEF_( 'Invalid_Face_Handle',                       0x23, \
                "invalid face handle" )
ERRORDEF_( 'Invalid_Size_Handle',                       0x24, \
                "invalid size handle" )
ERRORDEF_( 'Invalid_Slot_Handle',                       0x25, \
                "invalid glyph slot handle" )
ERRORDEF_( 'Invalid_CharMap_Handle',                    0x26, \
                "invalid charmap handle" )
ERRORDEF_( 'Invalid_Cache_Handle',                      0x27, \
                "invalid cache manager handle" )
ERRORDEF_( 'Invalid_Stream_Handle',                     0x28, \
                "invalid stream handle" )

# driver errors

ERRORDEF_( 'Too_Many_Drivers',                          0x30, \
                "too many modules" )
ERRORDEF_( 'Too_Many_Extensions',                       0x31, \
                "too many extensions" )

# memory errors

ERRORDEF_( 'Out_Of_Memory',                             0x40, \
                "out of memory" )
ERRORDEF_( 'Unlisted_Object',                           0x41, \
                "unlisted object" )

# stream errors

ERRORDEF_( 'Cannot_Open_Stream',                        0x51, \
                "cannot open stream" )
ERRORDEF_( 'Invalid_Stream_Seek',                       0x52, \
                "invalid stream seek" )
ERRORDEF_( 'Invalid_Stream_Skip',                       0x53, \
                "invalid stream skip" )
ERRORDEF_( 'Invalid_Stream_Read',                       0x54, \
                "invalid stream read" )
ERRORDEF_( 'Invalid_Stream_Operation',                  0x55, \
                "invalid stream operation" )
ERRORDEF_( 'Invalid_Frame_Operation',                   0x56, \
                "invalid frame operation" )
ERRORDEF_( 'Nested_Frame_Access',                       0x57, \
                "nested frame access" )
ERRORDEF_( 'Invalid_Frame_Read',                        0x58, \
                "invalid frame read" )

# raster errors

ERRORDEF_( 'Raster_Uninitialized',                      0x60, \
                "raster uninitialized" )
ERRORDEF_( 'Raster_Corrupted',                          0x61, \
                "raster corrupted" )
ERRORDEF_( 'Raster_Overflow',                           0x62, \
                "raster overflow" )
ERRORDEF_( 'Raster_Negative_Height',                    0x63, \
                "negative height while rastering" )

# cache errors

ERRORDEF_( 'Too_Many_Caches',                           0x70, \
                "too many registered caches" )

# TrueType and SFNT errors

ERRORDEF_( 'Invalid_Opcode',                            0x80, \
                "invalid opcode" )
ERRORDEF_( 'Too_Few_Arguments',                         0x81, \
                "too few arguments" )
ERRORDEF_( 'Stack_Overflow',                            0x82, \
                "stack overflow" )
ERRORDEF_( 'Code_Overflow',                             0x83, \
                "code overflow" )
ERRORDEF_( 'Bad_Argument',                              0x84, \
                "bad argument" )
ERRORDEF_( 'Divide_By_Zero',                            0x85, \
                "division by zero" )
ERRORDEF_( 'Invalid_Reference',                         0x86, \
                "invalid reference" )
ERRORDEF_( 'Debug_OpCode',                              0x87, \
                "found debug opcode" )
ERRORDEF_( 'ENDF_In_Exec_Stream',                       0x88, \
                "found ENDF opcode in execution stream" )
ERRORDEF_( 'Nested_DEFS',                               0x89, \
                "nested DEFS" )
ERRORDEF_( 'Invalid_CodeRange',                         0x8A, \
                "invalid code range" )
ERRORDEF_( 'Execution_Too_Long',                        0x8B, \
                "execution context too long" )
ERRORDEF_( 'Too_Many_Function_Defs',                    0x8C, \
                "too many function definitions" )
ERRORDEF_( 'Too_Many_Instruction_Defs',                 0x8D, \
                "too many instruction definitions" )
ERRORDEF_( 'Table_Missing',                             0x8E, \
                "SFNT font table missing" )
ERRORDEF_( 'Horiz_Header_Missing',                      0x8F, \
                "horizontal header (hhea) table missing" )
ERRORDEF_( 'Locations_Missing',                         0x90, \
                "locations (loca) table missing" )
ERRORDEF_( 'Name_Table_Missing',                        0x91, \
                "name table missing" )
ERRORDEF_( 'CMap_Table_Missing',                        0x92, \
                "character map (cmap) table missing" )
ERRORDEF_( 'Hmtx_Table_Missing',                        0x93, \
                "horizontal metrics (hmtx) table missing" )
ERRORDEF_( 'Post_Table_Missing',                        0x94, \
                "PostScript (post) table missing" )
ERRORDEF_( 'Invalid_Horiz_Metrics',                     0x95, \
                "invalid horizontal metrics" )
ERRORDEF_( 'Invalid_CharMap_Format',                    0x96, \
                "invalid character map (cmap) format" )
ERRORDEF_( 'Invalid_PPem',                              0x97, \
                "invalid ppem value" )
ERRORDEF_( 'Invalid_Vert_Metrics',                      0x98, \
                "invalid vertical metrics" )
ERRORDEF_( 'Could_Not_Find_Context',                    0x99, \
                "could not find context" )
ERRORDEF_( 'Invalid_Post_Table_Format',                 0x9A, \
                "invalid PostScript (post) table format" )
ERRORDEF_( 'Invalid_Post_Table',                        0x9B, \
                "invalid PostScript (post) table" )

# CFF, CID, and Type 1 errors

ERRORDEF_( 'Syntax_Error',                              0xA0, \
                "opcode syntax error" )
ERRORDEF_( 'Stack_Underflow',                           0xA1, \
                "argument stack underflow" )
ERRORDEF_( 'Ignore',                                    0xA2, \
                "ignore" )
ERRORDEF_( 'No_Unicode_Glyph_Name',                     0xA3, \
                "no Unicode glyph name found" )


# BDF errors

ERRORDEF_( 'Missing_Startfont_Field',                   0xB0, \
                "`STARTFONT' field missing" )
ERRORDEF_( 'Missing_Font_Field',                        0xB1, \
                "`FONT' field missing" )
ERRORDEF_( 'Missing_Size_Field',                        0xB2, \
                "`SIZE' field missing" )
ERRORDEF_( 'Missing_Fontboundingbox_Field',             0xB3, \
                "`FONTBOUNDINGBOX' field missing" )
ERRORDEF_( 'Missing_Chars_Field',                       0xB4, \
                "`CHARS' field missing" )
ERRORDEF_( 'Missing_Startchar_Field',                   0xB5, \
                "`STARTCHAR' field missing" )
ERRORDEF_( 'Missing_Encoding_Field',                    0xB6, \
                "`ENCODING' field missing" )
ERRORDEF_( 'Missing_Bbx_Field',                         0xB7, \
                "`BBX' field missing" )
ERRORDEF_( 'Bbx_Too_Big',                               0xB8, \
                "`BBX' too big" )
ERRORDEF_( 'Corrupted_Font_Header',                     0xB9, \
                "Font header corrupted or missing fields" )
ERRORDEF_( 'Corrupted_Font_Glyphs',                     0xBA, \
                "Font glyphs corrupted or missing fields" )



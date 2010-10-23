#! encoding: utf-8

import sys, os, os.path
import ctypes
import unittest
import math
import logging
import types
import tempfile
from PIL import Image

import freetype2 as FT

class TestCaseResponsibility(Exception):
    pass

class TestCaseHarness(unittest.TestCase):
    def test_id(self):
        """ Strip off the __main__ part at the beginning """
        return '.'.join(self.id().split('.')[1:])
    
    def get_font_path(self):
        raise TestCaseResponsibility()

    def setUp(self):
        log = logging.getLogger(self.test_id())
        log.debug("setUp")
        # Silly unittest calls setUp even though we have no test* methods
        if self.__class__ == TestCaseHarness: return
        self.library = FT.Library()
        error = FT.Init_FreeType(ctypes.byref(self.library))
        self.assertEqual(error,0)
        self.assert_(os.path.exists(self.get_font_path()))
        self.facep = FT.Face()
        error = FT.New_Face(self.library,self.get_font_path(),0,ctypes.byref(self.facep))
        self.assertEqual(error,0)
        self.face = self.facep.contents
        
    def tearDown(self):
        log = logging.getLogger(self.test_id())
        log.debug("tearDown")
        if self.__class__ == TestCaseHarness: return
        error = FT.Done_Face(self.facep)
        self.assertEqual(error,0)
        error = FT.Done_FreeType(self.library)
        self.assertEqual(error,0)

    def image_from_bitmap(self,bitmap):
        """ Returns a '1' or 'L' mode PIL image from the given FT.Bitmap
        """
        self.assert_(bitmap.pixel_mode in [FT.PIXEL_MODE_MONO,FT.PIXEL_MODE_GRAY])
        out_mode = 'L' if bitmap.pixel_mode == FT.PIXEL_MODE_GRAY else '1'
        # Create a string buffer of the Bitmap's size (with memory owned by Python)
        string_buffer = ctypes.create_string_buffer(bitmap.pitch*bitmap.rows)
        # Copy the data over
        ctypes.memmove(string_buffer,bitmap.buffer,bitmap.pitch*bitmap.rows)
        # Now make an image in the normal PIL way
        return Image.fromstring(out_mode,(bitmap.width,bitmap.rows), 
            string_buffer, "raw", out_mode, 0, 1)
    
    def find_glyph_format(self,glyph_format):
        """ Returns the programmer-readable constant for the glyph_format.
        """
        for possible_format in ['GLYPH_FORMAT_NONE','GLYPH_FORMAT_COMPOSITE',
                                'GLYPH_FORMAT_BITMAP','GLYPH_FORMAT_OUTLINE',
                                'GLYPH_FORMAT_PLOTTER']:
            if getattr(FT,possible_format) == glyph_format:
                return possible_format
        return None
    
    def find_pixel_mode(self,pixelMode):
        for possible_mode in ['PIXEL_MODE_NONE','PIXEL_MODE_MONO',
                              'PIXEL_MODE_GRAY','PIXEL_MODE_GRAY2',
                              'PIXEL_MODE_GRAY4','PIXEL_MODE_LCD',
                              'PIXEL_MODE_LCD_V']:
            if getattr(FT,possible_mode) == pixelMode:
                return possible_mode
        return None
    def render_simple(self,log,text,disallow_bitmaps,output_name):
        """ Step 1 7.a. Simple Text Rendering
        
            This is a direct port of the code in 7.a. of
            Step 1 of the freetype tutorial.
        """
        log = logging.getLogger(self.test_id())
        log.debug("Entry")

        error = FT.Set_Pixel_Sizes(self.facep,0,16)
        self.assertEqual(error,0)
        
        dest = Image.new('L',(200,60))
        pen_x, pen_y = 0, 50
        
        for n in xrange(len(text)):
            # This log statement is important if fonts are missing a glyph
            log.debug("Getting character %s",text[n])
            glyph_index = FT.Get_Char_Index(self.facep,ord(text[n]))
            self.assertNotEqual(glyph_index,0)

            # By using LOAD_NO_BITMAP, we unsure that this test suite 
            # only has to handle outline forms that can be rendered to
            # 8bpp Bitmaps.  If you use the more common LOAD_DEFAULT,
            # you may or may not get an embedded 1bpp bitmap depending
            # on the font.
            error = FT.Load_Glyph(self.facep,glyph_index,
               FT.LOAD_NO_BITMAP if disallow_bitmaps else FT.LOAD_DEFAULT)
            self.assertEqual(error,0)

            error = FT.Render_Glyph(self.face.glyph,FT.RENDER_MODE_NORMAL)
            self.assertEqual(error,0)

            glyph = self.face.glyph.contents
            color_image = Image.new('L',(glyph.bitmap.width,glyph.bitmap.rows),255)
            glyph_image = self.image_from_bitmap(glyph.bitmap)

            log.debug("Drawing character %s at pen loc (%d,%d) offset by "
                "bitmap origin (%d,%d)",text[n],pen_x,pen_y,
                glyph.bitmap_left,glyph.bitmap_top)
            dest.paste(color_image,(pen_x+glyph.bitmap_left,pen_y-glyph.bitmap_top),glyph_image) # glyph==mask

            pen_x += FT.IFromF26Dot6(glyph.advance.x)
            pen_y += FT.IFromF26Dot6(glyph.advance.y)

        output_path = self.get_output_path(output_name)
        dest.save(output_path)
        log.info(" Image saved to %s",output_path)

    def render_refined(self,log,text,disallow_bitmaps,output_name):
        """ Step 1 7.b. Refined Text Test
        
            This is a direct port of the b. Refined Code example in
            Step 1 of the freetype tutorial.
        """
        error = FT.Set_Pixel_Sizes(self.facep,0,16)
        self.assertEqual(error,0)
        
        dest = Image.new('L',(200,60))
        pen_x, pen_y = 0, 50
        
        for n in xrange(len(text)):
            error = FT.Load_Char( self.facep,ord(text[n]), 
               FT.LOAD_RENDER|(FT.LOAD_NO_BITMAP if disallow_bitmaps else 0) )
            self.assertEqual(error,0)
            
            glyph = self.face.glyph.contents
            color_image = Image.new('L',(glyph.bitmap.width,glyph.bitmap.rows),255)
            glyph_image = self.image_from_bitmap(glyph.bitmap)

            log.debug("Drawing character %s at pen loc (%d,%d) offset by "
                "bitmap origin (%d,%d)",text[n],pen_x,pen_y,
                glyph.bitmap_left,glyph.bitmap_top)
            dest.paste(color_image,(pen_x+glyph.bitmap_left,pen_y-glyph.bitmap_top),glyph_image) # glyph==mask

            pen_x += FT.IFromF26Dot6(glyph.advance.x)
            pen_y += FT.IFromF26Dot6(glyph.advance.y)
            
        output_path = self.get_output_path(output_name)
        dest.save(output_path)
        log.info(" Image saved to %s",output_path)

    def render_transformed(self,log,text,output_name):
        """ Step 1 7.c. Transformed Text Test
        
            This code is a direct port of the freetype tutorial where 
            the transformation math is incorporated into the pen values 
            passed to Set_Transform.
        """
        my_target_height = 50
        output_width, output_height = 200, 60
        angle = math.radians(10.0)
        
        error = FT.Set_Pixel_Sizes(self.facep,0,16)
        self.assertEqual(error,0)
        
        dest = Image.new('L',(output_width, output_height))
        
        # This time the pen calculations are in F26.6
        pen = FT.Vector( FT.ToF26Dot6(0),
                         FT.ToF26Dot6(my_target_height-output_height))
        
        matrix = FT.Matrix(  FT.ToFixed(math.cos(angle)),
                             FT.ToFixed(-math.sin(angle)),
                             FT.ToFixed(math.sin(angle)),
                             FT.ToFixed(math.cos(angle)) )
        log.debug("Set matrix to %f %f / %f %f",FT.FromFixed(matrix.xx),
            FT.FromFixed(matrix.xy),FT.FromFixed(matrix.yx),FT.FromFixed(matrix.yy))
        
        for n in xrange(len(text)):
            FT.Set_Transform( self.face, 
                               ctypes.byref(matrix), 
                               ctypes.byref(pen) )
            log.debug("Set transform to rot(%f) + (%f,%f)",math.degrees(angle),
                FT.FromF26Dot6(pen.x),FT.FromF26Dot6(pen.y))
            error = FT.Load_Char( self.facep, 
                                   ord(text[n]), 
                                   FT.LOAD_RENDER|FT.LOAD_NO_BITMAP )
            self.assertEqual(error,0)
            
            glyph = self.face.glyph.contents
            color_image = Image.new('L',(glyph.bitmap.width,glyph.bitmap.rows),255)
            glyph_image = self.image_from_bitmap(glyph.bitmap)
            log.debug("Drawing character %s at (%d,%d)",text[n],
                glyph.bitmap_left,my_target_height-glyph.bitmap_top)
            
            dest.paste(color_image,
                       (glyph.bitmap_left,my_target_height-glyph.bitmap_top),
                       glyph_image) # glyph==mask
            log.debug("Pen advance is (%f,%f)",
                FT.FromF26Dot6(glyph.advance.x),FT.FromF26Dot6(glyph.advance.y))
            
            pen.x += glyph.advance.x
            pen.y += glyph.advance.y
        output_path = self.get_output_path(output_name)
        dest.save(output_path)
        log.info(" Image saved to %s",output_path)

class Step1Kanji(TestCaseHarness):
    def get_font_path(self):
        return r"/Library/Fonts/Osaka.ttf"
    def get_output_path(self,test_name):
        return os.path.join(tempfile.gettempdir(),"ft2_part1k_%s.png"%test_name)

    def test_face(self):
        log = logging.getLogger(self.test_id())
        log.debug("Entry")

        log.debug("face.num_glyphs is %d",self.face.num_glyphs)
        for face_flag in [ 'FACE_FLAG_SCALABLE','FACE_FLAG_FIXED_SIZES',
            'FACE_FLAG_FIXED_WIDTH','FACE_FLAG_SFNT','FACE_FLAG_HORIZONTAL',
            'FACE_FLAG_VERTICAL','FACE_FLAG_KERNING','FACE_FLAG_FAST_GLYPHS',
            'FACE_FLAG_MULTIPLE_MASTERS','FACE_FLAG_GLYPH_NAMES',
            'FACE_FLAG_EXTERNAL_STREAM','FACE_FLAG_HINTER',
            'FACE_FLAG_CID_KEYED','FACE_FLAG_TRICKY']:
            log.debug("face.face_flags[%s] is %r",face_flag,
                bool(self.face.face_flags & getattr(FT,face_flag)))
        log.debug("face.family_name,style_name is %s, %s",
                self.face.family_name,self.face.style_name)
        log.debug("face.num_charmaps is %d",self.face.num_charmaps)
        log.debug("face.num_fixed_sizes is %d",self.face.num_fixed_sizes)
        for i in xrange(self.face.num_fixed_sizes):
            bs = self.face.available_sizes[i]
            log.debug("Embedded strike #%d is size %f (%d,%d)",i,
                      FT.FromF26Dot6(bs.size),bs.width,bs.height)
        
        error = FT.Set_Char_Size(
            self.facep,   # handle to face object
            0,       # char_width
            FT.ToF26Dot6(16),   # char_height
            64,     # horizontal device resolution
            64 )    # vertical device resolution
        self.assertEqual(error,0)
        
        error = FT.Set_Pixel_Sizes(
            self.facep,  # handle to face object
            0,      # pixel_width
            16 )    # pixel_height
        self.assertEqual(error,0)
        
        glyph_index = FT.Get_Char_Index( self.facep, ord(unicode('A')) )
        self.assertFalse(glyph_index == 0)
        log.debug("glyph_index of unicode A is %d",glyph_index)
        
        error = FT.Load_Glyph(
            self.facep,         # handle to face object
            glyph_index,   # glyph index
            0 )            # load flags, see below
        self.assertEqual(error,0)
        
        glyphslotp = self.facep.contents.glyph
        glyphslot = glyphslotp.contents
        glyph_format_name = self.find_glyph_format(glyphslot.format)
        if glyph_format_name != None:
            log.debug("Format of glyph is %s",glyph_format_name)
        else:
            log.info("Format of glyph is unknown!!!")
            
        if glyphslot.format != FT.GLYPH_FORMAT_BITMAP:
            error = FT.Render_Glyph(glyphslotp,FT.RENDER_MODE_NORMAL)
            self.assertEqual(error,0)
            self.assertEqual(glyphslot.format,FT.GLYPH_FORMAT_BITMAP)
            log.debug("Glyph converted to bitmap")

        log.debug("Glyph bitmap num_grays is %d",glyphslot.bitmap.num_grays)
        log.debug("Glyph bitmap pixel_mode is %r",
                  self.find_pixel_mode(glyphslot.bitmap.pixel_mode))
        
        for i in xrange(self.face.num_charmaps):
            charmap = self.face.charmaps[i].contents
            for possible_encoding in ['ENCODING_NONE','ENCODING_MS_SYMBOL',
                'ENCODING_UNICODE','ENCODING_SJIS','ENCODING_GB2312',
                'ENCODING_BIG5','ENCODING_WANSUNG','ENCODING_JOHAB',
                'ENCODING_MS_GB2312','ENCODING_MS_BIG5',
                'ENCODING_MS_WANSUNG','ENCODING_MS_JOHAB',
                'ENCODING_ADOBE_STANDARD','ENCODING_ADOBE_EXPERT',
                'ENCODING_ADOBE_CUSTOM','ENCODING_ADOBE_LATIN_1',
                'ENCODING_OLD_LATIN_2','ENCODING_APPLE_ROMAN',]:
                if getattr(FT,possible_encoding) == charmap.encoding:
                    log.debug("Char map #%d is %s (platform %d, encoding %d)",
                        i,possible_encoding,charmap.platform_id,charmap.encoding_id)
                    break
            else:
                log.debug("Char map #%d is unknown encoding %d (platform %d, encoding %d)",
                        i,charmap.encoding,charmap.platform_id,charmap.encoding_id)

        matrix = FT.Matrix(FT.ToFixed(1.0),FT.ToFixed(0.0),FT.ToFixed(0.0),FT.ToFixed(1.0))
        delta = FT.Vector()
        
        FT.Set_Transform(
            self.facep,      # target face object
            ctypes.byref(matrix),    # pointer to 2x2 matrix
            ctypes.byref(delta) )    # pointer to 2d vector
        log.debug("Matrix set")
        
        error = FT.Load_Glyph(
            self.facep,         # handle to face object
            glyph_index,   # glyph index
            0 )            # load flags, see below
        self.assertEqual(error,0)
        log.debug("Glyph reloaded")
        
        FT.Set_Transform(
            self.facep,      # target face object
            None,
            None )
        log.debug("Matrix reset")
        

    def test_render_simple(self):
        """ Runs the simple rendering test with bitmaps off.
        """
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        text = u'心は甚くなりますのでいたく通りに'
        self.render_simple(log,text,True,'simple')

    def test_render_simple_bitmap(self):
        """ Runs the simple rendering test with bitmaps allowed.
        """
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        text = u'心は甚くなりますのでいたく通りに'
        self.render_simple(log,text,False,'simple_b')

    def test_render_refined(self):
        """ Runs the simple rendering test with bitmaps off.
        """
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        text = u'心は甚くなりますのでいたく通りに'
        self.render_refined(log,text,True,'refined')

    def test_render_refined_bitmap(self):
        """ Runs the simple rendering test with bitmaps allowed.
        """
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        text = u'心は甚くなりますのでいたく通りに'
        self.render_refined(log,text,False,'refined_b')
        
    def test_render_transformed(self):
        log = logging.getLogger(self.test_id())
        text = unicode(u'心は甚くなりますのでいたく通りに')
        self.render_transformed(log, text, 'transformed')
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Here's how to enable debug logging for one test:
    # logging.getLogger('Step1.test_face').setLevel(logging.DEBUG)
    unittest.main()



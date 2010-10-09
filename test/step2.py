# encoding: utf-8

import sys, os, os.path
import ctypes
import unittest
import math
import logging
import types
import tempfile
from PIL import Image

import freetype2 as FT
from cgi import log

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
        font_path = self.get_font_path()
        self.assert_(os.path.exists(font_path))
        self.facep = FT.Face()
        error = FT.New_Face(self.library,font_path,0,ctypes.byref(self.facep))
        self.assertEqual(error,0)
        self.face = self.facep.contents
        
    def tearDown(self):
        log = logging.getLogger(self.test_id())
        log.debug("tearDown")
        # Silly unittest calls setUp even though we have no test* methods
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
    
    def render_kerned(self,log,text,output_name):
        log.debug("Entry")

        # Nice and big so the kerning actually has an effect
        error = FT.Set_Pixel_Sizes(self.facep,0,48)
        self.assertEqual(error,0)
        
        dest = Image.new('L',(300,80))
        pen_x, pen_y = 0, 60
        delta = FT.Vector()
        
        use_kerning = FT.HAS_KERNING(self.face)
        previous = None
        for n in xrange(len(text)):

            glyph_index = FT.Get_Char_Index(self.facep,ord(text[n]))
            self.assertNotEqual(glyph_index,0)
            
            if use_kerning and previous:
                error = FT.Get_Kerning( self.face, previous, glyph_index,
                      FT.KERNING_DEFAULT, ctypes.byref(delta) )
                self.assertEqual(error,0)
                pen_x += FT.IFromF26Dot6(delta.x)

            error = FT.Load_Glyph(self.facep,glyph_index,FT.LOAD_RENDER)
            self.assertEqual(error,0)

            glyph = self.face.glyph.contents
            # PIL doesn't like drawing spaces
            if glyph.bitmap.width > 0 and glyph.bitmap.rows > 0:
                color_image = Image.new('L',(glyph.bitmap.width,glyph.bitmap.rows),255)
                glyph_image = self.image_from_bitmap(glyph.bitmap)
    
                log.debug("Drawing character %s at pen loc (%d,%d) offset by "
                    "bitmap origin (%d,%d)",text[n],pen_x,pen_y,
                    glyph.bitmap_left,glyph.bitmap_top)
                dest.paste(color_image,
                           (pen_x+glyph.bitmap_left,pen_y-glyph.bitmap_top),
                           glyph_image) # glyph==mask

            pen_x += FT.IFromF26Dot6(glyph.advance.x)
            pen_y += FT.IFromF26Dot6(glyph.advance.y)
            
            previous = glyph_index

        test_output = self.get_output_path(output_name)
        dest.save(test_output)
        log.info(" Image saved to %s",test_output)
        
    def measure_bbox_render(self,log,text,output_name):
        log.debug("Entry")

        def get_glyph_positions(text):
            pen_x, pen_y = 0, 0
            glyph_positions = [ ]
    
            use_kerning = FT.HAS_KERNING(self.face)
            previous = None
            
            # The measuring part
            for char in unicode(text):
                glyph_index = FT.Get_Char_Index(self.facep,ord(char))
                self.assertNotEqual(glyph_index,0)
                
                if use_kerning and previous:
                    delta = FT.Vector()
                    error = FT.Get_Kerning(self.facep,previous,glyph_index,
                                            FT.KERNING_DEFAULT,ctypes.byref(delta))
                    self.assertEqual(error,0)
                    pen_x += FT.IFromF26Dot6(delta.x)
                    
                error = FT.Load_Glyph(self.facep,glyph_index,FT.LOAD_DEFAULT)
                self.assertEqual(error,0)
                
                glyph_p = FT.Glyph()
                error = FT.Get_Glyph(self.face.glyph,ctypes.byref(glyph_p))
                self.assertEqual(error,0)
                
                glyph_positions.append((glyph_p,(pen_x,pen_y)))
                
                pen_x += FT.IFromF26Dot6(self.face.glyph.contents.advance.x)
                
                previous = glyph_index
            
            return glyph_positions
      
            
        def calculate_bbox(glyph_positions):
            bbox = FT.BBox()
            bbox.xMin = bbox.yMin = FT.ToFixed(16000)
            bbox.xMax = bbox.yMax = FT.ToFixed(-16000)
            
            glyph_bbox = FT.BBox()

            for (glyph_p,(pos_x,pos_y)) in glyph_positions:
                
                FT.Glyph_Get_CBox(glyph_p,FT.GLYPH_BBOX_PIXELS,
                                   ctypes.byref(glyph_bbox))
                glyph_bbox.xMin += pos_x
                glyph_bbox.yMin += pos_y
                glyph_bbox.xMax += pos_x
                glyph_bbox.yMax += pos_y
        
                if glyph_bbox.xMin < bbox.xMin:
                    bbox.xMin = glyph_bbox.xMin
                if glyph_bbox.yMin < bbox.yMin:
                    bbox.yMin = glyph_bbox.yMin
                if glyph_bbox.xMax > bbox.xMax:
                    bbox.xMax = glyph_bbox.xMax
                if glyph_bbox.yMax > bbox.yMax:
                    bbox.yMax = glyph_bbox.yMax
        
            if bbox.xMin > bbox.xMax:
                bbox.xMin = bbox.xMax = 0
            if bbox.yMin > bbox.yMax:
                bbox.yMin = bbox.yMax = 0
            
            return bbox

        error = FT.Set_Pixel_Sizes(self.facep,0,48)
        self.assertEqual(error,0)
        
        my_target_width = 300
        my_target_height = 80
        
        dest = Image.new('L',(my_target_width,my_target_height))
        
        glyph_positions = get_glyph_positions(text)
        log.debug("Got glyphs and positions")
        
        bbox = calculate_bbox(glyph_positions)
        log.debug("Calculated bbox is (%d,%d), (%d,%d)",
                  bbox.xMin,bbox.yMin,bbox.xMax,bbox.yMax)
        
        string_width = bbox.xMax - bbox.xMin
        string_height = bbox.yMax - bbox.yMin
        log.debug("String size is (%d,%d)",string_width,string_height)
        
        start_x = FT.ToF26Dot6((my_target_width - string_width)/2)
        start_y = FT.ToF26Dot6((my_target_height - string_height)/2)
        
        pen = FT.Vector()
        
        for (glyph_p,(pos_x,pos_y)) in glyph_positions:
            
            pen.x = start_x + FT.ToF26Dot6(pos_x)
            pen.y = start_y + FT.ToF26Dot6(pos_y)
            log.debug("Pen is at (%f,%f)",FT.FromF26Dot6(pen.x),FT.FromF26Dot6(pen.y))
             
            error = FT.Glyph_To_Bitmap( ctypes.byref(glyph_p),
                        FT.RENDER_MODE_NORMAL,ctypes.byref(pen), 0 )
            self.assertEqual(error,0)
            
            bitmap_glyph_p = ctypes.cast(glyph_p,ctypes.POINTER(FT.BitmapGlyphRec))
            bitmap_glyph = bitmap_glyph_p.contents
        
            if bitmap_glyph.bitmap.width > 0 and bitmap_glyph.bitmap.rows > 0:
                color_image = Image.new('L',(bitmap_glyph.bitmap.width,bitmap_glyph.bitmap.rows),255)
                glyph_image = self.image_from_bitmap(bitmap_glyph.bitmap)
    
                log.debug("Drawing glyph at loc (%d,%d)",
                    bitmap_glyph.left,my_target_height-bitmap_glyph.top)
                dest.paste(color_image,
                           (bitmap_glyph.left,my_target_height-bitmap_glyph.top),
                           glyph_image) # glyph==mask
        
        test_output = self.get_output_path(output_name)
        dest.save(test_output)
        log.info(" Image saved to %s",test_output)

        for (glyph_p,(bee,bah)) in glyph_positions:
            FT.Done_Glyph(glyph_p)

    def measured_transformed_render(self,log,text,output_name):
        log.debug("Entry")

        def get_glyph_info(text):
            """ Returns an array of (glyph_index,(x,y),glyph_p) tuples
            """
            pen = FT.Vector(FT.ToF26Dot6(0),FT.ToF26Dot6(0)) # In F26Dot6 this time
            return_value = [ ]
            use_kerning = FT.HAS_KERNING(self.face)
            previous = None
            
            # The measuring part
            for char in unicode(text):
                glyph_index = FT.Get_Char_Index(self.facep,ord(char))
                self.assertNotEqual(glyph_index,0)
                
                if use_kerning and previous:
                    delta = FT.Vector()
                    error = FT.Get_Kerning(self.facep,previous,glyph_index,
                                            FT.KERNING_DEFAULT,ctypes.byref(delta))
                    self.assertEqual(error,0)
                    log.debug("Applying kerning delta of %f",FT.FromF26Dot6(delta.x))
                    pen.x += delta.x
                    
                error = FT.Load_Glyph(self.facep,glyph_index,FT.LOAD_DEFAULT)
                self.assertEqual(error,0)
                
                glyph_p = FT.Glyph()
                error = FT.Get_Glyph(self.face.glyph,ctypes.byref(glyph_p))
                self.assertEqual(error,0)
                
                log.debug("Before transform, character %s's advance is (%f,%f)",repr(char),
                          FT.FromFixed(glyph_p.contents.advance.x),
                          FT.FromFixed(glyph_p.contents.advance.y))
                
                error = FT.Glyph_Transform(glyph_p,None,ctypes.byref(pen))
                self.assertEqual(error,0)
                
                return_value.append((glyph_index,(pen.x,pen.y),glyph_p))
                
                log.debug("Character %s's advance is (%f,%f)",repr(char),
                          FT.FromFixed(glyph_p.contents.advance.x),
                          FT.FromFixed(glyph_p.contents.advance.y))
                
                pen.x += FT.ToF26Dot6(FT.FromFixed(glyph_p.contents.advance.x))
                
                log.debug("After character %s, pen is (%f,%f)",repr(char),
                          FT.FromF26Dot6(pen.x),FT.FromF26Dot6(pen.y))
                
                previous = glyph_index
            
            return return_value
         
        def calculate_bbox(glyph_info):
            """ Returns bbox in grid-fitted pixel coordinates in 
                F26Dot6 format.
            """
            bbox = FT.BBox()
            bbox.xMin = bbox.yMin = FT.ToFixed(16000)
            bbox.xMax = bbox.yMax = FT.ToFixed(-16000)
            
            glyph_bbox = FT.BBox()

            for (glyph_index,(pos_x,pos_y),glyph_p) in glyph_info:
                
                FT.Glyph_Get_CBox(glyph_p,FT.GLYPH_BBOX_PIXELS,
                                   ctypes.byref(glyph_bbox))
                log.debug("bbox for glyph_index %d is (%f,%f) (%f,%f)",glyph_index,
                          glyph_bbox.xMin,glyph_bbox.yMin,glyph_bbox.xMax,glyph_bbox.yMax)

                if glyph_bbox.xMin < bbox.xMin:
                    bbox.xMin = glyph_bbox.xMin
                if glyph_bbox.yMin < bbox.yMin:
                    bbox.yMin = glyph_bbox.yMin
                if glyph_bbox.xMax > bbox.xMax:
                    bbox.xMax = glyph_bbox.xMax
                if glyph_bbox.yMax > bbox.yMax:
                    bbox.yMax = glyph_bbox.yMax
        
            if bbox.xMin > bbox.xMax:
                bbox.xMin = bbox.xMax = 0
            if bbox.yMin > bbox.yMax:
                bbox.yMin = bbox.yMax = 0
            
            return bbox

        error = FT.Set_Pixel_Sizes(self.facep,0,48)
        self.assertEqual(error,0)
        
        my_target_width = 300
        my_target_height = 80
        angle = math.radians(10.0)
        
        dest = Image.new('L',(my_target_width,my_target_height))
        
        glyph_info = get_glyph_info(text)
        log.debug("Got glyphs and positions")
        
        bbox = calculate_bbox(glyph_info)
        log.debug("Calculated bbox is (%f,%f), (%f,%f)",
                  FT.FromF26Dot6(bbox.xMin),FT.FromF26Dot6(bbox.yMin),
                  FT.FromF26Dot6(bbox.xMax),FT.FromF26Dot6(bbox.yMax))
        
        string_width = bbox.xMax - bbox.xMin
        string_height = bbox.yMax - bbox.yMin
        log.debug("String size is (%d,%d)",string_width,string_height)
        
        start = FT.Vector(
            FT.ToF26Dot6((my_target_width - string_width)/2),
            FT.ToF26Dot6((my_target_height - string_height)/2) 
        )
        
        matrix = FT.Matrix( FT.ToFixed(math.cos(angle)),
                             FT.ToFixed(-math.sin(angle)),
                             FT.ToFixed(math.sin(angle)),
                             FT.ToFixed(math.cos(angle)) )
        log.debug("Set matrix to %f %f / %f %f",FT.FromFixed(matrix.xx),
            FT.FromFixed(matrix.xy),FT.FromFixed(matrix.yx),FT.FromFixed(matrix.yy))

        for (glyph_index,(x,y),glyph_p) in glyph_info:
            
            # This is the variable from the tutorial named "image"
            # ... an unforunate choice of name perhaps.
            image_p = FT.Glyph()
            
            error = FT.Glyph_Copy(glyph_p,ctypes.byref(image_p))
            self.assertEqual(error,0)
            
            error = FT.Glyph_Transform(image_p,ctypes.byref(matrix),ctypes.byref(start))
            self.assertEqual(error,0)
            
            FT.Glyph_Get_CBox(image_p,FT.GLYPH_BBOX_PIXELS,ctypes.byref(bbox))
            
            if bbox.xMax <= 0 or bbox.xMin >= my_target_width or \
                    bbox.yMax <= 0 or bbox.yMin >= my_target_height:
                log.debug("Skipping output of glyph; outside bbox")
                # The tutorial code has a memory leak here -- I chose 
                # to insert the required Done_Glyph call even though it's
                # not in the tutorial
                FT.Done_Glyph(image_p)
                continue
            
            error = FT.Glyph_To_Bitmap( ctypes.byref(image_p),
                        FT.RENDER_MODE_NORMAL,None, 1 )
            self.assertEqual(error,0)
            
            bitmap_glyph_p = ctypes.cast(image_p,ctypes.POINTER(FT.BitmapGlyphRec))
            bitmap_glyph = bitmap_glyph_p.contents
        
            if bitmap_glyph.bitmap.width > 0 and bitmap_glyph.bitmap.rows > 0:
                color_image = Image.new('L',(bitmap_glyph.bitmap.width,bitmap_glyph.bitmap.rows),255)
                glyph_image = self.image_from_bitmap(bitmap_glyph.bitmap)
    
                log.debug("Drawing glyph at loc (%d,%d)",
                    bitmap_glyph.left,my_target_height-bitmap_glyph.top)
                dest.paste(color_image,
                           (bitmap_glyph.left,my_target_height-bitmap_glyph.top),
                           glyph_image) # glyph==mask
            
            FT.Done_Glyph(image_p)
        
        test_output = self.get_output_path(output_name)
        dest.save(test_output)
        log.info(" Image saved to %s",test_output)

        for (glyph_index,(bee,bah),glyph_p) in glyph_info:
            FT.Done_Glyph(glyph_p)


class Step2(TestCaseHarness):
    def get_font_path(self):
        return r"Vera.ttf"
    def get_output_path(self,test_name):
        return os.path.join(tempfile.gettempdir(),"ft2_part2_%s.png"%test_name)

    def test_glyph(self):
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        
        error = FT.Set_Pixel_Sizes(self.facep,0,16)
        self.assertEqual(error,0)
        
        glyph_index = FT.Get_Char_Index( self.facep, ord(unicode('W')) )
        self.assertFalse(glyph_index == 0)
        log.debug("glyph_index of unicode W is %d",glyph_index)
        
        error = FT.Load_Glyph(self.facep,glyph_index,FT.LOAD_DEFAULT)
        # By the way, the constant above is mistakenly listed as 
        # FT_LOAD_NORMAL in the online tutorial
        self.assertEqual(error,0)
        
        glyph_p = FT.Glyph()
        error = FT.Get_Glyph( self.face.glyph, ctypes.byref(glyph_p) )
        self.assertEqual(error,0)
        
        glyph = glyph_p.contents
        log.debug("glyph %r is format %s",glyph,self.find_glyph_format(glyph.format))
        
        FT.Done_Glyph(glyph_p)
        # We do del's of the variables here just to emphasize the importance
        # of not having a lingering reference to the glyph after we've released
        # it
        del glyph_p

    def test_glyph_copy_and_transform(self):
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        
        error = FT.Set_Pixel_Sizes(self.facep,0,16)
        self.assertEqual(error,0)
        
        glyph_index = FT.Get_Char_Index( self.facep, ord(unicode('W')) )
        self.assertFalse(glyph_index == 0)
        log.debug("glyph_index of unicode W is %d",glyph_index)
        
        error = FT.Load_Glyph(self.facep,glyph_index,FT.LOAD_DEFAULT)
        # By the way, the constant above is mistakenly listed as 
        # FT_LOAD_NORMAL in the online tutorial
        self.assertEqual(error,0)
        
        glyph_p = FT.Glyph()
        error = FT.Get_Glyph( self.face.glyph, ctypes.byref(glyph_p) )
        self.assertEqual(error,0)

        glyph2p = FT.Glyph()
        error = FT.Glyph_Copy(glyph_p,ctypes.byref(glyph2p))
        self.assertEqual(error,0)

        # translate `glyph'
        delta = FT.Vector( FT.ToF26Dot6(-100), FT.ToF26Dot6(50))
        FT.Glyph_Transform(glyph_p,None,ctypes.byref(delta))
        self.assertEqual(error,0)
        log.debug("Glyph %r translated.",glyph_p.contents)

        # transform glyph2 (horizontal shear) */
        matrix = FT.Matrix( FT.ToFixed(1.0), FT.ToFixed(0.12), FT.ToFixed(0.0), FT.ToFixed(1.0) )
        FT.Glyph_Transform(glyph2p,ctypes.byref(matrix),None)
        self.assertEqual(error,0)
        log.debug("Glyph %r sheared.",glyph2p.contents)

        FT.Done_Glyph(glyph_p)
        del glyph_p

        FT.Done_Glyph(glyph2p)
        del glyph2p

    def test_glyph_cbox(self):
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        
        error = FT.Set_Pixel_Sizes(self.facep,0,16)
        self.assertEqual(error,0)
        
        glyph_index = FT.Get_Char_Index( self.facep, ord(unicode('W')) )
        self.assertFalse(glyph_index == 0)
        
        error = FT.Load_Glyph(self.facep,glyph_index,FT.LOAD_DEFAULT)
        self.assertEqual(error,0)
        
        glyph_p = FT.Glyph()
        error = FT.Get_Glyph( self.face.glyph, ctypes.byref(glyph_p) )
        self.assertEqual(error,0)

        # translate `glyph'
        delta = FT.Vector( FT.ToF26Dot6(10), FT.ToF26Dot6(5))
        FT.Glyph_Transform(glyph_p,None,ctypes.byref(delta))
        self.assertEqual(error,0)

        cbox = FT.BBox()
        FT.Glyph_Get_CBox(glyph_p,FT.GLYPH_BBOX_UNSCALED,ctypes.byref(cbox))
        log.debug("Glyph W's             unscaled "
                       "coordinates are (%8.4f,%8.4f) (%8.4f,%8.4f)",
            FT.FromF26Dot6(cbox.xMin),FT.FromF26Dot6(cbox.yMin),
            FT.FromF26Dot6(cbox.xMax),FT.FromF26Dot6(cbox.yMax))
        
        FT.Glyph_Get_CBox(glyph_p,FT.GLYPH_BBOX_GRIDFIT,ctypes.byref(cbox))
        log.debug("Glyph W's grid-fitted unscaled "
                       "coordinates are (%8.4f,%8.4f) (%8.4f,%8.4f)",
            FT.FromF26Dot6(cbox.xMin),FT.FromF26Dot6(cbox.yMin),
            FT.FromF26Dot6(cbox.xMax),FT.FromF26Dot6(cbox.yMax))
        
        FT.Glyph_Get_CBox(glyph_p,FT.GLYPH_BBOX_TRUNCATE,ctypes.byref(cbox))
        log.debug("Glyph W's                pixel "
                       "coordinates are (%8.4f,%8.4f) (%8.4f,%8.4f)",
            float(cbox.xMin),float(cbox.yMin),
            float(cbox.xMax),float(cbox.yMax))
        
        FT.Glyph_Get_CBox(glyph_p,FT.GLYPH_BBOX_GRIDFIT,ctypes.byref(cbox))
        log.debug("Glyph W's grid-fitted pixel    "
                       "coordinates are (%8.4f,%8.4f) (%8.4f,%8.4f)",
            FT.FromF26Dot6(cbox.xMin),FT.FromF26Dot6(cbox.yMin),
            FT.FromF26Dot6(cbox.xMax),FT.FromF26Dot6(cbox.yMax))
        
        FT.Done_Glyph(glyph_p)
        del glyph_p

    def test_glyph_to_bitmap(self):
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        
        error = FT.Set_Pixel_Sizes(self.facep,0,16)
        self.assertEqual(error,0)
        
        glyph_index = FT.Get_Char_Index( self.facep, ord(unicode('W')) )
        self.assertFalse(glyph_index == 0)
        
        error = FT.Load_Glyph(self.facep,glyph_index,FT.LOAD_DEFAULT)
        self.assertEqual(error,0)
        
        glyph_p = FT.Glyph()
        error = FT.Get_Glyph( self.face.glyph, ctypes.byref(glyph_p) )
        self.assertEqual(error,0)
        
        glyph_format = self.find_glyph_format(glyph_p.contents.format)
        log.debug("The glyph's format is %s",glyph_format)

        origin = FT.Vector(FT.ToF26Dot6(0.5),FT.ToF26Dot6(0.0))

        error = FT.Glyph_To_Bitmap(ctypes.byref(glyph_p),
                                    FT.RENDER_MODE_NORMAL,
                                    None,
                                    1)
        self.assertEqual(error,0)
        
        glyph_format = self.find_glyph_format(glyph_p.contents.format)
        log.debug("After conversion the glyph's format is %s",glyph_format)

        bitmap_glyph_p = ctypes.cast(glyph_p,ctypes.POINTER(FT.BitmapGlyphRec))
        bitmap_glyph = bitmap_glyph_p.contents
        
        log.debug("After conversion the root glyph is %r",bitmap_glyph.root)
        
        glyph_format = self.find_glyph_format(bitmap_glyph.root.format)
        log.debug("After conversion the bitmap glyph's format is %s",glyph_format)
        
        log.debug("Bitmap glyph's offsets are (%d,%d)",
                       bitmap_glyph.left,bitmap_glyph.top)
        log.debug("Bitmap glyph's dimensions are (%d,%d) and pitch is %d",
                       bitmap_glyph.bitmap.width,bitmap_glyph.bitmap.rows,
                       bitmap_glyph.bitmap.pitch)
        
        FT.Done_Glyph(ctypes.cast(bitmap_glyph_p,FT.Glyph))
        
        del bitmap_glyph
        del bitmap_glyph_p
        del glyph_p
        
    def test_global_metrics(self):
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        
        if not FT.IS_SCALABLE(self.face):
            log.debug("No scaling information for face")
            return
        
        log.debug("Face units_per_em is %d",self.face.units_per_EM)
        log.debug("Face bbox is (%d,%d), (%d,%d)",self.face.bbox.xMin,self.face.bbox.yMin,
                  self.face.bbox.xMax,self.face.bbox.yMax)
        log.debug("Face ascender is %d, descender is %d, and height is %d",
                  self.face.ascender,self.face.descender,self.face.height)
        log.debug("Face maximum advance is (%d,%d)",self.face.max_advance_width,
                  self.face.max_advance_height)
        log.debug("Face underline position and thickness are %d and %d",
                  self.face.underline_position, self.face.underline_thickness)
        
        error = FT.Set_Pixel_Sizes(self.facep,0,16)
        self.assertEqual(error,0)
        
        log.debug("Face scaled ascender and descender are %f and %f",
                  FT.FromF26Dot6(self.face.size.contents.metrics.ascender),
                  FT.FromF26Dot6(self.face.size.contents.metrics.descender))

        log.debug("Face scaled height and max_advance are %f and %f",
                  FT.FromF26Dot6(self.face.size.contents.metrics.height),
                  FT.FromF26Dot6(self.face.size.contents.metrics.max_advance))

    def test_kerning(self):
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        
        if not FT.HAS_KERNING(self.face):
            log.debug("Face does not have kerning info.")
            return
    
        error = FT.Set_Pixel_Sizes(self.facep,0,48)
        self.assertEqual(error,0)
        
        kerning = FT.Vector()
        
        for left_str, right_str in (('5','6'),('A','W')):
            left_glyph_index = FT.Get_Char_Index( self.facep, ord(unicode(left_str)) )
            self.assertFalse(left_glyph_index == 0)
        
            right_glyph_index = FT.Get_Char_Index( self.facep, ord(unicode(right_str)) )
            self.assertFalse(right_glyph_index == 0)
            
            error = FT.Get_Kerning( self.facep,
                          left_glyph_index,
                          right_glyph_index,
                          FT.KERNING_DEFAULT,
                          ctypes.byref(kerning) )
            self.assertEqual(error,0)
            log.debug("The kerning for the pair %s/%s is (%f,%f)",left_str,right_str,
                FT.FromF26Dot6(kerning.x),FT.FromF26Dot6(kerning.y))
        
            error = FT.Get_Kerning( self.facep,
                          left_glyph_index,
                          right_glyph_index,
                          FT.KERNING_UNFITTED,
                          ctypes.byref(kerning) )
            self.assertEqual(error,0)
            log.debug("The unfitted kerning for the pair %s/%s is (%f,%f)",left_str,right_str,
                FT.FromF26Dot6(kerning.x),FT.FromF26Dot6(kerning.y))
        
            error = FT.Get_Kerning( self.facep,
                          left_glyph_index,
                          right_glyph_index,
                          FT.KERNING_UNSCALED,
                          ctypes.byref(kerning) )
            self.assertEqual(error,0)
            log.debug("The unscaled kerning for the pair %s/%s is (%d,%d)",left_str,right_str,
                kerning.x,kerning.y)
            
    def test_render_kerned(self):
        log = logging.getLogger(self.test_id())
        # Astonishly, PCmyoungjo.ttf is missing such basic Kanji as 国!
        text = 'AW Root Beer is the best'
        self.render_kerned(log,text,'kerned')

    def test_measure_bbox_render(self):
        log = logging.getLogger(self.test_id())
        text = 'Weather'
        self.measure_bbox_render(log, text, 'measured')
        
    def test_measured_transformed_render(self):
        log = logging.getLogger(self.test_id())
        text = 'Slider'
        self.measured_transformed_render(log,text,'meas_trans')
        
    def test_kerning(self):
        log = logging.getLogger(self.test_id())
        log.debug("Entry")
        
        if not FT.IS_SCALABLE(self.face):
            log.warn("Face is not scalable.")
            return
    
        error = FT.Set_Pixel_Sizes(self.facep,0,48)
        self.assertEqual(error,0)
        
        metrics = self.face.size.contents.metrics
        log.debug("Face x_ppem, y_ppem is (%f, %f)",metrics.x_ppem,metrics.y_ppem)
        log.debug("Face x_scale, y_scale is (%f, %f)",FT.FromFixed(metrics.x_scale),
                  FT.FromFixed(metrics.y_scale))

class Step2Kanji(Step2):
    def get_font_path(self):
        return r"sazanami-mincho.ttf"

    def get_output_path(self,test_name):
        return os.path.join(tempfile.gettempdir(),"ft2_part2k_%s.png"%test_name)
    
    def test_render_kerned(self):
        log = logging.getLogger(self.test_id())
        # Astonishly, PCmyoungjo.ttf is missing such basic Kanji as 国!
        text = unicode(u'東京は国の一番こんでいる町です。')
        self.render_kerned(log,text,'kerned')

    def test_measure_bbox_render(self):
        log = logging.getLogger(self.test_id())
        text = unicode(u'ペラペラくん')
        self.measure_bbox_render(log, text, 'measured')
        
    def test_measured_transformed_render(self):
        log = logging.getLogger(self.test_id())
        text = unicode(u'三角系')
        self.measured_transformed_render(log,text,'meas_trans')
        


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("In step2, current directory is %s",os.getcwd())
    # Here's how to enable debug logging for one test:
    # logging.getLogger('Step2.test_face').setLevel(logging.DEBUG)
    unittest.main()



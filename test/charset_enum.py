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

    def find_glyph_format(self,glyph_format):
        """ Returns the programmer-readable constant for the glyph_format.
        """
        for possible_format in ['GLYPH_FORMAT_NONE','GLYPH_FORMAT_COMPOSITE',
                                'GLYPH_FORMAT_BITMAP','GLYPH_FORMAT_OUTLINE',
                                'GLYPH_FORMAT_PLOTTER']:
            if getattr(FT,possible_format) == glyph_format:
                return possible_format
        return None

class Step1(TestCaseHarness):
    def get_font_path(self):
        return r"Vera.ttf"
    def get_output_path(self,test_name):
        return os.path.join(tempfile.gettempdir(),"ft2_part1_%s.png"%test_name)

    def range_test(self,range,value):
        if range[0] == None or value < range[0]:
            range[0] = value
        if range[1] == None or value > range[1]:
            range[1] = value

    def test_face(self):
        log = logging.getLogger(self.test_id())
        log.debug("Entry")

        log.info("face.num_glyphs is %d",self.face.num_glyphs)
        log.info("face.num_charmaps is %d",self.face.num_charmaps)

        error = FT.Select_Charmap(self.facep, FT.ENCODING_UNICODE)
        self.assertEqual(error,0)

        mapping_pair_count = 0
        glyph_range = [ None, None ]
        char_code_range = [ None, None ]
        glyph_index = FT.UInt()
        char_code = FT.Get_First_Char(self.facep,ctypes.byref(glyph_index))
        while glyph_index.value != 0:
            mapping_pair_count += 1
            self.range_test(glyph_range,glyph_index.value)
            self.range_test(char_code_range,char_code)
            char_code = FT.Get_Next_Char(self.facep,char_code,ctypes.byref(glyph_index))
        self.assert_(char_code_range[1] > char_code_range[0])
        self.assert_(glyph_range[1] > glyph_range[0])
        log.info("Unicode char codes: %d [%d-%d]",mapping_pair_count,*char_code_range)
        log.info("Unicode glyph indices: %d [%d-%d]",mapping_pair_count,*glyph_range)
        
        
class Step1Kanji(Step1):
    def get_font_path(self):
        return r"sazanami-mincho.ttf"
    def get_output_path(self,test_name):
        return os.path.join(tempfile.gettempdir(),"ft2_part1k_%s.png"%test_name)

    # We inherit test_face(), so it will run again on this font

        

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Here's how to enable debug logging for one test:
    # logging.getLogger('Step1.test_face').setLevel(logging.DEBUG)
    unittest.main()



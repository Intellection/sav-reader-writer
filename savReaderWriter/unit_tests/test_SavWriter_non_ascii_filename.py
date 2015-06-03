#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import sys
from os.path import basename, join
import tempfile
import savReaderWriter as rw

is_windows = sys.platform.startswith("win")

# issue #35: IOError with umlauts in path to a file for sav.SavReader 
# Mostly a Windows-specific thing, see generic.Generic.wideCharToMultiByte
class Test_NonAsciiSavFileName(unittest.TestCase):

    def func(self, savFileName):
        self.outfile = join(tempfile.gettempdir(), 
                            basename(savFileName))
        with rw.SavWriter(self.outfile, [b'v1'], {b'v1': 0}) as writer:
            for i in range(10):
                writer.writerow([i])
        with rw.SavReader(self.outfile) as reader:
            self.assertEqual(reader.all(), [[float(i)] for i in range(10)])
        self.assertTrue(os.path.exists(self.outfile))

    def test_nonascii_u_filename_german(self):
        self.u_savFileName = u"test_data/scheiß Encoding.sav"
        self.func(self.u_savFileName) 

    @unittest.skipIf(is_windows, "Chinese in a Western European windows?")
    def test_nonascii_u_filename_chinese(self):
        self.u_savFileName2 = u"test_data/響應投資豐盛生命計畫 募集百萬愛心.sav"
        self.func(self.u_savFileName2) 

    def test_nonascii_b_filename(self):
        self.b_savFileName = b"test_data/schei\xdf Encoding.sav"
        self.func(self.b_savFileName) 

    def tearDown(self):
        try:
            os.remove(self.outfile)
        except:
            pass 

if __name__ == "__main__":
    unittest.main()


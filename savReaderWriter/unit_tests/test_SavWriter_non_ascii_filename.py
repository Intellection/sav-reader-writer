#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import sys
from os.path import basename, join
import tempfile
import zipfile
import savReaderWriter as rw

is_windows = sys.platform.startswith("win")

# issue #35: IOError with umlauts in path to a file for sav.SavReader 
# Mostly a Windows-specific thing, see generic.Generic.wideCharToMultiByte
class Test_NonAsciiSavFileName(unittest.TestCase):

    def func(self, savFileName):
        
        self.outfile = tempfile.mktemp(suffix="_out.sav")
        with rw.SavWriter(self.outfile, [b'v1'], {b'v1': 0}) as writer:
            for i in range(10):
                writer.writerow([i])
        with rw.SavReader(self.outfile) as reader:
            self.assertEqual(reader.all(), [[float(i)] for i in range(10)])
        self.assertTrue(os.path.exists(self.outfile))

    def test_nonascii_u_filename_german(self):
        u_savFileName = u"test_data/scheiß Encoding.sav"
        self.func(u_savFileName) 

    @unittest.skipIf(is_windows, "Chinese in a Western European windows?")
    def test_nonascii_u_filename_chinese(self):
        # file is zipped: Chinese chars cause errors with .whl creation in Win
        zipFileName = "test_data/chinese_chars.sav.zip" 
        zf = zipfile.ZipFile(zipFileName)
        u_savFileName = zf.infolist()[0].filename
        u_savFileName = join(tempfile.gettempdir(), u_savFileName)
        with open(u_savFileName, "wb") as f:
            f.write(zf.read(basename(u_savFileName)))
        self.func(u_savFileName) 
        os.remove(u_savFileName)

    def test_nonascii_b_filename(self):
        b_savFileName = b"test_data/schei\xdf Encoding.sav"
        self.func(b_savFileName) 

    def tearDown(self):
        try:
            os.remove(self.outfile)
        except:
            pass 

if __name__ == "__main__":
    unittest.main()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
## Use nested context managers
##############################################################################

import unittest
import os
import tempfile
from savReaderWriter import *

# I previously used 'encoding_and_locale_set' in generic.py
class test_SavReader_nested(unittest.TestCase):
    """Check whether context managers may be nested"""

    def setUp(self):
        self.infilename = "test_data/Employee data.sav"
        self.outfilename = os.path.join(tempfile.gettempdir(), 
                                        "test_nested.zsav")

    def test_nested_managers(self):
        kwargs = dict(savFileName=self.outfilename, 
                      varNames=[b'id'], 
                      varTypes={b'id': 0})
        with SavReader(self.infilename) as reader, \
             SavWriter(**kwargs) as writer:
            for record in reader:
                writer.writerow(record[0:1])

    def test_nested_managers_ioUtf8(self):
        """Nested mgrs, mixed codepage and unicode mode."""
        kwargs = dict(savFileName=self.outfilename, 
                      varNames=[b'id', b'gender'], 
                      varTypes={b'id': 0, b'gender': 1},
                      ioUtf8=True )
        with SavReader(self.infilename) as codepage_reader, \
             SavWriter(**kwargs) as unicode_writer:
            for record in codepage_reader:
                unicode_writer.writerow(record[0:2])
        with SavReader(self.outfilename) as reader:
            actual_records = reader[:10]
            desired_records = [[1.0, b'm'],
                               [2.0, b'm'],
                               [3.0, b'f'],
                               [4.0, b'f'],
                               [5.0, b'm'],
                               [6.0, b'm'],
                               [7.0, b'm'],
                               [8.0, b'f'],
                               [9.0, b'f'],
                               [10.0, b'f']]
 
            self.assertEqual(actual_records, desired_records)

    def tearDown(self):
        try:
            os.remove(self.outfilename)
        except:
            pass 

if __name__ == "__main__":
    unittest.main()
        



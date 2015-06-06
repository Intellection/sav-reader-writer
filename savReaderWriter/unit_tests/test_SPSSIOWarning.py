#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
## Check if the custom error class does its job
##############################################################################

import unittest
import os
import warnings
import savReaderWriter as rw

savrw_display_warns = os.getenv("SAVRW_DISPLAY_WARNS")

class test_SPSSIOWarning(unittest.TestCase):

    def setUp(self):
        self.savFileName = "test_data/Employee data.sav"

    msg = "Set SAVRW_DISPLAY_WARNS to 'default' or 'always' to test warnings"
    @unittest.skipUnless(savrw_display_warns in ("default", "always"), msg)
    def test_raises_SPSSIOWarning(self):
        with warnings.catch_warnings(record=True) as warn:
            with rw.SavHeaderReader(self.savFileName) as header:
                metadata = str(header)
                spss_warnings = [item.message for item in warn]
                self.assertTrue(spss_warnings)
                self.assertTrue("SPSS_NO_LABELS" in str(spss_warnings))

if __name__ == "__main__":
    unittest.main()



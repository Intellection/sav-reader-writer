#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
## Check if the custom error class does its job
##############################################################################

import unittest
import os
import warnings
import sys
import savReaderWriter as rw

savrw_display_warns = os.getenv("SAVRW_DISPLAY_WARNS")

class test_SPSSIOWarning(unittest.TestCase):

    def setUp(self):
        self.savFileName = "test_data/Employee data.sav"

    msg1 = "Fails with Tox in Python 3.3"  # TODO: why does this happen???
    msg2 = "Set SAVRW_DISPLAY_WARNS to 'default' or 'always' to test warnings"
    @unittest.skipIf(sys.version_info[:2] == (3, 3), msg1)
    @unittest.skipUnless(savrw_display_warns in ("default", "always"), msg2)
    def test_raises_SPSSIOWarning(self):
        with warnings.catch_warnings(record=True) as warn:
            with rw.SavHeaderReader(self.savFileName) as header:
                metadata = str(header)
                spss_warnings = [item.message for item in warn]
                self.assertTrue(spss_warnings)
                self.assertTrue("SPSS_NO_LABELS" in str(spss_warnings))

if __name__ == "__main__":
    unittest.main()



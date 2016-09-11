#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tempfile
import unittest

from savReaderWriter import SavReader, SavWriter


# issue 52 "Incorrect date decoding in Python 3"
class DecodeSPSSDateTest(unittest.TestCase):
    def test(self):
        with tempfile.NamedTemporaryFile(suffix='.sav') as tmpfile:
            with SavWriter(tmpfile.name, ['date'], {b'date': 0}, formats={b'date': b'EDATE40'}, ioUtf8=True, ioLocale="C.UTF-8") as writer:
                writer.writerow([writer.spssDateTime(b"2000-01-01", "%Y-%m-%d")])

            with SavReader(tmpfile.name, returnHeader=False, ioUtf8=True, ioLocale="C.UTF-8") as reader:
                print(sys.version_info)
                date = list(reader)[0][0]
                self.assertEqual('2000-01-01', date)

    
if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tempfile
import unittest

from savReaderWriter import SavReader, SavWriter


# issue 52 "Incorrect date decoding in Python 3"
class test_SavReader_decode_SPSSDate(unittest.TestCase):

    @unittest.skipIf(sys.platform.startswith("win"), "'No C.UTF-8' on Windows")
    def test_date_conversion(self):
        with tempfile.NamedTemporaryFile(suffix='.sav') as tmpfile:
            with SavWriter(tmpfile.name, ['date'], {b'date': 0}, 
                           formats={b'date': b'EDATE40'}, ioUtf8=True, 
                           ioLocale="C.UTF-8") as writer:
                record = [writer.spssDateTime(b"2000-01-01", "%Y-%m-%d")]
                writer.writerow(record)

            with SavReader(tmpfile.name, returnHeader=False, ioUtf8=True, 
                           ioLocale="C.UTF-8") as reader:
                date = list(reader)[0][0]
                self.assertEqual('2000-01-01', date)

    
if __name__ == "__main__":
    unittest.main()

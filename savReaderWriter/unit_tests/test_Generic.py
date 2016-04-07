# -*- coding: utf-8 -*-
"""
Unittests for class savReaderWriter.generic.Generic
"""
from collections import namedtuple
import sys

import savReaderWriter

def test_version_info():
    actual = savReaderWriter.Generic("").spssioVersion
    desired = namedtuple("_", "major minor patch fixpack")(21, 0, 0, 1)
    assert desired == actual

def test_missingValuesLowHigh():
    actual = savReaderWriter.Generic("").missingValuesLowHigh
    desired = namedtuple("_", "lo hi")(-sys.float_info.max, sys.float_info.max)
    assert desired == actual

    
if __name__ == "__main__":

    import nose
    nose.main()
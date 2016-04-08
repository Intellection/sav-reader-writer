# -*- coding: utf-8 -*-
"""
Writing rows from arrays et al.
"""


import os
import re
from os.path import join
from tempfile import gettempdir
from collections import namedtuple
from unittest.case import SkipTest

import nose
from nose.tools import with_setup, assert_raises

try:
    pandasOK = True
    import pandas as pd
except ImportError:
    pandasOK = False
try:
    numpyOK = True
    import numpy as np
except ImportError:
    numpyOK = False
    
import savReaderWriter as srw
from py3k import *
 

args = ( ["v1", "v2"], dict(v1=0, v2=0) )
desired = [[None, 1.0], [2.0, 3.0], [4.0, 5.0], [6.0, 7.0], 
           [8.0, 9.0], [10.0, 11.0], [12.0, 13.0], [14.0, 15.0], 
           [16.0, 17.0], [18.0, 19.0]]
           
skip = any([not pandasOK, not numpyOK, not isCPython])  # --> pypy


def setUp():
    os.chdir(gettempdir())
 
def tearDown():
    for item in os.listdir("."):
        if re.match(r"output_*\.sav", item):
            os.remove(item)
 
@with_setup(setUp, tearDown)
def test_writerows_numpy():
    if skip:
        raise SkipTest
    data = [range(10), range(10, 20)]
    array = np.array(data, dtype=np.float64).reshape(10, 2)
    array[0, 0] = np.nan
    savFileName = "output_np.sav"
    with srw.SavWriter(savFileName, *args) as writer:
        writer.writerows(array)
    with srw.SavReader(savFileName, recodeSysmisTo=None) as reader:
        actual = reader.all()
    assert actual == desired, actual
        
def test_writerows_pandas():
    if skip:
        raise SkipTest
    df = pd.DataFrame({"a": range(0, 20, 2), "b": range(1, 20, 2)})
    df.loc[0, "a"] = np.nan
    savFileName = "output_pd.sav"
    with srw.SavWriter(savFileName, *args) as writer:
        writer.writerows(df)
    with srw.SavReader(savFileName) as reader:
        actual = reader.all()
    assert actual == desired, actual

def test_writerows_namedtuple():
    Record = namedtuple("Record", args[0])
    records = [Record(*record) for record in desired]
    savFileName = "output_namedtuple.sav"
    with srw.SavWriter(savFileName, *args) as writer:
        writer.writerows(records)
    with srw.SavReader(savFileName) as reader:
        actual = reader.all()
    assert actual == desired, actual
 
def test_writerows_tuple():
    records = tuple([tuple(record) for record in desired])
    savFileName = "output_tuple.sav"
    with srw.SavWriter(savFileName, *args) as writer:
        writer.writerows(records)
    with srw.SavReader(savFileName) as reader:
        actual = reader.all()
    assert actual == desired, actual

def test_writerows_erroneous_flat_n():
    records = [0, 1]  # wrong!,
    savFileName = "output_error1.sav"
    with srw.SavWriter(savFileName, *args) as writer:
        assert_raises(TypeError, writer.writerows, records)

def test_writerows_erroneous_flat_s():
    records = ["a", "b"]  # wrong!
    string_args = ["v1", "v2"], dict(v1=1, v2=1)
    savFileName = "output_error2.sav"
    with srw.SavWriter(savFileName, *string_args) as writer:
        assert_raises(TypeError, writer.writerows, records)

def test_writerows_erroneous_flat_empty():
    records = []  # wrong!
    string_args = ["v1", "v2"], dict(v1=1, v2=1)
    savFileName = "output_error3.sav"
    with srw.SavWriter(savFileName, *string_args) as writer:
        assert_raises(ValueError, writer.writerows, records)
        
if __name__ == "__main__":

    nose.main()

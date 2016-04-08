# -*- coding: utf-8 -*-
"""
Accented varSets -- issue #39
"""

from os.path import join
from os import remove
from tempfile import gettempdir

import nose

import savReaderWriter as srw

varNames = [b'salbegin', b'salary']
kwargs = dict(savFileName = join(gettempdir(), "variable_set.sav"),
              varNames    = varNames,
              varTypes    = dict(zip(varNames, [0, 0])),
              varSets     = {b'\xc3\xbcberhaupt': varNames})

def test_accented_varSet_codepage_mode():
    with srw.SavWriter(**kwargs) as writer:
        for i in range(10):
            writer.writerow([1, 1])
    with srw.SavHeaderReader(kwargs["savFileName"]) as header:
        actual = header.varSets
    desired = {b'\xc3\xbcberhaupt': [b'salbegin', b'salary']}
    remove(kwargs["savFileName"])
    assert actual == desired, actual


def test_accented_varSet_unicode_mode():
    kwargs["varSets"] = {u'\xfcberhaupt': varNames}
    kwargs["ioUtf8"] = True
    with srw.SavWriter(**kwargs) as writer:
        for i in range(10):
            writer.writerow([1, 1])
    with srw.SavHeaderReader(kwargs["savFileName"], ioUtf8=True) as header:
        actual = header.varSets
    desired = {u'\xfcberhaupt': [u'salbegin', u'salary']}
    remove(kwargs["savFileName"])
    assert actual == desired, actual


if __name__ == "__main__":
    
    nose.main()    
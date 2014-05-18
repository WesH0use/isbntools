#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
""" nose tests

"""
import os
from ..dev.file import File
from nose.tools import assert_equals, assert_raises


TESTFILE = '/tmp/deleteme.pdf'
NEW_BASENAME = 'deleteme-PLEASE.pdf'


def setup_module():
    f = open(TESTFILE, 'w')
    f.write('ooo')
    f.close()
    os.chdir(os.path.dirname(TESTFILE))

def teardown_module():
    os.remove(os.path.join(os.path.dirname(TESTFILE), NEW_BASENAME))


def test_exists():
    f = File(TESTFILE)    


def test_validate():
    f = File(TESTFILE)
    assert f.validate('basename.pdf') == True
    assert f.validate('as/basename.pdf') == False
    assert f.validate('.basename.pdf') == True
    assert f.validate('.basename') == False
    assert f.validate('') == False


def test_mkwinsafe():
    f = File(TESTFILE)
    assert f.mkwinsafe('Açtr: ') == 'Açtr'
    assert f.mkwinsafe('as/tiõ') == 'astiõ'
    assert f.mkwinsafe('file ""name?') == 'file name'
    assert f.mkwinsafe('file ""name?', space='_') == 'file_name'
    assert f.mkwinsafe('file   name ') == 'file name'


def test_baserename():
    f = File(TESTFILE)
    assert f.baserename(NEW_BASENAME) == True
    assert f.baserename(NEW_BASENAME) == True



    






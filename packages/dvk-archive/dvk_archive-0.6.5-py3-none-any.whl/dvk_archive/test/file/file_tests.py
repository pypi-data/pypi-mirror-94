#!/usr/bin/env python3

"""
Combined unit tests for the file package
"""

from dvk_archive.test.file.test_dvk import all_tests as test_dvk
from dvk_archive.test.file.test_dvk_handler import all_tests as test_handler

def test_all():
    """
    Run all file tests.
    """
    test_handler()
    test_dvk()

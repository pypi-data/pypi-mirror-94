#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of ofunctions package

"""
ofunctions is a general library for basic repetitive tasks that should be no brainers :)

Versioning semantics:
    Major version: backward compatibility breaking changes
    Minor version: New functionality
    Patch version: Backwards compatible bug fixes

"""

__intname__ = 'ofunctions'
__author__ = 'Orsiris de Jong'
__copyright__ = 'Copyright (C) 2014-2021 Orsiris de Jong'
__description__ = 'Very basic platform identification'
__licence__ = 'BSD 3 Clause'
__version__ = '1.0.0'
__build__ = '2021020901'

import os
import sys


def get_os() -> str:
    """
    Simple windows / linux identification that handles msys too
    """
    if os.name == 'nt':
        return 'Windows'
    if os.name == 'posix':
        # uname property does not exist under windows
        # pylint: disable=E1101
        result = os.uname()[0]

        if result.startswith('MSYS_NT-'):
            result = 'Windows'

        return result
    else:
        raise OSError("Cannot get os, os.name=[%s]." % os.name)


def python_arch() -> str:
    """
    Get current python interpreter architecture,
    """
    if get_os() == "Windows":
        if 'AMD64' in sys.version:
            return 'x64'
        return 'x86'
    else:
        # uname property does not exist under windows
        # pylint: disable=E1101
        return os.uname()[4]


def is_64bit_python() -> bool:
    """
    Detect if python is 64 bit but stay OS agnostic
    """
    return sys.maxsize > 2 ** 32

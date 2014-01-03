#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ***** BEGIN LICENSE BLOCK *****
# Copyright (C) 2012-2014, Hayaki Saito 
# 
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions: 
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software. 
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE. 
# 
# ***** END LICENSE BLOCK *****


import db.unicode6_2.normal
import db.unicode6_2.cjk
_normal_pattern_fullwidth = db.unicode6_2.normal.pattern_fullwidth
_normal_pattern_combining = db.unicode6_2.normal.pattern_combining
_cjk_pattern_fullwidth = db.unicode6_2.cjk.pattern_fullwidth
_cjk_pattern_combining = db.unicode6_2.cjk.pattern_combining


def _generate_ucs4_codepoints(run):
    c1 = None
    for s in run:
        c = ord(s)
        if c < 0xd800:
            yield c
        elif c < 0xdc00:
            c1 = (c - 0xd800) << 10
        elif c < 0xe000 and c1:
            yield c1 | (c - 0xdc00)
            c1 = None
        else:
            yield c


def wcwidth(c):
    if c < 0x20:
        return -1
    elif c < 0x7f:
        return 1
    elif c < 0xa0:
        return -1
    elif c < 0x10000:
        s = unichr(c)
        if _normal_pattern_combining.match(s):
            return 0
        elif _normal_pattern_fullwidth.match(s):
            return 2
        return 1
    elif c < 0x1F300:
        if c < 0x1F200:
            return 1
        return 2
    elif c < 0x20000:
        return 1
    elif c < 0xE0000:
        return 2
    return 1


def wcwidth_cjk(c):
    if c < 0x20:
        return -1
    elif c < 0x7f:
        return 1
    elif c < 0xa0:
        return -1
    elif c < 0x10000:
        s = unichr(c)
        if _cjk_pattern_combining.match(s):
            return 0
        elif _cjk_pattern_fullwidth.match(s):
            return 2
        return 1
    elif c < 0x1F100:
        return 1
    elif c < 0x1F1A0:
        if c == 0x1F12E:
            return 1
        elif c == 0x1F16A:
            return 1
        elif c == 0x1F16B:
            return 1
        return 2
    elif c < 0x1F300:
        if c < 0x1F200:
            return 1
        return 2
    elif c < 0x20000:
        return 1
    return 2


def wcswidth(run):
    n = 0
    for c in _generate_ucs4_codepoints(run):
        width = wcwidth(c)
        if width == -1:
            return -1
        n += width
    return n


def wcswidth_cjk(run):
    n = 0
    for c in _generate_ucs4_codepoints(run):
        width = wcwidth_cjk(c)
        if width == -1:
            return -1
        n += width
    return n

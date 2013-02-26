#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ***** BEGIN LICENSE BLOCK *****
# Copyright (C) 2012  Hayaki Saito <user@zuse.jp>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

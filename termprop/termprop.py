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

__author__ = "Hayaki Saito (user@zuse.jp)"
__version__ = "0.0.5"
__license__ = "GPL v3"

import sys
import os
import termios
import select
import re
import wcwidth as ww

_cpr_pattern = re.compile('\x1b\[([0-9]+);([0-9]+)R')


def _getcpr():
    data = ""
    for i in xrange(0, 3):
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()
        rfd, wfd, xfd = select.select([0], [], [], 1.5)
        if rfd:
            data += os.read(0, 1024)
            m = _cpr_pattern.match(data)
            if m is None:
                continue
            row = int(m.group(1))
            col = int(m.group(2))
            return row, col
    return None

_bg_pattern = re.compile(
    '\x1b\][0-9]+;rgb\:([0-9A-Fa-f]+\/[0-9A-Fa-f]+\/[0-9A-Fa-f]+)\x1b\\\\')


def _getbg():
    data = ""
    for i in xrange(0, 3):
        sys.stdout.write("\x1b]11;?\x1b\\")
        sys.stdout.flush()
        rfd, wfd, xfd = select.select([0], [], [], 0.2)
        if rfd:
            data += os.read(0, 1024)
            m = _bg_pattern.match(data)
            if m is None:
                continue
            params = m.group(1).split("/")
            return params

_da1_pattern = re.compile('\x1b\[(\?[0-9;\.]+)c')


def _getda1():
    data = ""
    for i in xrange(0, 3):
        sys.stdout.write("\x1b[c")
        sys.stdout.flush()
        rfd, wfd, xfd = select.select([0], [], [], 0.2)
        if rfd:
            data += os.read(0, 1024)
            m = _da1_pattern.match(data)
            if m is None:
                continue
            return m.group(1)
    return "-"

_da2_pattern = re.compile('\x1b\[([>\?0-9;]+)c')


def _getda2():
    data = ""
    for i in xrange(0, 3):
        sys.stdout.write("\x1b[>c")
        sys.stdout.flush()
        rfd, wfd, xfd = select.select([0], [], [], 0.2)
        if rfd:
            data += os.read(0, 1024)
            m = _da2_pattern.match(data)
            if m is None:
                continue
            return m.group(1)
    return "-"


def _getenq(stdin, stdout):
    data = ""
    sys.stdin.flush()
    stdout.write("\x05")
    stdout.flush()

    rfd, wfd, xfd = select.select([sys.stdin.fileno()], [], [], 0.1)
    if rfd:
        data = os.read(0, 1024)
        return data


_CPR_OK = 0
_CPR_OFF_BY_ONE = 1
_CPR_NOT_SUPPORTED = 2


def _guess_cpr():
    sys.stdout.write("\x0d")
    pos = _getcpr()
    if pos is None:
        return _CPR_NOT_SUPPORTED
    y, x = pos
    if x == 0:
        return _CPR_OFF_BY_ONE
    return _CPR_OK


def _get_width(s):
    pos = _getcpr()
    if not pos is None:
        y1, x1 = pos
        sys.stdout.write(s)
        pos = _getcpr()
        if not pos is None:
            y2, x2 = pos
            size = x2 - x1
            sys.stdout.write("\x0d\x1b[K")
            return size
    return -1


def _get_bg():
    return _getbg()


def _guess_cjk():
    if _get_width("▽") == 2:
        return True
    return False


def _guess_combine():
    if _get_width("が") == 2:
        return True
    return False


def _guess_nonbmp():
    if _get_width("𠀁") == 2:
        return True
    return False


def _guess_title():
    if _get_width("\x1b]2;a\x1b\\") == 0:
        return True
    return False


def _guess_mb_title():
    if _get_width("\x1b]2;＜\x1b\\") == 0:
        return True
    return False


class Termprop:

    has_cpr = False
    has_color_report = False
    has_256color = False
    cpr_off_by_one_glitch = False
    is_cjk = False
    has_nonbmp = False
    has_combine = False
    has_title = False
    has_mb_title = False
    color_bg = ""
    da1 = -1
    da2 = -1
    has_256color = False

    """
    # not implemented
    parser_model = 1 # 0: ISO-2022 / 1: Unicode
    presentation_width_glitch = False
    has_spacing_combining = False
    wide_Yijing_hexagrams = True
    printable_bidi_controls = False
    cjk_combine_glitch = False
    euc3 = False
    euc4 = False
    width_data_version = 500
    combining_data_version = 500
    """
    __count = 0
    __oldtermios = 0

    def __init__(self):
        self.setupterm()
        sys.stdout.write("\x1b7\x1b[30;8m\x1b[?25l")
        try:
            cpr_state = _guess_cpr()

            # get device attributes
            self.da1 = _getda1()
            self.da2 = _getda2()

            # detect CPR(DSR 6) capability
            if cpr_state == _CPR_NOT_SUPPORTED:
                self.has_cpr = False
                self.cpr_off_by_one_glitch = False
            elif cpr_state == _CPR_OFF_BY_ONE:
                self.has_cpr = True
                self.cpr_off_by_one_glitch = True
            else:
                self.has_cpr = True
                self.cpr_off_by_one_glitch = False

            # detect width options with CPR(DSR 6)
            if self.has_cpr:
                self.is_cjk = _guess_cjk()
                self.has_nonbmp = _guess_nonbmp()
                self.has_combine = _guess_combine()

            # select wcwidth
            if self.is_cjk:
                self.set_cjk()
            else:
                self.set_noncjk()

            env_term = os.getenv("TERM", "")

            if not env_term.startswith("vt"):

                self.color_bg = _get_bg()
                if self.color_bg:
                    self.has_color_report = True

                # detect title capability
                self.has_title = _guess_title()
                if self.has_title:
                    self.has_mb_title = _guess_mb_title()

                # detect color capability
                _pattern_256color = re.compile('(256color|terminator|iTerm)')
                if _pattern_256color.match(env_term):
                    self.has_256color = True

                sys.stdout.write("\x1b]2;\x1b\\")

        finally:
            sys.stdout.write("\x1b[?25h\x1b[0m\x1b8")
            self.cleanupterm()

    def set_cjk(self):
        self.is_cjk = True
        self.wcwidth = ww.wcwidth_cjk
        self.wcswidth = ww.wcswidth_cjk

    def set_noncjk(self):
        self.is_cjk = False
        self.wcwidth = ww.wcwidth
        self.wcswidth = ww.wcswidth

    def wcwidth(self, c):
        _wcwidth = self.wcwidth
        return _wcwidth(c)

    def wcswidth(self, s):
        _wcswidth = self.wcswidth
        return _wcswidth(s)

    def getyx(self):
        self.setupterm()
        try:
            pos = _getcpr()
            if pos is None:
                return (0, 0)
            if not self.cpr_off_by_one_glitch:
                return pos
            y, x = pos
            return (y + 1, x + 1)
        finally:
            self.cleanupterm()

    def is_vte(self):
        if self.da1 != "?62;9;":
            return False
        if not re.match(">1;[23][0-9]{3};0", self.da2):
            return False
        return True

    def setupterm(self):
        self.__count += 1
        if self.__count == 1:
            self.__oldtermios = termios.tcgetattr(0)
            new = termios.tcgetattr(0)
            new[3] &= ~(termios.ECHO | termios.ICANON)
            new[6][termios.VMIN] = 20
            new[6][termios.VTIME] = 1
            termios.tcsetattr(0, termios.TCSANOW, new)

    def cleanupterm(self):
        if self.__count > 0:
            self.__count -= 1
            if self.__count == 0:
                termios.tcsetattr(0, termios.TCSADRAIN, self.__oldtermios)
                self.__oldtermios = None

    def test(self):
        print "has_cpr: %s" % self.has_cpr
        print "has_color_report: %s" % self.has_color_report
        print "color_bg: %s" % self.color_bg
        print "cpr_off_by_one_glitch: %s" % self.cpr_off_by_one_glitch
        print "cjk: %s" % self.is_cjk
        print "nonbmp: %s" % self.has_nonbmp
        print "combine: %s" % self.has_combine
        print "title: %s" % self.has_title
        print "mb_title: %s" % self.has_mb_title
        print "DA1: %s" % self.da1
        print "DA2: %s" % self.da2
        print "is_vte: %s" % self.is_vte()


def makepattern():
    prop = Termprop()
    prop.setupterm()
    try:
        first = 0x020
        end = 0x10000
        table = [-1] * (first - 1) + [1] * (end - first + 1) + [-2]
        for c in xrange(first, end):

            sys.stdout.write(u"\x0d" + unichr(c))
            pos = _getcpr()
            if pos is None:
                raise Exception("cpr failed")
            y, x = pos
            if prop.cpr_off_by_one_glitch:
                width = x + 1 - 1
            else:
                width = x - 1
            if width == 0:
                table[c] = -1
                continue

            sys.stdout.write(u"\x0da" + unichr(c))
            pos = _getcpr()
            if pos is None:
                raise Exception("cpr failed")
            y, x = pos
            if prop.cpr_off_by_one_glitch:
                comb_width = x + 1 - 2
            else:
                comb_width = x - 2
            if comb_width == 0:
                table[c] = 0
                continue

            if width != 1 and width != 2:
                #raise Exception("char: %d, width: %d" % (c, width))
                print "char: %x, width: %d" % (c, width)
            table[c] = width

        start = -1
        ranges = []
        for c in xrange(first, end + 1):
            width = table[c]
            if start != -1 and width != 0:
                if start == c - 1:
                    ranges.append("\u%04x" % start)
                elif start == c - 2:
                    ranges.append("\u%04x\u%04x" % (start, c - 1))
                else:
                    ranges.append("\u%04x-\u%04x" % (start, c - 1))
                start = -1
            elif start == -1 and width == 0:
                start = c
        combining_pattern = "/^[" + "".join(ranges) + "]$/"
        start = -1
        ranges = []
        for c in xrange(first, end + 1):
            width = table[c]
            if start != -1 and width != 2:
                if start == c - 1:
                    ranges.append("\u%04x" % start)
                elif start == c - 2:
                    ranges.append("\u%04x\u%04x" % (start, c - 1))
                else:
                    ranges.append("\u%04x-\u%04x" % (start, c - 1))
                start = -1
            elif start == -1 and width == 2:
                start = c
        fullwidth_pattern = "/^[" + "".join(ranges) + "]$/"
        start = -1
        ranges = []
        for c in xrange(first, end + 1):
            width = table[c]
            if start != -1 and width != -1:
                if start == c - 1:
                    ranges.append("\u%04x" % start)
                elif start == c - 2:
                    ranges.append("\u%04x\u%04x" % (start, c - 1))
                else:
                    ranges.append("\u%04x-\u%04x" % (start, c - 1))
                start = -1
            elif start == -1 and width == -1:
                start = c
        control_pattern = "/^[" + "".join(ranges) + "]$/"
    finally:
        prop.cleanupterm()
    return """
import re
combining_pattern = re.compile(u'%s')
fullwidth_pattern = re.compile(u'%s')
control_pattern = re.compile(u'%s')
""" % (combining_pattern,
       fullwidth_pattern,
       control_pattern)


def test():
    Termprop().test()

if __name__ == "__main__":
    test()

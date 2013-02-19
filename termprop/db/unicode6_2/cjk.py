#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ***** BEGIN LICENSE BLOCK *****
# Copyright (C) 2012-2013  Hayaki Saito <user@zuse.jp>
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

import re
pattern_fullwidth = re.compile(u'^[\u00a1\u00a4\u00a7\u00a8\u00aa\u00ad\u00ae\u00b0-\u00b4\u00b6-\u00ba\u00bc-\u00bf\u00c6\u00d0\u00d7\u00d8\u00de-\u00e1\u00e6\u00e8-\u00ea\u00ec\u00ed\u00f0\u00f2\u00f3\u00f7-\u00fa\u00fc\u00fe\u0101\u0111\u0113\u011b\u0126\u0127\u012b\u0131-\u0133\u0138\u013f-\u0142\u0144\u0148-\u014b\u014d\u0152\u0153\u0166\u0167\u016b\u01ce\u01d0\u01d2\u01d4\u01d6\u01d8\u01da\u01dc\u0251\u0261\u02c4\u02c7\u02c9-\u02cb\u02cd\u02d0\u02d8-\u02db\u02dd\u02df\u0391-\u03a1\u03a3-\u03a9\u03b1-\u03c1\u03c3-\u03c9\u0401\u0410-\u044f\u0451\u1100-\u115f\u2010\u2013-\u2016\u2018\u2019\u201c\u201d\u2020-\u2022\u2024-\u2027\u2030\u2032\u2033\u2035\u203b\u203e\u2074\u207f\u2081-\u2084\u20ac\u2103\u2105\u2109\u2113\u2116\u2121\u2122\u2126\u212b\u2153\u2154\u215b-\u215e\u2160-\u216b\u2170-\u2179\u2189\u2190-\u2199\u21b8\u21b9\u21d2\u21d4\u21e7\u2200\u2202\u2203\u2207\u2208\u220b\u220f\u2211\u2215\u221a\u221d-\u2220\u2223\u2225\u2227-\u222c\u222e\u2234-\u2237\u223c\u223d\u2248\u224c\u2252\u2260\u2261\u2264-\u2267\u226a\u226b\u226e\u226f\u2282\u2283\u2286\u2287\u2295\u2299\u22a5\u22bf\u2312\u2329\u232a\u2460-\u24e9\u24eb-\u254b\u2550-\u2573\u2580-\u258f\u2592-\u2595\u25a0\u25a1\u25a3-\u25a9\u25b2\u25b3\u25b6\u25b7\u25bc\u25bd\u25c0\u25c1\u25c6-\u25c8\u25cb\u25ce-\u25d1\u25e2-\u25e5\u25ef\u2605\u2606\u2609\u260e\u260f\u2614\u2615\u261c\u261e\u2640\u2642\u2660\u2661\u2663-\u2665\u2667-\u266a\u266c\u266d\u266f\u269e\u269f\u26be\u26bf\u26c4-\u26cd\u26cf-\u26e1\u26e3\u26e8-\u26ff\u273d\u2757\u2776-\u277f\u2b55-\u2b59\u2e80-\u2e99\u2e9b-\u2ef3\u2f00-\u2fd5\u2ff0-\u2ffb\u3000-\u3029\u302e-\u303e\u3041-\u3096\u309b-\u30ff\u3105-\u312d\u3131-\u318e\u3190-\u31ba\u31c0-\u31e3\u31f0-\u321e\u3220-\u32fe\u3300-\u4dbf\u4e00-\ua48c\ua490-\ua4c6\ua960-\ua97c\uf900-\ufa6d\ufa70-\ufad9\ufe10-\ufe19\ufe30-\ufe52\ufe54-\ufe66\ufe68-\ufe6b\uff01-\uff60\uffe0-\uffe6\ufffd\uac00-\ud7a3\ue000-\uf8ff\ufa6e\ufa6f\ufada]$')
pattern_combining = re.compile(u'^[\u0300-\u036f\u0483-\u0489\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7\u0600-\u0604\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06dd\u06df-\u06e4\u06e7\u06e8\u06ea-\u06ed\u070f\u0711\u0730-\u074a\u07a6-\u07b0\u07eb-\u07f3\u0816-\u0819\u081b-\u0823\u0825-\u0827\u0829-\u082d\u0859-\u085b\u08e4-\u08fe\u0900-\u0902\u093a\u093c\u0941-\u0948\u094d\u0951-\u0957\u0962\u0963\u0981\u09bc\u09c1-\u09c4\u09cd\u09e2\u09e3\u0a01\u0a02\u0a3c\u0a41\u0a42\u0a47\u0a48\u0a4b-\u0a4d\u0a51\u0a70\u0a71\u0a75\u0a81\u0a82\u0abc\u0ac1-\u0ac5\u0ac7\u0ac8\u0acd\u0ae2\u0ae3\u0b01\u0b3c\u0b3f\u0b41-\u0b44\u0b4d\u0b56\u0b62\u0b63\u0b82\u0bc0\u0bcd\u0c3e-\u0c40\u0c46-\u0c48\u0c4a-\u0c4d\u0c55\u0c56\u0c62\u0c63\u0cbc\u0cbf\u0cc6\u0ccc\u0ccd\u0ce2\u0ce3\u0d41-\u0d44\u0d4d\u0d62\u0d63\u0dca\u0dd2-\u0dd4\u0dd6\u0e31\u0e34-\u0e3a\u0e47-\u0e4e\u0eb1\u0eb4-\u0eb9\u0ebb\u0ebc\u0ec8-\u0ecd\u0f18\u0f19\u0f35\u0f37\u0f39\u0f71-\u0f7e\u0f80-\u0f84\u0f86\u0f87\u0f8d-\u0f97\u0f99-\u0fbc\u0fc6\u102d-\u1030\u1032-\u1037\u1039\u103a\u103d\u103e\u1058\u1059\u105e-\u1060\u1071-\u1074\u1082\u1085\u1086\u108d\u109d\u1160-\u11ff\u135d-\u135f\u1712-\u1714\u1732-\u1734\u1752\u1753\u1772\u1773\u17b4\u17b5\u17b7-\u17bd\u17c6\u17c9-\u17d3\u17dd\u180b-\u180d\u18a9\u1920-\u1922\u1927\u1928\u1932\u1939-\u193b\u1a17\u1a18\u1a56\u1a58-\u1a5e\u1a60\u1a62\u1a65-\u1a6c\u1a73-\u1a7c\u1a7f\u1b00-\u1b03\u1b34\u1b36-\u1b3a\u1b3c\u1b42\u1b6b-\u1b73\u1b80\u1b81\u1ba2-\u1ba5\u1ba8\u1ba9\u1bab\u1be6\u1be8\u1be9\u1bed\u1bef-\u1bf1\u1c2c-\u1c33\u1c36\u1c37\u1cd0-\u1cd2\u1cd4-\u1ce0\u1ce2-\u1ce8\u1ced\u1cf4\u1dc0-\u1de6\u1dfc-\u1dff\u200b-\u200f\u202a-\u202e\u2060-\u2064\u206a-\u206f\u20d0-\u20f0\u2cef-\u2cf1\u2d7f\u2de0-\u2dff\u302a-\u302d\u3099\u309a\ua66f-\ua672\ua674-\ua67d\ua69f\ua6f0\ua6f1\ua802\ua806\ua80b\ua825\ua826\ua8c4\ua8e0-\ua8f1\ua926-\ua92d\ua947-\ua951\ua980-\ua982\ua9b3\ua9b6-\ua9b9\ua9bc\uaa29-\uaa2e\uaa31\uaa32\uaa35\uaa36\uaa43\uaa4c\uaab0\uaab2-\uaab4\uaab7\uaab8\uaabe\uaabf\uaac1\uaaec\uaaed\uaaf6\uabe5\uabe8\uabed\ufb1e\ufe00-\ufe0f\ufe20-\ufe26\ufeff\ufff9]$')

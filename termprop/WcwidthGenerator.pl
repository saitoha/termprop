#!/usr/bin/perl
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


use strict;
my %wcmap1;
my %wcmap2;
my %wclmap1;
my %wclmap2;

open(IN, "EastAsianWidth.txt") or die;

while (<IN>) {
    if ($_ =~ /^([0-9A-F]{4});(F|W)/) {
        $wcmap1{$1} = 2;
    } elsif ($_ =~ /^([0-9A-F]{4})\.\.([0-9A-F]{4});(F|W)/) {
        my $first = hex $1;
        my $last = hex $2;
        for (my $i = $first; $i <= $last; $i++) {
            $wcmap1{sprintf("%04x", $i)} = 2;
        }
    }
    if ($_ =~ /^([0-9A-F]{4});(F|W|A)/) {
        my $key = $1;
        $wcmap2{$key} = 2;
    } elsif ($_ =~ /^([0-9A-F]{4})\.\.([0-9A-F]{4});(F|W|A)/) {
        my $first = hex $1;
        my $last = hex $2;
        for (my $i = $first; $i <= $last; $i++) {
            $wcmap2{sprintf("%04x", $i)} = 2;
        }
    }

#    if ($_ =~ /^([0-9A-F]{5});(F|W)/) {
#        my $n = hex $1;
#        my $first = sprintf "%04x", (($n >> 10) + 0xD800);
#        my $second = sprintf "%04x", (($n & 0x3ff) + 0xDC00);
#        $wclmap1{$first+""}{$second+""} = 2;
#    } elsif ($_ =~ /^([0-9A-F]{5})\.\.([0-9A-F]{5});(F|W)/) {
#        my $begin = hex $1;
#        my $end = hex $2;
#        for (my $i = $begin; $i <= $end; $i++) {
#            my $first = sprintf "%04x", (($i >> 10) + 0xD800);
#            my $second = sprintf "%04X", (($i & 0x3ff) + 0xDC00);
#            $wclmap1{$first+""}{$second+""} = 2;
#        }
#    }
#    if ($_ =~ /^([0-9A-F]{5});(F|W|A)/) {
#        my $n = hex $1;
#        my $first = sprintf "%04x", (($n >> 10) + 0xD800);
#        my $second = sprintf "%04x", (($n & 0x3ff) + 0xDC00);
#        $wclmap2{$first+""}{$second+""} = 2;
#    } elsif ($_ =~ /^([0-9A-F]{5})\.\.([0-9A-F]{5});(F|W|A)/) {
#        my $begin = hex $1;
#        my $last = hex $2;
#        for (my $i = $begin; $i <= $last; $i++) {
#            my $first = sprintf "%04x", (($i >> 10) + 0xD800);
#            my $second = sprintf "%04x", (($i & 0x3ff) + 0xDC00);
#            $wclmap2{$first+""}{$second+""} = 2;
#        }
#    }

}

close(IN);

open(IN, "UnicodeData.txt") or die;
while (<IN>) {
    # Mark Nonspacing / Mark, Enclosing / Other, format
    if ($_ =~ /^00AD;/) {
        next;
    }
    if ($_ =~ /^([0-9A-F]{4});[^;]*;(Mn|Me|Cf)/
     || $_ =~ /^11[6-9A-F][0-9A-F];/
     || $_ =~ /^200B;/ )
    {
        $wcmap1{$1} = 0;
        $wcmap2{$1} = 0;
    }
#    if ($_ =~ /^([0-9A-F]{5});[^;]*;(Mn|Me|Cf)/) {
#        my $n = hex $1;
#        my $first = sprintf "%04x", (($n >> 10) + 0xD800);
#        my $second = sprintf "%04x", (($n & 0x3ff) + 0xDC00);
#        $wclmap1{$first}{$second} = 0;
#        $wclmap2{$first}{$second} = 0;
#    }
}
close(IN);

sub print_characters {
    my ($s, %wcmap) = @_;
    my $last = 0;
    my $previous = 0;
    my @results = ();
    foreach (sort keys %wcmap) {
        if (ref($wcmap{$_}) ne "HASH") {
            my $current = hex $_;
            if ($wcmap{$_} == $s) {
                if ($previous == $current - 1) {
                    # pass
                } else {
                    if ($last == $previous) {
                        push @results, sprintf("\\u%04x", $current);
                        $last = $current;
                    } elsif ($previous - $last <= 1) {
                        push @results, sprintf("\\u%04x\\u%04x", $previous, $current);
                        $last = $current;
                    } else {
                        push @results, sprintf("-\\u%04x\\u%04x", $previous, $current);
                        $last = $current;
                    }
                }
                $previous = $current;
            }
        } else {
            my $first = $_;
            my $seconds = &print_characters($s, %{$wcmap{$first}});
            if (length($seconds) > 0) {
                if (length($seconds) < 8) {
                    push(@results, sprintf "|\\u%s%s", $first, $seconds);
                } else {
                    push(@results, sprintf "|\\u%s[%s]", $first, $seconds);
                }
            }
        }
    }
    return join "", @results;
}
print <<EOF;
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ***** BEGIN LICENSE BLOCK *****
# Copyright (C) 2012  Hayaki Saito <user\@zuse.jp>
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
pattern1 = re.compile(u'^[@{[print_characters 2, %wcmap1]}]\$')
pattern2 = re.compile(u'^[@{[print_characters 0, %wcmap1]}]\$')
pattern3 = re.compile(u'^[@{[print_characters 2, %wcmap2]}]\$')
pattern4 = re.compile(u'^[@{[print_characters 0, %wcmap2]}]\$')


def mk_wcwidth(c):
    if c < 0x10000:
        s = unichr(c)
        if pattern1.match(s):
            return 2
        elif pattern2.match(s):
            return 0
        return 1
    elif c < 0x1F200:
        return 1
    elif c < 0x1F300:
        return 2
    elif c < 0x20000:
        return 1
    elif c < 0xE0000:
        return 2
    return 1


def mk_wcwidth_cjk(c):
    if c < 0x10000:
        s = unichr(c)
        if pattern3.match(s):
            return 2
        elif pattern4.match(s):
            return 0
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
    elif c < 0x1F200:
        return 1
    elif c < 0x1F300:
        return 2
    elif c < 0x20000:
        return 1
    return 2


def wcwidth(s):
    return mk_wcwidth(ord(s))


def wcwidth_cjk(s):
    return mk_wcwidth_cjk(ord(s))


def wcswidth(run):
    n = 0
    for s in run:
        n += mk_wcwidth(ord(s))
    return n


def wcswidth_cjk(run):
    n = 0
    for s in run:
        n += mk_wcwidth_cjk(ord(s))
    return n
EOF

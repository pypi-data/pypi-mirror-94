# *************************************************************************
#
# Copyright (c) 2021 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

import pprint


def strf(in_str):
    pp = pprint.PrettyPrinter(indent=4, width=60, depth=30)
    return pp.pformat(in_str)


def list2strf(in_list, cell_size, in_hex=False):
    s = "[ "
    cell = ""
    for i in in_list:
        if in_hex:
            cell = hex(i)[2:]
        else:
            cell = str(i)
        c_l = len(cell)
        if c_l > cell_size:
            cell = cell[:cell_size - 1] + "?"
        if c_l < cell_size:
            cell = " " * (cell_size - c_l) + cell
        s = s + cell + " "
    s = s + "]"
    return s

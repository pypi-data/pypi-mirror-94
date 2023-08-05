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


def get_round(in_list, num):
    new_l = []
    for i in in_list:
        new_l.append(round(i, num))
    return new_l


def get_max_deviation(in_list):
    lmax = float(max(in_list))
    lmin = float(min(in_list))
    delta = lmax - lmin
    if not delta:
        return 0
    return delta / lmax

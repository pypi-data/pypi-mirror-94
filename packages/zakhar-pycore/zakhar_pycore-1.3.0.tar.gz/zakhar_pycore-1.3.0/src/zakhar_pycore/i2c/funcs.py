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

from .low_level_i2c import i2c_write_byte_data, i2c_read_byte_from
from time import sleep


def cmd(addr, cmd, arg=0x0, wait_for_exec=False):
    if arg:
        i2c_write_byte_data(addr, 0x1, arg)  # write
    i2c_write_byte_data(addr, 0, cmd)  # write
    while (wait_for_exec and i2c_read_byte_from(addr, 0x0)):
        sleep(.1)
    sleep(.1)


def read(addr, reg):
    return i2c_read_byte_from(addr, reg)


def write(addr, reg, val):
    i2c_write_byte_data(addr, reg, val)  # write

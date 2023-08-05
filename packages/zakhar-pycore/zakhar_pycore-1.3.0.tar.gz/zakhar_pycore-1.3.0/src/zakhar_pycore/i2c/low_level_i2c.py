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

from smbus2 import SMBus
from threading import Lock

bus = SMBus(1)  # indicates /dev/i2c-1
i2c_mutex = Lock()


def i2c_read_byte(addr):
    global i2c_mutex
    with i2c_mutex:
        b = bus.read_byte(addr)
        print('Read byte %s from %s' % (hex(b), hex(addr)))
        return b


def i2c_write_byte(addr, val):
    global i2c_mutex
    with i2c_mutex:
        bus.write_byte(addr, val)
        print('Wrote byte %s to %s' % (hex(val), hex(addr)))


def i2c_write_byte_data(addr, reg, val):
    global i2c_mutex
    with i2c_mutex:
        bus.write_byte_data(addr, reg, val)
        print('Wrote byte %s from %s:%s' % (hex(val), hex(addr), hex(reg)))


def i2c_read_byte_from(addr, reg):
    global i2c_mutex
    with i2c_mutex:
        b = bus.read_byte_data(addr, reg)
        return b


def i2cdetect(bus_num):
    b = SMBus(bus_num)
    devs = []
    for a in range(0xff):
        try:
            b.read_byte(a)
            devs.append(hex(a))
        except IOError:
            pass
    return devs

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

from ..dev_types import Register

CMD = Register(0x00, "R/W", "Command register. The device is reading commands from here")
ARG = Register(0x01, "R/W", "Optional argument of the command")
DIST_L = Register(0x02, "RO", "Value of the left distance sensor in cm")
DIST_C = Register(0x03, "RO", "Value of the central distance sensor in cm")
DIST_R = Register(0x04, "RO", "Value of the right distance sensor in cm")
LIGHT_HI = Register(0x05, "RO", "Value of the light sensor, higher part. The less the brighter")
LIGHT_LO = Register(0x06, "RO", "Value of the light sensor, lower part. The less the brighter")

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
MODE = Register(0x02, "RO", "The Mode register")
SPEED = Register(0x03, "RO", "Current speed mode (0-3)")
ANGLE_X_S = Register(0x04, "RO", "Sing of the angle for X (0,1)")
ANGLE_X = Register(0x05, "RO", "The value of the X angle (0-180)")
ANGLE_Y_S = Register(0x05, "RO", "Sing of the angle for Y (0,1)")
ANGLE_Y = Register(0x06, "RO", "The value of the Y angle (0-180)")
ANGLE_Z_S = Register(0x07, "RO", "Sing of the angle for Z (0,1)")
ANGLE_Z = Register(0x08, "RO", "The value of the Z angle (0-180)")

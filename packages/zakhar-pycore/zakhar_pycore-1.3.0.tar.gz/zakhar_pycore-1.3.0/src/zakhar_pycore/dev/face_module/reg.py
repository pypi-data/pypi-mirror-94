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

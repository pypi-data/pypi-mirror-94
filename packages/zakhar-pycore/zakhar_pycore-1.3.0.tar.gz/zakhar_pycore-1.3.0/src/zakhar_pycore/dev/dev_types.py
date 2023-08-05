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

class Register(int):
    def __new__(cls, address: int, *args, **kwargs):
        if address < 0:
            raise ValueError("positive types must not be less than zero")
        return super().__new__(cls, address)

    def __init__(self, address: int, access_type: str = "", comment="", *args, **kwargs) -> None:
        super().__init__()
        self.access_type = access_type
        self.comment = comment


class Interface(str):
    pass

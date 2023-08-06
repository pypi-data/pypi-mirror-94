#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie EveLoop Team, all rights reserved

APPLICATION_VERSION = "0.1.4"
APPLICATION_AUTHORS = ["Tuxa", "Mo"]
APPLICATION_NAME = "Galaxie EveLoop"
APPLICATION_COPYRIGHT = "2021 - Galaxie EveLoop Team all right reserved"

__all__ = [
    "Bus",
    "MainLoop",
]

from glxeveloop.loop import MainLoop
from glxeveloop.bus import Bus
mainloop = MainLoop()

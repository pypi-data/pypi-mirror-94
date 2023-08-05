#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie EveLoop Team, all rights reserved

APPLICATION_VERSION = "0.1.3"
APPLICATION_AUTHORS = ["Tuxa", "Mo"]
APPLICATION_NAME = "Galaxie EveLoop"
APPLICATION_COPYRIGHT = "2021 - Galaxie EveLoop Team all right reserved"

__all__ = [
    "Events",
    "Bus",
    "Hooks",
    "Loop",
    "Timer",
    "Memory",
    "FPS",
    "mainloop"
]

from glxeveloop.events import Events
from glxeveloop.bus import Bus
from glxeveloop.hooks import Hooks
from glxeveloop.loop import Loop
from glxeveloop.timer import Timer
from glxeveloop.memory import Memory
from glxeveloop.fps import FPS

mainloop = Loop()

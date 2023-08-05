#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses.libs.handlers

import os
import logging

logging.basicConfig(
    filename=os.path.realpath(os.path.join(GLXCurses.get_os_temporary_dir(),
                                           "galaxie-curses.log")),
    level=logging.DEBUG,
    format="%(asctime)s, %(levelname)s, %(message)s",
)


class Handlers(
    GLXCurses.libs.handlers.button.HandlersButton,
    GLXCurses.libs.handlers.container.HandlersContainer,
    GLXCurses.libs.handlers.editable.HandlersEditable,
    GLXCurses.libs.handlers.label.HandlersLabel,
    GLXCurses.libs.handlers.textview.HandlersTextView,
    GLXCurses.libs.handlers.widget.HandlersWidget,
):
    def __init__(self):
        GLXCurses.libs.handlers.button.HandlersButton.__init__(self)
        GLXCurses.libs.handlers.container.HandlersContainer.__init__(self)
        GLXCurses.libs.handlers.editable.HandlersEditable.__init__(self)
        GLXCurses.libs.handlers.label.HandlersLabel.__init__(self)
        GLXCurses.libs.handlers.textview.HandlersTextView.__init__(self)
        GLXCurses.libs.handlers.widget.HandlersWidget.__init__(self)

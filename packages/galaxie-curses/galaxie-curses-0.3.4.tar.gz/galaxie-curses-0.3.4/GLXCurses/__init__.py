#!/usr/bin/env python
# -*- coding: utf-8 -*-
# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html

APPLICATION_VERSION = "0.3.4rc2"
APPLICATION_AUTHORS = ['Tuxa', 'Mo']
APPLICATION_NAME = "Galaxie Curses"
APPLICATION_COPYRIGHT = "2016-2021 - Galaxie Curses Team all right reserved"
__all__ = [
    "GLXC",
    "Clipboard",
    "Screen",
    "Colors",
    "Style",
    "Object",
    "Widget",
    "Container",
    "TextTag",
    "TextTagTable",
    "TextBuffer",
    "TextView",
    "Bin",
    "Box",
    "VBox",
    "HBox",
    "Window",
    "RadioButton",
    "CheckButton",
    "Adjustment",
    "Dialog",
    "Application",
    "Frame",
    "MenuBar",
    "Menu",
    "MenuItem",
    "StatusBar",
    "MessageBar",
    "ToolBar",
    "Misc",
    "Label",
    "ProgressBar",
    "HSeparator",
    "VSeparator",
    "EntryBuffer",
    "Editable",
    "Entry",
    "EntryCompletion",
    "Range",
    "Actionable",
    "FileSelect",
    "Image",
    "ImageConvert",
]

from GLXCurses.libs.XDGBaseDirectory import XDGBaseDirectory
from GLXCurses.libs.Utils import *
from GLXCurses.libs.TextAttributes import TextAttributes
from GLXCurses.libs.TextUtils import TextUtils
from GLXCurses.libs.TextFonts import TextFonts
from GLXCurses.Constants import GLXC
from GLXCurses.libs.Movable import Movable
from GLXCurses.libs.Dividable import Dividable
from GLXCurses.libs.File import File
from GLXCurses.libs.ImageConvert import ImageConvert
from GLXCurses.Clipboards import Clipboard
from GLXCurses.libs.TTY import Screen
from GLXCurses.Aera import Area
from GLXCurses.libs.Colors import Colors
from GLXCurses.Style import Style
from GLXCurses.libs.Colorable import Colorable
from GLXCurses.libs.GroupElement import GroupElement
from GLXCurses.libs.Group import Group
from GLXCurses.libs.Groups import Groups
from GLXCurses.libs.Spot import Spot
from GLXCurses.Application import Application
from GLXCurses.Object import Object
from GLXCurses.libs.ChildElement import ChildElement
from GLXCurses.libs.ChildProperty import ChildProperty
from GLXCurses.Widget import Widget
from GLXCurses.Container import Container
from GLXCurses.Bin import Bin
from GLXCurses.Box import Box
from GLXCurses.VBox import VBox
from GLXCurses.HBox import HBox
from GLXCurses.Window import Window
from GLXCurses.Frame import Frame
from GLXCurses.Button import Button
from GLXCurses.RadioButton import RadioButton
from GLXCurses.CheckButton import CheckButton
from GLXCurses.Adjustment import Adjustment
from GLXCurses.Dialog import Dialog
from GLXCurses.MenuBar import MenuBar
from GLXCurses.Menu import Menu
from GLXCurses.MenuItem import MenuItem
from GLXCurses.StatusBar import StatusBar
from GLXCurses.MessageBar import MessageBar
from GLXCurses.ToolBar import ToolBar
from GLXCurses.Misc import Misc
from GLXCurses.TextTag import TextTag
from GLXCurses.TextTagTable import TextTagTable
from GLXCurses.TextBuffer import TextBuffer
from GLXCurses.TextView import TextView
from GLXCurses.Label import Label
from GLXCurses.ProgressBar import ProgressBar
from GLXCurses.HSeparator import HSeparator
from GLXCurses.VSeparator import VSeparator
from GLXCurses.EntryBuffer import EntryBuffer
from GLXCurses.Editable import Editable
from GLXCurses.Entry import Entry
from GLXCurses.EntryCompletion import EntryCompletion
from GLXCurses.Range import Range
from GLXCurses.Actionable import Actionable

# from GLXCurses.VuMeter import VuMeter
from GLXCurses.FileChooserMenu import FileChooserMenu
from GLXCurses.FileChooser import FileSelect
from GLXCurses.Image import Image
from GLXCurses.libs.ImageConvert import ImageConvert

# MainLoop init
from glxeveloop import mainloop

application = Application()

mainloop.debug = True
mainloop.hooks.debug = True
mainloop.timer.debug = True
mainloop.hooks.cmd = application.eveloop_cmd
mainloop.hooks.finalization = application.eveloop_finalization
mainloop.hooks.statement = application.eveloop_input_event
mainloop.hooks.dispatch = application.eveloop_dispatch_application
mainloop.hooks.keyboard_interruption = application.eveloop_keyboard_interruption
mainloop.timer.fps.min = 20.0
mainloop.timer.fps.max = 60.0

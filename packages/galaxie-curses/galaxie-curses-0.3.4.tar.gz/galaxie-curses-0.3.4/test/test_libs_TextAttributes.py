import unittest
import GLXCurses


class TestTextAttributes(unittest.TestCase):
    def setUp(self):
        self.text_attributes = GLXCurses.TextAttributes()

    def test_attributes(self):
        self.text_attributes.attributes = ["Hello.42"]
        self.assertEqual("Hello.42", self.text_attributes.attributes[0])
        self.text_attributes.attributes = ["Hello.42", "Hello.42"]
        self.assertEqual("Hello.42", self.text_attributes.attributes[1])
        self.text_attributes.attributes = None
        self.assertEqual([], self.text_attributes.attributes)
        self.assertRaises(
            TypeError, setattr, self.text_attributes, "attributes", "Hello.42"
        )

    def test_label(self):
        self.text_attributes.label = None
        self.assertEqual("", self.text_attributes.label)
        self.text_attributes.label = "Hello.42"
        self.assertEqual("Hello.42", self.text_attributes.label)
        self.assertRaises(TypeError, setattr, self.text_attributes, "label", 42)

    def test_markdown_is_used(self):
        self.text_attributes.markdown_is_used = None
        self.assertFalse(self.text_attributes.markdown_is_used)
        self.text_attributes.markdown_is_used = True
        self.assertTrue(self.text_attributes.markdown_is_used)
        self.text_attributes.markdown_is_used = False
        self.assertFalse(self.text_attributes.markdown_is_used)
        self.assertRaises(
            TypeError, setattr, self.text_attributes, "markdown_is_used", 42
        )

    def test_mnemonic_char(self):
        self.text_attributes.mnemonic_char = None
        self.assertEqual("_", self.text_attributes.mnemonic_char)
        self.text_attributes.mnemonic_char = "#"
        self.assertEqual("#", self.text_attributes.mnemonic_char)
        self.text_attributes.mnemonic_char = None
        self.assertEqual("_", self.text_attributes.mnemonic_char)
        self.assertRaises(TypeError, setattr, self.text_attributes, "mnemonic_char", 42)
        self.assertRaises(
            ValueError, setattr, self.text_attributes, "mnemonic_char", "42"
        )

    def test_mnemonic_is_used(self):
        self.text_attributes.mnemonic_is_used = None
        self.assertFalse(self.text_attributes.mnemonic_is_used)
        self.text_attributes.mnemonic_is_used = True
        self.assertTrue(self.text_attributes.mnemonic_is_used)
        self.text_attributes.mnemonic_is_used = False
        self.assertFalse(self.text_attributes.mnemonic_is_used)
        self.assertRaises(
            TypeError, setattr, self.text_attributes, "mnemonic_is_used", 42
        )

    def test_mnemonic_use_underline(self):
        self.text_attributes.mnemonic_use_underline = None
        self.assertFalse(self.text_attributes.mnemonic_use_underline)
        self.text_attributes.mnemonic_use_underline = True
        self.assertTrue(self.text_attributes.mnemonic_use_underline)
        self.text_attributes.mnemonic_use_underline = False
        self.assertFalse(self.text_attributes.mnemonic_use_underline)
        self.assertRaises(
            TypeError, setattr, self.text_attributes, "mnemonic_use_underline", 42
        )

    def test_new(self):
        text_attributes_1 = GLXCurses.TextAttributes()
        text_attributes_1.attributes = ["Hello.42"]
        self.assertEqual(["Hello.42"], text_attributes_1.attributes)
        text_attributes_2 = text_attributes_1.new()
        self.assertEqual(text_attributes_1, text_attributes_2)
        self.assertEqual([], text_attributes_1.attributes)

    def test_prepare_attributes(self):
        self.text_attributes = self.text_attributes.new()
        self.text_attributes.label = "Hello.42"
        self.text_attributes.prepare_attributes()
        self.assertEqual(8, len(self.text_attributes.attributes))
        for item in self.text_attributes.attributes:
            self.assertEqual(
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_NORMAL": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "A_PROTECT": False,
                    "A_ITALIC": False,
                    "CURSES_ATTRIBUTES": 0,
                    "CHAR": item["CHAR"],
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                item,
            )
        self.assertEqual(
            len(self.text_attributes.label), len(self.text_attributes.attributes)
        )

        self.text_attributes.label = None
        self.text_attributes.prepare_attributes()
        self.assertEqual(0, len(self.text_attributes.attributes))
        for item in self.text_attributes.attributes:
            self.assertEqual("Hello", item)

    def test_parse_markdown_with_mnemonic(self):
        self.text_attributes.new()
        self.assertEqual(0, len(self.text_attributes.attributes))
        self.text_attributes.label = "***_Hello.++42++***"
        self.text_attributes.prepare_attributes()
        self.assertEqual(
            len(self.text_attributes.attributes), len(self.text_attributes.attributes)
        )
        self.assertEqual(19, len(self.text_attributes.attributes))
        self.text_attributes.mnemonic_use_underline = True
        self.text_attributes.parse_markdown_with_mnemonic()
        self.assertEqual(
            [
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "*",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "*",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "*",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "_",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "H",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": True,
                    "UNDERLINE": True,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "e",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "l",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "l",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "o",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": ".",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "+",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "+",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": True,
                    "CHAR": "4",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": True,
                    "CHAR": "2",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "+",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "+",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "*",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "*",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "*",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
            ],
            self.text_attributes.attributes,
        )

    def test_parse_markdown_with_no_mnemonic(self):
        self.text_attributes.new()
        self.assertEqual(0, len(self.text_attributes.attributes))
        self.text_attributes.label = "**_Hello.++42++_**"
        self.text_attributes.prepare_attributes()
        self.assertEqual(
            len(self.text_attributes.attributes), len(self.text_attributes.attributes)
        )
        self.assertEqual(18, len(self.text_attributes.attributes))
        self.text_attributes.mnemonic_use_underline = True
        self.text_attributes.parse_markdown_with_no_mnemonic()
        self.assertEqual(
            [
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "*",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "*",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "_",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "H",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "e",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "l",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "l",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "o",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": ".",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "+",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "+",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": True,
                    "CHAR": "4",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": True,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": True,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": True,
                    "CHAR": "2",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "+",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "+",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "_",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "*",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_ITALIC": False,
                    "A_NORMAL": False,
                    "A_PROTECT": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "CHAR": "*",
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": True,
                    "MNEMONIC": False,
                },
            ],
            self.text_attributes.attributes,
        )

    def test_parse_text(self):
        self.text_attributes = self.text_attributes.new()
        self.text_attributes.label = "**_Hello.42**"
        self.text_attributes.mnemonic_is_used = True
        self.assertEqual(0, len(self.text_attributes.attributes))
        self.text_attributes.parse_text()
        self.text_attributes.mnemonic_is_used = True
        self.text_attributes.mnemonic_use_underline = True
        self.text_attributes.parse_text()
        self.assertFalse(self.text_attributes.attributes[0]["HIDDEN"])
        self.assertEqual("*", self.text_attributes.attributes[0]["CHAR"])
        self.assertFalse(self.text_attributes.attributes[1]["HIDDEN"])
        self.assertEqual("*", self.text_attributes.attributes[1]["CHAR"])
        self.assertFalse(self.text_attributes.attributes[0]["HIDDEN"])
        self.assertEqual("*", self.text_attributes.attributes[0]["CHAR"])
        self.assertFalse(self.text_attributes.attributes[1]["HIDDEN"])
        self.assertEqual("*", self.text_attributes.attributes[1]["CHAR"])
        self.assertEqual("H", self.text_attributes.attributes[3]["CHAR"])
        self.assertTrue(self.text_attributes.attributes[2]["HIDDEN"])
        self.assertTrue(self.text_attributes.attributes[3]["A_UNDERLINE"])
        self.assertFalse(self.text_attributes.attributes[3]["A_BOLD"])
        self.assertFalse(self.text_attributes.attributes[3]["A_ITALIC"])

    def test_parse(self):
        self.text_attributes = self.text_attributes.new()
        self.text_attributes.parse(
            label="**_Hello.42_**",
            markdown_is_used=True,
            mnemonic_is_used=False,
            mnemonic_char=None,
            mnemonic_use_underline=None,
        )
        self.assertTrue(self.text_attributes.attributes[0]["HIDDEN"])
        self.assertFalse(self.text_attributes.attributes[3]["MNEMONIC"])
        self.text_attributes.parse(
            label="**_Hello.42_**",
            markdown_is_used=True,
            mnemonic_is_used=True,
            mnemonic_char=None,
            mnemonic_use_underline=None,
        )
        self.assertTrue(self.text_attributes.attributes[0]["HIDDEN"])
        self.assertTrue(self.text_attributes.attributes[2]["HIDDEN"])
        self.assertFalse(self.text_attributes.attributes[3]["HIDDEN"])
        self.assertTrue(self.text_attributes.attributes[3]["MNEMONIC"])
        self.text_attributes.parse(
            label="**_Hello.42**",
            markdown_is_used=False,
            mnemonic_is_used=False,
            mnemonic_char=None,
            mnemonic_use_underline=None,
        )
        self.assertFalse(self.text_attributes.attributes[0]["HIDDEN"])
        self.assertFalse(self.text_attributes.attributes[3]["MNEMONIC"])
        self.text_attributes.parse(
            label="**_Hello.42**",
            markdown_is_used=False,
            mnemonic_is_used=True,
            mnemonic_char=None,
            mnemonic_use_underline=None,
        )
        self.assertFalse(self.text_attributes.attributes[0]["HIDDEN"])
        self.assertTrue(self.text_attributes.attributes[3]["MNEMONIC"])


if __name__ == "__main__":
    unittest.main()

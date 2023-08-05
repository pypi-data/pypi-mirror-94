import unittest
import GLXCurses


class TestTextUtils(unittest.TestCase):
    def setUp(self):
        self.text_utils = GLXCurses.TextUtils()

    def test_height(self):
        self.assertEqual(24, self.text_utils.height)
        self.text_utils.height = 42
        self.assertEqual(42, self.text_utils.height)
        self.text_utils.height = None
        self.assertEqual(24, self.text_utils.height)

        self.assertRaises(TypeError, setattr, self.text_utils, "height", "Hello.42")

    def test_lines(self):
        self.text_utils.lines = None
        self.assertEqual([], self.text_utils.lines)
        self.text_utils.lines = ["42"]
        self.assertEqual(["42"], self.text_utils.lines)
        self.text_utils.lines = None
        self.assertEqual([], self.text_utils.lines)
        self.assertRaises(TypeError, setattr, self.text_utils, "lines", "Hello.42")

    def test_text(self):
        self.text_utils.text = None
        self.assertEqual("", self.text_utils.text)
        self.text_utils.text = "Hello.42"
        self.assertEqual("Hello.42", self.text_utils.text)
        self.assertRaises(TypeError, setattr, self.text_utils, "text", 42)

    def test_width(self):
        self.assertEqual(80, self.text_utils.width)
        self.text_utils.width = 42
        self.assertEqual(42, self.text_utils.width)
        self.text_utils.width = None
        self.assertEqual(80, self.text_utils.width)

        self.assertRaises(TypeError, setattr, self.text_utils, "width", "Hello.42")

    def test_wrap(self):
        self.text_utils.wrap = None
        self.assertFalse(self.text_utils.wrap)
        self.text_utils.wrap = False
        self.assertFalse(self.text_utils.wrap)
        self.text_utils.wrap = True
        self.assertTrue(self.text_utils.wrap)
        self.assertRaises(TypeError, setattr, self.text_utils, "wrap", "Hello.42")

    def test_wrap_mode(self):
        self.text_utils.wrap_mode = None
        self.assertEqual(GLXCurses.GLXC.WRAP_WORD, self.text_utils.wrap_mode)
        for mode in GLXCurses.GLXC.WrapMode:
            self.text_utils.wrap_mode = mode
            self.assertEqual(mode, self.text_utils.wrap_mode)
        self.text_utils.wrap_mode = GLXCurses.GLXC.WRAP_WORD
        self.assertEqual(GLXCurses.GLXC.WRAP_WORD, self.text_utils.wrap_mode)
        self.assertRaises(TypeError, setattr, self.text_utils, "wrap_mode", 42)
        self.assertRaises(ValueError, setattr, self.text_utils, "wrap_mode", "Hello.42")

    def test_text_wrap(self):
        self.text_utils.text = (
            "How does it work?\n"
            "   Well, the reduce\n"
            "* A Quick Guide to GPLv3\n"
            "* Why Upgrade to GPLv3\n"
            "* Frequently Asked Questions about the GNU licenses\n"
            "* How to use GNU licenses for your own software\n"
            "* Translations of the GPL\n"
            "* The GPL in other formats: plain __text, Texinfo, LaTeX, standalone HTML, \n"
            "ODF, Docbook v4 or v5, Markdown, and RTF\n"
            "* GPLv3 logos to use with your project\n"
            "* Old versions of the GNU GPL\n"
            "* What to do if you see a possible GPL violation\n"
        )
        self.text_utils.wrap = False
        self.assertEqual(
            [
                "How does it work?",
                "   Well, the reduce",
                "* A Quick Guide to GPLv3",
                "* Why Upgrade to GPLv3",
                "* Frequently Asked Questions about the GNU licenses",
                "* How to use GNU licenses for your own software",
                "* Translations of the GPL",
                "* The GPL in other formats: plain __text, Texinfo, LaTeX, standalone HTML, ",
                "ODF, Docbook v4 or v5, Markdown, and RTF",
                "* GPLv3 logos to use with your project",
                "* Old versions of the GNU GPL",
                "* What to do if you see a possible GPL violation",
            ],
            self.text_utils.text_wrap(),
        )
        self.text_utils.wrap = True
        self.text_utils.width = 10
        self.text_utils.wrap_mode = GLXCurses.GLXC.WRAP_WORD_CHAR
        self.assertEqual(
            ['How does',
             'it work?',
             '   Well,',
             'the reduce',
             '* A Quick',
             'Guide to',
             'GPLv3',
             '* Why',
             'Upgrade to',
             'GPLv3',
             '*',
             'Frequently',
             'Asked',
             'Questions',
             'about the',
             'GNU',
             'licenses',
             '* How to',
             'use GNU',
             'licenses',
             'for your',
             'own',
             'software',
             '* Translat',
             'ions of',
             'the GPL'],
            self.text_utils.text_wrap(),
        )
        self.text_utils.width = 20
        self.assertEqual(
            ['How does it work?',
             '   Well, the reduce',
             '* A Quick Guide to',
             'GPLv3',
             '* Why Upgrade to',
             'GPLv3',
             '* Frequently Asked',
             'Questions about the',
             'GNU licenses',
             '* How to use GNU',
             'licenses for your',
             'own software',
             '* Translations of',
             'the GPL',
             '* The GPL in other',
             'formats: plain',
             '__text, Texinfo,',
             'LaTeX, standalone',
             'HTML,',
             'ODF, Docbook v4 or',
             'v5, Markdown, and',
             'RTF',
             '* GPLv3 logos to use',
             'with your project',
             '* Old versions of',
             'the GNU GPL'],
            self.text_utils.text_wrap(),
        )


if __name__ == "__main__":
    unittest.main()

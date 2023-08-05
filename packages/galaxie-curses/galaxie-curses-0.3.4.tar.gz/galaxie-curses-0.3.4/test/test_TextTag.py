import unittest

import GLXCurses


class TestTextTag(unittest.TestCase):
    def test_accumulative_margin(self):
        text_tag = GLXCurses.TextTag()
        self.assertFalse(text_tag.accumulative_margin)

        text_tag.accumulative_margin = True
        self.assertTrue(text_tag.accumulative_margin)

        text_tag.accumulative_margin = None
        self.assertFalse(text_tag.accumulative_margin)

        self.assertRaises(TypeError, setattr, text_tag, "accumulative_margin", 42)

    def test_background(self):
        text_tag = GLXCurses.TextTag()
        self.assertEqual("BLUE", text_tag.background)

        text_tag.background = "WHITE"
        self.assertEqual("WHITE", text_tag.background)

        text_tag.background = None
        self.assertEqual("BLUE", text_tag.background)

        self.assertRaises(TypeError, setattr, text_tag, "background", 42)

    def test_background_full_height(self):
        text_tag = GLXCurses.TextTag()
        self.assertFalse(text_tag.background_full_height)

        text_tag.background_full_height = True
        self.assertTrue(text_tag.background_full_height)

        text_tag.background_full_height = None
        self.assertFalse(text_tag.background_full_height)

        self.assertRaises(TypeError, setattr, text_tag, "background_full_height", 42)

    def test_background_full_height_set(self):
        text_tag = GLXCurses.TextTag()
        self.assertFalse(text_tag.background_full_height_set)

        text_tag.background_full_height_set = True
        self.assertTrue(text_tag.background_full_height_set)

        text_tag.background_full_height_set = None
        self.assertFalse(text_tag.background_full_height_set)

        self.assertRaises(
            TypeError, setattr, text_tag, "background_full_height_set", 42
        )

    def test_background_rgb(self):
        text_tag = GLXCurses.TextTag()

        self.assertEqual({"r": 0, "g": 0, "b": 255}, text_tag.background_rgb)

        text_tag.background_rgb = {"r": 0, "g": 255, "b": 0}
        self.assertEqual({"r": 0, "g": 255, "b": 0}, text_tag.background_rgb)

        text_tag.background_rgb = None
        self.assertEqual({"r": 0, "g": 0, "b": 255}, text_tag.background_rgb)

        self.assertRaises(TypeError, setattr, text_tag, "background_rgb", 42)

    def test_background_set(self):
        text_tag = GLXCurses.TextTag()
        self.assertFalse(text_tag.background_set)

        text_tag.background_set = True
        self.assertTrue(text_tag.background_set)

        text_tag.background_set = None
        self.assertFalse(text_tag.background_set)

        self.assertRaises(TypeError, setattr, text_tag, "background_set", 42)

    def test_direction(self):
        text_tag = GLXCurses.TextTag()
        self.assertEqual(text_tag.direction, GLXCurses.GLXC.TEXT_DIR_NONE)

        text_tag.direction = GLXCurses.GLXC.TEXT_DIR_LTR
        self.assertEqual(text_tag.direction, GLXCurses.GLXC.TEXT_DIR_LTR)

        text_tag.direction = GLXCurses.GLXC.TEXT_DIR_RTL
        self.assertEqual(text_tag.direction, GLXCurses.GLXC.TEXT_DIR_RTL)

        text_tag.direction = None
        self.assertEqual(text_tag.direction, GLXCurses.GLXC.TEXT_DIR_NONE)

        text_tag.direction = "left-to-right"
        self.assertEqual(text_tag.direction, GLXCurses.GLXC.TEXT_DIR_LTR)

        text_tag.direction = "right-to-left"
        self.assertEqual(text_tag.direction, GLXCurses.GLXC.TEXT_DIR_RTL)

        self.assertRaises(TypeError, setattr, text_tag, "direction", 42)
        self.assertRaises(TypeError, setattr, text_tag, "direction", "Hello.42")

    def test_editable(self):
        text_tag = GLXCurses.TextTag()
        self.assertTrue(text_tag.editable)

        text_tag.editable = False
        self.assertFalse(text_tag.editable)

        text_tag.editable = None
        self.assertTrue(text_tag.editable)

        self.assertRaises(TypeError, setattr, text_tag, "editable", 42)

    def test_editable_set(self):
        text_tag = GLXCurses.TextTag()
        self.assertFalse(text_tag.editable_set)

        text_tag.editable_set = True
        self.assertTrue(text_tag.editable_set)

        text_tag.editable_set = None
        self.assertFalse(text_tag.editable_set)

        self.assertRaises(TypeError, setattr, text_tag, "editable_set", 42)


if __name__ == "__main__":
    unittest.main()

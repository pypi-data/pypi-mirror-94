import unittest
import GLXCurses


class TestColorable(unittest.TestCase):

    def test_background_color_normal(self):
        colorable = GLXCurses.Colorable()
        colorable.background_color_normal = (0, 0, 0)

        self.assertEqual((0, 0, 0), colorable.background_color_normal)

        colorable.background_color_normal = None
        self.assertEqual((0, 0, 255), colorable.background_color_normal)

        self.assertRaises(TypeError, setattr, colorable, "background_color_normal", 42)

    def test_foreground_color_normal(self):
        colorable = GLXCurses.Colorable()
        colorable.foreground_color_normal = (0, 0, 255)

        self.assertEqual((0, 0, 255), colorable.foreground_color_normal)

        colorable.foreground_color_normal = None
        self.assertEqual((180, 180, 180), colorable.foreground_color_normal)

        self.assertRaises(TypeError, setattr, colorable, "foreground_color_normal", 42)

    def test_background_color_prelight(self):
        colorable = GLXCurses.Colorable()
        colorable.background_color_prelight = (0, 0, 0)

        self.assertEqual((0, 0, 0), colorable.background_color_prelight)

        colorable.background_color_prelight = None
        self.assertEqual((0, 255, 255), colorable.background_color_prelight)

        self.assertRaises(
            TypeError, setattr, colorable, "background_color_prelight", 42
        )

    def test_foreground_color_prelight(self):
        colorable = GLXCurses.Colorable()
        colorable.foreground_color_prelight = (0, 255, 255)

        self.assertEqual((0, 255, 255), colorable.foreground_color_prelight)

        colorable.foreground_color_prelight = None
        self.assertEqual((0, 0, 0), colorable.foreground_color_prelight)

        self.assertRaises(
            TypeError, setattr, colorable, "foreground_color_prelight", 42
        )


if __name__ == "__main__":
    unittest.main()

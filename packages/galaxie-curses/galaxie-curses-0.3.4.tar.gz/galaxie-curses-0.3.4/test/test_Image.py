import unittest
import GLXCurses
import os


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.image = GLXCurses.Image()
        self.image.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "glxcurses.png")
        self.image.load_image()

    def test_data(self):
        self.image.data = None
        self.assertTrue(self.image.data == [])
        self.image.data.append('Hello')
        self.image.data.append('42')
        self.assertTrue(self.image.data == ['Hello', '42'])
        self.image.data = None
        self.assertTrue(self.image.data == [])

        self.assertRaises(TypeError, setattr, self.image, "data", "Hello.42")

    def test_hsp_debug(self):
        self.image.hsp_debug = None
        self.assertTrue(self.image.hsp_debug == [])
        self.image.hsp_debug.append('Hello')
        self.image.hsp_debug.append('42')
        self.assertTrue(self.image.hsp_debug == ['Hello', '42'])
        self.image.hsp_debug = None
        self.assertTrue(self.image.hsp_debug == [])

        self.assertRaises(TypeError, setattr, self.image, "hsp_debug", "Hello.42")

    def test_width_max(self):
        self.image.width_max = 42
        self.assertEqual(42, self.image.width_max)

        self.image.width_max = None
        self.assertEqual(80, self.image.width_max)

        self.assertRaises(TypeError, setattr, self.image, "width_max", "Hello.42")

    def test_width_original(self):
        self.image.width_original = 42
        self.assertEqual(42, self.image.width_original)

        self.image.width_original = None
        self.assertEqual(80, self.image.width_original)

        self.assertRaises(TypeError, setattr, self.image, "width_original", "Hello.42")

    def test_height_max(self):
        self.image.height_max = 42
        self.assertEqual(42, self.image.height_max)

        self.image.height_max = None
        self.assertEqual(20, self.image.height_max)

        self.assertRaises(TypeError, setattr, self.image, "height_max", "Hello.42")

    def test_height_original(self):
        self.image.height_original = 42
        self.assertEqual(42, self.image.height_original)

        self.image.height_original = None
        self.assertEqual(20, self.image.height_original)

        self.assertRaises(TypeError, setattr, self.image, "height_original", "Hello.42")

    def test_is_resized(self):
        self.image.is_resized = False
        self.assertFalse(self.image.is_resized)

        self.image.is_resized = True
        self.assertTrue(self.image.is_resized)

        self.image.is_resized = None
        self.assertFalse(self.image.is_resized)

        self.assertRaises(TypeError, setattr, self.image, "is_resized", "Hello.42")

    def test_load_image(self):
        self.image.load_image(path=self.image.path)
        self.assertTrue('PIL.PngImagePlugin.PngImageFile' in str(type(self.image.image_object)))
        self.assertEqual(80, self.image.width_original)
        self.assertEqual(23, self.image.height_original)

    def test(self):
        # Black
        self.assertEqual(0, self.image.rgb_to_ansi16(0, 0, 0))
        # Red
        self.assertEqual(1, self.image.rgb_to_ansi16(170, 0, 0))
        # Green
        self.assertEqual(2, self.image.rgb_to_ansi16(0, 170, 0))
        # Yellow
        # self.assertEqual(3, self.image.rgb_to_ansi16(170, 85, 0))
        # TODO make better yellow color test
        self.assertEqual(3, self.image.rgb_to_ansi16(255, 255, 0))
        # Blue
        self.assertEqual(4, self.image.rgb_to_ansi16(0, 0, 170))
        # Magenta
        self.assertEqual(5, self.image.rgb_to_ansi16(170, 0, 170))
        # Cyan
        self.assertEqual(6, self.image.rgb_to_ansi16(0, 170, 170))
        # White
        self.assertEqual(7, self.image.rgb_to_ansi16(170, 170, 170))

    def test_to_data(self):
        self.image.to_data()
        self.image.is_resized = True

        self.assertEqual(960, len(self.image.data))
        self.assertEqual({'char': '█', 'color': 1081344, 'x': 0, 'y': 0}, self.image.data[0])
        self.assertEqual({'char': '█', 'color': 1081344, 'x': 21, 'y': 7}, self.image.data[581])

        max_x_found = 0
        max_y_found = 0
        for item in self.image.data:
            if max_x_found <= item['x']:
                max_x_found = item['x']

            if max_y_found <= item['y']:
                max_y_found = item['y']

        self.assertEqual(self.image.width_original - 1, max_x_found)
        self.assertEqual(int((self.image.height_original - 1) / 2), max_y_found)

        # self.image.width_max = 42
        # self.image.height_max = 42
        #
        # self.image.to_data()
        # max_x_found = 0
        # max_y_found = 0
        # for item in self.image.data:
        #     if max_x_found <= item['x']:
        #         max_x_found = item['x']
        #
        #     if max_y_found <= item['y']:
        #         max_y_found = item['y']
        #
        # self.assertEqual(self.image.width_original - 1, max_x_found)
        # self.assertEqual(self.image.height_original - 1, max_y_found)


if __name__ == "__main__":
    unittest.main()

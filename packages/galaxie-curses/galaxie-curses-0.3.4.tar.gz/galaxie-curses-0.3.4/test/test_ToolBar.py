import unittest
import GLXCurses


class TestToolBar(unittest.TestCase):
    def setUp(self):
        self.win = GLXCurses.Window()
        self.win.title = "ToolBar Tests"
        self.toolbar = GLXCurses.ToolBar()
        GLXCurses.Application().add_window(self.win)
        GLXCurses.Application().toolbar = self.toolbar
        self.toolbar.labels = [
            "Help",
            "Menu",
            "View",
            "Edit",
            "Copy",
            "RenMov",
            "Mkdir",
            "Delete",
            "PullDn",
            "Quit",
        ]

    def test_draw(self):
        GLXCurses.Application().refresh()

    def test_labels(self):
        self.toolbar.labels = None
        self.assertEqual([], self.toolbar.labels)
        self.toolbar.labels = ["Help"]
        self.assertEqual([{"id": " 1", "text": "Help"}], self.toolbar.labels)
        self.toolbar.labels = ["Help", "42"]
        self.assertEqual(
            [{"id": " 1", "text": "Help"}, {"id": " 2", "text": "42"}],
            self.toolbar.labels,
        )
        self.toolbar.labels = [
            "Help",
            "Menu",
            "View",
            "Edit",
            "Copy",
            "RenMov",
            "Mkdir",
            "Delete",
            "PullDn",
            "Quit",
        ]
        self.assertEqual(10, len(self.toolbar.labels))

        for i in self.toolbar.labels:
            self.assertTrue("text" in i)
            self.assertTrue("id" in i)

        self.assertRaises(TypeError, setattr, self.toolbar, "labels", 42)

    def test_buttonbar_init_button_positions(self):
        self.toolbar.width = 80
        self.toolbar.init_button_positions()
        self.assertEqual(8, self.toolbar.labels[0]["end_coord"])

        self.toolbar.width = 50
        self.toolbar.init_button_positions()
        self.assertEqual(7, self.toolbar.labels[0]["end_coord"])

    def test_buttonbar_get_button_width(self):
        self.toolbar.width = 80
        self.toolbar.init_button_positions()
        self.assertEqual(8, self.toolbar.labels[0]["end_coord"])
        self.assertEqual(8, self.toolbar.get_button_width(i=0))
        self.assertEqual(8, self.toolbar.get_button_width(i=1))

        self.assertRaises(TypeError, self.toolbar.get_button_width, i="Hello.42")

    def test_get_button_by_x_coord(self):
        self.toolbar.width = 80
        self.toolbar.init_button_positions()
        self.assertEqual(-1, self.toolbar.get_button_by_x_coord(x=500))
        self.assertEqual(0, self.toolbar.get_button_by_x_coord(x=6))
        self.assertEqual(3, self.toolbar.get_button_by_x_coord(x=25))
        self.assertEqual(8, self.toolbar.get_button_by_x_coord(x=70))

        self.assertRaises(TypeError, self.toolbar.get_button_by_x_coord, x="Hello.42")

    def test_set_label_text(self):
        self.assertRaises(
            TypeError, self.toolbar.set_label_text, idx="42", text="Hello.42"
        )
        self.assertRaises(TypeError, self.toolbar.set_label_text, idx=42, text=42)
        self.toolbar.labels = ["Help"]
        self.assertEqual([{"id": " 1", "text": "Help"}], self.toolbar.labels)
        self.toolbar.set_label_text(idx=0, text="Hello.42")
        self.assertEqual([{"id": " 1", "text": "Hello.42"}], self.toolbar.labels)


if __name__ == "__main__":
    unittest.main()

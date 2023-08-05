import unittest
import GLXCurses


class TestFileChooserMenu(unittest.TestCase):
    def setUp(self):
        self.filechoosermenu = GLXCurses.FileChooserMenu()

    def test_label(self):
        self.filechoosermenu.label = 'Hello.42'
        self.assertEqual('Hello.42', self.filechoosermenu.label)

        self.assertRaises(TypeError, setattr, self.filechoosermenu, 'label', 42)

    def test_history_box_num_cols(self):
        self.filechoosermenu.history_box_num_cols = 42
        self.assertEqual(42, self.filechoosermenu.history_box_num_cols)

        self.assertRaises(TypeError, setattr, self.filechoosermenu, 'history_box_num_cols', 'Hello.42')

    def test_history_dir_list(self):
        self.filechoosermenu.history_dir_list = ['Hello.42']
        self.assertEqual(['Hello.42'], self.filechoosermenu.history_dir_list)

        self.assertRaises(TypeError, setattr, self.filechoosermenu, 'history_dir_list', 'Hello.42')

if __name__ == '__main__':
    unittest.main()

import unittest
import os
from GLXCurses.libs.TTY import Screen


class TestTTY(unittest.TestCase):
    # def test_term_variable(self):
    #
    #     if os.environ.get('TERM'):
    #         del os.environ['TERM']
    #         self.assertIsNone(os.environ.get('TERM'))
    #         import GLXCurses
    #         self.assertEqual('linux', os.environ.get('TERM'))

    def test_cbreak(self):
        screen = Screen()
        # self.assertEqual(True, getattr(screen, 'cbreak'))
        setattr(screen, "cbreak", False)
        self.assertEqual(False, getattr(screen, "cbreak"))
        setattr(screen, "cbreak", True)
        self.assertEqual(True, getattr(screen, "cbreak"))
        setattr(screen, "cbreak", None)
        self.assertEqual(False, getattr(screen, "cbreak"))
        setattr(screen, "cbreak", None)
        self.assertRaises(ValueError, setattr, screen, "cbreak", 42)
        screen.close()

    def test_echo(self):
        screen = Screen()
        # self.assertEqual(False, getattr(screen, 'echo'))
        setattr(screen, "echo", True)
        self.assertEqual(True, getattr(screen, "echo"))
        setattr(screen, "echo", None)
        self.assertEqual(False, getattr(screen, "echo"))
        setattr(screen, "echo", True)
        self.assertEqual(True, getattr(screen, "echo"))
        self.assertRaises(TypeError, setattr, screen, "echo", "42")
        self.assertRaises(TypeError, setattr, screen, "echo", 42.42)
        self.assertRaises(TypeError, setattr, screen, "echo", [])
        self.assertRaises(TypeError, setattr, screen, "echo", {})
        screen.close()

    def test_halfdelay(self):
        screen = Screen()
        # self.assertEqual(None, getattr(screen, 'halfdelay'))
        setattr(screen, "halfdelay", 42)
        self.assertEqual(42, getattr(screen, "halfdelay"))
        setattr(screen, "halfdelay", -42)
        self.assertEqual(1, getattr(screen, "halfdelay"))
        setattr(screen, "halfdelay", 420)
        self.assertEqual(255, getattr(screen, "halfdelay"))
        setattr(screen, "halfdelay", None)
        self.assertEqual(None, getattr(screen, "halfdelay"))
        self.assertRaises(TypeError, setattr, screen, "halfdelay", "Hello.42")
        screen.close()

    def test_intrflush(self):
        screen = Screen()
        setattr(screen, "intrflush", True)
        self.assertEqual(True, getattr(screen, "intrflush"))
        setattr(screen, "intrflush", False)
        self.assertEqual(False, getattr(screen, "intrflush"))
        setattr(screen, "intrflush", None)
        self.assertEqual(False, getattr(screen, "intrflush"))
        self.assertRaises(ValueError, setattr, screen, "intrflush", 42)
        screen.close()

    def test_keypad(self):
        screen = Screen()
        # self.assertEqual(True, getattr(screen, 'keypad'))
        setattr(screen, "keypad", None)
        self.assertEqual(False, getattr(screen, "keypad"))
        setattr(screen, "keypad", True)
        self.assertEqual(True, getattr(screen, "keypad"))
        setattr(screen, "keypad", False)
        self.assertEqual(False, getattr(screen, "keypad"))
        self.assertRaises(ValueError, setattr, screen, "keypad", 42)
        screen.close()

    def test_meta(self):
        screen = Screen()
        # setattr(screen, 'meta', True)
        self.assertEqual(True, getattr(screen, "meta"))
        setattr(screen, "meta", False)
        self.assertEqual(False, getattr(screen, "meta"))
        setattr(screen, "meta", None)
        self.assertEqual(False, getattr(screen, "meta"))
        self.assertRaises(ValueError, setattr, screen, "meta", 42)
        screen.close()

    def test_nodelay(self):
        screen = Screen()
        # self.assertEqual(None, getattr(screen, 'nodelay'))
        setattr(screen, "nodelay", True)
        self.assertEqual(True, getattr(screen, "nodelay"))
        setattr(screen, "nodelay", False)
        self.assertEqual(False, getattr(screen, "nodelay"))
        setattr(screen, "nodelay", None)
        self.assertEqual(False, getattr(screen, "nodelay"))
        self.assertRaises(ValueError, setattr, screen, "nodelay", 42)
        screen.close()

    def test_raw(self):
        screen = Screen()
        # self.assertEqual(None, getattr(screen, 'raw'))
        setattr(screen, "raw", True)
        self.assertEqual(True, getattr(screen, "raw"))
        setattr(screen, "raw", False)
        self.assertEqual(False, getattr(screen, "raw"))
        setattr(screen, "raw", None)
        self.assertEqual(False, getattr(screen, "raw"))
        self.assertRaises(ValueError, setattr, screen, "raw", 42)
        screen.close()

    def test_qiflush(self):
        screen = Screen()
        # self.assertEqual(None, getattr(screen, 'qiflush'))
        setattr(screen, "qiflush", True)
        self.assertEqual(True, getattr(screen, "qiflush"))
        setattr(screen, "qiflush", False)
        self.assertEqual(False, getattr(screen, "qiflush"))
        setattr(screen, "qiflush", None)
        self.assertEqual(False, getattr(screen, "qiflush"))
        self.assertRaises(ValueError, setattr, screen, "qiflush", 42)
        screen.close()

    def test_timeout(self):
        screen = Screen()
        # self.assertEqual(None, getattr(screen, 'timeout'))
        setattr(screen, "timeout", 1)
        self.assertEqual(1, getattr(screen, "timeout"))
        setattr(screen, "timeout", 0)
        self.assertEqual(0, getattr(screen, "timeout"))
        setattr(screen, "timeout", -1)
        self.assertEqual(-1, getattr(screen, "timeout"))
        setattr(screen, "timeout", None)
        self.assertEqual(0, getattr(screen, "timeout"))
        self.assertRaises(TypeError, setattr, screen, "timeout", "Hello.42")
        screen.close()

    def test_check_terminal(self):
        screen = Screen()
        del os.environ["TERM"]

        self.assertRaises(EnvironmentError, screen.check_terminal)

        # xterm
        os.environ["TERM"] = "xterm"
        self.assertTrue(screen.check_terminal())
        del os.environ["TERM"]
        self.assertRaises(EnvironmentError, screen.check_terminal)

        # rvt
        os.environ["TERM"] = "konsole"
        self.assertTrue(screen.check_terminal())
        del os.environ["TERM"]
        self.assertRaises(EnvironmentError, screen.check_terminal)

        # rvt
        os.environ["TERM"] = "rxvt"
        self.assertTrue(screen.check_terminal())
        del os.environ["TERM"]
        self.assertRaises(EnvironmentError, screen.check_terminal)

        # Eterm
        os.environ["TERM"] = "Eterm"
        self.assertTrue(screen.check_terminal())
        del os.environ["TERM"]
        self.assertRaises(EnvironmentError, screen.check_terminal)

        # dtterm
        os.environ["TERM"] = "dtterm"
        self.assertTrue(screen.check_terminal())
        del os.environ["TERM"]
        self.assertRaises(EnvironmentError, screen.check_terminal)

        # screen
        os.environ["TERM"] = "screen"
        os.environ["DISPLAY"] = ":0"
        self.assertTrue(screen.check_terminal())
        del os.environ["TERM"]
        self.assertRaises(EnvironmentError, screen.check_terminal)
        os.environ["TERM"] = "screen"
        del os.environ["DISPLAY"]
        self.assertIsNone(screen.check_terminal())

        screen.close()


if __name__ == "__main__":
    unittest.main()

import unittest
import os
import GLXCurses


class MyTestCase(unittest.TestCase):
    def test_extension(self):
        file = GLXCurses.File()
        file.extension = "cpuinfo"

        self.assertEqual(file.extension, "cpuinfo")

        file.extension = None
        self.assertIsNone(file.extension)

        self.assertRaises(TypeError, setattr, file, "extension", 42)

    def test_name(self):
        file = GLXCurses.File()
        file.name = "cpuinfo"

        self.assertEqual(file.name, "cpuinfo")

        file.name = None
        self.assertIsNone(file.name)

        self.assertRaises(TypeError, setattr, file, "name", 42)

    def test_directory(self):
        file = GLXCurses.File()
        file.directory = "/proc"

        self.assertEqual(file.directory, "/proc")

        file.directory = None
        self.assertIsNone(file.directory)

        self.assertRaises(TypeError, setattr, file, "directory", 42)

    def test_path(self):
        file = GLXCurses.File()
        file.path = "/proc/cpuinfo"

        self.assertEqual(file.path, "/proc/cpuinfo")
        self.assertEqual(file.directory, "/proc")
        self.assertEqual(file.name, "cpuinfo")
        self.assertIsNone(file.extension)

        file.path = "/proc/cpuinfo.txt"

        self.assertEqual("/proc/cpuinfo.txt", file.path)
        self.assertEqual("/proc", file.directory)
        self.assertEqual("cpuinfo", file.name)
        self.assertEqual(".txt", file.extension)

        file.path = "/proc/cpuinfo.txt.gz"

        self.assertEqual(file.path, "/proc/cpuinfo.txt.gz")
        self.assertEqual(file.directory, "/proc")
        self.assertEqual(file.name, "cpuinfo")
        self.assertEqual(file.extension, ".txt.gz")

        file.path = "/proc/.bashrc"

        self.assertEqual(file.path, "/proc/.bashrc")
        self.assertEqual(file.directory, "/proc")
        self.assertEqual(file.name, ".bashrc")
        self.assertIsNone(file.extension)

        file.path = "/proc/.bash.rc"
        self.assertEqual(file.path, "/proc/.bash.rc")
        self.assertEqual(file.directory, "/proc")
        self.assertEqual(file.name, ".bash")
        self.assertEqual(file.extension, ".rc")

        file.path = None
        self.assertIsNone(file.extension)
        self.assertIsNone(file.name)
        self.assertIsNone(file.directory)
        self.assertIsNone(file.path)

        self.assertRaises(TypeError, setattr, file, "path", 42)

    def test_overwrite(self):
        file = GLXCurses.File()
        self.assertFalse(file.overwrite)
        file.overwrite = True
        self.assertTrue(file.overwrite)
        file.overwrite = False
        self.assertFalse(file.overwrite)
        file.overwrite = None
        self.assertFalse(file.overwrite)

        self.assertRaises(TypeError, setattr, file, "overwrite", 42)

    def test_is_binary(self):
        file = GLXCurses.File()
        file.path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "glxcurses.png"
        )
        self.assertTrue(file.is_binary())
        file.path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "glxcurses.txt"
        )
        self.assertFalse(file.is_binary())
        file.path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "glxcurses.i_do_not_exist"
        )
        self.assertRaises(FileNotFoundError, file.is_binary)

    def test_is_text(self):
        file = GLXCurses.File()
        file.path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "glxcurses.png"
        )
        self.assertFalse(file.is_text())
        file.path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "glxcurses.txt"
        )
        self.assertTrue(file.is_text())
        file.path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "glxcurses.i_do_not_exist"
        )
        self.assertRaises(FileNotFoundError, file.is_text)

    def test_found_best_output_file_name(self):
        # Clean everything
        file0_path = os.path.join(
            GLXCurses.get_os_temporary_dir(), "glxcurses-tests-UtilsFile{0}".format("")
        )

        file1_path = os.path.join(
            GLXCurses.get_os_temporary_dir(),
            "glxcurses-tests-UtilsFile{0}".format("-1"),
        )
        file2_path = os.path.join(
            GLXCurses.get_os_temporary_dir(),
            "glxcurses-tests-UtilsFile{0}".format("-2"),
        )
        file3_path = os.path.join(
            GLXCurses.get_os_temporary_dir(),
            "glxcurses-tests-UtilsFile{0}".format("-3"),
        )

        if os.path.isfile(file0_path):
            os.remove(file0_path)
        if os.path.isfile(file1_path):
            os.remove(file1_path)
        if os.path.isfile(file2_path):
            os.remove(file2_path)
        if os.path.isfile(file3_path):
            os.remove(file3_path)

        self.assertFalse(os.path.isfile(file0_path))
        self.assertFalse(os.path.isfile(file1_path))
        self.assertFalse(os.path.isfile(file2_path))
        self.assertFalse(os.path.isfile(file3_path))

        # Create files
        file0 = os.open(file0_path, os.O_RDWR | os.O_CREAT)
        os.close(file0)
        file1 = os.open(file1_path, os.O_RDWR | os.O_CREAT)
        os.close(file1)
        file2 = os.open(file2_path, os.O_RDWR | os.O_CREAT)
        os.close(file2)
        self.assertTrue(os.path.isfile(file0_path))
        self.assertTrue(os.path.isfile(file1_path))
        self.assertTrue(os.path.isfile(file2_path))

        file = GLXCurses.File()
        file.path = file0_path

        file.overwrite = False
        self.assertEqual(file.found_best_output_file_name(), file3_path)

        file.overwrite = True
        self.assertEqual(file.found_best_output_file_name(), file.path)

        # Clean everything
        if os.path.isfile(file0_path):
            os.remove(file0_path)
        if os.path.isfile(file1_path):
            os.remove(file1_path)
        if os.path.isfile(file2_path):
            os.remove(file2_path)
        if os.path.isfile(file3_path):
            os.remove(file3_path)

        self.assertFalse(os.path.isfile(file0_path))
        self.assertFalse(os.path.isfile(file1_path))
        self.assertFalse(os.path.isfile(file2_path))
        self.assertFalse(os.path.isfile(file3_path))

        # Test with extension
        file0_path = os.path.join(
            GLXCurses.get_os_temporary_dir(),
            "glxcurses-tests-UtilsFile{0}.txt".format(""),
        )

        file1_path = os.path.join(
            GLXCurses.get_os_temporary_dir(),
            "glxcurses-tests-UtilsFile{0}.txt".format("-1"),
        )
        file2_path = os.path.join(
            GLXCurses.get_os_temporary_dir(),
            "glxcurses-tests-UtilsFile{0}.txt".format("-2"),
        )
        file3_path = os.path.join(
            GLXCurses.get_os_temporary_dir(),
            "glxcurses-tests-UtilsFile{0}.txt".format("-3"),
        )

        if os.path.isfile(file0_path):
            os.remove(file0_path)
        if os.path.isfile(file1_path):
            os.remove(file1_path)
        if os.path.isfile(file2_path):
            os.remove(file2_path)
        if os.path.isfile(file3_path):
            os.remove(file3_path)

        self.assertFalse(os.path.isfile(file0_path))
        self.assertFalse(os.path.isfile(file1_path))
        self.assertFalse(os.path.isfile(file2_path))
        self.assertFalse(os.path.isfile(file3_path))

        # Create files
        file0 = os.open(file0_path, os.O_RDWR | os.O_CREAT)
        os.close(file0)
        file1 = os.open(file1_path, os.O_RDWR | os.O_CREAT)
        os.close(file1)
        file2 = os.open(file2_path, os.O_RDWR | os.O_CREAT)
        os.close(file2)
        self.assertTrue(os.path.isfile(file0_path))
        self.assertTrue(os.path.isfile(file1_path))
        self.assertTrue(os.path.isfile(file2_path))

        file = GLXCurses.File()
        file.path = file0_path

        file.overwrite = False
        self.assertEqual(file.found_best_output_file_name(), file3_path)

        file.overwrite = True
        self.assertEqual(file.found_best_output_file_name(), file.path)

        # Clean everything
        if os.path.isfile(file0_path):
            os.remove(file0_path)
        if os.path.isfile(file1_path):
            os.remove(file1_path)
        if os.path.isfile(file2_path):
            os.remove(file2_path)
        if os.path.isfile(file3_path):
            os.remove(file3_path)

        self.assertFalse(os.path.isfile(file0_path))
        self.assertFalse(os.path.isfile(file1_path))
        self.assertFalse(os.path.isfile(file2_path))
        self.assertFalse(os.path.isfile(file3_path))


if __name__ == "__main__":
    unittest.main()

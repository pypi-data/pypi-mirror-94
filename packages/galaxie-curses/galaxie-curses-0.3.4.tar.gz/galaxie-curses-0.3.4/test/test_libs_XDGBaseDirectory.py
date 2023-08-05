import unittest

from GLXCurses.libs.Utils import get_os_temporary_dir
from GLXCurses.libs.XDGBaseDirectory import XDGBaseDirectory
from GLXCurses.libs.XDGBaseDirectory import control_directory
import os


class TestXDGBasedir(unittest.TestCase):
    def test_resource(self):
        basedir = XDGBaseDirectory()
        basedir.resource = "Hello"
        self.assertEqual("Hello", basedir.resource)
        basedir.resource = "Hello{0}42".format(os.path.sep)
        self.assertEqual("Hello{0}42".format(os.path.sep), basedir.resource)
        self.assertRaises(TypeError, setattr, basedir, "resource", None)

    def test_set_resource(self):
        basedir = XDGBaseDirectory()
        basedir.set_resource("Hello")
        self.assertEqual("Hello", basedir.resource)
        basedir.set_resource("Hello", "42")
        self.assertEqual("Hello{0}42".format(os.path.sep), basedir.resource)

        self.assertRaises(AssertionError, basedir.set_resource, "/Hello")
        self.assertRaises(TypeError, basedir.set_resource, None)

    def test_XDG_DATA_HOME(self):
        basedir = XDGBaseDirectory()
        os.environ["XDG_DATA_HOME"] = "Hello.42"
        self.assertEqual(
            basedir.xdg_data_home,
            os.path.join(os.path.join(os.path.expanduser("~"), ".local"), "share"),
        )
        del os.environ["XDG_DATA_HOME"]
        os.environ["XDG_DATA_HOME"] = os.environ["HOME"]
        self.assertEqual(basedir.xdg_data_home, os.environ["HOME"])
        del os.environ["XDG_DATA_HOME"]
        self.assertEqual(
            basedir.xdg_data_home,
            os.path.join(os.path.join(os.path.expanduser("~"), ".local"), "share"),
        )

    def test_XDG_CONFIG_HOME(self):
        basedir = XDGBaseDirectory()
        os.environ["XDG_CONFIG_HOME"] = "Hello.42"
        self.assertEqual(
            basedir.xdg_config_home, os.path.join(os.path.expanduser("~"), ".config")
        )
        del os.environ["XDG_CONFIG_HOME"]
        os.environ["XDG_CONFIG_HOME"] = os.environ["HOME"]
        self.assertEqual(basedir.xdg_config_home, os.environ["HOME"])
        del os.environ["XDG_CONFIG_HOME"]
        self.assertEqual(
            basedir.xdg_config_home, os.path.join(os.path.expanduser("~"), ".config")
        )

    def test_XDG_DATA_DIRS(self):
        basedir = XDGBaseDirectory()
        os.environ["XDG_DATA_DIRS"] = "Hello.42"

        self.assertEqual(basedir.xdg_data_home, basedir.xdg_data_dirs)
        del os.environ["XDG_DATA_DIRS"]

        os.environ["XDG_DATA_DIRS"] = "{0}:{0}".format(os.path.expanduser("~"))
        self.assertEqual(
            basedir.xdg_data_dirs,
            "{0}:{1}:{1}".format(basedir.xdg_data_home, os.path.expanduser("~")),
        )
        del os.environ["XDG_DATA_DIRS"]
        self.assertEqual("/usr/local/share/:/usr/share/", basedir.xdg_data_dirs)

    def test_XDG_CONFIG_DIRS(self):
        basedir = XDGBaseDirectory()
        os.environ["XDG_CONFIG_DIRS"] = "Hello.42"

        self.assertEqual(basedir.xdg_config_home, basedir.xdg_config_dirs)
        del os.environ["XDG_CONFIG_DIRS"]

        os.environ["XDG_CONFIG_DIRS"] = "{0}:{0}".format(os.path.expanduser("~"))
        self.assertEqual(
            basedir.xdg_config_dirs,
            "{0}:{1}".format(basedir.xdg_config_home, os.path.expanduser("~")),
        )
        del os.environ["XDG_CONFIG_DIRS"]
        self.assertEqual(
            "{0}:/etc/xdg".format(basedir.xdg_config_home), basedir.xdg_config_dirs
        )

    def test_XDG_CACHE_HOME(self):
        basedir = XDGBaseDirectory()
        os.environ["XDG_CACHE_HOME"] = "Hello.42"
        self.assertEqual(
            basedir.xdg_cache_home, os.path.join(os.path.expanduser("~"), ".cache")
        )
        del os.environ["XDG_CACHE_HOME"]
        os.environ["XDG_CACHE_HOME"] = os.environ["HOME"]
        self.assertEqual(basedir.xdg_cache_home, os.environ["HOME"])
        del os.environ["XDG_CACHE_HOME"]
        self.assertEqual(
            basedir.xdg_cache_home, os.path.join(os.path.expanduser("~"), ".cache")
        )

    def test_XDG_RUNTIME_DIR(self):
        basedir = XDGBaseDirectory()
        if os.environ.get("XDG_RUNTIME_DIR"):
            del os.environ["XDG_RUNTIME_DIR"]

        fallback = os.path.join(
            get_os_temporary_dir(),
            "glxcurses-runtime-dir-fallback-{0}".format(os.geteuid()),
        )
        fallback_fake = os.path.join(
            get_os_temporary_dir(),
            "glxcurses-runtime-dir-fallback-{0}".format("fake42"),
        )
        if os.path.isdir(fallback):
            os.rmdir(fallback)
        self.assertFalse(os.path.isdir(fallback))
        # self.assertWarns(UserWarning, getattr, basedir, 'xdg_runtime_dir')

        self.assertEqual(basedir.xdg_runtime_dir, fallback)
        self.assertTrue(os.path.isdir(fallback))

        # Test link

        if os.path.isdir(fallback):
            os.rmdir(fallback)
        if os.path.isdir(fallback_fake):
            os.rmdir(fallback_fake)
        os.makedirs(fallback_fake)

        os.symlink(fallback_fake, fallback)
        self.assertTrue(os.path.islink(fallback))
        self.assertEqual(basedir.xdg_runtime_dir, fallback)

        self.assertFalse(os.path.islink(fallback))
        self.assertFalse(os.path.isfile(fallback))
        self.assertTrue(os.path.isdir(fallback))

        # Test file
        if os.path.isdir(fallback):
            os.rmdir(fallback)
        if os.path.isdir(fallback_fake):
            os.rmdir(fallback_fake)

        self.assertFalse(os.path.exists(fallback))
        self.assertFalse(os.path.exists(fallback_fake))

        fd = os.open(fallback, os.O_RDWR | os.O_CREAT)
        os.close(fd)
        self.assertTrue(os.path.isfile(fallback))
        self.assertEqual(basedir.xdg_runtime_dir, fallback)

        self.assertFalse(os.path.islink(fallback))
        self.assertFalse(os.path.isfile(fallback))
        self.assertTrue(os.path.isdir(fallback))

        # Test permission
        if os.path.isdir(fallback):
            os.rmdir(fallback)
        if os.path.isdir(fallback_fake):
            os.rmdir(fallback_fake)

        self.assertFalse(os.path.exists(fallback))
        self.assertFalse(os.path.exists(fallback_fake))

        os.makedirs(fallback, mode=0o777)
        self.assertEqual(oct(os.stat(fallback).st_mode)[-3:], "755")
        self.assertEqual(basedir.xdg_runtime_dir, fallback)
        self.assertEqual(oct(os.stat(fallback).st_mode)[-3:], "700")

        if os.environ.get("XDG_RUNTIME_DIR"):
            del os.environ["XDG_RUNTIME_DIR"]
        os.environ["XDG_RUNTIME_DIR"] = fallback
        self.assertEqual(basedir.xdg_runtime_dir, fallback)

        # Clean everything
        if os.path.isdir(fallback):
            os.rmdir(fallback)
        if os.path.isdir(fallback_fake):
            os.rmdir(fallback_fake)

        self.assertFalse(os.path.exists(fallback))
        self.assertFalse(os.path.exists(fallback_fake))

    def test_config_path(self):
        basedir = XDGBaseDirectory()
        basedir.set_resource("Galaxie-tests")
        if os.path.isdir(os.path.join(basedir.xdg_config_home, basedir.resource)):
            os.rmdir(os.path.join(basedir.xdg_config_home, basedir.resource))

        self.assertFalse(
            os.path.isdir(os.path.join(basedir.xdg_config_home, basedir.resource))
        )

        self.assertEqual(
            basedir.config_path, os.path.join(basedir.xdg_config_home, basedir.resource)
        )

        self.assertTrue(
            os.path.isdir(os.path.join(basedir.xdg_config_home, basedir.resource))
        )

        if os.path.isdir(os.path.join(basedir.xdg_config_home, basedir.resource)):
            os.rmdir(os.path.join(basedir.xdg_config_home, basedir.resource))

    def test_data_path(self):
        basedir = XDGBaseDirectory()
        basedir.set_resource("Galaxie-tests")
        if os.path.isdir(os.path.join(basedir.xdg_data_home, basedir.resource)):
            os.rmdir(os.path.join(basedir.xdg_data_home, basedir.resource))

        self.assertFalse(
            os.path.isdir(os.path.join(basedir.xdg_data_home, basedir.resource))
        )

        self.assertEqual(
            basedir.data_path, os.path.join(basedir.xdg_data_home, basedir.resource)
        )

        self.assertTrue(
            os.path.isdir(os.path.join(basedir.xdg_data_home, basedir.resource))
        )

        if os.path.isdir(os.path.join(basedir.xdg_data_home, basedir.resource)):
            os.rmdir(os.path.join(basedir.xdg_data_home, basedir.resource))

    def test_cache_path(self):
        basedir = XDGBaseDirectory()
        basedir.set_resource("Galaxie-tests")
        if os.path.isdir(os.path.join(basedir.xdg_cache_home, basedir.resource)):
            os.rmdir(os.path.join(basedir.xdg_cache_home, basedir.resource))

        self.assertFalse(
            os.path.isdir(os.path.join(basedir.xdg_cache_home, basedir.resource))
        )

        self.assertEqual(
            basedir.cache_path, os.path.join(basedir.xdg_cache_home, basedir.resource)
        )

        self.assertTrue(
            os.path.isdir(os.path.join(basedir.xdg_cache_home, basedir.resource))
        )

        if os.path.isdir(os.path.join(basedir.xdg_cache_home, basedir.resource)):
            os.rmdir(os.path.join(basedir.xdg_cache_home, basedir.resource))

    def test_config_paths(self):
        basedir = XDGBaseDirectory()
        basedir.set_resource("Galaxie-tests")
        if not os.path.isdir(os.path.join("/tmp", "galaxie-test-1")):
            os.mkdir(os.path.join("/tmp", "galaxie-test-1"))
        if not os.path.isdir(os.path.join("/tmp", "galaxie-test-1", basedir.resource)):
            os.mkdir(os.path.join("/tmp", "galaxie-test-1", basedir.resource))
        if not os.path.isdir(os.path.join("/tmp", "galaxie-test-2")):
            os.mkdir(os.path.join("/tmp", "galaxie-test-2"))
        if not os.path.isdir(os.path.join("/tmp", "galaxie-test-2", basedir.resource)):
            os.mkdir(os.path.join("/tmp", "galaxie-test-2", basedir.resource))

        os.environ["XDG_CONFIG_DIRS"] = ":".join(
            [
                os.path.join("/tmp", "galaxie-test-1"),
                os.path.join("/tmp", "galaxie-test-2"),
            ]
        )

        self.assertEqual(
            basedir.config_paths[0],
            os.path.join(basedir.xdg_config_home, basedir.resource),
        )
        self.assertEqual(len(basedir.config_paths), 3)
        del os.environ["XDG_CONFIG_DIRS"]

        if os.path.isdir(os.path.join("/tmp", "galaxie-test-1", basedir.resource)):
            os.rmdir(os.path.join("/tmp", "galaxie-test-1", basedir.resource))
            os.rmdir(os.path.join("/tmp", "galaxie-test-1"))
        if os.path.isdir(os.path.join("/tmp", "galaxie-test-2", basedir.resource)):
            os.rmdir(os.path.join("/tmp", "galaxie-test-2", basedir.resource))
            os.rmdir(os.path.join("/tmp", "galaxie-test-2"))

    def test_data_paths(self):
        basedir = XDGBaseDirectory()
        basedir.set_resource("Galaxie-tests")
        if not os.path.isdir(os.path.join("/tmp", "galaxie-test-1")):
            os.mkdir(os.path.join("/tmp", "galaxie-test-1"))
        if not os.path.isdir(os.path.join("/tmp", "galaxie-test-1", basedir.resource)):
            os.mkdir(os.path.join("/tmp", "galaxie-test-1", basedir.resource))
        if not os.path.isdir(os.path.join("/tmp", "galaxie-test-2")):
            os.mkdir(os.path.join("/tmp", "galaxie-test-2"))
        if not os.path.isdir(os.path.join("/tmp", "galaxie-test-2", basedir.resource)):
            os.mkdir(os.path.join("/tmp", "galaxie-test-2", basedir.resource))

        os.environ["XDG_DATA_DIRS"] = ":".join(
            [
                os.path.join("/tmp", "galaxie-test-1"),
                os.path.join("/tmp", "galaxie-test-2"),
            ]
        )
        self.assertEqual(
            basedir.data_paths[0], os.path.join(basedir.xdg_data_home, basedir.resource)
        )
        self.assertEqual(len(basedir.data_paths), 3)
        del os.environ["XDG_DATA_DIRS"]

        if os.path.isdir(os.path.join("/tmp", "galaxie-test-1", basedir.resource)):
            os.rmdir(os.path.join("/tmp", "galaxie-test-1", basedir.resource))
            os.rmdir(os.path.join("/tmp", "galaxie-test-1"))
        if os.path.isdir(os.path.join("/tmp", "galaxie-test-2", basedir.resource)):
            os.rmdir(os.path.join("/tmp", "galaxie-test-2", basedir.resource))
            os.rmdir(os.path.join("/tmp", "galaxie-test-2"))

    def test_control_directory(self):
        basedir = XDGBaseDirectory()
        basedir.set_resource("Galaxie-tests")

        fallback = os.path.join(
            get_os_temporary_dir(),
            "glxcurses-runtime-dir-fallback-{0}".format(os.geteuid()),
        )
        if os.path.isdir(fallback):
            os.rmdir(fallback)
        self.assertFalse(os.path.exists(fallback))

        control_directory(directory=fallback)
        self.assertTrue(os.path.exists(fallback))

        self.assertRaises(TypeError, control_directory, directory=None)
        self.assertRaises(TypeError, control_directory, directory=fallback, mode=None)

        if os.path.isdir(fallback):
            os.rmdir(fallback)
        self.assertFalse(os.path.exists(fallback))


if __name__ == "__main__":
    unittest.main()

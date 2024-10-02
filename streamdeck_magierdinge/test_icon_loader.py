import unittest
from icon_loader import load_icon


class IconLoaderTest(unittest.TestCase):
    def test_something(self):
        icon = load_icon('local_florist')
        self.assertIsNotNone(icon)


if __name__ == '__main__':
    unittest.main()

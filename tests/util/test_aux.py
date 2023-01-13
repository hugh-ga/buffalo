import unittest

from buffalo.misc import aux


class TestOption(unittest.TestCase):
    def test0_init_from_dict(self):
        opt = aux.Option({"string": "str", "int": 1, "float": 0.1})
        self.assertTrue(opt["string"] == opt.string == "str")
        self.assertTrue(opt["int"] == opt.int == 1)
        self.assertTrue(opt["float"] == opt.float == 0.1)


if __name__ == "__main__":
    unittest.main()

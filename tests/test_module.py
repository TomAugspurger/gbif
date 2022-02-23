import unittest

import stactools.gbif


class TestModule(unittest.TestCase):

    def test_version(self):
        self.assertIsNotNone(stactools.gbif.__version__)

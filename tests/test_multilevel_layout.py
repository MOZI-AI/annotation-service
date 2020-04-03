__author__ = "Abdulrahman Semrie<xabush@singularitynet.io>"

import unittest
from utils.multi_level import multi_level_layout
from config import TEST_FOLDER
import os

class TestMLL(unittest.TestCase):

    def setUp(self):
        self.input_file = os.path.join(TEST_FOLDER, "test.json")

    def test_mll(self):
        graph_dict = multi_level_layout(self.input_file)
        self.assertTrue(len(graph_dict) > 0)

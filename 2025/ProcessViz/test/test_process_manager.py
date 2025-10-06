import unittest
from process_manager import *

class TestProcessManager(unittest.TestCase):

    def test_that_list_of_processes_is_of_correct_type(self):
        self.assertIsInstance(get_processes(), dict)
    
    def test_that_VSCode_is_running(self):
        current_processes = get_processes()
        self.assertIn("python.exe", current_processes)
    

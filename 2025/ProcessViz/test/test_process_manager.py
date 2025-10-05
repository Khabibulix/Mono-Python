import unittest
from process_manager import *

class TestProcessManager(unittest.TestCase):

    def test_that_list_of_processes_is_of_correct_type(self):
        self.assertIsInstance(get_all_names_for__running_processes(), list)
    
    def test_that_VSCode_is_running(self):
        current_processes = get_all_names_for__running_processes()
        self.assertIn("Code.exe", current_processes)
    

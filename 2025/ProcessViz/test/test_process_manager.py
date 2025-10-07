import unittest, random
from process_manager import *

class TestProcessManager(unittest.TestCase):

    def test_that_list_of_processes_is_of_correct_type(self):
        self.assertIsInstance(get_processes(), dict)
    
    def test_that_Python_is_running(self):
        current_processes = get_processes()
        self.assertIsNotNone(current_processes["python.exe"])
    
    def test_that_key_is_present_in_datas(self):
        current_processes = get_processes()
        keys = ["PID", "memory usage", "path", "time alive", "status", "connections"]
        self.assertIsNotNone(current_processes["python.exe"].get(random.choice(keys)))
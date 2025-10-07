import unittest, random, psutil
from src.process_manager import *

class TestProcessManager(unittest.TestCase):

    def test_that_list_of_processes_is_of_correct_type(self):
        self.assertIsInstance(get_processes(), dict)
    
    def test_that_System_is_running(self):
        current_processes = get_processes()
        self.assertIsNotNone(current_processes["System"])
    
    def test_that_key_is_present_in_datas(self):
        current_processes = get_processes()
        self.assertIsNotNone(current_processes["python.exe"].get("PID"))
    
    def test_get_infos_for_process_with_pid(self):
        first_five_existing_pid = psutil.pids()[:5]
        self.assertNotEqual(get_infos_for_process_with_pid(random.choice(first_five_existing_pid)), [])
    
    def test_get_processes_correctly_fill_datas(self):
        get_processes()
        self.assertGreater(len(datas), 0)
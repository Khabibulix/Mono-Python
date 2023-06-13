import re

import pytest
import os
import importlib
from samples.Blocker import *

def testing_os_import():
    assert importlib.util.find_spec("os")

def test_host_file():
    assert "\\" in hosts_file_path

def test_reading_host_file():
    assert reading_host_file() is not None

def test_localhost_address():
    assert "127" in localhost

def test_file_size():
    assert size_of_file == 60

def testing_Blocker_method_adding_site():
    bk = Blocker("127")
    assert getattr(bk, "adding_site")

def testing_Blocker_method_deleting_site():
    bk = Blocker("127")
    assert getattr(bk, "deleting_site")

def testing_regex_easy_difficulty():
    ip1 = "10.10.10.10"
    assert checking_for_ip(ip1)

def testing_regex_easy_difficulty_for_second_time():
    ip2 = "10.10.test.10"
    assert checking_for_ip(ip2) is False

def testing_regex_medium_difficulty():
    ip3 = "10.10.256.10"
    assert checking_for_ip(ip3) is False
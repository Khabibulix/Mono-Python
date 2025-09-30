import unittest, random
from basic_connection import *
from utils import *


class TestBasicConnection(unittest.TestCase):

    def test_fetch_data_from_site(self):
        self.assertIsInstance(fetch_data_from_site("http://www.jenesuis.net"), str)

    
    def test_grab_all_links_return_not_empty_array(self):
        soup = creating_soup(fetch_data_from_site("http://jenesuis.net"))
        self.assertGreater(len(grab_all_links_from_existing_soup(soup, "http://jenesuis.net")), 0)
    
    def test_grab_all_links_contains_a_valid_url_for_random_value(self):
        soup = creating_soup(fetch_data_from_site("http://jenesuis.net"))
        self.assertTrue(is_valid_url(random.choice(grab_all_links_from_existing_soup(soup, "http://jenesuis.net"))))
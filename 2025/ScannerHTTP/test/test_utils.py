import unittest
from utils import *

class TestUtilsFunction(unittest.TestCase):
    
    def test_is_file_empty_after_deletion(self):
        delete_content_of_file("output.csv")
        self.assertTrue(is_file_empty("output.csv"))
    
    def test_is_valid_url_with_shitty_url(self):
        self.assertFalse(is_valid_url("httpdr://www.google.com"))

    def test_is_valid_url_with_valid_url(self):
        self.assertTrue(is_valid_url("http://www.google.com"))

    
    def test_extract_index_page(self):
        self.assertEqual(extract_index_page("http://www.google.com/contact"), "http://www.google.com")


if __name__ == "__main__":
    unittest.main()


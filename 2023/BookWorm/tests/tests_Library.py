from ..src.Library import *

import pytest
import os
import mock
import builtins

CURRENT_PATH = os.path.dirname(__file__)
path_to_output_file = os.path.relpath('..\\src\\output.txt', CURRENT_PATH)
library = Library()

def test_possible_choices():
    assert len(POSSIBLE_CHOICES) == 6 and "exit" in POSSIBLE_CHOICES

def test_adding_book():
    current_size_of_file = os.path.getsize(path_to_output_file)
    with mock.patch.object(builtins, 'input', lambda _: 'Emile Zola'):
        library.adding_book()
        assert os.path.getsize(path_to_output_file) > current_size_of_file







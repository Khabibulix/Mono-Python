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
    with mock.patch.object(builtins, 'input', lambda _: 'Emile Zolu'):
        library.adding_book()
        try:
            output_file = open(path_to_output_file, "r")
            print(output_file.read())
        finally:
            output_file.close()







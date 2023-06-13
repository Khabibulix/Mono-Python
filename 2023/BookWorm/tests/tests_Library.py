from ..src.Library import *
from pathlib import Path

import pytest
import os
import mock
import builtins


PATH_TO_BOOKWORM_DIRECTORY = Path(__file__).parents[1]
OUTPUT_FILE_PATH = Path.joinpath(PATH_TO_BOOKWORM_DIRECTORY, "src\output.txt")

# TODO Grab size of file using Pathlib
# current_size_of_file = os.path.getsize(path_to_output_file)
library = Library()

def test_possible_choices():
    assert len(POSSIBLE_CHOICES) == 6 and "exit" in POSSIBLE_CHOICES

def test_adding_book():
    with mock.patch.object(builtins, 'input', lambda _: 'Emile Zola'):
        library.adding_book()
        assert os.path.getsize(path_to_output_file) > current_size_of_file







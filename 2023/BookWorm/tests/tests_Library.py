from ..src.Library import *

from pathlib import Path, WindowsPath
import pytest
import os
import mock
import builtins


PATH_TO_BOOKWORM_DIRECTORY = Path(__file__).parents[1]
OUTPUT_FILE_DIRECTORY = Path.joinpath(PATH_TO_BOOKWORM_DIRECTORY, "src")

current_size_of_file = os.path.getsize(OUTPUT_FILE_DIRECTORY)

library = Library()

def test_possible_choices():
    assert len(POSSIBLE_CHOICES) == 6 and "exit" in POSSIBLE_CHOICES

def test_path_to_output_file_is_correct():
    assert OUTPUT_FILE_DIRECTORY == WindowsPath("C:/Users/33623/Documents/Mono-Python/2023/BookWorm/src")

#CODE FOR TESTING ADD FUNCTION TO FIX
# with mock.patch.object(builtins, 'input', lambda _: 'Emile Zola, Germinal'):
#     library.adding_book(OUTPUT_FILE_DIRECTORY)
#     assert os.path.getsize(OUTPUT_FILE_DIRECTORY) > current_size_of_file







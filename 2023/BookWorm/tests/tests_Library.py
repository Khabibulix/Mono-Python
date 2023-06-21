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

def test_path_to_output_file_is_correct():
    assert OUTPUT_FILE_DIRECTORY == WindowsPath("C:/Users/33623/Documents/Mono-Python/2023/BookWorm/src")

def test_adding_book_without_coma():
    assert library.adding_book("Emile Zola Germinal") == "Missing coma"

def test_adding_book_with_shitty_input():
    assert library.adding_book("To, To") == "Nope"

def test_adding_book_with_correct_input_one():
    assert library.adding_book("Emile Zola, Germinal") == "Germinal written by Emile Zola has been successfully added to library!"

def test_adding_book_with_correct_input_two():
    assert library.adding_book("Rastapopoulos, Memories") == "Memories written by Rastapopoulos has been successfully added to library!"


#     library.adding_book(OUTPUT_FILE_DIRECTORY)
#     assert os.path.getsize(OUTPUT_FILE_DIRECTORY) > current_size_of_file







from ..src.Library import *

from pathlib import Path, WindowsPath
import pytest
import os
import mock
import builtins


PATH_TO_BOOKWORM_DIRECTORY = Path(__file__).parents[1]
OUTPUT_FILE_DIRECTORY = Path.joinpath(PATH_TO_BOOKWORM_DIRECTORY, "src")


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

def test_delete_book_with_value_error():
    assert library.delete_book("e") == "NAN"

def test_delete_book_with_number_too_large():
    LEN = len(open('output.txt', 'r').readlines())
    assert library.delete_book(LEN + 1) == "Number incorrect"

def test_delete_book_with_zero():
    assert library.delete_book(0) == "Number incorrect"







import pytest
from Book_Chooser import Book_Chooser
from data import next_books

bc = Book_Chooser()

def test_choosing_from_list():
    assert bc.choosing_from_list() in next_books

def test_choosing_books_and_preparing_for_output():
    assert str(bc.choosing_book_and_preparing_for_output())

def test_printing_price_informations_about_book():
    assert str(bc.printing_price_informations_about_book()).startswith("https://")


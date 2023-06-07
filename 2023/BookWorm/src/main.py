# TODO: Make I/O
import os
from pprint import pprint #Used for outputting file

IS_FILE_EMPTY = os.path.getsize('output.txt') == 0

#Utilities
def pretty_print(list_to_print):
    """["author", "title"] -> "AUTHOR, title\""""
    for item in list_to_print:
        item[0] = item[0].upper()
        print(', '.join(item))

# #Core functions
def adding_book():
        author = ""
        title = ""

        author = input("Please enter the author: ")
        title = input("Please enter the title: ")

        #Author should be a string, but title could be an int --> 1984
        if len(title) >= 3 and isinstance(author, str) and len(author) > 8:
            try:
                output_file = open('output.txt', 'a')
                output_file.write("\n" + author)
                output_file.write(", " +title)
            finally:
                output_file.close()
        else:
            print("Please enter a correct book/author\n")
            adding_book()

def delete_book:
    try:
        output_file = open('output.txt', 'r')
        print(output_file.read())
        book_deleted = input("Which book do you want to delete?: \n"
                             "To delete the first book, enter 1...")

        if book_deleted and int(book_deleted):
            # TODO !!!Error when empty input
            content_of_file = output_file.readlines()
            book_deleted = content_of_file[book_deleted - 1]
            delete_book_in_output_file(book_deleted)

        else:
            print("Enter the number of the book you want to delete, please")
            delete_book()

    finally:
        output_file.close()
#
#
# def search_for_book(string_to_search):
#     possible_matches = []
#     for item in list_of_books:
#         if string_to_search.lower() in item[0].lower() or string_to_search.lower() in item[1].lower():
#             possible_matches.append(item)
#     print(possible_matches)





# Asking and managing input
possible_choices = ["1", "2", "3","4","exit"]
user_choice = ""
while user_choice != "exit":

    user_choice = input("\nDo you want to look at a book? Press 1. \n"
                        "Do you want to add a book? Press 2 \n"
                        "Do you want to delete a book from the list? Press 3.\n"
                        "Do you want to search for a book? Press 4.\n"
                        "If you want to quit, write exit.\n"
                        )
    if user_choice in possible_choices:

        # We check if the list is empty else we print the list
        try:
            output_file = open('output.txt', 'r')
            if user_choice == "1" and IS_FILE_EMPTY:
                print("The file is empty yet.")
                # TODO Adding option to move directly to adding func
            elif user_choice == "1" and not IS_FILE_EMPTY:
                print(output_file.read())
        finally:
            output_file.close()

        if user_choice == "2":
            adding_book()

        if user_choice == "3":
            delete_book()
        #
        # if user_choice == "4":
        #     searching_input = input("Please enter the name of the author, or the book:\n")
        #     search_for_book(searching_input)
        #     user_consent = input("\nShall we take you back? Y/N:\n")
        #     if user_consent == "Y":
        #         continue

    else:
        print("Not a valid choice!")

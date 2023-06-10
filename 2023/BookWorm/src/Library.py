import os

IS_FILE_EMPTY = os.path.getsize('output.txt') == 0
POSSIBLE_CHOICES = ["1", "2", "3","4","5","exit"]
EMPTY_FILE_MESSAGE = "The file is empty yet"
WELCOME_MESSAGE = "\nDo you want to look your library? Press 1.\n" \
                  "Do you want to add a book? Press 2 \n" \
                  "Do you want to delete a book? Press 3.\n" \
                  "Do you want to search for a book? Press 4.\n" \
                  "Do you want to update a book? Press 5. \n" \
                  "If you want to quit, write exit.\n"

class Library:
    def adding_book(self):
        author = ""
        title = ""

        author = input("Please enter the author: ")
        title = input("Please enter the title: ")

        # Author should be a string, but title could be an int --> 1984
        if len(title) >= 3 and isinstance(author, str) and len(author) > 8:
            try:
                output_file = open('output.txt', 'a')
                output_file.write("\n" + author)
                # TODO: Need to do some basic string editing here, to capitalize all
                output_file.write(", " + title)
            finally:
                output_file.close()
        else:
            print("Please enter a correct book/author\n")
            self.adding_book()

    def delete_book(self):

        try:
            output_file = open('output.txt', 'r')
            if IS_FILE_EMPTY:
                print(EMPTY_FILE_MESSAGE)
                answer = input("Do you want to add a new book?\n y/n")
                if answer == 'y':
                    adding_book()
            print(f"\nHere is the content of your library: \n {output_file.read()}")
            book_to_delete = input("\nWhich book do you want to delete?: \n"
                                   "To delete the first book, enter 1...")

        finally:
            output_file.close()

            try:
                if book_to_delete and int(book_to_delete):

                    try:
                        output_file = open('output.txt', 'r')
                        content_of_file = output_file.readlines()
                        book_to_delete = content_of_file[int(book_to_delete) - 1]

                    finally:
                        output_file.close()

                    try:
                        output_file = open('output.txt', 'w+')
                        for line in content_of_file:
                            if line != book_to_delete:
                                output_file.write(line)

                    finally:
                        output_file.close()

            except:
                print(f"'{book_to_delete}' is not a correct number")
                delete_book()

    def update_book(self):

        try:
            output_file = open('output.txt', "r")

            if IS_FILE_EMPTY:
                print(EMPTY_FILE_MESSAGE)
                answer = input("Do you want to add a new book?y/n\n")
                if answer.lower() == 'y':
                    adding_book()

            print(f"\nHere is the content of your library: \n {output_file.read()}")
            book_to_update = input("\nWhich book do you want to update?: \n"
                                   "To update the first book, enter 1...")

        finally:
            output_file.close()

        try:
            if book_to_update and int(book_to_update):

                try:
                    output_file = open('output.txt', 'r')
                    content_of_file = output_file.readlines()
                    book_to_update = content_of_file[int(book_to_update) - 1]

                finally:
                    output_file.close()

                try:
                    output_file = open('output.txt', 'w')
                    new_book_author = input("What is the author of the new book?:\n")
                    new_book_title = input("What is the title of the new book?:\n")
                    for line in content_of_file:
                        if line != book_to_update:
                            output_file.write(line)
                        else:
                            output_file.write(f"{new_book_author} , {new_book_title}")

                finally:
                    output_file.close()

        except:
            print(f"'{book_to_update}' is not a correct number")
            update_book()

    def search_for_book(self, string_to_search):
        possible_matches = []

        try:
            output_file = open('output.txt', 'r')
            for line in output_file.readlines():
                if string_to_search in line:
                    possible_matches.append(line)

        finally:
            output_file.close()
        print(*possible_matches, sep='\n')

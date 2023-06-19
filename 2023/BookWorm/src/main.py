import Library

def main():
    library = Library.Library()
    user_choice = ""
    while user_choice != "exit":

        user_choice = input(Library.WELCOME_MESSAGE)
        if user_choice in Library.POSSIBLE_CHOICES:

            # We check if the list is empty else we print the list
            try:
                output_file = open('output.txt', 'r')
                if user_choice == "1" and Library.IS_FILE_EMPTY:
                    print(Library.EMPTY_FILE_MESSAGE)
                    # TODO Adding option to move directly to adding func
                elif user_choice == "1" and not Library.IS_FILE_EMPTY:
                    # TODO Need to strip whitespaces and newlines
                    print(output_file.read())

            finally:
                output_file.close()

            if user_choice == "2":
                library.adding_book()

            if user_choice == "3":
                library.delete_book()

            if user_choice == "4":
                if not Library.IS_FILE_EMPTY:
                    searching_input = input("Please enter the name of the author, or the book:\n")
                    library.search_for_book(searching_input)
                    user_consent = input("\nShall we take you back? Y/N:\n")
                    if user_consent == "Y":
                        continue
                else:
                    print(Library.EMPTY_FILE_MESSAGE)

            if user_choice == "5":
                library.update_book()


        else:
            print("Not a valid choice!")

if __name__ == "__main__":
    main()



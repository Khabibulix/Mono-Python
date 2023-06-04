
list_of_books = [["Goggins", "Can't hurt me"],
                 ["Zola", "Germinal"],
                 ["Baudelaire", "Les fleurs du mal"],
                 ["Zola", "La Bête Humaine"]]

def pretty_print(list_to_print):
    """["author", "title"] -> "AUTHOR, title\""""
    for item in list_to_print:
        item[0] = item[0].upper()
        print(', '.join(item))


def adding_book_to_list():
    author = ""
    title = ""

    author = input("Please enter the author: ")
    title = input("Please enter the title: ")

    if isinstance(title, str) and len(title) > 3 and isinstance(author, str) and len(author) > 10:
        list_of_books.append([author, title])
    else:
        print("Please enter a correct book/author\n")
        adding_book_to_list()


def delete_book():
    print(list_of_books)
    book_deleted = input("Which book do you want to delete?: ")
    list_of_books.pop(int(book_deleted) - 1)


def search_for_book(string_to_search):
    possible_matches = []
    for item in list_of_books:
        if string_to_search.lower() in item[0].lower() or string_to_search.lower() in item[1].lower():
            possible_matches.append(item)
    pretty_print(possible_matches)






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
        if user_choice == "1" and len(list_of_books) == 0:
            print("The list is empty yet.")
        if user_choice == "1" and len(list_of_books) > 0:
            pretty_print(list_of_books)

        if user_choice == "2":
            adding_book_to_list()

        if user_choice == "3":
            delete_book()

        if user_choice == "4":
            searching_input = input("Please enter the name of the author, or the book:\n")
            search_for_book(searching_input)
            user_consent = input("Shall we take you back? Y/N:\n")
            if user_consent == "Y":
                continue

    else:
        print("Not a valid choice!")

"""
Différents inputs à checker: Titre et auteur, on veut un titre de moins de 200 caractères, un auteur de moins de 40 caractères

"""


# TODO Ajouter option de recherche

list_of_books = [["Goggins", "Can't hurt me"], ["Zola", "Germinal"]]

# Functions


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
        print("Please enter a correct book/author")
        adding_book_to_list()

    return list_of_books


def delete_book():
    print(list_of_books)
    book_deleted = input("Which book do you want to delete?: ")
    list_of_books.pop(int(book_deleted) - 1)


# Asking and managing input
possible_choices = ["1", "2", "3", "exit"]
user_choice = ""
while user_choice != "exit":

    user_choice = input("\nDo you want to look at a book? Press 1. \n"
                        "Do you want to add a book? Press 2 \n"
                        "Do you want to delete a book from the list? Press 3.\n"
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

    else:
        print("Not a valid choice!")

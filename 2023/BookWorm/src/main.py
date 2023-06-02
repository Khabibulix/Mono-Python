list_of_books = []

# Asking and managing input
possible_choices = ["1", "2", "3"]
user_choice = ""
while user_choice != "exit":
    user_choice = input("\nDo you want to look at a book? Press 1. \n"
                        "Do you want to add a book? Press 2 \n"
                        "Do you want to delete a book from the list? Press 3.\n")
    if user_choice in possible_choices:

        # We check if the list is empty else we print the list
        if user_choice == "1" and len(list_of_books) == 0:
            print("The list is empty yet.")
        if user_choice == "1" and len(list_of_books) > 0:
            # TODO: Make a nicer print!
            print(list_of_books)

        if user_choice == "2":
            author = input("Please enter the author: ")
            title = input("Please enter the title: ")
            list_of_books.append([author, title])

        if user_choice == "3":
            print(list_of_books)
            book_deleted = input("Which book do you want to delete?: ")
            # TODO Adding logic to check for number
            list_of_books.pop(int(book_deleted) - 1)





    else:
        print("Not a valid choice!")

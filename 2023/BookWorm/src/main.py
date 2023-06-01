list_of_books = {}

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
            list_of_books.update({"Book": {"author": author, "title": title}})





    else:
        print("Not a valid choice!")

list_of_books = []

#Asking and managing input
possible_choices = ["1", "2", "3"]
user_choice = ""
while user_choice != "exit":
    user_choice = input("\nDo you want to look at a book? Press 1. \n"
                        "Do you want to add a book? Press 2 \n"
                        "Do you want to delete a book from the list? Press 3.\n")
    if user_choice in possible_choices:
        print(f"You chose {user_choice}!")
    else:
        print("Not a valid choice!")

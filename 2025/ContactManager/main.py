"""
User input correct avec differents choix
Feature pour read fichier existant

Helper function pour valider num de tel?
Tests avec unittest
"""
from Contact import ContactList
from helpers import check_input_for_name, check_input_for_phone_number, check_input_for_file_name

def main():
    contact_list = ContactList({})
    while True:
        user_input = input("\nWelcome in Contact Manager, would you like to?\n" \
        "1) Add a contact?\n" \
        "2) Remove a contact?\n" \
        "3) Search a contact?\n" \
        "4) Modify a contact?\n" \
        "5) Save your contact list?\n" \
        "6) View an existing contact list?\n" \
        "7) Quit?\n" \
        "")
        match user_input:
            case "1":
                #Add
                while True:
                    contact_name_input_for_adding = input("Please enter the full name of the contact to add: ")
                    contact_number_input_for_adding = input("Please enter the number of the contact to add: ")
                    if check_input_for_phone_number and check_input_for_name:
                        contact_list.add_contact(contact_name_input_for_adding, contact_number_input_for_adding)
                        print(f"{contact_name_input_for_adding} successfully added to contact list!\n")
                        break
                    else:
                        print("Sorry the format is incorrect, we need the full name separated by a space and a valid phone number.")
            case "2":
                #Remove
                while True:
                    contact_to_remove = input("\nEnter the full name of the contact you want to delete: ")
                    if check_input_for_name and contact_list.search_contact(contact_to_remove):
                        contact_list.remove_contact(contact_to_remove)
                        print(f"{contact_to_remove} successfully remove from contact list! \n")
                    elif len(contact_list.contacts) == 0:
                        print("Sorry but contact list is actually empty, please add contacts")                    
                    else:
                        print("Sorry the format is incorrect, we need the full name separated by a space")
            case "3":
                while True:
                    contact_to_search = input("\nPlease enter the full name of the contact you want to search:")
                    if check_input_for_name:
                        fetched_contact = contact_list.search_contact(contact_to_search)
                        if fetched_contact is None:
                            print("No contact for this name, returning to menu")
                        else:
                            print(f"The number for {contact_to_search} is {fetched_contact}.")
                        break
                    else:
                        print("Sorry the format is incorrect, we need the full name separated by a space")
            case "4":
                #Modify
                while True:
                    contact_to_modify = input("Please enter the full name of the contact you want to modify: ")
                    if check_input_for_name(contact_to_modify):
                        if contact_list.search_contact(contact_to_modify) is not None:
                            new_number = input(f"Please enter the new number of {contact_to_modify}: ")
                            if check_input_for_phone_number:
                                contact_list.modify_contact(contact_to_modify, new_number)
                                print(f"\nContact {contact_to_modify} succesfully modified")
                                break
                            else:
                                print("Please enter a valid phone number: ")
                        else:
                            print("Hey, contact does not exist, maybe add it first.")
                    else:
                         print("Sorry the format is incorrect, we need the full name separated by a space")
            case "5":
                #Save
                if len(contact_list.contacts) != 0:
                    file_name = input("Please choose a name for the contact list:")
                    if check_input_for_file_name:
                        contact_list.save_contacts(file_name)
                        print(f"{file_name}.csv was succesfully created")
                else:
                    print("\nImpossible to save an empty list")

            case "6":
                #View
                if len(contact_list.contacts) == 0:
                    print("\nContact list is empty for now")
                else:
                    print(contact_list.contacts)
            case "7":
                #Quit
                break
    




if __name__ == "__main__":
    main()

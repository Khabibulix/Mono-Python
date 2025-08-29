"""
User input correct avec differents choix
Feature pour read fichier existant

Helper function pour valider num de tel?
Tests avec unittest
"""
from Contact import ContactList
from helpers import *

def main():
    contact_list = ContactList({})
    while True:
        user_input = input("Welcome in Contact Manager, would you like to?\n" \
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
                    contact_list.add_contact(contact_name_input_for_adding, contact_number_input_for_adding)
            case "2":
                #Remove
                #Careful with empty?
                pass
            case "3":
                #Search
                pass
            case "4":
                #Modify
                pass
            case "5":
                #Save
                pass
            case "6":
                #View
                pass
            case "7":
                #Quit
                break
    # contact_list.add_contact("Phil Lambert", "0622435434")
    # contact_list.add_contact("Arnaud Lefevre", "0690324356")
    # contact_list.add_contact("Damien Dujardin", "0664234398")
    # contact_list.add_contact("Arthur Delabranche", "0622435434")
    # contact_list.save_contacts("contacts")




if __name__ == "__main__":
    main()

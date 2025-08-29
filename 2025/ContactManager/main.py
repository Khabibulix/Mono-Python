"""
Features: Add contact, remove contact, modify contact, search contact
Console app with different choices with inputs
Output in CSV with name and phone number.

Helper function pour valider num de tel?
Tests avec unittest
"""
from Contact import ContactList

def main():
    contact_list = ContactList({})
    contact_list.add_contact("Phil Lambert", "0622435434")
    contact_list.add_contact("Arnaud Lefevre", "0690324356")
    contact_list.add_contact("Damien Dujardin", "0664234398")
    contact_list.add_contact("Arthur Delabranche", "0622435434")
    contact_list.save_contacts("contacts")




if __name__ == "__main__":
    main()

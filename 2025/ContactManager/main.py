"""
Features: Add contact, remove contact, modify contact, search contact
Console app with different choices with inputs
Output in CSV with name and phone number.
"""
from Contact import ContactList

contact_list = ContactList({})
contact_list.add_contact("Phil", "0622435434")
print(contact_list.contacts)

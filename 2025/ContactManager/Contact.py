class ContactList:
    """
    Stocks contact in the form of a dictionary
    @param: (dict) contacts
    """
    def __init__(self, contacts):
        self.contacts = contacts

    def add_contact(self,contact_name, contact_number):
        """
        Add contact to ContactList object
        @param: (string) contact_name
        @param: (string) contact_number
        """
        self.contacts[contact_name] = contact_number

    def search_contact(contact):
        pass

    def remove_contact(contact):
        pass

    def modify_contact(contact):
        pass



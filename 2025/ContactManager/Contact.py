class ContactList:
    """
    Stocks contact in the form of a dictionary
    @param: (dict) contacts
    """
    def __init__(self, contacts):
        self.contacts = contacts

    def add_contact(self,contact_name, contact_number):
        """Add contact to contacts.

        Args:
            contact_name (string): Full name of contact
            contact_number (string): Phone number of contact
        """
        self.contacts[contact_name] = contact_number

    def search_contact(self,contact_name):
        """Search for contact knowing the name

        Args:
            contact_name (string): Full name of contact

        Returns:
            int: Phone number of contact
        """
        return self.contacts.get(contact_name)

    def remove_contact(self, contact_name):
        """Remove contact knowing name

        Args:
            contact_name (string): Full name of contact to remove
        """
        self.contacts.pop(contact_name)

    def modify_contact(self, contact_name, contact_number):
        """Modify contact via his name

        :param contact_name: Full name of contact to modify
        :type contact_name: String
        :param contact_number: Number of modified contact
        :type contact_name: String
        """
        self.contacts[contact_name] = contact_number

    def save_contacts(self):
        pass



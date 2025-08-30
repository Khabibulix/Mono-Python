def check_input_for_name(name):
    """Must be string, separated by space

    :param name: Name to check
    :type name: string
    """
    if " " in name:
        names = name.split(" ")
        if names[0].isalpha() and names[1].isalpha() and len(names[0]) >= 3 and len(names[1]) >= 3:
            return True
        return False
    else:
        return False

def check_input_for_phone_number(number):
    """Checking user input for phone number 

    :param number: Phone number, ten digits beginning by zero
    :type number: string of digits
    """
    if len(number) != 10 or number[0] != "0":
        return False
    else:
        return True

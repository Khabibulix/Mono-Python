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

def check_input_for_file_name(filename):
    """User input checking for filename.
    \n'file' is correct, extension is added after
    Numbers are correct too, but no special characters except '-_'
    Length should be less than 30 chracters

    :param filename: Name choosed by the user
    :type filename: str
    """
    chars_authorized = "-_"
    for letter in filename:
                if letter.isalpha():
                    continue
                elif letter.isascii() and letter not in chars_authorized:
                    return False
                else:
                    return True

    if filename.isalpha():
        if len(filename) <= 30:
            return True
        else:
            return False
    else:
        return False

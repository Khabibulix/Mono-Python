def check_input_for_name(name):
    """Must be string, separated by space

    :param name: Name to check
    :type name: string
    """
    if " " in name:
        names = name.split(" ")
        if names[0].isalpha() and names[1].isalpha() and :
            return True
    else:
        return False
#and " " in name and len(name) >= 3 else False

print(check_input_for_name("Roger"))
print(check_input_for_name("Roger Dupont"))
print(check_input_for_name("Ao Tang"))
print(check_input_for_name("1234"))
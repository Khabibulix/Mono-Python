import os

def cleaning_comas(string):
    """ 
    Replace "," by "." to make float conversion later on
    @param (string) string (Input that will be cleaned)
    @return (string) string
    
    @input 12,4
    @output 12.4
    """
    if isinstance(string, str) and "," in string:
        coma_idx = str(string).find(",")
        string.replace(",", "")   
        return str(string[:coma_idx]) + "." + str(string[coma_idx + 1:])


def is_file_a_valid_txt_file(file):
    """
    @param (String) file
    @return (Boolean) True si file finit par ".txt"
    """
    return new_file_name[-4:] == ".txt"


def checking_if_expenses_file_exists_in_output_files():
    """ 
    Using os.path() to check existence of a file
    @return (Boolean) File is here, if False we'll need to recreate it
    """
    if is_file_a_valid_txt_file:
        return os.path.isfile("./output_files/expenses.txt")

def rename_file(new_name):
    """
    Rename a file
    @param (String) new_name
    """
    os.rename("./output_files/expenses.txt", "./output_files/" + new_name)


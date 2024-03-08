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


def is_string_a_valid_txt_file_name(file):
    """
    @param (String) file
    @return (Boolean) True si file finit par ".txt"
    """
    return file[-4:] == ".txt"

def modifying_file_name_into_valid_text_file_name(file):
    """ 
    @param (String) file (potential invalid file name for text)
    @return (String) file (valid file name)
    @input "test"
    @output "test.txt"
    """
    return file + ".txt"



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


def create_file(new_name="expenses.txt"):
    """ 
    Recreate an output file using input name
    @param (String) new_name (User input name for file)
    """
    file = open("./output_files/" + new_name, "w").close()


def creating_new_budget(file_name):  
    """
    Using user input we recreate a new budget file:
        1) If the file_name is not a valid text file ("text_file.txt"), we change it in adding extension
        2) If expenses.txt exists, we rename it and we recreate it
        3) If it doesn't exists, we create a file which name is file_name
    @param (String) file_name (User input)
    """

    if is_string_a_valid_txt_file_name(file_name):

        if checking_if_expenses_file_exists_in_output_files:
            rename_file(file_name)
            create_file()

        else:
            create_file(file_name)

    else:
        file_name = modifying_file_name_into_valid_text_file_name(file_name)
        creating_new_budget(file_name)

#TODO Fonction entière à revoir!
def asking_for_expense_input(): 
    """ 
    Contains all logic to add input for the function Budget.add_expense
    """   
    input_expense = input("Please enter the amount of the expense: ")
    input_cleaned = helpers.cleaning_comas(input_expense)  
    
    input_description = input("\nPlease enter the description for the expense, now: ")
    
    #TODO Comportement naze ici, il faudrait checker la validité du float avant
    try:
        budget_for_month.add_expense(input_description, float(input_cleaned))
    except ValueError as te:
        #logging.error("User entered a shitty input", te)
        print("Input for expense doesn't seem valid...")

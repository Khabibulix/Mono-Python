from Budget import Budget
import os, sys, logging

logging.basicConfig(
    level=logging.WARNING,
    filename="main.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s"
    )


#____________________________________________________________
# #TODO 
# Faire le choix 3
# Rajouter tests
# AJouter fonction helper qui checke l'existence de expenses.txt, sinon le créer.
# Rajouter data visualisation avec un camembert par exemple
#____________________________________________________________

budget_for_month = Budget(1000)

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


def asking_for_expense_input(): 
    """ 
    Contains all logic to add input for the function Budget.add_expense
    """   
    input_expense = input("Please enter the amount of the expense: ")
    input_cleaned = cleaning_comas(input_expense)  
    input_description = input("\nPlease enter the description for the expense, now: ")
    
    #TODO Comportement naze ici, il faudrait checker la validité du float avant
    try:
        budget_for_month.add_expense(input_description, float(input_cleaned))
    except ValueError as te:
        #logging.error("User entered a shitty input", te)
        print("Input for expense doesn't seem valid...")
            
def does_file_exists(file):
    pass

def main():
    
    #input_budget = input(" How much do you have for this month?\n")
    while True:

        input_instruction_choice = input("\nWhat do you want to do?\n Press 1 to add an expense\n Press 2 to see all expenses for the month\n Press 3 to begin a new budget\n Press 4 to quit\n")
        
        if input_instruction_choice == "1":
            asking_for_expense_input()
           
        elif input_instruction_choice == "2":
            print(budget_for_month.get_expenses())
            print(f"You have {budget_for_month.get_budget_remaining()} euros left!")
        
        elif input_instruction_choice == "3":
            """
            Ici on veut:
            1) sauvegarder le fichier texte/csv ailleurs
            2) supprimer fichier texte pour repartir à zéro
            3) redéfinir un budget initial
            """
            while True:
                new_file_name = input("Please enter the name of the new budget text file: ")
                #TODO Checker si le file expenses.txt existe aussi!
                if new_file_name[-4:] == ".txt":
                    os.rename("./output_files/expenses.txt", "./output_files/" + new_file_name)
                    open("./output_files/expenses.txt").close()
                    break
                else:
                    print("The input must end by .txt")

            while True:
                #TODO Gérer logique pour éviter input foireux ou négatif
                new_initial_budget = input("Enter the new initial budget: ")
                budget_of_the_month = Budget(new_initial_budget)
                try:
                    int(new_initial_budget)
                    break
                except TypeError as te:
                    print("Invalid input")
        
        elif input_instruction_choice == "4":
            print(f"Hope you had a great time, bye!")
            sys.exit()
        else:
            print("Shitty input, sorry.")
    
   


if __name__ == "__main__":
    main()
from Budget import Budget
import sys, os
#____________________________________________________________
# #TODO 
# Faire le choix 3
# Rajouter tests
# Rajouter data visualisation avec un camembert par exemple
#____________________________________________________________
budget_for_month = Budget(1000)

def asking_for_expense_input(): 
    """ 
    Contains all logic to add input for the function Budget.add_expense
    """   
    input_expense = input("Please enter the amount of the expense: ")
    
    #12,4 is now 12.4
    if "," in str(input_expense):
        index_of_coma = str(input_expense).find(",")
        str(input_expense).replace(",", "")   
        input_expense = str(input_expense[:index_of_coma]) + "." + str(input_expense[index_of_coma + 1:])

    input_description = input("\nPlease enter the description for the expense, now: ")
    
    try:
        float(input_expense)
        budget_for_month.add_expense(input_description, input_expense)
    except ValueError as te:
        print("Input for expense doesn't seem valid...")
            


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
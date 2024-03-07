from Budget import Budget
import sys
#____________________________________________________________
# #TODO 
# Mettre données dans un fichier texte ou CSV pour la sauvegarde
# Stocker budget du mois séparément ou en dur, car 
# trop chiant à chaque début de programme
# Supprimer budget du mois dans le fichier programmatiquement
# Faire le choix 3
# Rajouter tests
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
        budget_for_month.add_expense(input_expense, input_description)
    except ValueError as te:
        print("Input for expense doesn't seem valid...")
            


def main():
    
    #input_budget = input(" How much do you have for this month?\n")
    while True:

        input_instruction_choice = input("\nWhat do you want to do? Press 1 to add an expense, Press 2 to see all expenses for the month, Press 4 to quit:\n")
        
        if input_instruction_choice == "1":
            asking_for_expense_input()
            #TODO Add another one?
           
        elif input_instruction_choice == "2":
            budget_for_month.get_representation_for_all_expenses()
            print(f"You have {budget_for_month.get_budget_remaining()} euros left!")
        
        elif input_instruction_choice == "3":
            """
            Ici on veut:
            1) sauvegarder le fichier texte/csv ailleurs
            2) supprimer fichier texte pour repartir à zéro
            3) redéfinir un budget initial
            """
            pass
        
        elif input_instruction_choice == "4":
            print(f"Hope you had a great time, bye!")
            sys.exit()
        else:
            print("Shitty input, sorry.")
    
   


if __name__ == "__main__":
    main()
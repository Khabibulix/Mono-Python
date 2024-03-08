from Budget import Budget
import helpers_functions as helpers
import os, sys, logging

logging.basicConfig(
    level=logging.WARNING,
    filename="main.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s"
    )


#____________________________________________________________
# TODO 
# Rajouter tests
# Rajouter data visualisation avec un camembert par exemple
# Le principe de la data viz serait le suivant, on veut voir combien de sous il nous reste sur le budget initial en mode joli
# Le budget restant ne doit pas être négatif, gérer ce cas!
# Rajouter une helper function qui checke les strings pour éviter pb de paths
# Ajouter fichier texte direct à la classe pour éviter les outputs bizarres
#____________________________________________________________

budget_for_month = Budget(1000)       



def main():
    
    #input_budget = input(" How much do you have for this month?\n")
    while True:

        input_instruction_choice = input("\nWhat do you want to do?\n Press 1 to add an expense\n Press 2 to see all expenses for the month\n Press 3 to begin a new budget\n Press 4 to quit\n")
        
        if input_instruction_choice == "1":
            helpers.asking_for_expense_input()
           
        elif input_instruction_choice == "2":
            print(budget_for_month.get_expenses())
            #TODO Attention au négatif ici!
            print(f"You have {budget_for_month.get_budget_remaining()} euros left!")
        
        elif input_instruction_choice == "3":
            new_file_name = input("Please enter the name of the new budget text file: ")
            helpers.creating_new_budget(new_file_name)                
                

            while True:
                #TODO Gérer logique pour éviter input foireux ou négatif
                #TODO Boucle dans boucle, à chier, go fonction récursive
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
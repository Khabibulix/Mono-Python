import unittest
from Budget import Budget
from helpers_functions import cleaning_comas

class BudgetTests(unittest.TestCase):

    def test_constructor_with_bad_argument(self):
        budget = Budget("test")
        with self.assertRaises(TypeError):
            budget.initial_budget - 10

    def test_add_expense(self):
        budget = Budget(1000)
        #TODO Attention si fichier non existant
        with open("./output_files/expenses.txt", "r") as file:
            current_length_of_expenses = len(file.readlines())
            budget.add_expense("test_expense", 25)
            self.assertGreater(len(file.readlines()), current_length_of_expenses)
            budget.clear_budget()

    def test_get_expenses(self):
        budget = Budget(1000)
        budget.add_expense("test_expense", 25)
        self.assertIsInstance(budget.get_expenses(), list)


    def test_get_budget_remaining_with_two_correct_expenses(self):
        #TODO Logique bizarre ici, je pense qu'on écrase la valeur dans get_budget_remaining
        #TODO Ne doit pas être négatif, ajouter un test pour éviter ça!
        budget = Budget(1000)
        budget.add_expense("Telephone", 79.0)
        budget.add_expense("Switch", 279.0)
        self.assertEqual(budget.get_budget_remaining(), 642.0)
        
    def test_cleaning_comas_in_helpers_functions(self):
        self.assertEqual(cleaning_comas("12,4"), "12.4")
   
unittest.main()
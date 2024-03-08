import unittest
from Budget import Budget

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
        budget = Budget(1000)
        budget.add_expense("Telephone", 79.0)
        budget.add_expense("Switch", 279.0)
        self.assertEqual(budget.get_budget_remaining(), 358.0)
        
   
budget = Budget(1000)
budget.clear_budget()
unittest.main()
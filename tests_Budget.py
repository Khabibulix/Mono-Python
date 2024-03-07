import unittest
from Budget import Budget

class BudgetTests(unittest.TestCase):

    def test_constructor_with_bad_argument(self):
        budget = Budget("test")
        with self.assertRaises(TypeError):
            budget.initial_budget - 10

    def test_add_expense(self):
        budget = Budget(1000)
        current_length_of_expenses = len(budget.get_expenses())
        budget.add_expense(25, "test_expense")
        self.assertTrue(len(budget.get_expenses()), current_length_of_expenses + 1)
    
    def test_get_expenses(self):
        budget = Budget(1000)
        budget.add_expense(25, "test_expense")
        self.assertIsInstance(budget.get_expenses(), list)
    
    def test_get_budget_remaining_with_two_correct_expenses(self):
        budget = Budget(1000)
        budget.add_expense(79.0, "Telephone")
        budget.add_expense(279.0, "Switch")
        self.assertEqual(budget.get_budget_remaining(), 358.0)

   

unittest.main()
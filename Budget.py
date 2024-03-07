class Budget:
    """
    Stocks a list of expenses.
    @param: (float) initial_budget
    """
    def __init__(self, initial_budget):
        self.initial_budget = initial_budget
        self.expenses = []
    
    
    def add_expense(self, expense, expense_description):
        """
        Add expense to expenses list
        @param: (float) expense
        @param: (string) expense_description
        """
        #TODO List length doesnt change, FIX
        return self.expenses.append({"expense":expense, "expense_description":expense_description})
    
    def get_expenses(self):
        """
        Standard getter.
        @return (list) expenses
        """
        if len(self.expenses) == 0:
            print("You have currently no expenses!")
        else:
            return self.expenses
    
    def get_representation_for_all_expenses(self):
        """
        Nicer print, uses self.get_expenses datas.
        """
        for item in self.get_expenses():
            print(f"You bought some {item["expense_description"]} for {item["expense"]} euros!")
    
    def get_budget_remaining(self):
        """
        Performs calculation on self.initial_budget.
        @return (float) budget_total 
        """
        budget_total = 0
        for expense in self.expenses:
            budget_total += expense["expense"]
        return budget_total



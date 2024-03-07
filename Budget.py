class Budget:
    """
    Stocks a list of expenses.
    @param: (float) initial_budget
    """
    def __init__(self, initial_budget):
        self.initial_budget = initial_budget
    
    
    def add_expense(self, expense_description, expense):
        """
        Add expense to expenses list
        @param: (float) expense
        @param: (string) expense_description
        """
        with open("expenses.txt", "a") as file:
            file.write(expense_description + ":" + str(expense) + "\n")
    
    def get_expenses(self):
        """
        Retrieve data from file
        @return (list) expenses
        """
        with open("expenses.txt", "r") as file:
            if file == "":
                print("You have currently no expenses!")
            else:
                return file.readlines()

    def get_budget_remaining(self):
        """
        Performs calculation on self.initial_budget.
        @return (float) budget_total 
        """
        budget_total = 0
        for expense in self.get_expenses():
            #cf forum.checkmk.com/t/internal-error-invalid-literal-for-int-with-base-10-when-opening-main-dashboard/31567/18
            budget_total += int(float(expense.split(":")[1]))
        return budget_total
    
    def clear_budget(self):
        """ 
        Erases the content of the file, will be useful for creating new budget
        """
        open("expenses.txt","w").close()


budget = Budget(1000)
budget.add_expense(expense_description="Cheese", expense=51)
budget.get_budget_remaining()



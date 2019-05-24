import formula


class Revenue:
    def __init__(self, total_revenue, cost_of_revenue):
        self.total_revenue = total_revenue
        self.cost_of_revenue = cost_of_revenue
        self.gross_profit = self.total_revenue - self.cost_of_revenue

    def get_margin(self):
        formula.get_gross_profit_margin(self.gross_profit, self.total_revenue)


class OperatingExpenses:
    def __init__(self,
                 research_development,
                 selling_general_and_administrative,
                 non_recurring,
                 others):
        self.research_development = research_development
        self.selling_general_and_administrative = selling_general_and_administrative
        self.non_recurring = non_recurring
        self.others = others

    def get_total(self):
        return self.research_development + \
               self.selling_general_and_administrative + \
               self.non_recurring + \
               self.others


class OtherIncomeAndExpense:
    def __init__(self, other_expense_or_income, interest_expense, income_tax_expense):
        self.other_expense_or_income = other_expense_or_income
        self.interest_expense = interest_expense
        self.income_tax_expense = income_tax_expense

    def get_total(self):
        return self.other_expense_or_income + self.income_tax_expense + self.income_tax_expense


class IncomeStatement:
    def __init__(self,
                 total_revenue,
                 cost_of_revenue,
                 research_development,
                 selling_general_and_administrative,
                 non_recurring,
                 others,
                 other_expense_or_income,
                 interest_expense,

                 income_tax_expense):
        self.revenue = Revenue(total_revenue, cost_of_revenue)
        self.operating_expense = OperatingExpenses(research_development,
                                                   selling_general_and_administrative,
                                                   non_recurring,
                                                   others)

        self.other_income_or_expense = OtherIncomeAndExpense(other_expense_or_income,
                                                             interest_expense,
                                                             income_tax_expense)
        self.net_income = self.revenue.gross_profit - \
                          self.operating_expense.get_total() - \
                          self.other_income_or_expense.get_total()

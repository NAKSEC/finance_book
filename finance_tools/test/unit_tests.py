import unittest
import sys
sys.path.append("../")
from modules.calculation.incomeStatement import OperatingExpenses, Revenue, IncomeStatement


class TestIncomeStatement(unittest.TestCase):

    def test_revenue(self):
        income = 10000
        cogs = 500
        expected_result_margin = float(income - cogs)/float(income)
        expected_result_profit = income-cogs
        revenue = Revenue(income, cogs)
        self.assertEqual(revenue.get_margin(), expected_result_margin, "Should be %f" % expected_result_margin)
        self.assertEqual(revenue.gross_profit, expected_result_profit, "Should be %f" % expected_result_profit)

    def test_operating_expense(self):
        r_and_d = 1000
        selling_g_and_admin = 100
        non_recurring = 200
        others = 100
        expected = r_and_d + selling_g_and_admin + non_recurring + others
        operating_expense = OperatingExpenses(r_and_d, selling_g_and_admin, non_recurring, others)
        self.assertEqual(operating_expense.get_total(), expected, "Should be %f" % expected)

    def test_full_income_statement(self):
        total_revenue = 10000
        cost_of_revenue = 500
        research_development = 200
        selling_general_and_administrative = 100
        non_recurring = 20
        others = 30
        other_expense_or_income = 10
        interest_expense = 40
        income_tax_expense = 20
        income_statement = IncomeStatement(total_revenue,
                                           cost_of_revenue,
                                           research_development,
                                           selling_general_and_administrative,
                                           non_recurring,
                                           others,
                                           other_expense_or_income,
                                           interest_expense,
                                           income_tax_expense)

        expected = total_revenue -\
                   cost_of_revenue - \
                   research_development - \
                   selling_general_and_administrative - \
                   non_recurring - \
                   others - \
                   other_expense_or_income - \
                   interest_expense - \
                   income_tax_expense

        self.assertEqual(income_statement.net_income, expected, "Should be %f, actual was : %f " % (expected, income_statement.net_income))


if __name__ == '__main__':
    unittest.main()
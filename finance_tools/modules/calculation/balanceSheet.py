import formula


class CurrentAssets():
    def __init__(self, date, cash, short_term_investment, net_receivable, inventory, other_current_assets):
        self.date = date
        self.cash = cash
        self.short_term_investment = short_term_investment
        self.net_receivable = net_receivable
        self.inventory = inventory
        self.other_current_assets = other_current_assets

    def get_total(self):
        return self.cash + self.short_term_investment + self.net_receivable + self.inventory + self.other_current_assets


class LongTermAssets():
    def __init__(self,
                 date,
                 long_term_investment,
                 property_plant_equipment,
                 goodwill,
                 intangible_assets,
                 amortization,
                 other_assets,
                 deferred_long_term_assets_change):
        self.date = date
        self.long_term_investment = long_term_investment
        self.property_plant_equipment = property_plant_equipment
        self.goodwill = goodwill
        self.intangible_assets = intangible_assets
        self.amortization = amortization
        self.other_assets = other_assets
        self.deferred_long_term_assets_change = deferred_long_term_assets_change

    def get_total(self):
        return self.long_term_investment + \
               self.property_plant_equipment + \
               self.goodwill + \
               self.intangible_assets + \
               self.amortization + \
               self.other_assets + \
               self.deferred_long_term_assets_change


class CurrentLiabilities():
    def __init__(self, date, accounts_payable, short_debt, other_current_liabilities):
        self.date = date
        self.accounts_payable = accounts_payable
        self.short_debt = short_debt
        self.other_current_liabilities = other_current_liabilities

    def get_total(self):
        return self.accounts_payable + self.short_debt + self.other_current_liabilities


class LongTermLiabilities():
    def __init__(self,
                 date,
                 long_term_debt,
                 other_liabilities,
                 deferred_long_term_liability,
                 minority_interest,
                 negative_goodwill):
        self.date = date
        self.long_term_debt = long_term_debt
        self.other_liabilities = other_liabilities
        self.deferred_long_term_liability = deferred_long_term_liability
        self.minority_interest = minority_interest
        self.negative_goodwill = negative_goodwill

    def get_total(self):
        return self.long_term_debt + \
               self.other_liabilities + \
               self.deferred_long_term_liability + \
               self.minority_interest + \
               self.negative_goodwill


class Equity():
    def __init__(self,
                 date,
                 misc_stocks_options_warrants,
                 redeemable_preferred_stock,
                 preferred_stock,
                 common_stock,
                 retained_earnings,
                 treasury_stock,
                 capital_surplus,
                 other_stockholder_equity):
        self.date = date
        self.misc_stocks_options_warrants = misc_stocks_options_warrants
        self.redeemable_preferred_stock = redeemable_preferred_stock
        self.preferred_stock = preferred_stock
        self.common_stock = common_stock
        self.retained_earnings = retained_earnings
        self.treasury_stock = treasury_stock
        self.capital_surplus = capital_surplus
        self.other_stockholder_equity = other_stockholder_equity

    def get_total(self):
        return self.misc_stocks_options_warrants + \
               self.redeemable_preferred_stock + \
               self.preferred_stock + \
               self.common_stock + \
               self.retained_earnings + \
               self.treasury_stock + \
               self.capital_surplus + \
               self.other_stockholder_equity


class BalanceSheet():
    def __init__(self,
                 company_name,
                 date,
                 cash,
                 short_term_investment,
                 net_receivable,
                 inventory,
                 other_current_assets,
                 long_term_investment,
                 property_plant_equipment,
                 goodwill,
                 intangible_assets,
                 amortization,
                 other_assets,
                 deferred_long_term_assets_change,
                 accounts_payable,
                 short_debt,
                 other_current_liabilities,
                 long_term_debt,
                 other_liabilities,
                 deferred_long_term_liability,
                 minority_interest,
                 negative_goodwill,
                 misc_stocks_options_warrants,
                 redeemable_preferred_stock,
                 preferred_stock,
                 common_stock,
                 retained_earnings,
                 treasury_stock,
                 capital_surplus,
                 other_stockholder_equity):
        self.company_name = company_name
        self.current_assets = CurrentAssets(date,
                                            cash,
                                            short_term_investment,
                                            net_receivable,
                                            inventory,
                                            other_current_assets)
        self.long_term_assets = LongTermAssets(date,
                                               long_term_investment,
                                               property_plant_equipment,
                                               goodwill,
                                               intangible_assets,
                                               amortization,
                                               other_assets,
                                               deferred_long_term_assets_change)

        self.current_liabilities = CurrentLiabilities(date, accounts_payable, short_debt, other_current_liabilities)

        self.long_term_liabilities = LongTermLiabilities(date,
                                                         long_term_debt,
                                                         other_liabilities,
                                                         deferred_long_term_liability,
                                                         minority_interest,
                                                         negative_goodwill)

        self.equity = Equity(date,
                             misc_stocks_options_warrants,
                             redeemable_preferred_stock,
                             preferred_stock,
                             common_stock,
                             retained_earnings,
                             treasury_stock,
                             capital_surplus,
                             other_stockholder_equity)

    def verify(self):
        return (self.current_assets + self.long_term_assets) == \
               (self.current_liabilities + self.long_term_liabilities + self.equity)

    def get_current_ratio(self):
        return formula.get_current_ratio(self.current_assets.get_total(), self.current_liabilities.get_total())

    def get_quick_ratio(self):
        return formula.get_quick_ratio(self.current_assets.get_total(),
                                       self.current_liabilities.get_total(),
                                       self.current_assets.inventory)

    def get_debt_to_equity(self):
        return formula.get_debt_to_equity(self.current_liabilities.get_total() +
                                          self.long_term_liabilities.get_total(),
                                          self.equity.get_total())

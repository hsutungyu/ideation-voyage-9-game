from business import Business
from household import HouseholdItem

class Account:

    def __init__(self, normal_currency, premium_currency):
        self.currency = [normal_currency, premium_currency]
        self.household_items = list()
        self.business_investments = list()

    def addHouseholdItem(self, name, weekly_fee, image_path):
        self.household_items.append(HouseholdItem(name, weekly_fee, image_path))

    def addBusiness(self, name, bid_price, current_price, risk_percentage):
        self.business_investments.append(
            Business(name, bid_price, current_price, risk_percentage))
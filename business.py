import random


class Business:

    def __init__(self, name, bid_price, current_price, risk_percentage):
        self.name = name
        self.bid_price = bid_price
        self.current_price = current_price
        self.risk_percentage = risk_percentage

    # randomly change the current price by multiplying values between 1 - risk_percentage and 1 + risk_percentage
    # return the new current price
    def setCurrentPrice(self):
        randomChange = round(
            random.uniform(1 - self.risk_percentage,
                           1 + self.risk_percentage), 2)  # 2 decimal places
        self.current_price *= randomChange
        self.current_price = round(self.current_price, 2)
        return self.current_price

    # return the profit/loss ofthe investment
    def getPriceDifference(self):
        return round(self.current_price - self.bid_price, 2)

    # return a space separated string of name, bid price, current price and profit/loss
    def __str__(self):
        return f"{self.name} {self.bid_price} {self.current_price} {self.getPriceDifference()}"
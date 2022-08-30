# random event class is for direct change, i.e., no decisions by children needed
class RandomEvent:

    def __init__(self, name, description, action, business):
        self.name = name
        self.description = description
        self.action = action  # action would be a float multiplier that changes the value of a business
        self.business = business

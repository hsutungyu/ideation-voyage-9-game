# mission class is for making decisions
class Mission:

    def __init__(self, name, description, good_decision, bad_decision):
        self.name = name
        self.description = description
        self.good_decision = good_decision
        self.bad_decision = bad_decision
        
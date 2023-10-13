
class Selection:
    def __init__(self, name: str, event, price: float, active: bool, outcome: str):
        self.name = name
        self.event = event
        self.price = price
        self.active = active
        self.outcome = outcome

    def get_name(self):
        return self.name

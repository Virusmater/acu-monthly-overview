class Event:

    def __init__(self):
        self.title = ""
        self.subtitle = ""
        self.price = ""
        self.date = ""
        self.time = ""
        self.weekday = ""
        self.same_day = False
        self.month = ""
        self.year = ""
        self.recurrent = False
        self.weekday_num = -1
        self.is_weekly = False

    def set_price(self, price):
        if price == "Donation based":
            self.price = "Donation"
        else:
            self.price = price

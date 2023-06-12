

class SaleNumberRecord:
    def __init__(self, link, number, status, price, time_left, owner=None):
        self.link = link
        self.number = number
        self.status = status
        self.price = price
        self.time_left = time_left
        self.owner = owner

    def to_tuple(self) -> tuple:
        return (self.link, self.number, self.status, self.price, self.time_left, self.owner)


class SoldNumberRecord:
    def __init__(self, link, number, status, price, sold_time, owner=None):
        self.link = link
        self.number = number
        self.status = status
        self.price = price
        self.sold_time = sold_time
        self.owner = owner

    def to_tuple(self) -> tuple:
        return (self.link, self.number, self.status, self.price, self.sold_time, self.owner)

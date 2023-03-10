class Product:
    def __init__(self, name, sell_price, buy_price, sell_moving_week):
        self.name = name
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.sell_moving_week = sell_moving_week

    def __str__(self):
        return f'{self.name} {self.buy_price} {self.sell_price}'

    def __repr__(self):
        return f'{self.name} {self.buy_price} {self.sell_price}'

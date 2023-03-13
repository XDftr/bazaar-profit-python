import requests
import json

from data.product import Product


class BazaarData:
    def __init__(self):
        self.products = []
        self.objects = []
        self.data = None

    def request_data(self):
        products = requests.get("https://api.hypixel.net/skyblock/bazaar")
        self.data = products.json()
        with open('data/data_bazaar_full.json', 'w+') as f:
            json.dump(self.data, f, indent=4)
        with open('data/data_bazaar.json', 'w+') as f:
            json.dump(self.data["products"], f, indent=4)

        return self.data["products"]

    def create_classes(self):
        product_data = self.data["products"]

        for product in product_data:
            try:
                name = product_data.get(product).get("product_id")
                sell_price = product_data.get(product).get("sell_summary")[0].get("pricePerUnit")
                buy_price = product_data.get(product).get("buy_summary")[0].get("pricePerUnit")
                sell_moving_week = product_data.get(product).get("quick_status").get("sellMovingWeek")
                p = Product(name, buy_price, sell_price, sell_moving_week)
                self.products.append(p)
            except IndexError:
                continue

        return self.products
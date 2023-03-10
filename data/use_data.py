import json
import requests
import re

from data.product import Product
from data.exception import ProductNotFound
from data.object import Object


class UseData:
    def __init__(self):
        self.products = []
        self.objects = []
        self.data = None
        self.nr = 1

    def update_data(self):
        products = requests.get("https://api.hypixel.net/skyblock/bazaar")
        products.json()
        with open('data/data.json', 'w') as f:
            json.dump(products.json(), f)

    def create_classes(self):
        with open('data/data.json', 'r') as f:
            self.data = json.load(f)["products"]

        for product in self.data:
            try:
                name = self.data.get(product).get("product_id")
                sell_price = self.data.get(product).get("sell_summary")[0].get("pricePerUnit")
                buy_price = self.data.get(product).get("buy_summary")[0].get("pricePerUnit")
                sell_moving_week = self.data.get(product).get("quick_status").get("sellMovingWeek")
                p = Product(name, buy_price, sell_price, sell_moving_week)
                self.products.append(p)
            except IndexError:
                continue

    def calculate_data(self, item: dict):
        crafting_materials = item.get("crafting_materials")
        sell_item = item.get("sell_item")
        buy_price = 0
        sell_price = 0
        string_crafting = []
        string_sell = ""
        past_week_volume = 0

        for material in crafting_materials:
            string_crafting.append(f"{material}*{crafting_materials.get(material)}")
            product = next(filter(lambda p: p.name == material, self.products), None)
            if product is None:
                raise ProductNotFound(material)
            buy_price += product.buy_price * crafting_materials.get(material)

        for material in sell_item:
            string_sell = f"{material}*{sell_item.get(material)}"
            product = next(filter(lambda p: p.name == material, self.products), None)
            if product is None:
                raise ProductNotFound(material)
            sell_price += product.sell_price * sell_item.get(material)
            past_week_volume = product.sell_moving_week
        string_a = f"{string_sell} = ({', '.join(string_crafting)})"
        profit = round(sell_price - buy_price, 2)
        buy_price_1 = buy_price
        sell_price_1 = sell_price
        buy_price = buy_price * self.nr
        sell_price = sell_price * self.nr
        profit = profit * self.nr

        print(string_a)
        print(f"Count: {self.nr}")
        print(f"Materials buy price: {buy_price}")
        print(f"Item sell price: {sell_price}")
        print(f"Past week volume: {past_week_volume}")
        print(f"Profit {profit}")
        obj = Object(string_a, buy_price, sell_price, past_week_volume, profit, self.nr, buy_price_1, sell_price_1)
        self.objects.append(obj)

    def calculate_data2(self, item: dict):
        crafting_materials = item.get("crafting_materials")
        sell_item = item.get("sell_item")
        buy_price = 0
        sell_price = 0
        string_crafting = []
        string_sell = ""
        past_week_volume = 0

        for material in crafting_materials:
            string_crafting.append(f"{material}*{crafting_materials.get(material)}")
            product = next(filter(lambda p: p.name == material, self.products), None)
            if product is None:
                raise ProductNotFound(material)
            buy_price += product.buy_price * crafting_materials.get(material)

        for material in sell_item:
            string_sell = f"{material}*{sell_item.get(material)}"
            product = next(filter(lambda p: p.name == material, self.products), None)
            if product is None:
                raise ProductNotFound(material)
            sell_price += product.sell_price * sell_item.get(material)
            past_week_volume = product.sell_moving_week
        string_a = f"{string_sell} = ({', '.join(string_crafting)})"
        profit = round(sell_price - buy_price, 2)

        nr_true = 0

        while buy_price * nr_true < self.nr:
            nr_true += 1

        if nr_true > 0:
            nr_true -= 1

        buy_price_1 = buy_price
        sell_price_1 = sell_price

        buy_price = buy_price * nr_true
        sell_price = sell_price * nr_true
        profit = profit * nr_true

        print(string_a)
        print(f"Materials buy price: {buy_price}")
        print(f"Item sell price: {sell_price}")
        print(f"Past week volume: {past_week_volume}")
        print(f"Profit {profit}")
        if buy_price > 0:
            obj = Object(string_a, buy_price, sell_price, past_week_volume, profit, nr_true, buy_price_1, sell_price_1)
            self.objects.append(obj)

    def find_item(self, name):
        print("NAME:", self.data.get(name).get("product_id"))
        print("BUY:", self.data.get(name).get("sell_summary")[0])
        print("SELL:", self.data.get(name).get("buy_summary")[0])
        print("SOLD THIS WEEK:", self.data.get(name).get("quick_status").get("sellMovingWeek"))

    def run(self, nr=1, type="count"):
        self.nr = nr
        with open("./items_to_flip.txt", "r") as i:
            json_list = []
            for line in i:
                if line.startswith('#'):
                    continue
                data = line.strip()
                if data:
                    json_list.append(json.loads(data))

        self.create_classes()

        if type == "count":
            for i in json_list:
                self.calculate_data(i)
        else:
            for i in json_list:
                self.calculate_data2(i)

        self.save_objects_to_file()
        self.save_objects_to_file2()

    def test(self):
        pass

    def save_objects_to_file(self):
        obj = sorted(self.objects, key=lambda x: x.profit, reverse=True)

        with open('best_flip.txt', 'w') as f:
            f.write(f"Item kogus: {self.nr}\n\n")
            for o in obj:
                name = o.name

                def multiply(match):
                    return "*" + str(int(match.group(1)) * o.count)

                s = re.sub(r'\*(\d+)', multiply, name)


                f.write(f'Name: {s}\n'
                        f'Buy (item): {o.buy_price_1}\n'
                        f'Sell (item): {o.sell_price_1}\n'
                        f'Count: {o.count}\n'
                        f'Buy price: {"{:,}".format(o.buy_price)}\n'
                        f'Sell price: {"{:,}".format(o.sell_price)}\n'
                        f'Past week volume: {"{:,}".format(o.past_week_volume)}\n'
                        f'Profit: {"{:,}".format(o.profit)}\n'
                        f'Flip %: {round(o.profit / o.buy_price * 100, 2)}')
                if o != obj[-1]:
                    f.write("\n\n")

    def save_objects_to_file2(self):
        obj = sorted(self.objects, key=lambda x: x.profit / x.buy_price, reverse=True)

        with open('best_flip_by_%.txt', 'w') as f:
            f.write(f"Item kogus: {self.nr}\n\n")
            for o in obj:
                name = o.name

                def multiply(match):
                    return "*" + str(int(match.group(1)) * o.count)

                s = re.sub(r'\*(\d+)', multiply, name)

                f.write(f'Name: {s}\n'
                        f'Buy (item): {o.buy_price_1}\n'
                        f'Sell (item): {o.sell_price_1}\n'
                        f'Count: {o.count}\n'
                        f'Buy price: {"{:,}".format(o.buy_price)}\n'
                        f'Sell price: {"{:,}".format(o.sell_price)}\n'
                        f'Past week volume: {"{:,}".format(o.past_week_volume)}\n'
                        f'Profit: {"{:,}".format(o.profit)}\n'
                        f'Flip %: {round(o.profit / o.buy_price * 100, 2)}')
                if o != obj[-1]:
                    f.write("\n\n")

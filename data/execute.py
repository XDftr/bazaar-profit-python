import datetime
import json
import re

from data.bazaar_data import BazaarData
from data.bin_data import BinData
from data.exception import ProductNotFound
from data.object import Object


class Execute:
    def __init__(self, t, search_type="bazaar", arg=1, boolean = False):
        self.bin_data = {}  # TEST
        self.nr = arg
        self.search_type = search_type
        self.bazaar_objects = []
        self.bazaar_data = {}
        self.bazaar_products = []
        self.bin_objects = []
        self.file_type = ""
        self.boolean_bin = boolean

        if t == 'bazaar':
            self.parse_bazaar_data()
        elif t == 'auction':
            bazaar = BazaarData()
            self.bazaar_data = bazaar.request_data()
            self.bazaar_products = bazaar.create_classes()
            self.parse_bin_data()
        else:
            self.parse_bazaar_data()
            self.parse_bin_data()

    def parse_bazaar_data(self):
        file_path = "./items_to_flip.txt"
        bazaar = BazaarData()
        self.bazaar_data = bazaar.request_data()
        self.bazaar_products = bazaar.create_classes()
        json_list = self.load_flip_items(file_path)

        if self.search_type == "count":
            self.file_type = "Item Count"
        else:
            self.file_type = "Max Buy Price"

        for i in json_list:
            self.calculate_data(i)

        obj1 = sorted(self.bazaar_objects, key=lambda x: x.profit, reverse=True)
        filename1 = 'best_flip.txt'

        obj2 = sorted(self.bazaar_objects, key=lambda x: x.profit / x.buy_price, reverse=True)
        filename2 = 'best_flip_by_%.txt'

        self.save_objects_to_file(obj1, filename1)
        self.save_objects_to_file(obj2, filename2)

    def parse_bin_data(self):
        file_path = "./items_to_flip_bin.txt"
        json_list = self.load_flip_items(file_path)

        run = BinData()
        if self.boolean_bin:
            run.import_data()
            run.write_file()
            run.write_full_file()
        self.bin_data = run.read_from_file()

        for i in json_list:
            self.calculate_data_bin(i)

        obj1 = sorted(self.bazaar_objects, key=lambda x: x.profit, reverse=True)
        filename1 = 'best_flip_bin.txt'

        obj2 = sorted(self.bazaar_objects, key=lambda x: x.profit / x.buy_price, reverse=True)
        filename2 = 'best_flip_by_%_bin.txt'

        self.save_objects_to_file_bin(obj1, filename1)
        self.save_objects_to_file_bin(obj2, filename2)

    def find_bin(self, name):
        for i in self.bin_data.keys():
            if name in i:
                return i, self.bin_data.get(i)

    def calculate_data_bin(self, item:dict):
        crafting_materials = item.get("crafting_materials")
        sell_item = item.get("sell_item")
        buy_price = 0
        string_crafting = []

        for material in crafting_materials:
            string_crafting.append(f"{material}*{crafting_materials.get(material)}")
            product = next(filter(lambda p: p.name == material, self.bazaar_products), None)
            if product is None:
                raise ProductNotFound(material)
            buy_price += product.buy_price * crafting_materials.get(material)

        for material in self.bin_data.keys():
            if sell_item == material:
                string_sell = material
                sell_price = self.bin_data.get(material)
                break
        else:
            raise ProductNotFound(sell_item)

        string_a = f"{string_sell} = ({', '.join(string_crafting)})"
        profit = round(sell_price - buy_price, 2)
        buy_price = buy_price
        sell_price = sell_price
        profit = profit

        obj = Object(string_a, buy_price, sell_price, 0, profit, 1, 0, 0)
        self.bazaar_objects.append(obj)


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
            product = next(filter(lambda p: p.name == material, self.bazaar_products), None)
            if product is None:
                raise ProductNotFound(material)
            buy_price += product.buy_price * crafting_materials.get(material)

        for material in sell_item:
            string_sell = f"{material}*{sell_item.get(material)}"
            product = next(filter(lambda p: p.name == material, self.bazaar_products), None)
            if product is None:
                raise ProductNotFound(material)
            sell_price += product.sell_price * sell_item.get(material)
            past_week_volume = product.sell_moving_week

        if self.search_type == "count":
            self.count(string_sell, string_crafting, buy_price, sell_price, past_week_volume)
        else:
            self.buy_price(string_sell, string_crafting, buy_price, sell_price, past_week_volume)

    def count(self, string_sell, string_crafting, buy_price, sell_price, past_week_volume):
        string_a = f"{string_sell} = ({', '.join(string_crafting)})"
        profit = round(sell_price - buy_price, 2)
        buy_price_1 = buy_price
        sell_price_1 = sell_price
        buy_price = buy_price * self.nr
        sell_price = sell_price * self.nr
        profit = profit * self.nr

        obj = Object(string_a, buy_price, sell_price, past_week_volume, profit, self.nr, buy_price_1, sell_price_1)
        self.bazaar_objects.append(obj)

    def buy_price(self, string_sell, string_crafting, buy_price, sell_price, past_week_volume):
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

        if buy_price > 0:
            obj = Object(string_a, buy_price, sell_price, past_week_volume, profit, nr_true, buy_price_1, sell_price_1)
            self.bazaar_objects.append(obj)

    def find_item(self, name):
        print("NAME:", self.bazaar_data.get(name).get("product_id"))
        print("BUY:", self.bazaar_data.get(name).get("sell_summary")[0])
        print("SELL:", self.bazaar_data.get(name).get("buy_summary")[0])
        print("SOLD THIS WEEK:", self.bazaar_data.get(name).get("quick_status").get("sellMovingWeek"))

    def load_flip_items(self, filepath):
        with open(filepath, "r") as i:
            json_list = []
            for line in i:
                if line.startswith('#'):
                    continue
                data = line.strip()
                if data:
                    json_list.append(json.loads(data))
        return json_list

    def save_objects_to_file(self, obj, filename):
        with open(filename, 'w') as f:
            timestamp = datetime.datetime.now()
            f.write(timestamp.strftime("%d.%m.%Y %H:%M:%S") + "\n")
            f.write(f"{self.file_type}: {self.nr}\n\n")

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

    def save_objects_to_file_bin(self, obj, filename):
        with open(filename, 'w') as f:
            timestamp = datetime.datetime.now()
            f.write(timestamp.strftime("%d.%m.%Y %H:%M:%S") + "\n\n")

            for o in obj:
                name = o.name
                def multiply(match):
                    return "*" + str(int(match.group(1)) * o.count)

                s = re.sub(r'\*(\d+)', multiply, name)

                f.write(f'Name: {s}\n'
                        f'Buy price: {"{:,}".format(o.buy_price)}\n'
                        f'Sell price: {"{:,}".format(o.sell_price)}\n'
                        f'Profit: {"{:,}".format(o.profit)}\n'
                        f'Flip %: {round(o.profit / o.buy_price * 100, 2)}')
                if o != obj[-1]:
                    f.write("\n\n")
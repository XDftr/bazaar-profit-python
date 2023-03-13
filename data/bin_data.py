import json
import requests
from collections import defaultdict


class BinData:
    def __init__(self):
        self.data = {}
        self.full_data = {}
        self.total_pages = 0
        self.page = 0
        self.statistics = defaultdict(int)

    def request_data(self):
        response = requests.get(f'https://api.hypixel.net/skyblock/auctions?page={self.page}')

        return response.json()

    def import_data(self):
        # Make a GET request to the Hypixel API
        data = self.request_data()
        self.total_pages = data['totalPages']
        self.full_data = data

        while self.page < self.total_pages:
            for i in data['auctions']:
                bid = i['bin']
                name = i['item_name']
                price = i['starting_bid']
                if '✪' in name or '◆' in name or '⚚' in name and '✿' in name:
                    continue
                if bid:
                    self.add_item(name, price)
                    self.add_statistics(name)
            self.page += 1
            data = self.request_data()

    def add_item(self, name, price):
        if name in self.data.keys():
            if price < self.data.get(name):
                self.data[name] = price
        else:
            self.data[name] = price

    def add_statistics(self, name):
        exempt = ["Pure", "Silent", "Spicy", "Shaded", "Fierce", "Strong", "Odd", "Lvl", "Unyielding", "Strong",
                  "Mythic", "Titanic", "Necrotic", "Clean", "Wise", "Light", "Giant", "Heavy", "Smart", "Ancient",
                  "Reinforced", "Hurtful", "Skin", "Renowned", "New Year Cake", "Sharp", "Dragon", "Unreal",
                  "Legendary", "Fair", "Deadly", "Forceful", "⚚", "Heroic"]

        for i in exempt:
            if i in name:
                break
        else:
            self.statistics[name] += 1


    def write_statistics(self):
        sorted_dict = dict(sorted(self.statistics.items(), key=lambda item: item[1]))
        with open("data/statistics_bin.json", 'w+') as file:
            json.dump(sorted_dict, file, indent=4)

    def write_file(self):
        with open('data/data_bin.json', 'w') as file:
            # Write the dictionary to the file
            json.dump(self.data, file, indent=4)

    def write_full_file(self):
        with open('data/data_bin_full.json', 'w') as file:
            # Write the dictionary to the file
            json.dump(self.full_data, file, indent=4)

    def read_from_file(self):
        with open('data/data_bin.json', 'r') as file:
            self.data = json.load(file)
        return self.data

    def find_item(self, name):
        for i in self.data.keys():
            if name == i:
                print(i, self.data.get(i))
                break

#!/usr/bin/env python3

from DatabaseHandler import database_handler
from Constants import *


class Stockpile:
    def __init__(self):
        self.items = {}

    def get_quantity_of_type_id_in_stockpile(self, type_id):
        return self.items.get(type_id, 0)


    def add_item_to_stockpile(self, item_type_id, quantity):
        assert type(item_type_id) == int
        if self.items.get(item_type_id, None):
            self.items[item_type_id] += quantity
        else:
            self.items[item_type_id] = quantity

    def get_items_from_stockpile_file(self):
        with open(STOCKPILE_FILE_PATH) as stockpile_file:
            for line in stockpile_file.readlines():
                split_line = line.split('\t')
                print(split_line)
                quantity = split_line[1]
                if quantity == '':
                    quantity = 1
                else:
                    quantity = int(quantity.replace(',', ''))
                type_id = database_handler.get_type_id_for_name(split_line[0])
                assert type(type_id) == int
                yield type_id, quantity

    def process_stockpile_file(self):
        for type_id, quantity in self.get_items_from_stockpile_file():
            self.add_item_to_stockpile(type_id, quantity)






if __name__ == "__main__":
    x = Stockpile()
    x.process_stockpile_file()
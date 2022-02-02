#!/usr/bin/env python3

import Item
from CustomExceptions import NoBpFoundException
from Constants import *
from CustomExceptions import NoBpFoundException

import sqlite3



class BlueprintFactory:
    def __init__(self, database_path):
        self.products = {}
        self.database = sqlite3.connect(DATABASE_PATH)

    def get_blueprint_id_and_quantity_produced_for_product(self, product_id):
        todo = self.database.execute(f"SELECT {BLUEPRINT_ID_COLUMN_NAME}, {QUANTITY_COLUMN_NAME} FROM {BLUEPRINTS_AND_PRODUCTS_TABLE} WHERE {PRODUCT_ID_COLUMN_NAME} = '{product_id}'").fetchall()
        if len(todo) != 1:
            raise NoBpFoundException(f"no BP found for {product_id}, assuming PI bullshittery, buy this")
        blueprint_id, quantity_produced = todo[0][0], todo[0][1]
        return blueprint_id, quantity_produced

    def get_inputs_for_blueprint(self, blueprint_id):
        todo = self.database.execute(f"SELECT {INPUT_ID_COLUMN_NAME}, {QUANTITY_COLUMN_NAME}  FROM {BLUEPRINTS_AND_INPUTS_TABLE} WHERE {BLUEPRINT_ID_COLUMN_NAME} = '{blueprint_id}'").fetchall()
        return todo

    def create_item(self, product_id):
        blueprint_id, quantity_produced_per_run = self.get_blueprint_id_and_quantity_produced_for_product(product_id)

        inputs = self.get_inputs_for_blueprint(blueprint_id)
        return Item.Item(self.request_product, blueprint_id, product_id, quantity_produced_per_run, inputs)

    def create_raw_material(self, product_id):
        return Item.RawMaterial(product_id)

    def request_product(self, product_id, quantity_needed):
        if self.products.get(product_id, None):
            pass
        else:
            try:
                self.products[product_id] = self.create_item(product_id)
            except NoBpFoundException:
                self.products[product_id] = self.create_raw_material(product_id)
        self.products[product_id].request(quantity_needed)

    def get_name_for_type_id(self, type_id):
        todo = self.database.execute(f"SELECT {EN_NAME_COLUMN} FROM {TYPE_ID_AND_EN_NAME} WHERE {TYPE_ID_COLUMN} = {type_id}").fetchall()
        assert len(todo) == 1, f"expected 1 value returned from query, actual: {todo}"
        return todo[0][0]


    def janice_print_raws(self):
        for value in self.products.values():
            if type(value) == Item.RawMaterial:
                print(f"{self.get_name_for_type_id(value.product_id)}\t{value.amount_requested_from_upstream}")

    def janice_print_components(self):
        for value in self.products.values():
            if type(value) == Item.Item:
                print(f"{self.get_name_for_type_id(value.product_id)}\t{value.amount_requested_from_upstream}")


if __name__ == "__main__":
    x = BlueprintFactory(DATABASE_PATH)
    x.request_product(61207, 200)
    x.janice_print_raws()
    print("-------")
    x.janice_print_components()


#!/usr/bin/env python3

import Item
from CustomExceptions import NoBpFoundException
from Constants import *
from CustomExceptions import NoBpFoundException
import Stockpile
from DatabaseHandler import database_handler

import locale
locale.setlocale(locale.LC_ALL, 'en_US')
import sqlite3



class BlueprintFactory:
    def __init__(self, database_path):
        self.products = {}
        self.database = sqlite3.connect(DATABASE_PATH)
        self.stockpile = Stockpile.Stockpile()
        self.stockpile.process_stockpile_file()
        self.stockpile.process_in_progress_jobs_file()
        self.level_counter = -1
        self.items_to_treat_as_raw = self.get_items_to_treat_as_raw()

    def get_items_to_treat_as_raw(self):
        items_to_treat_as_raw = {}
        with open(TREAT_AS_RAW_FILE_PATH) as file:
            for line in file.readlines():
                items_to_treat_as_raw[database_handler.get_type_id_for_name(line.strip())] = True
        return items_to_treat_as_raw


    def get_blueprint_id_and_quantity_produced_for_product(self, product_id):
        todo = self.database.execute(f"SELECT {BLUEPRINT_ID_COLUMN_NAME}, {QUANTITY_COLUMN_NAME} FROM {BLUEPRINTS_AND_PRODUCTS_TABLE} WHERE {PRODUCT_ID_COLUMN_NAME} = '{product_id}'").fetchall()
        if len(todo) != 1:
            raise NoBpFoundException(f"no BP found for {product_id}, assuming PI bullshittery, buy this")
        blueprint_id, quantity_produced = todo[0][0], todo[0][1]
        return blueprint_id, quantity_produced

    def get_inputs_for_blueprint(self, blueprint_id):
        todo = self.database.execute(f"SELECT {INPUT_ID_COLUMN_NAME}, {QUANTITY_COLUMN_NAME}  FROM {BLUEPRINTS_AND_INPUTS_TABLE} WHERE {BLUEPRINT_ID_COLUMN_NAME} = '{blueprint_id}'").fetchall()
        return todo

    def create_item(self, product_id, material_efficiency):
        blueprint_id, quantity_produced_per_run = self.get_blueprint_id_and_quantity_produced_for_product(product_id)

        inputs = self.get_inputs_for_blueprint(blueprint_id)
        return Item.Item(self, blueprint_id, product_id, quantity_produced_per_run, inputs, material_efficiency)

    def create_raw_material(self, product_id):
        return Item.RawMaterial(self, product_id)

    def get_number_of_product_id_requested(self, product_id):
        if product := self.products.get(product_id, None):
            return product.amount_requested_from_upstream
        else:
            return 0


    def request_product(self, product_id, quantity_needed, material_efficiency=10):
        self.level_counter += 1
        if self.products.get(product_id, None):
            pass
        else:
            try:
                if not self.items_to_treat_as_raw.get(product_id, False):
                    self.products[product_id] = self.create_item(product_id, material_efficiency)
                else:
                    raise NoBpFoundException("treating as raw material")
            except NoBpFoundException:
                self.products[product_id] = self.create_raw_material(product_id)
        self.products[product_id].request(quantity_needed)
        self.level_counter -= 1

    def get_name_for_type_id(self, type_id):
        todo = self.database.execute(f"SELECT {EN_NAME_COLUMN} FROM {TYPE_ID_AND_EN_NAME_TABLE} WHERE {TYPE_ID_COLUMN} = {type_id}").fetchall()
        assert len(todo) == 1, f"expected 1 value returned from query, actual: {todo}"
        return todo[0][0]


    def janice_print_raws(self):
        values = []
        for value in self.products.values():
            values.append(value)
        def sort_foo(item):
            return item.product_id

        values.sort(key=sort_foo)
        for value in values:
            if type(value) == Item.RawMaterial and value.get_quantity_needed() > 0:
                print(f"{self.get_name_for_type_id(value.product_id)}\t{value.amount_requested_from_upstream}")

    def janice_print_components(self):
        for value in self.products.values():
            if type(value) == Item.Item and value.build_type == BUILD_TYPES['manufacturing'] and value.get_quantity_needed() > 0:
                # print(f"{value.product_id}:{self.get_name_for_type_id(value.product_id)}\t{value.get_quantity_needed()}")
                # print(f"{self.get_name_for_type_id(value.product_id)}\t{value.get_quantity_needed()}\tjob_cost: {value.get_job_cost()}")
                print(f"{self.get_name_for_type_id(value.product_id)}\t{value.get_quantity_needed()}")

    def print_job_instructions(self):
        steps = []
        for value in self.products.values():
            if type(value) == Item.Item:
                steps.append(value)
        def sorting_func(step):
            return step.job_level
        steps.sort(reverse=True, key=sorting_func)
        level = 0
        n = 0
        print(f"==========================")
        level = steps[0].job_level
        level_steps = []
        for step in steps: #TODO - this loop is disgusting, make it nice
            if step.job_level != level:
                def sort_foo(step):
                    return database_handler.get_name_for_type_id(step.product_id)
                level_steps.sort(key=sort_foo)
                for level_step in level_steps:
                    print_line = f"{level_step.job_level}:\t{self.get_name_for_type_id(level_step.product_id)}\t- {level_step.runs_requested_downstream} jobs"
                    if self.stockpile.jobs.get(level_step.product_id, 0) == level_step.runs_requested_downstream:
                        print_line += " [IN PROGRESS]"
                    elif level_step.is_step_blocked():
                        print_line += " [BLOCKED]"
                    print(print_line)
                print(f"========================== x{len(level_steps)}")
                level_steps.clear()
                level = step.job_level
            n += 1
            if step.runs_requested_downstream > 0:
                level_steps.append(step)
        else:
            for level_step in level_steps:
                print(
                    f"{level_step.job_level}:\t{self.get_name_for_type_id(level_step.product_id)}\t- {level_step.runs_requested_downstream} jobs")
            print(f"========================== x{len(level_steps)}")
            print(f"========================== x{n} total")



if __name__ == "__main__":
    x = BlueprintFactory(DATABASE_PATH)
    x.request_product(22548, 5, material_efficiency=10)
    print("-------")
    x.janice_print_raws()
    print("-------")
    x.janice_print_components()
    print("-------")
    job_costs = 0
    for job in x.products.values():
        job_costs += job.get_job_cost()
    print(locale.format_string("%d", job_costs, grouping=True))
    x.print_job_instructions()



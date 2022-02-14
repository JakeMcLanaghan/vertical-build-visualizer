#!/usr/bin/env python3

from DatabaseHandler import database_handler
from Constants import *


class Job:
    def __init__(self, blueprint_name, number_of_runs):
        self.blueprint_name = blueprint_name
        self.number_of_runs = number_of_runs
        self.blueprint_id = database_handler.get_type_id_for_name(self.blueprint_name)
        self.outputs_per_run, self.product_id = database_handler.get_quantity_produced_and_product_id_for_product_from_blueprint_id(self.blueprint_id)
        self.total_outputs = self.outputs_per_run * self.number_of_runs

class Stockpile:
    def __init__(self):
        # type_id against item objects
        self.items = {}
        # type_id of output against number of runs
        self.jobs = {}

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

    def get_jobs_from_in_progress_jobs_file(self):
        with open(IN_PROGRESS_JOBS_FILE_PATH) as jobs_file:
            for line in jobs_file.readlines():
                split_line = line.split('\t')
                blueprint_name = split_line[3]
                job_runs = split_line[1]
                yield blueprint_name, int(job_runs)

    def process_in_progress_jobs_file(self):
        # does not handle duplicate jobs
        for blueprint_name, job_runs in self.get_jobs_from_in_progress_jobs_file():
            job = Job(blueprint_name, job_runs)
            if self.jobs.get(job.product_id, None):
                self.jobs[job.product_id] += job.number_of_runs
            else:
                self.jobs[job.product_id] = job.number_of_runs





if __name__ == "__main__":
    x = Stockpile()
    x.process_stockpile_file()
    x.process_in_progress_jobs_file()
    print("---")
    print(x.jobs)
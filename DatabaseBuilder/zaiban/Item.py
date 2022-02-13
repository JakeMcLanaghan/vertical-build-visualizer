#!/usr/bin/env python3

import math
from DatabaseHandler import database_handler
from Constants import *

from collections import namedtuple

REACTION_MATERIAL_MODIFIER = 1 - 0.0264
T2_MANUFACTURING_STRUCTURE_MODIFIER = 0.99 * (1 - 0.024 * 2.1)
INDUSTRY_TAX_PERCENT = 0.1

REACTION_INDEX = database_handler.get_industry_index_for_system(30002877, REACTION_INDEX_COLUMN_NAME)
print(REACTION_INDEX)
MANUFACTURING_INDEX = database_handler.get_industry_index_for_system(30002877, MANUFACTURING_INDEX_COLUMN_NAME)
print(MANUFACTURING_INDEX)
class Item:
    def __init__(self, blueprint_factory, blueprint_id, product_id, quantity_produced_per_run, inputs, material_efficiency):
        self.blueprint_factory = blueprint_factory

        self.runs_requested_downstream = 0
        self.blueprint_id = blueprint_id
        self.product_id = product_id
        self.quantity_produced_per_run = quantity_produced_per_run
        self.inputs = inputs
        self.build_type = database_handler.get_build_type_for_blueprint_id(self.blueprint_id)
        if self.build_type == BUILD_TYPES['manufacturing']:
            self.material_efficiency = material_efficiency
        else:
            self.material_efficiency = None

        self.amount_requested_from_upstream = 0
        # reduce the amount requested from upstream by the amount in the stockpile
        self.amount_requested_from_upstream -= self.blueprint_factory.stockpile.get_quantity_of_type_id_in_stockpile(self.product_id)
        self.job_level = -1

    def set_level(self, level):
        if self.job_level < level:
            self.job_level = level

    def get_quantity_needed(self):
        return max(self.amount_requested_from_upstream, 0)

    def get_runs_required(self):
        return max(math.ceil(self.amount_requested_from_upstream / self.quantity_produced_per_run), 0)

    def request(self, quantity_requested):
        self.set_level(self.blueprint_factory.level_counter)
        self.amount_requested_from_upstream += quantity_requested
        runs_required = self.get_runs_required()
        additional_runs_required = runs_required - self.runs_requested_downstream
        if additional_runs_required > 0:
            self.runs_requested_downstream = runs_required
            for product_id, quantity_required in self.inputs:
                amount_to_request = quantity_required*additional_runs_required
                if self.build_type == BUILD_TYPES['reaction']:
                    amount_to_request = max(
                        math.ceil(amount_to_request * REACTION_MATERIAL_MODIFIER),
                        additional_runs_required)
                elif self.build_type == BUILD_TYPES['manufacturing']:
                    amount_to_request = max(
                        math.ceil(amount_to_request * T2_MANUFACTURING_STRUCTURE_MODIFIER * (1-self.material_efficiency/100)),
                        additional_runs_required)
                self.blueprint_factory.request_product(product_id, amount_to_request)

    def get_job_cost(self):

        estimated_value = 0
        for product_id, quantity_required in self.inputs:
            adjusted_price = database_handler.get_adjusted_price_for_type_id(product_id)
            estimated_value += adjusted_price * quantity_required
        estimated_value = round(estimated_value) * self.runs_requested_downstream
        job_cost = math.ceil(estimated_value * (1+INDUSTRY_TAX_PERCENT))
        if self.build_type == BUILD_TYPES['manufacturing']:
            job_cost *= 0.97
            job_cost *= MANUFACTURING_INDEX
        elif self.build_type == BUILD_TYPES['reaction']:
            job_cost *= REACTION_INDEX
        return round(job_cost)


class RawMaterial:
    def __init__(self, product_id):
        self.product_id = product_id
        self.amount_requested_from_upstream = 0

    def request(self, quantity_requested):
        self.amount_requested_from_upstream += quantity_requested

    def get_job_cost(self):
        return 0

if __name__ == "__main__":
    pass



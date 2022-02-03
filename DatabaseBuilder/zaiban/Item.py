#!/usr/bin/env python3

import math

class Item:
    def __init__(self, blueprint_factory, blueprint_id, product_id, quantity_produced_per_run, inputs):
        self.blueprint_factory = blueprint_factory


        self.runs_requested_downstream = 0
        self.blueprint_id = blueprint_id
        self.product_id = product_id
        self.quantity_produced_per_run = quantity_produced_per_run
        self.inputs = inputs

        self.amount_requested_from_upstream = 0
        # reduce the amount requested from upstream by the amount in the stockpile
        self.amount_requested_from_upstream -= self.blueprint_factory.stockpile.get_quantity_of_type_id_in_stockpile(self.product_id)

    def get_quantity_needed(self):
        return max(self.amount_requested_from_upstream, 0)

    def get_runs_required(self):
        return max(math.ceil(self.amount_requested_from_upstream / self.quantity_produced_per_run), 0)

    def request(self, quantity_requested):
        debug = False
        self.amount_requested_from_upstream += quantity_requested
        runs_required = self.get_runs_required()
        additional_runs_required = runs_required - self.runs_requested_downstream
        if additional_runs_required > 0:
            self.runs_requested_downstream = runs_required
            for product_id, quantity_required in self.inputs:
                self.blueprint_factory.request_product(product_id, quantity_required*additional_runs_required)

class RawMaterial:
    def __init__(self, product_id):
        self.product_id = product_id
        self.amount_requested_from_upstream = 0

    def request(self, quantity_requested):
        self.amount_requested_from_upstream += quantity_requested



#!/usr/bin/env python3

import math

class Item:
    def __init__(self, requester_callback, blueprint_id, product_id, quantity_produced_per_run, inputs):
        self.amount_requested_from_upstream = 0
        self.runs_requested_downstream = 0
        self.requester_callback = requester_callback
        self.blueprint_id = blueprint_id
        self.product_id = product_id
        self.quantity_produced_per_run = quantity_produced_per_run
        self.inputs = inputs

    def get_runs_required(self):
        return math.ceil(self.amount_requested_from_upstream / self.quantity_produced_per_run)

    def request(self, quantity_requested):
        debug = False
        self.amount_requested_from_upstream += quantity_requested
        runs_required = self.get_runs_required()
        additional_runs_required = runs_required - self.runs_requested_downstream
        if additional_runs_required > 0:
            self.runs_requested_downstream = runs_required
            for product_id, quantity_required in self.inputs:
                self.requester_callback(product_id, quantity_required*additional_runs_required)

class RawMaterial:
    def __init__(self, product_id):
        self.product_id = product_id
        self.amount_requested_from_upstream = 0

    def request(self, quantity_requested):
        self.amount_requested_from_upstream += quantity_requested



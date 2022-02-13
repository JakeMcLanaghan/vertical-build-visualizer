#!/usr/bin/env python3

import sqlite3
import os
import sys
import yaml
import pprint
import requests
import json

from Constants import *
import Constants

def prepare_db():
    os.remove(Constants.DATABASE_PATH)
    with sqlite3.connect(Constants.DATABASE_PATH) as connection:

        connection.execute(f"CREATE TABLE {BLUEPRINTS_AND_PRODUCTS_TABLE} ({BLUEPRINT_ID_COLUMN_NAME} INTEGER, {QUANTITY_COLUMN_NAME} INTEGER, {PRODUCT_ID_COLUMN_NAME} INTEGER)")
        connection.execute(f"CREATE TABLE {BLUEPRINTS_AND_INPUTS_TABLE} ({BLUEPRINT_ID_COLUMN_NAME} INTEGER, {QUANTITY_COLUMN_NAME} INTEGER, {INPUT_ID_COLUMN_NAME} INTEGER)")
        connection.execute(f"CREATE TABLE {TYPE_ID_AND_EN_NAME_TABLE} ({TYPE_ID_COLUMN} INTEGER, {EN_NAME_COLUMN} TEXT)")
        connection.execute(f"CREATE TABLE {BLUEPRINT_AND_BUILD_TYPE_TABLE} ({BLUEPRINT_ID_COLUMN_NAME} INTEGER, {BUILD_TYPE_COLUMN_NAME} INTEGER)")
        connection.execute(f"CREATE TABLE {TYPE_ID_AND_ADJUSTED_PRICE_TABLE} ({TYPE_ID_COLUMN} INTEGER, {ADJUSTED_PRICE_COLUMN_NAME} REAL)")
        connection.execute(f"CREATE TABLE {SYSTEM_ID_AND_INDUSTRY_INDEX_TABLE} ({SYSTEM_ID_COLUMN_NAME} INTEGER, {MANUFACTURING_INDEX_COLUMN_NAME} REAL, {REACTION_INDEX_COLUMN_NAME} REAL, {ME_RESEARCH_INDEX_COLUMN_NAME} REAL, {TE_RESEARCH_INDEX_COLUMN_NAME} REAL,  {COPYING_INDEX_COLUMN_NAME} REAL, {INVENTION_INDEX_COLUMN_NAME} REAL)")


def insert_blueprint_into_db(connection, blueprint_id, products, materials, build_type):
    assert len(products) == 1
    product = products[0]
    connection.execute(f"INSERT INTO {BLUEPRINTS_AND_PRODUCTS_TABLE} ({BLUEPRINT_ID_COLUMN_NAME}, {QUANTITY_COLUMN_NAME}, {PRODUCT_ID_COLUMN_NAME}) VALUES ({blueprint_id}, {product['quantity']}, {product['typeID']});")

    inputs_command = f"INSERT INTO {BLUEPRINTS_AND_INPUTS_TABLE} ({BLUEPRINT_ID_COLUMN_NAME}, {QUANTITY_COLUMN_NAME}, {INPUT_ID_COLUMN_NAME}) VALUES"
    for material in materials:
        inputs_command += f" ({blueprint_id}, {material['quantity']}, { material['typeID']}),"
    inputs_command = inputs_command[:-1] + ';'
    connection.execute(inputs_command)
    build_type_command = f"INSERT INTO {BLUEPRINT_AND_BUILD_TYPE_TABLE} ({BLUEPRINT_ID_COLUMN_NAME}, {BUILD_TYPE_COLUMN_NAME}) VALUES ({blueprint_id}, {build_type})"
    connection.execute(build_type_command)

def populate_adjusted_price_table():
    response = requests.get("https://esi.evetech.net/latest/markets/prices/?datasource=tranquility",
                            headers={"accept": "application/json", "Cache-Control": "no-cache"})
    list = json.loads(response.content)
    command = f"INSERT INTO {TYPE_ID_AND_ADJUSTED_PRICE_TABLE} VALUES (?, ?);"

    def generator():
        for item in list:
            yield item["type_id"], item["adjusted_price"]
    with sqlite3.connect(Constants.DATABASE_PATH) as connection:
        connection.executemany(command, generator())

def populate_industry_index_table():
    response = requests.get("https://esi.evetech.net/latest/industry/systems/?datasource=tranquility",
                            headers={"accept": "application/json", "Cache-Control": "no-cache"})
    list = json.loads(response.content)
    command = f"INSERT INTO {SYSTEM_ID_AND_INDUSTRY_INDEX_TABLE} VALUES (?, ?, ?, ?, ?, ?, ?);"

    def generator():
        for system in list:
            cost_indices_list = system["cost_indices"]
            cost_indices = {}
            for cost_index in cost_indices_list:
                cost_indices[cost_index["activity"]] = cost_index["cost_index"]
            yield system["solar_system_id"], \
                  cost_indices["manufacturing"], cost_indices["reaction"],\
                  cost_indices["researching_material_efficiency"], cost_indices["researching_time_efficiency"],\
                  cost_indices["copying"], cost_indices["invention"]

    with sqlite3.connect(Constants.DATABASE_PATH) as connection:
        connection.executemany(command, generator())


def insert_name_into_db(connection, type_id, en_name):
    name_command = f"INSERT INTO {TYPE_ID_AND_EN_NAME_TABLE} VALUES (?, ?);"
    connection.execute(name_command, (type_id, en_name))

def populate_blueprints_and_products():
    with sqlite3.connect(Constants.DATABASE_PATH) as connection:

        with open(BLUEPRINTS_YAML_PATH) as blueprint_yaml_file:
            data = yaml.load(blueprint_yaml_file, Loader=yaml.FullLoader)

            for value in data.values():
                try:
                    manufacturing_or_reaction = None
                    if temp := value["activities"].get('manufacturing', None):
                        manufacturing_or_reaction = temp
                        build_type = BUILD_TYPES['manufacturing']
                    elif temp := value["activities"].get('reaction', None):
                        manufacturing_or_reaction = temp
                        build_type = BUILD_TYPES['reaction']

                    if manufacturing_or_reaction and (products := manufacturing_or_reaction.get('products')) and (materials := manufacturing_or_reaction.get('materials')):
                        insert_blueprint_into_db(connection, value['blueprintTypeID'], products, materials, build_type)
                except:
                    pprint.pprint(value)
                    raise AssertionError()

        with open(TYPE_ID_YAML_PATH) as type_id_yaml_file:
            data = yaml.load(type_id_yaml_file, Loader=yaml.FullLoader)

            for key, value in data.items():
                try:
                    insert_name_into_db(connection, key, value["name"]["en"])
                except:
                    print(f"failed to parse en name for {key}:\n{value}")




def main():
    prepare_db()
    populate_adjusted_price_table()
    populate_industry_index_table()
    populate_blueprints_and_products()
    connection = sqlite3.connect(Constants.DATABASE_PATH)
    cur = connection.cursor()
    cur.execute("SELECT * FROM blueprintsAndInputs WHERE blueprintID = '22549'")
    rows = cur.fetchall()
    print(rows)
    for row in rows:
        print(row)
        cur.execute(f"SELECT blueprintID FROM blueprintsAndProducts WHERE productID = '{row[2]}'")
        x = cur.fetchall()
        if len(x) == 0:
            print(f"buy {row[2]}")
        else:
            print(x[0][0])
            cur.execute(f"SELECT * FROM blueprintsAndInputs WHERE blueprintID = '{x[0][0]}'")
            print(cur.fetchall())


if __name__ == "__main__":
    main()

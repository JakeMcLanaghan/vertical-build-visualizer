#!/usr/bin/env python3

import sqlite3
import os
import sys
import yaml
import pprint
import BlueprintFactory

from Constants import *
import Constants

def prepare_db():
    os.remove(Constants.DATABASE_PATH)
    with sqlite3.connect(Constants.DATABASE_PATH) as connection:

        connection.execute(f"CREATE TABLE {BLUEPRINTS_AND_PRODUCTS_TABLE} ({BLUEPRINT_ID_COLUMN_NAME} INTEGER, {QUANTITY_COLUMN_NAME} INTEGER, {PRODUCT_ID_COLUMN_NAME} INTEGER)")
        connection.execute(f"CREATE TABLE {BLUEPRINTS_AND_INPUTS_TABLE} ({BLUEPRINT_ID_COLUMN_NAME} INTEGER, {QUANTITY_COLUMN_NAME} INTEGER, {INPUT_ID_COLUMN_NAME} INTEGER)")
        connection.execute(f"CREATE TABLE {TYPE_ID_AND_EN_NAME} ({TYPE_ID_COLUMN} INTEGER, {EN_NAME_COLUMN} TEXT)")


def insert_blueprint_into_db(connection, blueprint_id, products, materials):
    assert len(products) == 1
    product = products[0]
    connection.execute(f"INSERT INTO {BLUEPRINTS_AND_PRODUCTS_TABLE} ({BLUEPRINT_ID_COLUMN_NAME}, {QUANTITY_COLUMN_NAME}, {PRODUCT_ID_COLUMN_NAME}) VALUES ({blueprint_id}, {product['quantity']}, {product['typeID']});")

    inputs_command = f"INSERT INTO {BLUEPRINTS_AND_INPUTS_TABLE} ({BLUEPRINT_ID_COLUMN_NAME}, {QUANTITY_COLUMN_NAME}, {INPUT_ID_COLUMN_NAME}) VALUES"
    for material in materials:
        inputs_command += f" ({blueprint_id}, {material['quantity']}, { material['typeID']}),"
    inputs_command = inputs_command[:-1] + ';'
    connection.execute(inputs_command)

def insert_name_into_db(connection, type_id, en_name):
    name_command = f"INSERT INTO {TYPE_ID_AND_EN_NAME} VALUES (?, ?);"
    connection.execute(name_command, (type_id, en_name))

def populate_blueprints_and_products():
    with sqlite3.connect(Constants.DATABASE_PATH) as connection:

        with open(BLUEPRINTS_YAML_PATH) as blueprint_yaml_file:
            data = yaml.load(blueprint_yaml_file, Loader=yaml.FullLoader)

            for value in data.values():
                try:
                    if ((manufacturing_or_reaction := value["activities"].get('manufacturing')) or (manufacturing_or_reaction := value["activities"].get('reaction'))) \
                            and (products := manufacturing_or_reaction.get('products')) and (materials := manufacturing_or_reaction.get('materials')):
                        insert_blueprint_into_db(connection, value['blueprintTypeID'], products, materials)
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

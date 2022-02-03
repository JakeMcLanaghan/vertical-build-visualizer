#!/usr/bin/env python3

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

DATABASE_NAME = "database.db"
DATABASE_PATH = os.path.join(SCRIPT_DIR, "..", DATABASE_NAME)

BLUEPRINTS_YAML = "blueprints.yaml"
TYPE_ID_YAML = "typeIDs.yaml"
BLUEPRINTS_YAML_PATH = os.path.join(SCRIPT_DIR, "..", BLUEPRINTS_YAML)
TYPE_ID_YAML_PATH = os.path.join(SCRIPT_DIR, "..", TYPE_ID_YAML)


BLUEPRINTS_AND_PRODUCTS_TABLE = "blueprintsAndProducts"
BLUEPRINTS_AND_INPUTS_TABLE = "blueprintsAndInputs"
TYPE_ID_AND_EN_NAME = "idAndEnName"

# connection.execute(
#     f"CREATE TABLE {Constants.BLUEPRINTS_AND_PRODUCTS} (blueprintID INTEGER, quantity INTEGER, productID INTEGER)")
# connection.execute(
#     f"CREATE TABLE {Constants.BLUEPRINTS_AND_INPUTS} (blueprintID INTEGER, quantity INTEGER, inputID INTEGER)")

BLUEPRINT_ID_COLUMN_NAME = "blueprintID"
PRODUCT_ID_COLUMN_NAME = "productID"
QUANTITY_COLUMN_NAME = "quantity"
INPUT_ID_COLUMN_NAME = "inputID"
TYPE_ID_COLUMN = "typeID"
EN_NAME_COLUMN = "enName"

STOCKPILE_FILE_NAME = "Stockpile.txt"
STOCKPILE_FILE_PATH = os.path.join(SCRIPT_DIR, "..", STOCKPILE_FILE_NAME)
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
TYPE_ID_AND_EN_NAME_TABLE = "idAndEnName"
BLUEPRINT_AND_BUILD_TYPE_TABLE = "blueprintAndBuildType"
TYPE_ID_AND_ADJUSTED_PRICE_TABLE = "typeIdAndAdjustedPrice"
SYSTEM_ID_AND_INDUSTRY_INDEX_TABLE = "systemIdAndIndustryIndex"

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
BUILD_TYPE_COLUMN_NAME = "buildType"
ADJUSTED_PRICE_COLUMN_NAME = "adjustedPrice"

SYSTEM_ID_COLUMN_NAME = "systemId"
MANUFACTURING_INDEX_COLUMN_NAME = "manufacturingIndex"
TE_RESEARCH_INDEX_COLUMN_NAME = "researchTimeEfficiencyIndex"
ME_RESEARCH_INDEX_COLUMN_NAME = "researchMaterialEfficiencyIndex"
COPYING_INDEX_COLUMN_NAME = "copyingIndex"
REACTION_INDEX_COLUMN_NAME = "reactionIndex"
INVENTION_INDEX_COLUMN_NAME = "inventionIndex"

BUILD_TYPES = {"manufacturing": 0, "reaction": 1}

STOCKPILE_FILE_NAME = "Stockpile.txt"
STOCKPILE_FILE_PATH = os.path.join(SCRIPT_DIR, "..", STOCKPILE_FILE_NAME)
TREAT_AS_RAW_FILE_NAME = "treatAsRaw.txt"
TREAT_AS_RAW_FILE_PATH = os.path.join(SCRIPT_DIR, "..", TREAT_AS_RAW_FILE_NAME)
IN_PROGRESS_JOBS = "InProgressJobs.txt"
IN_PROGRESS_JOBS_FILE_PATH = os.path.join(SCRIPT_DIR, "..", IN_PROGRESS_JOBS)
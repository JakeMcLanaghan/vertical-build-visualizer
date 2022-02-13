#!/usr/bin/env python3
import sqlite3
from Constants import *

class DatabaseHandler:
    def __init__(self):
        print(f"Constructing Database Handler: {id(self)}")
        self.connection = sqlite3.connect(DATABASE_PATH)

    def __del__(self):
        self.connection.close()

    def get_type_id_for_name(self, name):
        todo = self.connection.execute(
            f"SELECT {TYPE_ID_COLUMN} FROM {TYPE_ID_AND_EN_NAME_TABLE} WHERE {EN_NAME_COLUMN} = ?", (name,)).fetchall()
        assert len(todo) == 1, f"expected 1 value returned from query, actual: {name}"
        return todo[0][0]

    def get_name_for_type_id(self, type_id):
        todo = self.connection.execute(
            f"SELECT {EN_NAME_COLUMN} FROM {TYPE_ID_AND_EN_NAME_TABLE} WHERE {TYPE_ID_COLUMN} = {type_id}").fetchall()
        assert len(todo) == 1, f"expected 1 value returned from query, actual: {todo}"
        return todo[0][0]

    def get_build_type_for_blueprint_id(self, blueprint_id):
        todo = self.connection.execute(
            f"SELECT {BUILD_TYPE_COLUMN_NAME} FROM {BLUEPRINT_AND_BUILD_TYPE_TABLE} WHERE {BLUEPRINT_ID_COLUMN_NAME} = {blueprint_id}").fetchall()
        assert len(todo) == 1, f"expected 1 value returned from query, actual: {todo}"
        return todo[0][0]

    def get_adjusted_price_for_type_id(self, type_id):
        todo = self.connection.execute(
            f"SELECT {ADJUSTED_PRICE_COLUMN_NAME} FROM {TYPE_ID_AND_ADJUSTED_PRICE_TABLE} WHERE {TYPE_ID_COLUMN} = {type_id}").fetchall()
        assert len(todo) == 1, f"expected 1 value returned from query, actual: {todo}"
        return todo[0][0]

    def get_industry_index_for_system(self, system_id, index_column_name):
        todo = self.connection.execute(
            f"SELECT {index_column_name} FROM {SYSTEM_ID_AND_INDUSTRY_INDEX_TABLE} WHERE {SYSTEM_ID_COLUMN_NAME} = {system_id}").fetchall()
        assert len(todo) == 1, f"expected 1 value returned from query, actual: {todo}"
        return todo[0][0]




if __name__ == "__main__":
    x = DatabaseHandler()
    print(x.get_adjusted_price_for_type_id(38))
else:
    database_handler = DatabaseHandler()

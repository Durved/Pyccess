import json
import os
import sqlite3


class DatabaseConfig:
    def __init__(self, database_path, db_name=None) -> None:
        self.database_path = os.path.join(database_path, db_name)
        if not os.path.exists(self.database_path):
            os.mkdir(self.database_path)
        self.config_path = os.path.join(self.database_path, '.pcscfg')
        if db_name:
            self.db_name = db_name
            self.dbfile_path = os.path.join(self.database_path, f'{db_name}.db')
            self.save_configure()
        else:
            self.load_configure()

    def save_configure(self):
        # if os.path.exists(self.database_path):
        #     raise Exception(f'Database {self.database_path} alriady exists!')
        with open(self.config_path, 'w') as file:
            json.dump(self.to_dict(), file)

    def load_configure(self):
        if not os.path.exists(self.config_path):
            raise Exception(f'Can\'t load database {self.database_path}!')
        with open(self.config_path, 'r') as file:
            self.from_dict(json.load(file))

    def delete_database(self):
        if os.path.exists(self.dbfile_path):
            os.remove(self.dbfile_path)
        os.remove(self.config_path)
        os.rmdir(self.database_path)

    def to_dict(self):
        config = {
            'db_name': self.db_name,
            'dbfile_path': self.dbfile_path
        }
        return config

    def from_dict(self, json_file):
        self.db_name = json_file['db_name']
        self.dbfile_path = json_file['dbfile_path']


class Database:
    def __init__(self, database_config: DatabaseConfig) -> None:
        self.database_config = database_config
        self.db = sqlite3.connect(database_config.dbfile_path)
        self.cur = self.db.cursor()

    def get_table_list(self):
        table_list = self.cur.execute('PRAGMA main.table_list;').fetchall()
        if ('main', 'sqlite_sequence', 'table', 2, 0, 0) in table_list:
            table_list.remove(('main', 'sqlite_sequence', 'table', 2, 0, 0))
        table_list.remove(('main', 'sqlite_schema', 'table', 5, 0, 0))
        return table_list

    def create_table(self, table_name):
        self.cur.execute(
            f'CREATE TABLE "{table_name}"("{table_name}_id" INTEGER PRIMARY KEY AUTOINCREMENT);')
        self.db.commit()

    def rename_table(self, old_table_name, new_table_name):
        self.cur.execute(
            f'ALTER TABLE "{old_table_name}" RENAME TO "{new_table_name}";')
        self.db.commit()

    def delete_table(self, table_name):
        self.cur.execute(f'DROP TABLE "{table_name}";')
        self.db.commit()


class Table:
    def __init__(self, databse: Database, table_name=None):
        self.database = databse
        self.name = table_name

    def get_table_info(self):
        return self.database.cur.execute(f'PRAGMA table_info("{self.name}");').fetchall()

    def add_column(self, column_name, data_type):
        self.database.cur.execute(
            f'ALTER TABLE "{self.name}" ADD "{column_name}" {data_type}')
        self.database.db.commit()

    def delete_column(self, column_name):
        self.database.cur.execute(
            f'ALTER TABLE "{self.name}" DROP COLUMN {column_name};')
        self.database.db.commit()

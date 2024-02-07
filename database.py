import json
import os


class Database:
    def __init__(self, config_path, db_name=None, dbfile_path=None) -> None:
        self.config_path = config_path

        if db_name and dbfile_path:
            self.db_config = {
                "db_name": db_name,
                "dbfile_path": dbfile_path
            }
            self.save_database()
        else:
            self.load_database()

    def save_database(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.db_config, file)
        open(self.db_config['dbfile_path'], 'w').close()

    def load_database(self):
        if not os.path.exists(self.config_path):
            raise Exception(f'Can\'t load database {self.config_path}!')
        with open(self.config_path, 'r') as file:
            self.db_config = json.load(file)
    
    def get_db_name(self):
        return self.db_config['db_name']

    def get_dbfile_path(self):
        return self.config_path
    
    def delete_database(self):
        os.remove(self.db_config['dbfile_path'])
        os.remove(self.config_path)
        os.rmdir(self.config_path.rsplit('/', 1)[0])
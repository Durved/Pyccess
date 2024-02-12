import json
import os


class AppConfig:
    def __init__(self, config_path=None) -> None:
        if config_path:
            self.config_path = config_path
        else:
            self.config_path = 'app_config.json'

        self.load_config()

    def save_config(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file)

    def load_config(self):
        if not os.path.exists(self.config_path):
            self.config = self.default_config()
            self.save_config()
            return
        with open(self.config_path, 'r') as file:
            self.config = json.load(file)

    def get_base_databases_dir(self):
        return self.config['base_databases_dir']
    
    def set_base_databases_dir(self, databases_dir):
        self.config['base_database_dir'] = databases_dir

    def get_database_list(self):
        return self.config['database_list']
    
    def get_database_path(self, index):
        return self.config['database_list'][index]['path']
    
    def add_database_to_list(self, db_name, path):
        self.config['database_list'].append({'name': db_name, 'path': path})
        self.save_config()
    
    def delete_database_from_list(self, index):
        del self.config['database_list'][index]
        self.save_config()

    def default_config(self):
        config = {}
        config['base_databases_dir'] = os.path.expanduser(
            '~\\Pyccess databases\\')
        config['database_list'] = []
        return config

import json
import os
from tkinter import END, Misc, Toplevel, filedialog
from tkinter.ttk import Button, Entry, Label


class AddDatabaseWindow(Toplevel):
    
    def __init__(self, master):
        super().__init__(master)
        self.title("Добавить БД")
        self.resizable(False, False)

        Label(self, text="Название файла:").grid(row=0, column=0, padx=5, pady=5)
        Label(self, text="Название БД:").grid(row=1, column=0, padx=5, pady=5)
        Label(self, text="Путь к папке:").grid(row=2, column=0, padx=5, pady=5)

        self.filename_entry = Entry(self)
        self.filename_entry.grid(row=0, column=1, padx=5, pady=5)

        self.db_name_entry = Entry(self)
        self.db_name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.folder_entry = Entry(self)
        self.folder_entry.grid(row=2, column=1, padx=5, pady=5)

        Button(self, text="Выбрать папку", command=self.browse_folder).grid(row=2, column=2, padx=5, pady=5)
        Button(self, text="Создать", command=self.create_database).grid(row=3, column=1, padx=5, pady=5)
        self.focus_set()
        self.grab_set()
        
    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_entry.delete(0, END)
            self.folder_entry.insert(0, folder_path)
            
    def create_database(self):
        filename = self.filename_entry.get()
        db_name = self.db_name_entry.get()
        path = self.folder_entry.get()

        if filename and db_name and path:
            # Создание папки, если её нет
            folder_path = f'{path}/{filename}'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Создание пути до конфигурационного файла
            config_file_path = os.path.join(folder_path, filename + ".pcscfg")

            # Создание пути до файла базы данных
            db_file_path = os.path.join(folder_path, filename + ".db")

            # Запись информации в конфигурационный файл
            config_data = {
                "db_name": db_name,
                "db_file_path": db_file_path
            }
            with open(config_file_path, "w") as config_file:
                json.dump(config_data, config_file)

            # Создание пустого файла базы данных
            open(db_file_path, "a").close()

            # Обновление списка баз данных
            self.master.add_database_to_list(db_name, config_file_path)

            # Закрытие окна
            self.grab_release()
            self.master.focus_set()
            self.destroy()
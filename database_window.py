import json
import os
from tkinter import END, SINGLE, Listbox, Tk, messagebox
from tkinter.ttk import Button, Frame, Label
import app_config
import database_config
import add_database_window


class DatabaseWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Pyccess")

        # Создание фрейма для списка баз данных
        self.database_frame = Frame(self)
        self.database_frame.grid(
            row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.database_label = Label(
            self.database_frame, text="Список баз данных")
        self.database_label.grid(row=0, column=0, columnspan=2)

        self.database_listbox = Listbox(self.database_frame, selectmode=SINGLE)
        self.database_listbox.grid(
            row=1, column=0, columnspan=2, pady=5, sticky="nsew")

        self.add_button = Button(
            self.database_frame, text="Добавить БД", command=self.add_database)
        self.add_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.delete_button = Button(
            self.database_frame, text="Удалить БД", command=self.delete_database)
        self.delete_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Создание фрейма для кнопок "Редактор" и "АИС"
        self.action_frame = Frame(self)
        self.action_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.editor_button = Button(
            self.action_frame, text="Редактор", command=self.open_editor)
        self.editor_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.ais_button = Button(
            self.action_frame, text="АИС", command=self.open_ais)
        self.ais_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.app_config = app_config.AppConfig()

        self.load_database_list()

    def add_database(self):
        # Окно для ввода информации о новой базе данных
        os.mkdir('testes/test1')
        db = database_config.DatabaseConfig(
            'testes/test1/test1.pcscfg', 'Тестовая 1', 'testes/test1/test1.db')
        self.app_config.add_database_to_list(
            db.get_db_name(), db.get_dbfile_path())
        
        self.load_database_list()
        # add_database_window.AddDatabaseWindow(self)

    def delete_database(self):
        selected_index = self.database_listbox.curselection()
        if not selected_index:
            messagebox.showerror(
                "Ошибка", "Выберите базу данных для удаления.")
            return
        selected_index = selected_index[0]

        database_config.DatabaseConfig(self.app_config.get_database_list()[selected_index]['path']).delete_database()
        self.app_config.delete_database_from_list(selected_index)
        self.load_database_list()

    def open_editor(self):
        selected_index = self.database_listbox.curselection()
        if not selected_index:
            messagebox.showerror(
                "Ошибка", "Выберите базу данных для удаления.")
            return

        selected_index = selected_index[0]
        db_path = self.app_config.get_database_list()[selected_index]['path']
        print(f'Открытие редактора {db_path}')

    def open_ais(self):
        # Здесь будет функционал открытия АИС
        if len(self.database_listbox.curselection()) < 1:
            return
        print("Открытие АИС")

    def load_database_list(self):
        database_list = self.app_config.get_database_list()
        self.database_listbox.delete(0, END)
        for database in database_list:
            self.database_listbox.insert(END, database["name"])


if __name__ == "__main__":
    app = DatabaseWindow()
    app.mainloop()

import json
import os
from tkinter import END, SINGLE, Listbox, Tk, messagebox
from tkinter.ttk import Button, Frame, Label
from add_database_window import AddDatabaseWindow

class DatabaseWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Pyccess")

        # Создание фрейма для списка баз данных
        self.database_frame = Frame(self)
        self.database_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.database_label = Label(self.database_frame, text="Список баз данных")
        self.database_label.grid(row=0, column=0, columnspan=2)

        self.database_listbox = Listbox(self.database_frame, selectmode=SINGLE)
        self.database_listbox.grid(row=1, column=0, columnspan=2, pady=5, sticky="nsew")

        self.add_button = Button(self.database_frame, text="Добавить БД", command=self.add_database)
        self.add_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.delete_button = Button(self.database_frame, text="Удалить БД", command=self.delete_database)
        self.delete_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Создание фрейма для кнопок "Редактор" и "АИС"
        self.action_frame = Frame(self)
        self.action_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.editor_button = Button(self.action_frame, text="Редактор", command=self.open_editor)
        self.editor_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.ais_button = Button(self.action_frame, text="АИС", command=self.open_ais)
        self.ais_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.load_database_list()

    def add_database(self):
        # Окно для ввода информации о новой базе данных
        AddDatabaseWindow(self)

    def delete_database(self):
        # Здесь будет функционал удаления выбранной базы данных
        selected_index = self.database_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Ошибка", "Выберите базу данных для удаления.")
            return
        
        selected_index = selected_index[0]
        
        selected_name = self.database_listbox.get(selected_index)

        # Запрашиваем подтверждение удаления
        confirmation = messagebox.askyesno("Удаление базы данных", f"Вы уверены, что хотите удалить базу данных '{selected_name}'?")

        if confirmation:
            # Удаляем базу данных из списка
            self.database_listbox.delete(selected_index)
            # Удаляем базу данных из файла
            with open("database_list.json", "r") as file:
                database_list = json.load(file)
            
            del database_list[selected_index]

            with open("database_list.json", "w") as file:
                json.dump(database_list, file)

    def open_editor(self):
        # Здесь будет функционал открытия редактора
        if len(self.database_listbox.curselection()) < 1:
            return
        print(f'Открытие редактора {self.get_database_path()}')

    def open_ais(self):
        # Здесь будет функционал открытия АИС
        if len(self.database_listbox.curselection()) < 1:
            return
        print("Открытие АИС")

    def load_database_list(self):
        if os.path.exists("database_list.json"):
            with open("database_list.json", "r") as file:
                database_list = json.load(file)
                for database in database_list:
                    self.database_listbox.insert(END, database["name"])

    def get_database_path(self):
        if os.path.exists("database_list.json"):
            with open("database_list.json", "r") as file:
                database_list = json.load(file)
                return database_list[self.database_listbox.curselection()[0]]['path']
            
    def add_database_to_list(self, name, path):
        if os.path.exists("database_list.json"):
            with open("database_list.json", "r") as file:
                database_list = json.load(file)
        else:
            database_list = []
        
        database_list.append({"name": name, "path": path})

        with open("database_list.json", "w") as file:
            json.dump(database_list, file)

        self.database_listbox.insert(END, name)

if __name__ == "__main__":
    app = DatabaseWindow()
    app.mainloop()
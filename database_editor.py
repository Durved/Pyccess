from tkinter import END, SINGLE, Listbox, Tk, messagebox, simpledialog
from tkinter.ttk import Button, Frame, Label, LabelFrame, Treeview
from database import Database, DatabaseConfig, Table


class DatabaseEditor(Tk):

    def __init__(self, database_config: DatabaseConfig):
        super().__init__()
        self.database = Database(database_config)

        self.acction_frame = Frame(
            self, borderwidth=1, relief='solid', padding=2)
        self.acction_frame.grid(
            row=0, column=0, columnspan=2, padx=2, pady=2, sticky='nsew')

        self.create_table_button = Button(
            self.acction_frame, text='Создать', command=self.create_table)
        self.create_table_button.grid(row=0, column=0)

        self.modify_table_button = Button(
            self.acction_frame, text='Модифицировать', command=self.info_table)
        self.modify_table_button.grid(row=0, column=1)

        self.delete_table_button = Button(
            self.acction_frame, text='Удалить', command=self.delete_table)
        self.delete_table_button.grid(row=0, column=2)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.table_labelframe = Frame(
            self, borderwidth=1, relief='solid', padding=2)
        self.table_labelframe.grid(
            row=1, column=0, padx=2, pady=2, sticky='nsew')
        self.table_labelframe.rowconfigure(0, weight=1)

        self.table_listbox = Listbox(self.table_labelframe, selectmode=SINGLE)
        self.table_listbox.grid(row=0, column=0, sticky='nsew')
        self.table_listbox.bind('<Double-Button-1>', self.info_table)

        self.table_info = TableEditor(self)
        self.table_info.grid(row=1, column=1, padx=2, pady=2, sticky='nsew')

        self.load_list_table()

    def create_table(self):
        table_name = simpledialog.askstring(
            'Создать талбицу', 'Введите название таблицы:')
        if table_name is None:
            return
        self.database.create_table(table_name)
        self.load_list_table()

    def delete_table(self):
        selected_index = self.table_listbox.curselection()
        if not selected_index:
            messagebox.showerror(
                'Ошибка', 'Выберите таблицу для удаления.')
            return

        selected_index = selected_index[0]
        selected_name = self.table_listbox.get(selected_index)
        self.database.delete_table(selected_name)
        self.table_info.table.name = None
        self.table_info.update_table_info()
        self.load_list_table()

    def info_table(self, event=None):
        selected_index = self.table_listbox.curselection()
        if not selected_index:
            messagebox.showerror(
                'Ошибка', 'Выберите таблицу для редактирования.')
            return

        selected_index = selected_index[0]
        selected_name = self.table_listbox.get(selected_index)

        self.table_info.table.name = selected_name
        self.table_info.update_table_info()

    def load_list_table(self):
        tables = self.database.get_table_list()
        self.table_listbox.delete(0, END)
        for table in tables:
            self.table_listbox.insert(END, table[1])


class TableEditor(Frame):
    def __init__(self, master: DatabaseEditor):
        super().__init__(master=master, borderwidth=1, relief='solid', padding=2)

        self.table = Table(master.database)

        self.action_frame = Frame(self)
        self.action_frame.grid(row=0, column=0, sticky='nsew')

        self.add_column_button = Button(
            self.action_frame, text='Добавить', command=self.add_column)
        self.add_column_button.grid(row=0, column=0)

        self.delete_column_button = Button(
            self.action_frame, text='Удалить', command=self.delete_column)
        self.delete_column_button.grid(row=0, column=1)

        self.table_info_treeview = Treeview(self, columns=(
            'Primary Key', 'Name', 'Type'), show='headings')
        self.table_info_treeview.grid(row=1, column=0, sticky='nsew')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.table_info_treeview.heading('Name', text='Имя')
        self.table_info_treeview.heading('Type', text='Тип')
        self.table_info_treeview.heading('Primary Key', text='ПК')

        self.table_info_treeview.column(
            '#1', width=25, stretch=False, anchor='center')
        self.table_info_treeview.column('#2', width=100)
        self.table_info_treeview.column('#3', width=120)

    def update_table_info(self):
        self.table_info_treeview.delete(
            *self.table_info_treeview.get_children())
        if not self.table:
            return
        for i in self.table.get_table_info():
            values = ['X' if i[j] == 1 else '' if i[j] == 0 else i[j]
                      for j in (5, 1, 2)]
            self.table_info_treeview.insert('', END, values=values)

    def add_column(self):
        column_name = simpledialog.askstring(
            'Добавить столбец', 'Введите название столбца:')
        if column_name is None:
            return

        data_type = simpledialog.askstring(
            'Тип данных столбца', 'Введите тип данных столбца:')
        if data_type is None:
            return
        self.table.add_column(column_name, data_type.upper())
        self.update_table_info()

    def delete_column(self):
        for i in self.table_info_treeview.selection():
            self.table.delete_column(
                self.table_info_treeview.item(i)['values'][1])
        self.update_table_info()

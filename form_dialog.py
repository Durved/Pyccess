from tkinter import Toplevel
from tkinter.ttk import Button, Entry, Frame, Label


class FormDialog(Toplevel):
    def __init__(self, master, title: str, fields: list):
        super().__init__(master)
        self.title(title)

        self.withdraw()

        if master.winfo_viewable():
            self.transient(master)

        self.form_frame = Frame(self)
        self.form_frame.grid(row=0, column=0, padx=2, pady=2, columnspan=2, sticky='nsew')

        self.entries = {}
        for i, val in enumerate(fields):
            lb = Label(self.form_frame, text=val)
            lb.grid(row=i, column=0, sticky='e')

            e = Entry(self.form_frame)
            e.grid(row=i, column=1, sticky='ew')
            self.entries[val] = e

        self.action_frame = Frame(self)
        self.action_frame.grid(row=1, column=1, padx=2, pady=2, sticky='nsew')

        self.ok_button = Button(self.action_frame, text='Ok')
        self.ok_button.grid(row=0, column=0, sticky='ew')

        self.ok_button = Button(self.action_frame, text='Отмена', command=lambda: self.destroy())
        self.ok_button.grid(row=0, column=1, sticky='ew')

        self.wm_withdraw() # Remain invisible while we figure out the geometry
        self.update_idletasks() 
        self.wm_deiconify()
        _place_window(self, master)

        self.focus_set()

        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

def _place_window(w, parent=None):
    w.wm_withdraw() # Remain invisible while we figure out the geometry
    w.update_idletasks() # Actualize geometry information

    minwidth = w.winfo_reqwidth()
    minheight = w.winfo_reqheight()
    maxwidth = w.winfo_vrootwidth()
    maxheight = w.winfo_vrootheight()
    if parent is not None and parent.winfo_ismapped():
        x = parent.winfo_rootx() + (parent.winfo_width() - minwidth) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - minheight) // 2
        vrootx = w.winfo_vrootx()
        vrooty = w.winfo_vrooty()
        x = min(x, vrootx + maxwidth - minwidth)
        x = max(x, vrootx)
        y = min(y, vrooty + maxheight - minheight)
        y = max(y, vrooty)
        if w._windowingsystem == 'aqua':
            # Avoid the native menu bar which sits on top of everything.
            y = max(y, 22)
    else:
        x = (w.winfo_screenwidth() - minwidth) // 2
        y = (w.winfo_screenheight() - minheight) // 2

    w.wm_maxsize(maxwidth, maxheight)
    w.wm_geometry('+%d+%d' % (x, y))
    w.wm_deiconify() # Become visible at the desired location
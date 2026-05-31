from tkinter import *
from tksheet import Sheet
from tkinter import ttk
from styles_parameters import styleF #used in 31
from appFuncs import *
from sheetBackend import *



class App:
    root=None
    upper = None
    text_field=None
    sheet = None
    console = None

    def show_textfield(self):
        self.text_field = Text(self.upper, height=2, width=10)
        self.text_field.grid(row=2, column=0, padx=100, pady=5, sticky="we")

        enter = ttk.Button(self.upper, text="↵", command=lambda: enter_command(self.text_field, self.sheet), width=10)
        enter.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        button = ttk.Button(self.upper, text="A", command=lambda: pr(button, self.text_field), width = 10)
        button.grid(row=2, column=0, padx=5, pady=5, sticky = 'w')

        self.upper.grid_columnconfigure(0, weight=1)
        self.upper.grid_columnconfigure(1, weight=0)



    def create_upper(self):
        styleF()
        frm = ttk.Frame(self.root, style='Upper.TFrame')
        frm.grid(row=0, column=0, sticky="nsew")

        file = ttk.Button(frm, text='File', style='Default.TButton', takefocus=False)
        file.grid(row=0, column=0, padx=0, pady=0, sticky='w')
        home = ttk.Button(frm, text='Home', style='Active.Default.TButton', takefocus=False)
        home.grid(row=0, column=0, padx=100, pady=0, sticky='w')
        insert = ttk.Button(frm, text='Insert', style='Default.TButton', takefocus=False)
        insert.grid(row=0, column=0, padx=200, pady=0, sticky='w')
        file.configure(command=lambda: fileF([file, insert, home], self.cr_file))
        home.configure(command=lambda: homeF([home, insert, file], self.cr_home))
        insert.configure(command=lambda: insertF([insert, home, file], self.cr_insert))
        separator = ttk.Separator(frm, orient='horizontal')
        separator.grid(row=1, column=0, sticky='new', pady=(0, 50))
        return frm

    def create_body(self):
        frm = ttk.Frame(self.root)
        frm.grid(row=3, column=0, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

        frm.grid_columnconfigure(0, weight=1)

        frm.grid_rowconfigure(0, weight=0)
        frm.grid_rowconfigure(1, weight=0)
        frm.grid_rowconfigure(2, weight=0)
        frm.grid_rowconfigure(3, weight=1)

        self.sheet = Sheet(frm, data=database.data) #CREATING SHEET
        self.sheet.enable_bindings()
        self.sheet.grid(row=3, column=0, sticky="nsew")

    def create(self):
        self.root = Tk()
        self.root.title("my app")
        self.root.geometry("800x600")

        self.upper = self.create_upper()
        self.show_textfield()
        self.create_body()
        h, homeParams = self.cr_home()
        i, insParams = self.cr_insert()
        f, fileParams = self.cr_file()

        self.root.mainloop()

    def cr_home(self):
        frm = ttk.Frame(self.root)
        frm.grid(row=1, column=0, sticky="new")
        lab = ttk.Button(frm, text='home')
        lab.grid(row=0, column=0, sticky="new")
        params = frm.grid_info()

        return [frm, params]

    def cr_insert(self):
        frm = ttk.Frame(self.root)
        frm.grid(row=1, column=0, sticky="new")
        lab = ttk.Button(frm, text='insert')
        lab.grid(row=0, column=0, sticky="new")
        params = frm.grid_info()
        lab.grid_remove()
        return [frm, params]

    def cr_file(self):
        frm = ttk.Frame(self.root)
        frm.grid(row=1, column=0, sticky="new")
        lab = ttk.Button(frm, text='file')
        lab.grid(row=0, column=0, sticky="new")
        params = frm.grid_info()
        lab.grid_remove()
        return [frm, params]





app = App()
app.create()
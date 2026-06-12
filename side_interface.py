from tkinter import ttk, scrolledtext
from tkinter import *
from appFuncs import *

class Side:
    def __init__(self, root):
        self.root = root
        self.frmHom = None
        self.frmIns = None
        self.frmFil = None
        self.cr_home()
        self.cr_insert()
        self.cr_file()


    def cr_frm(self):
        frm = ttk.Frame(self.root, style='side_interface.TFrame')
        frm.grid(row=0, column=0, sticky="new", pady=(35, 0))
        return frm

    def cr_home(self):
        frm=self.cr_frm()
        lab = ttk.Button(frm, text='home')
        lab.grid(row=0, column=0, sticky="nsew", pady=(5, 5))
        self.frmHom = frm

    def cr_insert(self):
        frm=self.cr_frm()
        lab = ttk.Button(frm, text='insert')
        lab.grid(row=0, column=0, sticky="new",pady=(5, 5))
        self.frmIns = frm
        frm.grid_remove()


    def cr_file(self):
        frm=self.cr_frm()
        saveB = ttk.Button(frm, text='save')
        saveB.grid(row=0, column=0, sticky="new",pady=(5, 5), padx=2)
        openB = ttk.Button(frm, text='open', command=self.read_file)
        openB.grid(row=0, column=1, sticky="new", pady=(5, 5), padx=2)
        self.frmFil = frm
        frm.grid_remove()

    def read_file(self):
        inform, isError = open_file()
        new_screen = Tk()
        frm = ttk.Frame(new_screen)
        frm.grid(row=0,column=0, sticky='nsew')
        new_screen.grid_columnconfigure(0, weight=1)
        new_screen.grid_rowconfigure(0, weight=1)
        new_screen.geometry('800x400')
        if not isError:
            showing_text = '\n'.join(inform.split('\n')[0:min(inform.count('\n')+1, 100)])
            lbl = scrolledtext.ScrolledText(frm, width=40, height=30)
            lbl.grid(row=0, column=0, sticky='nsew')
            lbl.insert('insert',showing_text)
            lbl.config(state='disabled')
            split_field = Text(frm, height=1, width=20)
            split_field.grid(row=1, column=0, sticky='ne', pady=5, padx=100)
            splitB = ttk.Button(frm, text='↵', command=lambda: splitter(inform, split_field.get("1.0", "end-1c")))
            splitB.grid(row=1,column=0, sticky='ne', padx=15)
            tip=ttk.Label(frm, text='split symbol: ', borderwidth=5)
            tip.grid(row=1, column=0, sticky='ne', padx=(0,270))
            new_screen.minsize(600,20)
            frm.grid_rowconfigure(0, weight=1)
            frm.grid_columnconfigure(0, weight=1)
        else:
            lbl = ttk.Label(frm, text=inform)
            lbl.grid(row=0,column=0, sticky='nsew')



    def hide_home(self):
        self.frmHom.grid_remove()

    def hide_file(self):
        self.frmFil.grid_remove()

    def hide_ins(self):
        self.frmIns.grid_remove()

    def show_home(self):
        self.frmHom.grid()
        self.hide_ins()
        self.hide_file()

    def show_file(self):
        self.frmFil.grid()
        self.hide_ins()
        self.hide_home()

    def show_ins(self):
        self.frmIns.grid()
        self.hide_home()
        self.hide_file()
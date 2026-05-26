from tkinter import *
from tkinter import ttk
from itertools import product



class database():
    vals = [[]]*1000
    formulas = [[]]*1000


class app():

    def show_textfield(self, upper):
        def pr():
            if button.cget('text') == 'A':
                text_field.config(height=10)
                button.config(text = 'a')
            else:
                text_field.config(height=2)
                button.config(text='A')
        text_field = Text(upper,  height=2)
        text_field.grid(column=3, row=0)
        button = ttk.Button(upper, text="A", command=pr)
        button.grid(column=4, row=0)

    def create_upper(self, root):
        frm = ttk.Frame(root)
        frm.grid()
        ttk.Label(frm, text="smth").grid(column=0, row=0)
        return frm

    def create_body(self, root, upper):
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        for i in range(15):
            ttk.Label(frm, text=str(i)).grid(column=0, row=i)
            ttk.Label(frm, text=str(i)).grid(column=i, row=0)
        for i, j in list(product(range(1,15), range(1, 15))):
            ttk.Button(frm, text="     ", command=self.show_textfield(self, upper)).grid(column=i, row=j)

    def create(self):
        root = Tk()
        upper = self.create_upper(self, root)
        self.create_body(self, root, upper)
        root.mainloop()


a=app
app.create(self=a)
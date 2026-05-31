from styles_parameters import styleF
from sheetBackend import *


def stChange(buttons:list):
    for i in range(len(buttons)):
        if i==0:
            buttons[i].configure(style='Active.Default.TButton')
        else:
            buttons[i].configure(style='Default.TButton')

def fileF(buttons:list, func):
    stChange(buttons)
    func()

def insertF(buttons:list, func):
    stChange(buttons)
    func()

def homeF(buttons:list, func):
    stChange(buttons)
    func()


def pr(button, text_field):
    if button.cget('text') == 'A':
        text_field.config(height=10)
        button.config(text='a')
    else:
        text_field.config(height=2)
        button.config(text='A')


def enter_command(text_field, sheet):
    curr = sheet.get_currently_selected()
    if curr:
        text_field.update_idletasks()
        res = ceil_comm(text_field.get("1.0", "end-1c"))
        row = curr.row
        column=curr.column
        typ=curr.type_
        if typ=='cells':
            ceil_fill(row, column, res)
    sheet.refresh()
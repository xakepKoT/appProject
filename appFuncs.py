from styles_parameters import styleF
from sheetBackend import ceil_fill, ceil_comm, database
from tkinter import END, filedialog


def stChange(buttons:list):
    for i in range(len(buttons)):
        if i==0:
            buttons[i].configure(style='Active.Default.TButton')
        else:
            buttons[i].configure(style='Default.TButton')

def buttonF(buttons:list, func):
    stChange(buttons)
    func()


def pr(button, text_field):
    if button.cget('text') == '↑':
        text_field.config(height=10)
        button.config(text='↓')
    else:
        text_field.config(height=2)
        button.config(text='↑')


def enter_command(text_field, sheet):
    curr = sheet.get_currently_selected()
    if curr:
        text_field.update_idletasks()
        res, link, formula = ceil_comm(text_field.get("1.0", "end-1c"))
        row = curr.row
        column=curr.column
        typ=curr.type_
        if typ=='cells':
            ceil_fill(row, column, res, link, formula)
    sheet.refresh()


def sheet_clicked(text_field, sheet):
    curr = sheet.get_currently_selected()
    if curr:
        row = curr.row
        column = curr.column
        typ = curr.type_
        if typ == 'cells':
            text_field.delete("1.0", END)
            text_field.insert("1.0", database.formulas[row][column])


def sheet_modified(event):
    row, column = event.row, event.column
    old = database.data[row][column]
    database.data[row][column]=''
    data, linked, formula = ceil_comm(event.value)
    database.data[row][column] = old
    if not all([database.data[row][column] == data, database.linked[row][column] == linked, database.formulas[row][column] == formula]):
        ceil_fill(row, column, data, linked, formula)


def open_file(): #True - error, False - no errors
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path:
        content = "Selection was cancelled."
        return content, True
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        return "File not found.", True
    except PermissionError:
        return "Insufficient permissions to read the file.", True
    except Exception as e:
        return f"Unexpected error: {e}", True
    else:
        return content, False


def splitter(text, sp_symb):
    res=[]
    splitted = text.split('\n')
    max_l = max(len(i) for i in splitted)
    for i in splitted:
        el = i.split(sp_symb)
        res += [el+(max(100,2*max_l))*['']]
    res+=len(splitted)*[['']*max(100,2*max_l)]
    database.data = res
    database.formulas = list(i.copy() for i in res)#res.copy()
    database.linked = [[[] for c in range(len(res[0]))] for r in range(len(res))]
    database.sheet.set_sheet_data(database.data)
    database.sheet.refresh()
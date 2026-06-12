from styles_parameters import styleF
from sheetBackend import *
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

def sheet_clicked(text_field, sheet):
    curr = sheet.get_currently_selected()
    if curr:
        row = curr.row
        column = curr.column
        typ = curr.type_
        if typ == 'cells':
            text_field.delete("1.0", END)
            text_field.insert("1.0", database.data[row][column])

def open_file(): #True - error, False - no errors
    file_path = filedialog.askopenfilename(
        title="Выберите файл",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )

    if not file_path:
        content = "Выбор файла отменён."
        return content, True

    print(f"\nВыбран файл: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        return "Ошибка: Файл не найден.", True
    except PermissionError:
        return "Ошибка: Нет прав для чтения этого файла.", True
    except Exception as e:
        return f"Непредвиденная ошибка: {e}", True
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
    database.sheet.set_sheet_data(res)
    database.sheet.refresh()



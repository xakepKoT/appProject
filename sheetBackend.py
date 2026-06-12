from re import *
from traceback import format_exc
from tkinter import IntVar


class database():
    data=[['' for c in range(500)] for r in range(500)]
    linked = [[None for c in range(500)] for r in range(500)]
    sheet = None


pattern = r"#\$?[A-Z]+\$?[0-9]+"
patternA = r"[A-Z]+"
patternB = r"[0-9]+"
aind=ord('a')
def ceil_comm(s:str):
    data = database.data
    if s == ' '*s.count(' '):
        return s
    if s.strip()[0] == '=':
        s=s.strip()[1:]
        match=search(pattern, s)
        while match:
            result = match.group()
            row = int(search(patternB, result).group())-1
            letters = search(patternA, result).group()[::-1]
            column = sum((ord(letters[i].lower())-aind+1)*26**i for i in range(len(letters)))-1
            repl = data[row][column]
            if not repl.isdigit():
                repl = f"'{repl}'"
            s = s.replace(result, repl)
            match=search(pattern, s)
        try:
            eval(s)
        except:
            s=format_exc()
        else:
            s=eval(s)
    return s


def ceil_fill(row, column, data):
    database.data[row][column] = data



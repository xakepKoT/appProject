from re import *


class database():
    data=[['' for c in range(500)] for r in range(500)]
    linked = [[[] for c in range(500)] for r in range(500)]
    back_linked = [[[] for c in range(500)] for r in range(500)]
    formulas = [['' for c in range(500)] for r in range(500)]
    sheet = None


pattern = r"#\$?[A-Z]+\$?[0-9]+"
patternA = r"[A-Z]+"
patternB = r"[0-9]+"
patternList1 = r"#\[[A-Z]+:[A-Z]+\]"
patternList2 = r"#\[[0-9]+:[0-9]+\]"
aind=ord('a')
forbidden_names = ['__import__', 'eval', 'exec', 'compile', 'open', 'input', 'file',
            'os', 'sys', 'subprocess', 'shutil', 'glob', 'socket', 'pickle',
            'builtins', '__builtins__', '__import__', 'execfile', 'reload', 'inf', 'def']
def ceil_comm(s:str):
    formula = s
    data = database.data
    linked = []
    if s == ' '*s.count(' '):
        return s, linked, formula
    if s.strip()[0] == '=':
        for i in forbidden_names:
            if i in s:
                return f'forbidden: {i}', linked, formula
        s=s.strip()[1:]
        match=search(pattern, s)
        match1 = search(patternList1, s)
        match2 = search(patternList2, s)
        while match:
            result = match.group()
            row = int(search(patternB, result).group())-1
            letters = search(patternA, result).group()[::-1]
            column = sum((ord(letters[i].lower())-aind+1)*26**i for i in range(len(letters)))-1
            repl = data[row][column]
            linked.append([row, column])
            if not repl.isdigit():
                repl = f"'{repl}'"
            s = s.replace(result, repl)
            match=search(pattern, s)
        while match1:
            result = match1.group()
            letters = search(patternA, result).group()[::-1]
            column = sum((ord(letters[i].lower()) - aind + 1) * 26 ** i for i in range(len(letters))) - 1
            repl = '['+', '.join(list(data[i][column] for i in range(len(data)) if data[i][column] != ''))+']'
            linked=list([i, column] for i in range(len(data)))
            s = s.replace(result, repl)
            match1 = search(pattern, s)
        while match2:
            result = match2.group()
            row = int(search(patternB, result).group())-1
            repl = '['+', '.join(list(i for i in data[row] if i!=''))+']'
            linked=list([row, i] for i in range(len(data[row])))
            s = s.replace(result, repl)
            match2 = search(pattern, s)
        try:
            eval(s)
        except Exception as e:
            s=str(e)
        else:
            s=str(eval(s))
    return s, linked, formula


def ceil_fill(row, column, data, linked, formula):
    database.data[row][column] = data
    database.formulas[row][column] = formula
    for i in database.linked[row][column]:
        r,c = i
        database.data[r][c] = ceil_comm(database.formulas[r][c])[0]
    for i in linked:
        database.linked[i[0]][i[1]].append([row, column])
    for i in database.back_linked[row][column]:
        database.linked[i[0]][i[1]].pop(database.linked[i[0]][i[1]].index([row, column]))
    database.back_linked[row][column] = linked


def num_to_letters(n: int) -> str:
    if n < 0:
        raise ValueError("negative num was given")
    n += 1
    result = []

    while n > 0:
        n -= 1
        remainder = n % 26
        result.append(chr(ord('A') + remainder))
        n //= 26
    return ''.join(reversed(result))


def changed_paste(event):
    pattern_letters = r"\$+[A-Z]+"
    pattern_digits=r"\$+[0-9]+"
    cur = database.sheet.get_currently_selected()
    cur_row, cur_col = cur.row, cur.column
    value = database.formulas[cur_row][cur_col]
    for (row, col), val in list(event.data.items()):
        s = value
        s2=value
        if s=='':
            return event
        if s.strip()[0] == '=':
            match = search(pattern, s2)
            while match:
                result = match.group()
                lettersR=search(patternB, result).group()
                row2 = int(lettersR) - 1
                lettersC = search(patternA, result).group()[::-1]
                col2 = sum((ord(lettersC[i].lower()) - aind + 1) * 26 ** i for i in range(len(lettersC))) - 1
                diffR, diffC = row-cur_row+1, col-cur_col
                repl1=num_to_letters(col2+diffC) if not search(pattern_letters, result) else '$'+lettersC
                repl2=str(row2+diffR) if not search(pattern_digits, result) else '$'+lettersR
                repl = '#'+repl1+repl2
                s=s.replace(result, repl)
                s2=s2.replace(result, '')
                match = search(pattern, s2)

        data, linked, formula = ceil_comm(s)
        ceil_fill(row, col, data, linked, formula)
        event.data[(row, col)] = data

    return event

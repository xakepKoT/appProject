from sheetBackend import ceil_comm, num_to_letters, database, ceil_fill
from appFuncs import splitter


def test_num_to_letters():
    assert num_to_letters(0) == 'A'
    assert num_to_letters(25) == 'Z'
    assert num_to_letters(26) == 'AA'
    assert num_to_letters(51) == 'AZ'
    assert num_to_letters(52) == 'BA'
    assert num_to_letters(701) == 'ZZ'
    assert num_to_letters(702) == 'AAA'


def test_ceil_comm_basic():
    result, links, formula = ceil_comm('=2+3')
    assert result == '5'
    assert links == []
    assert formula == '=2+3'

    result, links, formula = ceil_comm('= 10 * 2')
    assert result == '20'
    assert links == []

    result, links, formula = ceil_comm('hello')
    assert result == 'hello'
    assert links == []
    assert formula == 'hello'

    result, links, formula = ceil_comm('   ')
    assert result == '   '
    assert links == []
    assert formula == '   '


def test_ceil_comm():
    database.data = [['' for _ in range(500)] for _ in range(500)]
    database.data[0][0] = '10'   # A1
    database.data[0][1] = '20'   # B1
    database.data[1][0] = '30'   # A2
    database.data[1][1] = '40'   # B2

    result, links, formula = ceil_comm('=#A1 + #B1')
    assert result == '30' or result == '30.0'  # 10 + 20
    assert links == [[0, 0], [0, 1]]
    assert formula == '=#A1 + #B1'

    result, links, formula = ceil_comm('=#$A$1 * 2')
    assert result == '20'or result == '20.0'
    assert links == [[0, 0]]

    database.data[0][2] = 'abc'  # C1
    result, links, formula = ceil_comm('=#C1')
    assert result == 'abc'
    assert links == [[0, 2]]

    result, links, formula = ceil_comm('=(#A1 + #B1) * #A2')
    assert result == '900' or result == '900.0'
    assert links == [[0,0], [0,1], [1,0]]

def test_ceil_comm_ranges():
    database.data = [['' for _ in range(500)] for _ in range(500)]
    for r in range(3):
        for c in range(3):
            database.data[r][c] = str((r+1) * (c+1))  # 1,2,3; 2,4,6; 3,6,9

    result, links, formula = ceil_comm('=#[A:A]')
    expected = '[1, 2, 3]'
    assert result == expected

    result, links, formula = ceil_comm('=#[1:1]')
    expected = '[1, 2, 3]'
    assert result == expected


def test_ceil_comm_errors():
    database.data = [['' for _ in range(500)] for _ in range(500)]
    result, links, formula = ceil_comm('=1/0')
    assert 'division by zero' in result or 'ZeroDivisionError' in result

    result, links, formula = ceil_comm('=2+')
    assert 'invalid syntax' in result or 'SyntaxError' in result

    result, links, formula = ceil_comm('=import os')
    assert result == 'forbidden: import' or result == 'forbidden: os'


def test_ceil_fill():
    ceil_fill(0, 0, '10', [], '')
    assert database.data[0][0] == '10'
    assert database.formulas[0][0] == ''
    val, links, formula = ceil_comm('=#A1*2')
    ceil_fill(0, 1, val, links, '=#A1*2')
    assert database.data[0][1] == '20' or database.data[0][1] == '20.0'
    assert database.formulas[0][1] == '=#A1*2'
    assert [0, 1] in database.linked[0][0]
    ceil_fill(0, 0, '5', [], '')
    assert database.data[0][1] == '10' or database.data[0][1] == '10.0'  # 5*2 = 10
    assert database.formulas[0][1] == '=#A1*2'
    database.data = [['' for _ in range(500)] for _ in range(500)]
    database.formulas = [['' for _ in range(500)] for _ in range(500)]
    database.linked = [[[] for _ in range(500)] for _ in range(500)]
    database.back_linked = [[[] for _ in range(500)] for _ in range(500)]



def test_all():
    test_num_to_letters()
    test_ceil_comm_basic()
    test_ceil_comm()
    test_ceil_comm_ranges()
    test_ceil_comm_errors()
    test_ceil_fill()
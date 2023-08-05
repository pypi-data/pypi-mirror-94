"""LIBrary to convert integers into Spreadsheet COLumn names, and vice versa"""

__version__ = "0.9.1"

from itertools import count

def int2scol(num):
    """convert integer num into spreadsheet column name
>>> for n in [-2, -1, 0, 1, 2, 25, 26, 27, 28, 701, 702, 703, 704]: print((n, int2scol(n)))
(-2, '-C')
(-1, '-B')
(0, 'A')
(1, 'B')
(2, 'C')
(25, 'Z')
(26, 'AA')
(27, 'AB')
(28, 'AC')
(701, 'ZZ')
(702, 'AAA')
(703, 'AAB')
(704, 'AAC')
"""
    neg = False
    if num < 0:
        neg = True
        num = -num
    sum = 0
    for exp in count(1, 1):
        prev = sum
        sum += 26 ** exp
        if num < sum:
            break
    num -= prev
    scol = ""
    for j in range(exp):
        num, mod = divmod(num, 26)
        scol = chr(65 + mod) + scol
    return "-" + scol if neg else scol

def scol2int(scol):
    """convert spreadsheet column name scol into integer
>>> all(n == scol2int(int2scol(n)) for n in range(-100000, 100000))
True
"""
    scol = scol.strip().upper()
    neg = False
    if scol.startswith("+"):
        scol = scol[1:]
    elif scol.startswith("-"):
        scol = scol[1:]
        neg = True
    if not scol:
        raise ValueError("scol2int: null string '' not allowed")
    err = "".join(char for char in scol if not("A" <= char <= "Z"))
    if err:
        raise ValueError(f"scol2int: characters {err!r} not allowed")
    exp = len(scol)
    num = (sum(26 ** j for j in range(1, exp)) +
           sum((ord(char) - 65) * 26 ** (exp - j - 1) for j, char in enumerate(scol)))
    return -num if neg else num

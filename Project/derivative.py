# derivative.py
# File dung de tinh dao ham ham mot bien

import sympy as sp


def compute_derivative(f):
    """
    Tinh dao ham cap 1 cua ham f theo bien x.
    Tham so:
        f : bieu thuc SymPy
    Tra ve:
        dao ham f'(x)
    """
    x = sp.symbols('x')
    return sp.diff(f, x)


def compute_nth_derivative(f, n):
    """
    Tinh dao ham cap n cua ham f theo bien x.
    Tham so:
        f : bieu thuc SymPy
        n : cap dao ham (so nguyen duong)
    Tra ve:
        dao ham cap n cua f
    """
    x = sp.symbols('x')
    if not isinstance(n, int) or n < 1:
        raise ValueError("n phải là số nguyên dương.")
    return sp.diff(f, x, n)

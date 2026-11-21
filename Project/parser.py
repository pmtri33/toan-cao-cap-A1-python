# parser.py
# Chuyen chuoi nguoi dung nhap thanh bieu thuc SymPy
# Ho tro:
#   - Ham mot bien f(x)
#   - Ham hai bien f(x, y)

import sympy as sp


def _log(value, base=10):
    return sp.log(value, base)


def _get_local_dict(variables):
    """
    Tao local_dict cho sympify, bao gom:
    - cac bien (x, y, ...)
    - cac ham toan hoc thong dung
    """
    local_dict = {}

    # Tao cac bien
    symbols = sp.symbols(' '.join(variables))
    if len(variables) == 1:
        symbols = (symbols,)

    for name, sym in zip(variables, symbols):
        local_dict[name] = sym

    # Them cac ham toan hoc
    local_dict.update({
        'sin': sp.sin,
        'cos': sp.cos,
        'tan': sp.tan,
        'cot': sp.cot,
        'sec': sp.sec,
        'csc': sp.csc,
        'asin': sp.asin,
        'acos': sp.acos,
        'atan': sp.atan,
        'sinh': sp.sinh,
        'cosh': sp.cosh,
        'tanh': sp.tanh,
        'exp': sp.exp,
        'log': _log,
        'ln': sp.log,
        'sqrt': sp.sqrt,
        'abs': sp.Abs,
        'pi': sp.pi,
        'e': sp.E,
        'E': sp.E
    })

    return local_dict


def parse_function(expr):
    """
    Parse ham mot bien f(x)
    """
    expr = expr.strip().replace("^", "**")
    local_dict = _get_local_dict(('x',))
    return sp.sympify(expr, locals=local_dict)


def parse_multivariable_function(expr, variables=('x', 'y')):
    """
    Parse ham nhieu bien (mac dinh f(x, y))

    Vi du:
        "x^2 + y^2"
        "sin(x*y)"
    """
    expr = expr.strip().replace("^", "**")
    local_dict = _get_local_dict(variables)
    return sp.sympify(expr, locals=local_dict)

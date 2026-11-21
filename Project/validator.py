# validator.py
# File dung de kiem tra du lieu nguoi dung nhap vao

import sympy as sp


def _log(value, base=10):
    return sp.log(value, base)


def _number_locals():
    return {
        "pi": sp.pi,
        "e": sp.E,
        "E": sp.E,
        "sqrt": sp.sqrt,
        "ln": sp.log,
        "log": _log,
    }


def validate_expression(expr):
    """
    Kiem tra chuoi bieu thuc co hop le hay khong.
    Tra ve (True, "") neu hop le
    Tra ve (False, message) neu khong hop le
    """
    if not expr or expr.strip() == "":
        return False, "Biểu thức rỗng."

    try:
        expr = expr.strip().replace("^", "**")
        x = sp.symbols('x')
        sp.sympify(expr, locals={**_number_locals(), "x": x})
        return True, ""
    except Exception:
        return False, "Biểu thức không hợp lệ."


def validate_number(value):
    """
    Kiem tra gia tri so (cho can tich phan)
    Tra ve (True, "") neu hop le
    Tra ve (False, message) neu khong hop le
    """
    try:
        number = sp.sympify(str(value).strip().replace("^", "**"), locals=_number_locals())
        if number.free_symbols:
            return False, "Giá trị không được chứa biến."
        if number.is_real is False:
            return False, "Giá trị phải là số thực."
        float(number.evalf())
        return True, ""
    except Exception:
        return False, "Giá trị không phải là số."

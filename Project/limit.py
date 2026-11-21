# limit.py
# File dung de tinh gioi han ham mot bien

import sympy as sp


def parse_limit_point(value):
    """
    Chuyen gia tri x0 nguoi dung nhap thanh gia tri SymPy.

    Ho tro:
        - So thuc: 0, 1.5, -2
        - Hang so: pi, E
        - Vo cuc: oo, inf, +oo, +inf, -oo, -inf
    """
    value = str(value).strip()
    if value in ("oo", "+oo", "inf", "+inf"):
        return sp.oo
    if value in ("-oo", "-inf"):
        return -sp.oo

    local_dict = {
        "pi": sp.pi,
        "e": sp.E,
        "E": sp.E,
        "oo": sp.oo,
        "inf": sp.oo,
    }
    return sp.sympify(value, locals=local_dict)


def is_infinite_limit_point(value):
    x0 = parse_limit_point(value)
    return x0 in (sp.oo, -sp.oo)


def compute_limit(f, x0, direction=None):
    """
    Tinh gioi han cua ham f khi x tien toi x0.

    Tham so:
        f         : bieu thuc SymPy theo bien x
        x0        : diem can tinh gioi han
        direction : None, "+", "-"

    Tra ve:
        - Neu direction la "+" hoac "-": gioi han mot ben
        - Neu direction la None: gioi han hai ben; neu hai ben khac nhau thi tra ve chuoi ket luan
    """
    x = sp.symbols("x")
    x0 = parse_limit_point(x0)

    if x0 in (sp.oo, -sp.oo):
        return sp.simplify(sp.limit(f, x, x0))

    if direction in ("+", "-"):
        return sp.simplify(sp.limit(f, x, x0, dir=direction))

    left_limit = sp.simplify(sp.limit(f, x, x0, dir="-"))
    right_limit = sp.simplify(sp.limit(f, x, x0, dir="+"))

    if sp.simplify(left_limit - right_limit) == 0:
        return left_limit

    return (
        "Không tồn tại giới hạn hai bên. "
        f"Giới hạn trái = {sp.sstr(left_limit)}, "
        f"giới hạn phải = {sp.sstr(right_limit)}"
    )


def compute_one_sided_limits(f, x0):
    """
    Tinh dong thoi gioi han trai va gioi han phai cua ham f khi x tien toi x0.

    Tra ve:
        (left_limit, right_limit)
    """
    x = sp.symbols("x")
    x0 = parse_limit_point(x0)

    if x0 in (sp.oo, -sp.oo):
        raise ValueError("Khong tinh gioi han trai/phai tai vo cuc.")

    left_limit = sp.simplify(sp.limit(f, x, x0, dir="-"))
    right_limit = sp.simplify(sp.limit(f, x, x0, dir="+"))
    return left_limit, right_limit

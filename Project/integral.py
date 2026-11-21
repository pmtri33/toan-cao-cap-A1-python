# integral.py
# File dung de tinh tich phan ham mot bien

import sympy as sp


def _log(value, base=10):
    return sp.log(value, base)


def parse_integral_bound(value):
    value = str(value).strip().lower()
    if "infty" in value:
        raise ValueError("Vo cuc chi duoc nhap la inf, +inf, -inf, oo, +oo hoac -oo.")
    if value in ("inf", "+inf", "oo", "+oo"):
        return sp.oo
    if value in ("-inf", "-oo"):
        return -sp.oo

    local_dict = {
        "pi": sp.pi,
        "e": sp.E,
        "E": sp.E,
        "sqrt": sp.sqrt,
        "ln": sp.log,
        "log": _log,
        "inf": sp.oo,
        "oo": sp.oo,
    }
    bound = sp.sympify(value, locals=local_dict)
    if bound.free_symbols:
        raise ValueError("Can tich phan khong duoc chua bien.")
    if bound.is_real is False:
        raise ValueError("Can tich phan phai la so thuc.")
    return sp.simplify(bound)


def _has_infinite_value(value):
    if value is None:
        return True
    if value in (sp.oo, -sp.oo, sp.zoo, sp.nan):
        return True
    return value.has(sp.oo, -sp.oo, sp.zoo, sp.nan)


def _singular_points(f, x):
    try:
        return sp.calculus.util.singularities(f, x)
    except Exception:
        return []


def _point_between(point, a, b):
    lower_ok = True if a == -sp.oo else sp.ask(sp.Q.gt(point, a))
    upper_ok = True if b == sp.oo else sp.ask(sp.Q.lt(point, b))
    return lower_ok and upper_ok


def _is_after(a, b):
    if a == b:
        return False
    if a == sp.oo:
        return True
    if b == -sp.oo:
        return True
    if a == -sp.oo or b == sp.oo:
        return False
    return sp.ask(sp.Q.gt(a, b)) is True


def _finite_singular_points(f, a, b, x):
    candidates = _singular_points(f, x)
    points = []
    for point in candidates:
        try:
            point = sp.simplify(point)
            if point.is_real is False:
                continue
            if _point_between(point, a, b):
                points.append(point)
        except Exception:
            continue
    return sorted(set(points), key=lambda item: float(sp.N(item)))


def _has_singular_endpoint(f, a, b, x):
    if a in (sp.oo, -sp.oo) and b in (sp.oo, -sp.oo):
        return False

    for point in _singular_points(f, x):
        try:
            point = sp.simplify(point)
            if point.is_real is False:
                continue
            if a not in (sp.oo, -sp.oo) and sp.simplify(point - a) == 0:
                return True
            if b not in (sp.oo, -sp.oo) and sp.simplify(point - b) == 0:
                return True
        except Exception:
            continue
    return False


def _limit_at(F, x, point, direction):
    if point in (sp.oo, -sp.oo):
        return sp.simplify(sp.limit(F, x, point))
    return sp.simplify(sp.limit(F, x, point, dir=direction))


def _segment_by_limits(F, x, a, b):
    lower = _limit_at(F, x, a, "+")
    upper = _limit_at(F, x, b, "-")
    value = sp.simplify(upper - lower)
    return lower, upper, value


def compute_indefinite_integral(f):
    """
    Tinh tich phan bat dinh cua ham f theo bien x.
    Tham so:
        f : bieu thuc SymPy
    Tra ve:
        nguyen ham cua f
    """
    x = sp.symbols('x')
    return sp.integrate(f, x)


def compute_definite_integral(f, a, b):
    """
    Tinh tich phan xac dinh cua ham f tren doan [a, b].
    Tham so:
        f : bieu thuc SymPy
        a : can duoi
        b : can tren
    Tra ve:
        gia tri tich phan xac dinh
    """
    x = sp.symbols('x')

    if sp.simplify(a - b) == 0:
        return sp.S.Zero

    sign = sp.S.One
    if _is_after(a, b):
        a, b = b, a
        sign = -sp.S.One

    singular_points = _finite_singular_points(f, a, b, x)
    has_singular_endpoint = _has_singular_endpoint(f, a, b, x)
    is_improper = (
        a in (sp.oo, -sp.oo)
        or b in (sp.oo, -sp.oo)
        or bool(singular_points)
        or has_singular_endpoint
    )
    if not is_improper:
        return sp.integrate(f, (x, a, b))

    F = sp.integrate(f, x)
    if isinstance(F, sp.Integral):
        return sp.integrate(f, (x, a, b))

    if a == -sp.oo and b == sp.oo:
        split_points = [sp.S.Zero]
    else:
        split_points = []
    split_points.extend(singular_points)

    points = [a] + split_points + [b]
    total = sp.S.Zero
    lines = ["Tich phan suy rong, tinh qua gioi han:"]

    for left, right in zip(points, points[1:]):
        lower, upper, value = _segment_by_limits(F, x, left, right)
        lines.append(
            f"Tren ({sp.sstr(left)}, {sp.sstr(right)}): "
            f"lim F(x)|_tren = {sp.sstr(upper)}, "
            f"lim F(x)|_duoi = {sp.sstr(lower)}, "
            f"gia tri = {sp.sstr(value)}"
        )
        if _has_infinite_value(value):
            lines.append("Ket luan: tich phan suy rong phan ky.")
            return "\n".join(lines)
        total += value

    total = sp.simplify(sign * total)
    lines.append(f"Ket qua: {sp.sstr(total)}")
    return "\n".join(lines)

import sympy as sp


n = sp.symbols("n", integer=True, positive=True)
N = sp.symbols("N", integer=True, positive=True)


def _log(value, base=10):
    return sp.log(value, base)


def parse_series_term(expr):
    expr = expr.strip()
    if "=" in expr:
        expr = expr.split("=", 1)[1].strip()

    local_dict = {
        "n": n,
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "cot": sp.cot,
        "sec": sp.sec,
        "csc": sp.csc,
        "exp": sp.exp,
        "log": _log,
        "ln": sp.log,
        "sqrt": sp.sqrt,
        "abs": sp.Abs,
        "pi": sp.pi,
        "e": sp.E,
        "E": sp.E,
        "oo": sp.oo,
        "inf": sp.oo,
    }
    return sp.sympify(expr.replace("^", "**"), locals=local_dict)


def _truth(value):
    if value is True or value == sp.S.true:
        return True
    if value is False or value == sp.S.false:
        return False
    return None


def _has_infinite_value(value):
    if value is None:
        return False
    return value in (sp.oo, -sp.oo, sp.zoo) or value.has(sp.oo, -sp.oo, sp.zoo)


def _safe_limit(expr, variable, point):
    try:
        return sp.simplify(sp.limit(expr, variable, point))
    except Exception:
        return None


def _has_alternating_factor(expr):
    for power in expr.atoms(sp.Pow):
        if power.base == -1 and n in power.exp.free_symbols:
            return True
    return False


def _compare_abs_less_than_one(value):
    value = sp.simplify(value)
    if value.is_number:
        return _truth(sp.Abs(value) < 1)
    return _truth(sp.ask(sp.Q.lt(sp.Abs(value), 1)))


def _compare_greater_than(value, bound):
    value = sp.simplify(value)
    if value.is_number:
        return _truth(value > bound)
    return _truth(sp.ask(sp.Q.gt(value, bound)))


def _is_geometric(term):
    ratio = sp.simplify(term.subs(n, n + 1) / term)
    if n not in ratio.free_symbols:
        return True, ratio
    return False, ratio


def _geometric_component_sum(term, start):
    is_geo, ratio = _is_geometric(term)
    if not is_geo:
        return None

    converges = _compare_abs_less_than_one(ratio)
    first_term = sp.simplify(term.subs(n, start))
    if converges is True:
        return {
            "term": term,
            "ratio": ratio,
            "first_term": first_term,
            "converges": True,
            "sum": sp.simplify(first_term / (1 - ratio)),
        }
    if converges is False:
        return {
            "term": term,
            "ratio": ratio,
            "first_term": first_term,
            "converges": False,
            "sum": None,
        }
    return {
        "term": term,
        "ratio": ratio,
        "first_term": first_term,
        "converges": None,
        "sum": None,
    }


def _sum_of_geometric_components(term, start):
    expanded = sp.expand(term)
    components = expanded.as_ordered_terms()
    if len(components) < 2:
        return None

    data = []
    for component in components:
        item = _geometric_component_sum(component, start)
        if item is None:
            return None
        data.append(item)

    return data


def _p_series_data(term):
    simplified = sp.factor(term)
    powers = simplified.as_powers_dict()
    exponent = powers.get(n)
    if exponent is None:
        return None

    coefficient = sp.simplify(simplified / (n ** exponent))
    if n in coefficient.free_symbols:
        return None

    p_value = sp.simplify(-exponent)
    if p_value.is_number and p_value.is_real is not False:
        return coefficient, p_value
    return None


def _alternating_data(term):
    candidates = [(-1) ** n, (-1) ** (n + 1), (-1) ** (n - 1)]
    for sign in candidates:
        base = sp.simplify(term / sign)
        if (
            n in base.free_symbols
            and not _has_alternating_factor(base)
            and sp.simplify(sign * base - term) == 0
        ):
            return sign, base
    return None


def _prove_nonnegative_from(start, expr):
    expr = sp.simplify(expr)
    if expr.is_number:
        return _truth(expr >= 0)

    for index in range(start, start + 20):
        value = sp.simplify(expr.subs(n, index))
        if value.is_number and _truth(value < 0) is True:
            return False

    direct = _truth(sp.ask(sp.Q.nonnegative(expr)))
    if direct is not None:
        return direct

    x = sp.symbols("x", real=True)
    expr_x = sp.simplify(expr.subs(n, x))
    try:
        counterexample = sp.reduce_inequalities([expr_x < 0, x >= start], x)
        if counterexample == sp.S.false:
            return True
        if counterexample == sp.S.true:
            return False
    except Exception:
        pass
    return None


def _monotone_decreasing_data(base, start):
    positivity = _prove_nonnegative_from(start, base)
    difference = sp.simplify(base - base.subs(n, n + 1))
    decreasing = _prove_nonnegative_from(start, difference)
    return {
        "difference": difference,
        "positive": positivity,
        "decreasing": decreasing,
    }


def _exact_sum(term, start):
    try:
        result = sp.summation(term, (n, start, sp.oo))
        if isinstance(result, sp.Sum):
            return None
        return sp.simplify(result)
    except Exception:
        return None


def _telescoping_sum(term, start):
    try:
        partial = sp.summation(term, (n, start, N))
    except Exception:
        return None, None

    if isinstance(partial, sp.Sum):
        return None, None

    total = _safe_limit(partial, N, sp.oo)
    if total is None:
        return sp.simplify(partial), None
    if _has_infinite_value(total):
        return sp.simplify(partial), total
    return sp.simplify(partial), total


def _telescoping_by_difference(term, start):
    expanded = sp.apart(term, n)
    candidates = expanded.as_ordered_terms()

    for candidate in candidates:
        next_candidate = candidate.subs(n, n + 1)

        if sp.simplify(term - (candidate - next_candidate)) == 0:
            partial = sp.simplify(candidate.subs(n, start) - candidate.subs(n, N + 1))
            total = _safe_limit(partial, N, sp.oo)
            return candidate, partial, total

        if sp.simplify(term - (next_candidate - candidate)) == 0:
            partial = sp.simplify(candidate.subs(n, N + 1) - candidate.subs(n, start))
            total = _safe_limit(partial, N, sp.oo)
            return candidate, partial, total

    return None, None, None


def analyze_series(term, start=1):
    start = int(start)
    if start < 0:
        raise ValueError("Chi so bat dau phai la so nguyen khong am.")

    term = sp.simplify(term)
    lines = [
        f"So hang tong quat a_n = {sp.sstr(term)}",
        f"Xet chuoi sum(a_n), n tu {start} den vo cuc.",
    ]

    is_geo, ratio = _is_geometric(term)
    if is_geo:
        geo_data = _geometric_component_sum(term, start)
        lines.append("Nhan dang: chuoi hinh hoc.")
        lines.append(f"Cong boi q = {sp.sstr(geo_data['ratio'])}")
        lines.append(f"So hang dau a_{start} = {sp.sstr(geo_data['first_term'])}")
        if geo_data["converges"] is True:
            lines.append("|q| < 1 nen chuoi hoi tu.")
            lines.append(f"Tong chinh xac S = a_{start}/(1 - q) = {sp.sstr(geo_data['sum'])}")
        elif geo_data["converges"] is False:
            lines.append("|q| >= 1 nen chuoi phan ky.")
        else:
            lines.append("Chua ket luan duoc tu dieu kien |q| < 1.")
        return "\n".join(lines)

    geo_components = _sum_of_geometric_components(term, start)
    if geo_components is not None:
        lines.append("Nhan dang: tong huu han cac chuoi hinh hoc.")
        total = sp.S.Zero
        all_convergent = True
        unknown_component = False

        for index, item in enumerate(geo_components, start=1):
            lines.append(
                f"Thanh phan {index}: {sp.sstr(item['term'])}, "
                f"q = {sp.sstr(item['ratio'])}, "
                f"a_{start} = {sp.sstr(item['first_term'])}"
            )
            if item["converges"] is True:
                total += item["sum"]
            elif item["converges"] is False:
                all_convergent = False
                lines.append(
                    f"Thanh phan {index} co |q| >= 1 nen chuoi ban dau phan ky."
                )
                break
            else:
                all_convergent = False
                unknown_component = True

        if all_convergent:
            lines.append("Tat ca thanh phan deu co |q| < 1 nen chuoi hoi tu.")
            lines.append(f"Tong chinh xac S = {sp.sstr(sp.simplify(total))}")
        elif unknown_component:
            lines.append("Chua ket luan duoc vi co thanh phan chua xac dinh duoc |q| < 1.")
        return "\n".join(lines)

    p_data = _p_series_data(term)
    if p_data is not None:
        coefficient, p_value = p_data
        converges = _compare_greater_than(p_value, 1)
        lines.append("Nhan dang: chuoi p dang c/n^p.")
        lines.append(f"c = {sp.sstr(coefficient)}, p = {sp.sstr(p_value)}")
        if converges is True:
            total = _exact_sum(term, start)
            lines.append("p > 1 nen chuoi hoi tu.")
            if total is not None:
                lines.append(f"Tong chinh xac S = {sp.sstr(total)}")
        elif converges is False:
            lines.append("p <= 1 nen chuoi phan ky.")
        else:
            lines.append("Chua ket luan duoc vi khong xac dinh duoc p > 1 hay khong.")
        return "\n".join(lines)

    alt_data = _alternating_data(term)
    if alt_data is not None:
        sign, base = alt_data
        exact = _exact_sum(term, start)
        abs_exact = _exact_sum(sp.Abs(term), start)
        limit_base = _safe_limit(base, n, sp.oo)
        monotone = _monotone_decreasing_data(base, start)
        lines.append("Nhan dang: chuoi dan dau.")
        lines.append(f"Nhan tu dau = {sp.sstr(sign)}")
        lines.append(f"b_n = {sp.sstr(base)}")
        if limit_base is not None:
            lines.append(f"lim b_n = {sp.sstr(limit_base)}")
        else:
            lines.append("Chua tinh duoc lim b_n bang SymPy.")
        lines.append(
            f"b_n - b_(n+1) = {sp.sstr(monotone['difference'])}"
        )
        if monotone["positive"] is True:
            lines.append(f"b_n >= 0 voi moi n >= {start}.")
        elif monotone["positive"] is False:
            lines.append(f"b_n khong luon >= 0 voi moi n >= {start}.")
        else:
            lines.append(f"Chua xac dinh duoc b_n co khong am voi moi n >= {start} hay khong.")

        if monotone["decreasing"] is True:
            lines.append(f"b_(n+1) <= b_n voi moi n >= {start}, nen b_n giam dan.")
        elif monotone["decreasing"] is False:
            lines.append(f"b_n khong giam dan tren moi n >= {start}.")
        else:
            lines.append("Chua chung minh duoc b_n giam dan bang SymPy.")

        if abs_exact is not None and not _has_infinite_value(abs_exact):
            lines.append("Chuoi gia tri tuyet doi hoi tu nen chuoi hoi tu tuyet doi.")
        elif exact is not None and not _has_infinite_value(exact):
            lines.append("Chuoi hoi tu. Neu chuoi |a_n| phan ky thi hoi tu co dieu kien.")
            lines.append(f"Tong chinh xac S = {sp.sstr(exact)}")
        elif limit_base == 0 and monotone["positive"] is True and monotone["decreasing"] is True:
            lines.append("b_n khong am, giam dan va tien ve 0 nen chuoi hoi tu theo tieu chuan Leibniz.")
        elif limit_base == 0:
            lines.append("b_n tien ve 0 nhung chua du dieu kien giam dan/khong am de ap dung tieu chuan Leibniz.")
        else:
            lines.append("So hang tong quat khong tien ve 0 nen chuoi phan ky.")
        return "\n".join(lines)

    base, partial, total = _telescoping_by_difference(term, start)
    if partial is not None:
        lines.append("Nhan dang: chuoi rut gon.")
        lines.append(f"a_n = g(n) - g(n + 1), voi g(n) = {sp.sstr(base)}")
        lines.append(f"S_N = {sp.sstr(partial)}")
        if total is None:
            lines.append("Chua tinh duoc lim S_N bang SymPy.")
        elif _has_infinite_value(total):
            lines.append(f"lim S_N = {sp.sstr(total)} nen chuoi phan ky.")
        else:
            lines.append("Chuoi hoi tu.")
            lines.append(f"Tong chinh xac S = lim S_N = {sp.sstr(total)}")
        return "\n".join(lines)

    partial, total = _telescoping_sum(term, start)
    if partial is not None:
        lines.append("Nhan dang: chuoi rut gon hoac SymPy tinh duoc tong rieng.")
        lines.append(f"S_N = {sp.sstr(partial)}")
        if total is None:
            lines.append("Chua tinh duoc lim S_N bang SymPy.")
        elif _has_infinite_value(total):
            lines.append(f"lim S_N = {sp.sstr(total)} nen chuoi phan ky.")
        else:
            lines.append("Chuoi hoi tu.")
            lines.append(f"Tong chinh xac S = lim S_N = {sp.sstr(total)}")
        return "\n".join(lines)

    exact = _exact_sum(term, start)
    if exact is not None:
        lines.append("SymPy tinh duoc tong vo han.")
        if _has_infinite_value(exact):
            lines.append(f"Ket qua = {sp.sstr(exact)} nen chuoi phan ky.")
        else:
            lines.append("Chuoi hoi tu.")
            lines.append(f"Tong chinh xac S = {sp.sstr(exact)}")
        return "\n".join(lines)

    try:
        convergence = sp.Sum(term, (n, start, sp.oo)).is_convergent()
    except Exception:
        convergence = None
    if convergence is True:
        lines.append("SymPy ket luan chuoi hoi tu, nhung chua tim duoc tong chinh xac.")
    elif convergence is False:
        lines.append("SymPy ket luan chuoi phan ky.")
    else:
        lines.append("Chua nhan dang duoc dang chuoi de ket luan tu dong.")
    return "\n".join(lines)

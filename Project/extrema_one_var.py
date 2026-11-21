# extrema_one_var.py
# File dung de tim cuc tri cua ham mot bien bang cach:
# 1. Tim diem dung tu dieu kien f'(x) = 0
# 2. Tinh dao ham cap hai f''(x) tai tung diem dung
# 3. Ket luan:
#    - f''(x0) > 0  : cuc tieu
#    - f''(x0) < 0  : cuc dai
#    - f''(x0) = 0  : chua xac dinh theo tieu chuan dao ham cap hai

import sympy as sp


def find_extrema_one_variable(f):
    """
    Tim diem dung va xac dinh cuc tri cua ham mot bien f(x).

    Tham so:
        f : bieu thuc SymPy theo bien x

    Tra ve:
        Chuoi van ban mo ta:
        - dao ham cap 1
        - cac diem dung
        - gia tri dao ham cap 2 tai diem dung
        - ket luan cuc tri
    """
    x = sp.symbols('x')

    # Dao ham cap 1 va cap 2
    f1 = sp.diff(f, x)
    f2 = sp.diff(f1, x)

    # Tim diem dung tu f'(x)=0
    critical_points = sp.solve(sp.Eq(f1, 0), x)

    lines = []
    lines.append("f(x) = {}".format(f))
    lines.append("f'(x) = {}".format(sp.simplify(f1)))
    lines.append("f''(x) = {}".format(sp.simplify(f2)))
    lines.append("")

    if not critical_points:
        lines.append("Không tìm thấy điểm dừng thỏa f'(x) = 0.")
        return "\n".join(lines)

    lines.append("Các điểm dừng:")
    for i, cp in enumerate(critical_points, start=1):
        lines.append("  {}. x = {}".format(i, cp))
    lines.append("")

    lines.append("Xét đạo hàm cấp hai tại từng điểm dừng:")
    extrema_points = []

    for cp in critical_points:
        second_value = sp.simplify(f2.subs(x, cp))
        f_value = sp.simplify(f.subs(x, cp))

        if second_value.is_real is False:
            conclusion = "Không kết luận được vì f''(x0) không thực."
        elif second_value.is_positive:
            conclusion = "Điểm cực tiểu"
            extrema_points.append((cp, f_value, "cực tiểu"))
        elif second_value.is_negative:
            conclusion = "Điểm cực đại"
            extrema_points.append((cp, f_value, "cực đại"))
        elif second_value.is_zero:
            conclusion = "Điểm có đạo hàm cấp hai bằng 0, chưa xác định cực trị theo tiêu chuẩn này"
        else:
            # Truong hop SymPy khong tu dong ket luan dau cua f''(x0)
            try:
                numeric_value = float(second_value.evalf())
                if numeric_value > 0:
                    conclusion = "Điểm cực tiểu"
                    extrema_points.append((cp, f_value, "cực tiểu"))
                elif numeric_value < 0:
                    conclusion = "Điểm cực đại"
                    extrema_points.append((cp, f_value, "cực đại"))
                else:
                    conclusion = "Điểm có đạo hàm cấp hai bằng 0, chưa xác định cực trị theo tiêu chuẩn này"
            except Exception:
                conclusion = "Không kết luận được dấu của đạo hàm cấp hai"

        lines.append("Tại x = {}:".format(cp))
        lines.append("  f''({}) = {}".format(cp, second_value))
        lines.append("  f({}) = {}".format(cp, f_value))
        lines.append("  Kết luận: {}".format(conclusion))
        lines.append("")

    lines.append("Tổng hợp các điểm cực trị:")
    if extrema_points:
        for i, (cp, f_value, kind) in enumerate(extrema_points, start=1):
            lines.append("  {}. x = {}, f(x) = {} -> {}".format(i, cp, f_value, kind))
    else:
        lines.append("  Không xác định được điểm cực trị nào bằng tiêu chuẩn đạo hàm cấp hai.")

    return "\n".join(lines)

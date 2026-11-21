# plot.py
# File dung de ve do thi ham mot bien tren doan [a, b]

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


def plot_one_variable_function(f, a, b, num_points=1000):
    """
    Vẽ đồ thị hàm một biến f(x) trên đoạn [a, b].

    Tham so:
        f          : bieu thuc SymPy theo bien x
        a, b       : hai dau mut cua doan ve
        num_points : so diem lay mau de ve do thi
    """
    x = sp.symbols("x")

    if a >= b:
        raise ValueError("Cận trái phải nhỏ hơn cận phải.")

    f_numeric = sp.lambdify(x, f, modules=["numpy"])
    x_vals = np.linspace(a, b, num_points)

    try:
        y_vals = f_numeric(x_vals)
    except Exception as exc:
        raise ValueError(f"Không thể tính giá trị hàm trên đoạn đã cho: {exc}") from exc

    y_vals = np.array(y_vals, dtype=float)
    y_vals[~np.isfinite(y_vals)] = np.nan

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label=f"y = {sp.simplify(f)}")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.xlim(a, b)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Đồ thị hàm một biến trên đoạn [{}, {}]".format(a, b))
    plt.grid(True)
    plt.legend()
    plt.show()

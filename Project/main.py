import tkinter as tk
from tkinter import ttk, messagebox
import traceback

import sympy as sp


def _log(value, base=10):
    return sp.log(value, base)


class MathApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Phần mềm Hỗ trợ Toán Cao Cấp A1")
        self.geometry("980x700")
        self.minsize(860, 620)

        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self.sidebar = ttk.Frame(self, relief=tk.SUNKEN, width=270)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.main_area = ttk.Frame(self)
        self.main_area.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.main_area.columnconfigure(0, weight=1)
        self.main_area.rowconfigure(0, weight=3)
        self.main_area.rowconfigure(1, weight=2)

        self.content_frame = ttk.Frame(self.main_area)
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))

        self.output_frame = ttk.LabelFrame(self.main_area, text="Kết quả")
        self.output_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)

        self.output_text = tk.Text(
            self.output_frame,
            height=16,
            state=tk.DISABLED,
            bg="#f4f4f4",
            font=("Consolas", 11),
            wrap=tk.WORD,
        )
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

        output_scrollbar = ttk.Scrollbar(
            self.output_frame,
            orient=tk.VERTICAL,
            command=self.output_text.yview,
        )
        output_scrollbar.grid(row=0, column=1, sticky="ns", pady=6)
        self.output_text.configure(yscrollcommand=output_scrollbar.set)

        self.setup_sidebar()
        self.show_home()

    def print_output(self, text=""):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, str(text) + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

    def reset_app(self):
        self.clear_output()
        self.show_home()

    def print_equation(self, lhs, rhs):
        self.print_output(f"{lhs} = {sp.sstr(rhs)}")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def setup_sidebar(self):
        ttk.Label(
            self.sidebar,
            text="MENU CHỨC NĂNG",
            font=("Arial", 12, "bold"),
        ).pack(pady=12)

        buttons = [
            ("1. Tính giới hạn hàm 1 biến", self.show_limit),
            ("2. Tính đạo hàm hàm 1 biến", self.show_derivative),
            ("3. Tính tích phân hàm 1 biến", self.show_integral),
            ("4. Tính cực trị hàm 1 biến", self.show_extrema_one_var),
            ("5. Vẽ đồ thị hàm 1 biến", self.show_plot),
            ("6. Tính chuỗi số", self.show_series),
        ]

        for text, command in buttons:
            ttk.Button(self.sidebar, text=text, command=command).pack(
                fill=tk.X,
                padx=12,
                pady=5,
            )

        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)
        ttk.Button(
            self.sidebar,
            text="Xóa kết quả",
            command=self.reset_app,
        ).pack(fill=tk.X, padx=12)

    def show_home(self):
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="Chương trình hỗ trợ Toán Cao Cấp A1",
            font=("Arial", 18, "bold"),
        ).pack(pady=(70, 10))
        ttk.Label(
            self.content_frame,
            text="Chọn một chức năng ở thanh menu bên trái.",
            font=("Arial", 12),
        ).pack(pady=10)

    def add_function_entry(self, frame, row=0):
        ttk.Label(frame, text="Hàm f(x):").grid(row=row, column=0, padx=6, pady=6, sticky=tk.E)
        entry = ttk.Entry(frame, width=38)
        entry.grid(row=row, column=1, padx=6, pady=6, sticky=tk.W)
        return entry

    def add_example_hint(self, frame, text, row):
        ttk.Label(
            frame,
            text=text,
            foreground="#777777",
            font=("Arial", 9, "italic"),
            wraplength=520,
            justify=tk.LEFT,
        ).grid(
            row=row,
            column=0,
            columnspan=2,
            padx=6,
            pady=(0, 10),
            sticky=tk.W,
        )

    def parse_expression(self, expr):
        from validator import validate_expression
        from parser import parse_function

        ok, message = validate_expression(expr)
        if not ok:
            raise ValueError(message)
        return parse_function(expr)

    def parse_number(self, value, label):
        from validator import validate_number

        ok, message = validate_number(value)
        if not ok:
            raise ValueError(f"{label}: {message}")

        local_dict = {
            "pi": sp.pi,
            "e": sp.E,
            "E": sp.E,
            "sqrt": sp.sqrt,
            "ln": sp.log,
            "log": _log,
        }
        return sp.simplify(sp.sympify(value.strip().replace("^", "**"), locals=local_dict))

    def parse_positive_integer(self, value, label):
        try:
            number = int(value)
        except Exception as exc:
            raise ValueError(f"{label} phải là số nguyên dương.") from exc

        if number < 1:
            raise ValueError(f"{label} phải là số nguyên dương.")
        return number

    def show_limit(self):
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="1. Tính giới hạn hàm một biến",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=10)

        expr_entry = self.add_function_entry(frame, row=0)
        ttk.Label(frame, text="x tiến tới x0:").grid(row=1, column=0, padx=6, pady=6, sticky=tk.E)
        x0_entry = ttk.Entry(frame, width=38)
        x0_entry.grid(row=1, column=1, padx=6, pady=6, sticky=tk.W)
        ttk.Label(frame, text="Hướng (+, -, hoặc để trống):").grid(
            row=2,
            column=0,
            padx=6,
            pady=6,
            sticky=tk.E,
        )
        direction_entry = ttk.Entry(frame, width=38)
        direction_entry.grid(row=2, column=1, padx=6, pady=6, sticky=tk.W)
        self.add_example_hint(
            frame,
            "Ví dụ: f(x) = abs(x)/x, x0 = 0, hướng để trống để xem cả giới hạn trái và phải.",
            row=3,
        )

        def calculate():
            expr = expr_entry.get().strip()
            x0_str = x0_entry.get().strip()
            direction = direction_entry.get().strip()

            if not expr or not x0_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập f(x) và điểm x0.")
                return
            if direction not in ("", "+", "-"):
                messagebox.showerror("Lỗi", "Hướng chỉ được nhập '+', '-' hoặc để trống.")
                return

            try:
                from limit import compute_limit, compute_one_sided_limits, is_infinite_limit_point

                f = self.parse_expression(expr)

                self.print_output("--- Giới hạn hàm một biến ---")
                self.print_equation("f(x)", f)

                if is_infinite_limit_point(x0_str):
                    result = compute_limit(f, x0_str)
                    self.print_output(f"lim x -> {x0_str} = {sp.sstr(result)}")
                elif direction:
                    result = compute_limit(f, x0_str, direction)
                    side_label = "+" if direction == "+" else "-"
                    self.print_output(f"lim x -> {x0_str}{side_label} = {sp.sstr(result)}")
                else:
                    left_limit, right_limit = compute_one_sided_limits(f, x0_str)
                    self.print_output(f"Giới hạn trái:  lim x -> {x0_str}- = {sp.sstr(left_limit)}")
                    self.print_output(f"Giới hạn phải: lim x -> {x0_str}+ = {sp.sstr(right_limit)}")

                    if sp.simplify(left_limit - right_limit) == 0:
                        self.print_output(f"Giới hạn: lim x -> {x0_str} = {sp.sstr(left_limit)}")
                    else:
                        self.print_output("Giới hạn không tồn tại vì giới hạn trái khác giới hạn phải.")
                self.print_output()
            except Exception as exc:
                self.print_output(f"Lỗi: {exc}\n{traceback.format_exc()}")

        ttk.Button(frame, text="Tính giới hạn", command=calculate).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=16,
        )

    def show_derivative(self):
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="2. Tính đạo hàm hàm một biến",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=10)

        expr_entry = self.add_function_entry(frame, row=0)
        ttk.Label(frame, text="Cấp đạo hàm n:").grid(
            row=1,
            column=0,
            padx=6,
            pady=6,
            sticky=tk.E,
        )
        n_entry = ttk.Entry(frame, width=38)
        n_entry.insert(0, "1")
        n_entry.grid(row=1, column=1, padx=6, pady=6, sticky=tk.W)

        ttk.Label(frame, text="Tại điểm x0 (tùy chọn):").grid(
            row=2,
            column=0,
            padx=6,
            pady=6,
            sticky=tk.E,
        )
        x0_entry = ttk.Entry(frame, width=38)
        x0_entry.grid(row=2, column=1, padx=6, pady=6, sticky=tk.W)
        self.add_example_hint(
            frame,
            "Ví dụ: f(x) = x^3 + sin(x), n = 2, x0 = 0 nếu muốn tính giá trị tại điểm.",
            row=3,
        )

        def calculate():
            expr = expr_entry.get().strip()
            n_str = n_entry.get().strip()
            x0_str = x0_entry.get().strip()

            if not expr:
                messagebox.showerror("Lỗi", "Vui lòng nhập biểu thức f(x).")
                return
            if not n_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập cấp đạo hàm n.")
                return

            try:
                from derivative import compute_derivative, compute_nth_derivative

                x = sp.symbols("x")
                f = self.parse_expression(expr)
                n = self.parse_positive_integer(n_str, "Cấp đạo hàm n")

                self.print_output("--- Đạo hàm hàm một biến ---")
                self.print_equation("f(x)", f)
                self.print_output(f"Cấp đạo hàm: n = {n}")

                x0 = None
                if x0_str:
                    x0 = self.parse_number(x0_str, "x0")

                for order in range(1, n + 1):
                    if order == 1:
                        derivative = compute_derivative(f)
                        derivative_label = "f'(x)"
                        value_label_template = "f'({})"
                    else:
                        derivative = compute_nth_derivative(f, order)
                        derivative_label = f"f^({order})(x)"
                        value_label_template = f"f^({order})" + "({})"

                    self.print_equation(derivative_label, derivative)

                    if x0 is not None:
                        value = sp.simplify(derivative.subs(x, x0))
                        self.print_equation(value_label_template.format(x0), value)

                self.print_output()
            except Exception as exc:
                self.print_output(f"Lỗi: {exc}\n{traceback.format_exc()}")

        ttk.Button(frame, text="Tính đạo hàm", command=calculate).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=16,
        )

    def show_integral(self):
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="3. Tính tích phân hàm một biến",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=10)

        expr_entry = self.add_function_entry(frame, row=0)
        ttk.Label(frame, text="Cận dưới a (bỏ trống nếu tính nguyên hàm):").grid(
            row=1,
            column=0,
            padx=6,
            pady=6,
            sticky=tk.E,
        )
        a_entry = ttk.Entry(frame, width=38)
        a_entry.grid(row=1, column=1, padx=6, pady=6, sticky=tk.W)
        ttk.Label(frame, text="Cận trên b:").grid(row=2, column=0, padx=6, pady=6, sticky=tk.E)
        b_entry = ttk.Entry(frame, width=38)
        b_entry.grid(row=2, column=1, padx=6, pady=6, sticky=tk.W)
        self.add_example_hint(
            frame,
            "Ví dụ nguyên hàm: f(x) = x^2 + cos(x). Tích phân xác định: a = 0, b = pi.",
            row=3,
        )

        def calculate():
            expr = expr_entry.get().strip()
            a_str = a_entry.get().strip()
            b_str = b_entry.get().strip()

            if not expr:
                messagebox.showerror("Lỗi", "Vui lòng nhập biểu thức f(x).")
                return

            try:
                f = self.parse_expression(expr)
                self.print_output("--- Tích phân hàm một biến ---")
                self.print_equation("f(x)", f)

                if a_str or b_str:
                    if not a_str or not b_str:
                        messagebox.showerror("Lỗi", "Cần nhập đủ cả cận a và cận b.")
                        return

                    from integral import compute_definite_integral, parse_integral_bound

                    a = parse_integral_bound(a_str)
                    b = parse_integral_bound(b_str)
                    result = compute_definite_integral(f, a, b)
                    if isinstance(result, str):
                        self.print_output(f"Tích phân trên [{a}, {b}]:")
                        self.print_output(result)
                    else:
                        self.print_output(f"Tích phân xác định trên [{a}, {b}] = {sp.sstr(result)}")
                else:
                    from integral import compute_indefinite_integral

                    result = compute_indefinite_integral(f)
                    self.print_output(f"Nguyên hàm F(x) = {sp.sstr(result)} + C")

                self.print_output()
            except Exception as exc:
                self.print_output(f"Lỗi: {exc}\n{traceback.format_exc()}")

        ttk.Button(frame, text="Tính tích phân", command=calculate).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=16,
        )

    def show_extrema_one_var(self):
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="4. Tính cực trị hàm một biến",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=10)

        expr_entry = self.add_function_entry(frame, row=0)
        self.add_example_hint(
            frame,
            "Ví dụ: f(x) = x^3 - 3*x hoặc f(x) = x^4 - 4*x^2.",
            row=1,
        )

        def calculate():
            expr = expr_entry.get().strip()
            if not expr:
                messagebox.showerror("Lỗi", "Vui lòng nhập biểu thức f(x).")
                return

            try:
                from extrema_one_var import find_extrema_one_variable

                f = self.parse_expression(expr)
                result = find_extrema_one_variable(f)
                self.print_output("--- Cực trị hàm một biến ---")
                self.print_equation("f(x)", f)
                self.print_output(result)
                self.print_output()
            except Exception as exc:
                self.print_output(f"Lỗi: {exc}\n{traceback.format_exc()}")

        ttk.Button(frame, text="Tính cực trị", command=calculate).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=16,
        )

    def show_plot(self):
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="5. Vẽ đồ thị hàm một biến",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=10)

        expr_entry = self.add_function_entry(frame, row=0)
        ttk.Label(frame, text="Cận trái a:").grid(row=1, column=0, padx=6, pady=6, sticky=tk.E)
        a_entry = ttk.Entry(frame, width=38)
        a_entry.grid(row=1, column=1, padx=6, pady=6, sticky=tk.W)
        ttk.Label(frame, text="Cận phải b:").grid(row=2, column=0, padx=6, pady=6, sticky=tk.E)
        b_entry = ttk.Entry(frame, width=38)
        b_entry.grid(row=2, column=1, padx=6, pady=6, sticky=tk.W)
        self.add_example_hint(
            frame,
            "Ví dụ: f(x) = sin(x)/x, a = -10, b = 10 hoặc f(x) = x^2 - 4.",
            row=3,
        )

        def calculate():
            expr = expr_entry.get().strip()
            a_str = a_entry.get().strip()
            b_str = b_entry.get().strip()

            if not expr or not a_str or not b_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập hàm f(x), cận a và cận b.")
                return

            try:
                from plot import plot_one_variable_function

                f = self.parse_expression(expr)
                a = self.parse_number(a_str, "Cận a")
                b = self.parse_number(b_str, "Cận b")
                a_float = float(sp.N(a))
                b_float = float(sp.N(b))

                if a_float >= b_float:
                    messagebox.showerror("Lỗi", "Cận trái a phải nhỏ hơn cận phải b.")
                    return

                self.print_output("--- Vẽ đồ thị hàm một biến ---")
                self.print_equation("f(x)", f)
                self.print_output(f"Khoảng vẽ: [{a}, {b}]")
                self.print_output("Đang hiển thị cửa sổ đồ thị...")
                plot_one_variable_function(f, a_float, b_float)
                self.print_output("Hoàn thành.")
                self.print_output()
            except Exception as exc:
                self.print_output(f"Lỗi: {exc}\n{traceback.format_exc()}")

        ttk.Button(frame, text="Vẽ đồ thị", command=calculate).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=16,
        )

    def show_series(self):
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="6. Tính chuỗi số",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=10)

        ttk.Label(frame, text="Số hạng tổng quát a_n:").grid(
            row=0,
            column=0,
            padx=6,
            pady=6,
            sticky=tk.E,
        )
        expr_entry = ttk.Entry(frame, width=42)
        expr_entry.grid(row=0, column=1, padx=6, pady=6, sticky=tk.W)

        ttk.Label(frame, text="Chỉ số bắt đầu n0:").grid(
            row=1,
            column=0,
            padx=6,
            pady=6,
            sticky=tk.E,
        )
        start_entry = ttk.Entry(frame, width=42)
        start_entry.insert(0, "1")
        start_entry.grid(row=1, column=1, padx=6, pady=6, sticky=tk.W)

        self.add_example_hint(
            frame,
            "Ví dụ: (1/2)^n, 1/(n*(n+1)), 1/n^2, (-1)^(n+1)/n, a_n=(2^n-3^n)/(5^n).",
            row=2,
        )

        def calculate():
            expr = expr_entry.get().strip()
            start_str = start_entry.get().strip()

            if not expr:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hạng tổng quát a_n.")
                return
            if not start_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập chỉ số bắt đầu n0.")
                return

            try:
                from series import analyze_series, parse_series_term

                term = parse_series_term(expr)
                try:
                    start = int(start_str)
                except Exception as exc:
                    raise ValueError("Chỉ số bắt đầu n0 phải là số nguyên không âm.") from exc
                if start < 0:
                    raise ValueError("Chỉ số bắt đầu n0 phải là số nguyên không âm.")
                result = analyze_series(term, start)

                self.print_output("--- Chuỗi số ---")
                self.print_output(result)
                self.print_output()
            except Exception as exc:
                self.print_output(f"Lỗi: {exc}\n{traceback.format_exc()}")

        ttk.Button(frame, text="Tính chuỗi số", command=calculate).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=16,
        )


if __name__ == "__main__":
    app = MathApp()
    app.mainloop()

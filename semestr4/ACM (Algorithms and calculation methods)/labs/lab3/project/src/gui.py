from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from tkinter import filedialog, ttk

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.aitken import build_nodes, calculate_function_values
from src.error_analysis import compute_error_rows
from src.functions import get_function_by_name
from src.graph_build import build_interpolation_figure
from src.io_utils import load_json_config
from src.models import PageConfig
from src.report import build_full_report, build_short_result
from src.theme import MAIN_THEME


@dataclass
class InterpolationState:
    function_name: str = "target"
    function_title: str = "sin(x^2) * exp(-(x/2)^2)"
    a: float = 0.0
    b: float = 3.0
    x_value: float = 1.5
    parts: int = 10
    plot_points: int = 400
    x_nodes: list[float] | None = None
    y_nodes: list[float] | None = None
    true_value: float | None = None
    rows: list | None = None
    report: str = ""


class BasePage(ctk.CTkFrame):
    def __init__(
        self,
        master: ctk.CTkFrame,
        page_config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
    ) -> None:
        super().__init__(master, corner_radius=0)
        self.page_config = page_config
        self.fonts = fonts
        self.grid_columnconfigure(0, weight=1)

    def apply_theme(self, palette: dict[str, str]) -> None:
        self.configure(fg_color=palette["bg"])


class MainPage(BasePage):
    def __init__(
        self,
        master: ctk.CTkFrame,
        page_config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
        app_state: InterpolationState,
    ) -> None:
        super().__init__(master, page_config, fonts)
        self.app_state = app_state

        self.result_var = tk.StringVar(value="Ready")
        self.error_var = tk.StringVar(value="")

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_form()
        self._build_actions()
        self._build_output()
        self.reset_defaults()

    def _build_header(self) -> None:
        self.header_card = ctk.CTkFrame(self, corner_radius=14, border_width=1)
        self.header_card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        self.header_card.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_card,
            text=self.page_config.title,
            anchor="w",
            font=self.fonts["title"],
        )
        self.title_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 4))

        self.subtitle_label = ctk.CTkLabel(
            self.header_card,
            text=self.page_config.subtitle,
            anchor="w",
            font=self.fonts["subtitle"],
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

    def _build_form(self) -> None:
        self.form_card = ctk.CTkFrame(self, corner_radius=14, border_width=1)
        self.form_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        self.form_card.grid_columnconfigure((0, 1), weight=1)

        self.function_label = ctk.CTkLabel(
            self.form_card,
            text="Function:",
            anchor="w",
            font=self.fonts["label"],
        )
        self.function_label.grid(row=0, column=0, sticky="w", padx=20, pady=(14, 6))

        self.function_menu = ctk.CTkOptionMenu(
            self.form_card,
            values=["target", "test"],
            font=self.fonts["body"],
            command=self._on_function_change,
        )
        self.function_menu.grid(row=1, column=0, sticky="ew", padx=(20, 8), pady=(0, 12))

        self.load_button = ctk.CTkButton(
            self.form_card,
            text="Load JSON",
            height=40,
            corner_radius=11,
            font=self.fonts["button"],
            command=self.load_json,
        )
        self.load_button.grid(row=1, column=1, sticky="ew", padx=(8, 20), pady=(0, 12))

        self.entry_a = self._build_labeled_entry(self.form_card, 2, 0, "a:")
        self.entry_b = self._build_labeled_entry(self.form_card, 2, 1, "b:")
        self.entry_x = self._build_labeled_entry(self.form_card, 4, 0, "x:")
        self.entry_parts = self._build_labeled_entry(self.form_card, 4, 1, "Parts:")
        self.entry_plot_points = self._build_labeled_entry(self.form_card, 6, 0, "Plot points:")

    def _build_labeled_entry(
        self,
        parent: ctk.CTkFrame,
        row: int,
        column: int,
        label_text: str,
    ) -> ctk.CTkEntry:
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            anchor="w",
            font=self.fonts["label"],
        )
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(0, 6))

        entry = ctk.CTkEntry(
            parent,
            height=40,
            corner_radius=10,
            font=self.fonts["body"],
        )
        entry.grid(row=row + 1, column=column, sticky="ew", padx=20, pady=(0, 12))
        return entry

    def _build_actions(self) -> None:
        self.actions = ctk.CTkFrame(self, fg_color="transparent")
        self.actions.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.actions.grid_columnconfigure((0, 1, 2), weight=1)

        self.compute_button = ctk.CTkButton(
            self.actions,
            text="Compute",
            height=40,
            corner_radius=11,
            font=self.fonts["button"],
            command=self.compute,
        )
        self.compute_button.grid(row=0, column=0, sticky="ew", padx=(0, 7))

        self.save_button = ctk.CTkButton(
            self.actions,
            text="Save Report",
            height=40,
            corner_radius=11,
            font=self.fonts["button"],
            command=self.save_report,
        )
        self.save_button.grid(row=0, column=1, sticky="ew", padx=7)

        self.clear_button = ctk.CTkButton(
            self.actions,
            text="Clear",
            height=40,
            corner_radius=11,
            font=self.fonts["button"],
            command=self.clear_all,
        )
        self.clear_button.grid(row=0, column=2, sticky="ew", padx=(7, 0))

    def _build_output(self) -> None:
        self.output_card = ctk.CTkFrame(self, corner_radius=14, border_width=1)
        self.output_card.grid(row=3, column=0, sticky="nsew")
        self.output_card.grid_columnconfigure(0, weight=1)
        self.output_card.grid_rowconfigure(4, weight=1)

        self.result_title = ctk.CTkLabel(
            self.output_card,
            text="Result",
            anchor="w",
            font=self.fonts["label"],
        )
        self.result_title.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 6))

        self.result_label = ctk.CTkLabel(
            self.output_card,
            textvariable=self.result_var,
            anchor="w",
            justify="left",
            wraplength=860,
            font=self.fonts["result"],
        )
        self.result_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))

        self.error_label = ctk.CTkLabel(
            self.output_card,
            textvariable=self.error_var,
            anchor="w",
            justify="left",
            wraplength=860,
            font=self.fonts["body"],
        )
        self.error_label.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))

        self.table_title = ctk.CTkLabel(
            self.output_card,
            text="Table",
            anchor="w",
            font=self.fonts["label"],
        )
        self.table_title.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 6))

        self.table_frame = tk.Frame(self.output_card, bg="#090909")
        self.table_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0, 14))
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        columns = ("degree", "approximation", "estimate", "actual_error")
        self.results_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=11,
        )

        self.results_table.heading("degree", text="n")
        self.results_table.heading("approximation", text="P_n(x)")
        self.results_table.heading("estimate", text="|P_n - P_(n-1)|")
        self.results_table.heading("actual_error", text="|f(x) - P_n(x)|")

        self.results_table.column("degree", width=70, anchor="center")
        self.results_table.column("approximation", width=190, anchor="center")
        self.results_table.column("estimate", width=190, anchor="center")
        self.results_table.column("actual_error", width=190, anchor="center")

        self.table_scrollbar = ttk.Scrollbar(
            self.table_frame,
            orient="vertical",
            command=self.results_table.yview,
        )
        self.results_table.configure(yscrollcommand=self.table_scrollbar.set)

        self.results_table.grid(row=0, column=0, sticky="nsew")
        self.table_scrollbar.grid(row=0, column=1, sticky="ns")

    def _fill_table(self, rows) -> None:
        for item in self.results_table.get_children():
            self.results_table.delete(item)

        for row in rows:
            estimate_text = "-" if row.estimate is None else f"{row.estimate:.10f}"
            self.results_table.insert(
                "",
                "end",
                values=(
                    row.degree,
                    f"{row.approximation:.10f}",
                    estimate_text,
                    f"{row.actual_error:.10f}",
                ),
            )

    def _on_function_change(self, choice: str) -> None:
        if choice == "test":
            self.entry_a.delete(0, tk.END)
            self.entry_a.insert(0, "0")
            self.entry_b.delete(0, tk.END)
            self.entry_b.insert(0, "3.1415926535")
            self.entry_x.delete(0, tk.END)
            self.entry_x.insert(0, "1.0")
            self.entry_parts.delete(0, tk.END)
            self.entry_parts.insert(0, "10")
            self.entry_plot_points.delete(0, tk.END)
            self.entry_plot_points.insert(0, "400")
        else:
            self.entry_a.delete(0, tk.END)
            self.entry_a.insert(0, "0")
            self.entry_b.delete(0, tk.END)
            self.entry_b.insert(0, "3")
            self.entry_x.delete(0, tk.END)
            self.entry_x.insert(0, "1.5")
            self.entry_parts.delete(0, tk.END)
            self.entry_parts.insert(0, "10")
            self.entry_plot_points.delete(0, tk.END)
            self.entry_plot_points.insert(0, "400")

    def load_json(self) -> None:
        path = filedialog.askopenfilename(
            title="Select JSON file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            loaded = load_json_config(path)

            function_name = str(loaded.get("function", "target"))
            self.function_menu.set(function_name)

            self.entry_a.delete(0, tk.END)
            self.entry_a.insert(0, str(loaded.get("a", 0)))

            self.entry_b.delete(0, tk.END)
            self.entry_b.insert(0, str(loaded.get("b", 3)))

            self.entry_x.delete(0, tk.END)
            self.entry_x.insert(0, str(loaded.get("x_value", 1.5)))

            self.entry_parts.delete(0, tk.END)
            self.entry_parts.insert(0, str(loaded.get("parts", 10)))

            self.entry_plot_points.delete(0, tk.END)
            self.entry_plot_points.insert(0, str(loaded.get("plot_points", 400)))

            self.result_var.set("JSON loaded. Press Compute.")
            self.error_var.set("")
        except Exception as exc:
            self.result_var.set("No result")
            self.error_var.set(f"Error: {exc}")

    def _parse_input(self) -> tuple[str, float, float, float, int, int]:
        function_name = self.function_menu.get()
        a = float(self.entry_a.get().strip())
        b = float(self.entry_b.get().strip())
        x_value = float(self.entry_x.get().strip())
        parts = int(self.entry_parts.get().strip())
        plot_points = int(self.entry_plot_points.get().strip())

        if b <= a:
            raise ValueError("Потрібно, щоб b > a.")
        if parts < 1:
            raise ValueError("Кількість частин має бути не меншою за 1.")
        if plot_points < 50:
            raise ValueError("Кількість точок для графіка має бути не меншою за 50.")
        if not (a <= x_value <= b):
            raise ValueError("Точка x повинна належати відрізку [a, b].")

        return function_name, a, b, x_value, parts, plot_points

    def compute(self) -> None:
        try:
            function_name, a, b, x_value, parts, plot_points = self._parse_input()
            func, function_title = get_function_by_name(function_name)

            x_nodes = build_nodes(a, b, parts)
            y_nodes = calculate_function_values(func, x_nodes)
            true_value, rows = compute_error_rows(func, x_nodes, y_nodes, x_value)

            report = build_full_report(
                func_name=function_title,
                a=a,
                b=b,
                x_value=x_value,
                x_nodes=x_nodes,
                y_nodes=y_nodes,
                rows=rows,
                true_value=true_value,
            )

            self.app_state.function_name = function_name
            self.app_state.function_title = function_title
            self.app_state.a = a
            self.app_state.b = b
            self.app_state.x_value = x_value
            self.app_state.parts = parts
            self.app_state.plot_points = plot_points
            self.app_state.x_nodes = x_nodes
            self.app_state.y_nodes = y_nodes
            self.app_state.true_value = true_value
            self.app_state.rows = rows
            self.app_state.report = report

            self.result_var.set(build_short_result(rows, true_value))
            self.error_var.set("")
            self._fill_table(rows)
        except Exception as exc:
            self.result_var.set("No result")
            self.error_var.set(f"Error: {exc}")

    def save_report(self) -> None:
        if not self.app_state.report.strip():
            self.result_var.set("No result")
            self.error_var.set("Error: Спочатку виконай обчислення.")
            return

        path = filedialog.asksaveasfilename(
            title="Save report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.app_state.report)
            self.error_var.set("")
        except Exception as exc:
            self.error_var.set(f"Error: {exc}")

    def clear_all(self) -> None:
        self.reset_defaults()

    def reset_defaults(self) -> None:
        self.function_menu.set("target")

        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, "0")

        self.entry_b.delete(0, tk.END)
        self.entry_b.insert(0, "3")

        self.entry_x.delete(0, tk.END)
        self.entry_x.insert(0, "1.5")

        self.entry_parts.delete(0, tk.END)
        self.entry_parts.insert(0, "10")

        self.entry_plot_points.delete(0, tk.END)
        self.entry_plot_points.insert(0, "400")

        self.result_var.set("Ready")
        self.error_var.set("")

        for item in self.results_table.get_children():
            self.results_table.delete(item)

        self.app_state.function_name = "target"
        self.app_state.function_title = "sin(x^2) * exp(-(x/2)^2)"
        self.app_state.a = 0.0
        self.app_state.b = 3.0
        self.app_state.x_value = 1.5
        self.app_state.parts = 10
        self.app_state.plot_points = 400
        self.app_state.x_nodes = None
        self.app_state.y_nodes = None
        self.app_state.true_value = None
        self.app_state.rows = None
        self.app_state.report = ""

    def apply_theme(self, palette: dict[str, str]) -> None:
        super().apply_theme(palette)

        for card in (self.header_card, self.form_card, self.output_card):
            card.configure(
                fg_color=palette["panel"],
                border_color=palette["surface_soft"],
            )

        self.title_label.configure(text_color=palette["text"])
        self.subtitle_label.configure(text_color=palette["muted"])
        self.function_label.configure(text_color=palette["muted"])

        for entry in (
            self.entry_a,
            self.entry_b,
            self.entry_x,
            self.entry_parts,
            self.entry_plot_points,
        ):
            entry.configure(
                fg_color=palette["surface"],
                border_color=palette["surface_soft"],
                text_color=palette["text"],
            )

        self.function_menu.configure(
            fg_color=palette["segment_active"],
            button_color=palette["segment"],
            button_hover_color=palette["segment_hover"],
            text_color=palette["text"],
        )

        self.compute_button.configure(
            fg_color=palette["accent"],
            hover_color=palette["accent_hover"],
            text_color=palette["accent_text"],
        )
        self.load_button.configure(
            fg_color=palette["segment"],
            hover_color=palette["segment_hover"],
            text_color=palette["text"],
        )
        self.save_button.configure(
            fg_color=palette["segment"],
            hover_color=palette["segment_hover"],
            text_color=palette["text"],
        )
        self.clear_button.configure(
            fg_color=palette["segment"],
            hover_color=palette["segment_hover"],
            text_color=palette["text"],
        )

        self.result_title.configure(text_color=palette["muted"])
        self.table_title.configure(text_color=palette["muted"])
        self.result_label.configure(text_color=palette["text"])
        self.error_label.configure(text_color=palette["error"])

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#111111",
            foreground="#F5F7FA",
            fieldbackground="#111111",
            rowheight=28,
            bordercolor="#1B1B1B",
            borderwidth=1,
        )
        style.configure(
            "Treeview.Heading",
            background="#131313",
            foreground="#F5F7FA",
            relief="flat",
        )
        style.map(
            "Treeview",
            background=[("selected", "#1F2D3C")],
            foreground=[("selected", "#F5F7FA")],
        )


class GraphPage(BasePage):
    def __init__(
        self,
        master: ctk.CTkFrame,
        page_config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
        app_state: InterpolationState,
    ) -> None:
        super().__init__(master, page_config, fonts)
        self.app_state = app_state

        self.status_var = tk.StringVar(value="Ready to build graph")
        self.error_var = tk.StringVar(value="")
        self.canvas: FigureCanvasTkAgg | None = None

        self.grid_rowconfigure(3, weight=1)

        self._build_header()
        self._build_controls()
        self._build_output()
        self._build_plot_area()

    def _build_header(self) -> None:
        self.header_card = ctk.CTkFrame(self, corner_radius=14, border_width=1)
        self.header_card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        self.header_card.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_card,
            text=self.page_config.title,
            anchor="w",
            font=self.fonts["title"],
        )
        self.title_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 4))

        self.subtitle_label = ctk.CTkLabel(
            self.header_card,
            text=self.page_config.subtitle,
            anchor="w",
            font=self.fonts["subtitle"],
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

    def _build_controls(self) -> None:
        self.controls_card = ctk.CTkFrame(self, corner_radius=14, border_width=1)
        self.controls_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        self.controls_card.grid_columnconfigure(0, weight=1)

        self.info_label = ctk.CTkLabel(
            self.controls_card,
            text=(
                "Побудова графіка функції, повної інтерполяції за схемою Ейткена "
                "та абсолютної похибки |f(x)-P(x)|."
            ),
            anchor="w",
            justify="left",
            wraplength=860,
            font=self.fonts["body"],
        )
        self.info_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 12))

        self.build_button = ctk.CTkButton(
            self.controls_card,
            text="Build Graph",
            height=40,
            corner_radius=11,
            font=self.fonts["button"],
            command=self.build_graph,
        )
        self.build_button.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 14))

    def _build_output(self) -> None:
        self.output_card = ctk.CTkFrame(self, corner_radius=14, border_width=1)
        self.output_card.grid(row=2, column=0, sticky="ew")
        self.output_card.grid_columnconfigure(0, weight=1)

        self.status_title = ctk.CTkLabel(
            self.output_card,
            text="Status",
            anchor="w",
            font=self.fonts["label"],
        )
        self.status_title.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 6))

        self.status_label = ctk.CTkLabel(
            self.output_card,
            textvariable=self.status_var,
            anchor="w",
            justify="left",
            wraplength=860,
            font=self.fonts["result"],
        )
        self.status_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))

        self.error_label = ctk.CTkLabel(
            self.output_card,
            textvariable=self.error_var,
            anchor="w",
            justify="left",
            wraplength=860,
            font=self.fonts["body"],
        )
        self.error_label.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 14))

    def _build_plot_area(self) -> None:
        self.plot_card = ctk.CTkFrame(self, corner_radius=14, border_width=1)
        self.plot_card.grid(row=3, column=0, sticky="nsew", pady=(14, 0))
        self.plot_card.grid_columnconfigure(0, weight=1)
        self.plot_card.grid_rowconfigure(0, weight=1)

        self.plot_container = ctk.CTkFrame(self.plot_card, fg_color="transparent")
        self.plot_container.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self.plot_container.grid_columnconfigure(0, weight=1)
        self.plot_container.grid_rowconfigure(0, weight=1)

    def build_graph(self) -> None:
        try:
            if self.app_state.x_nodes is None or self.app_state.y_nodes is None:
                raise ValueError("Спочатку виконай обчислення на сторінці Main.")

            self.status_var.set("Building graph...")
            self.error_var.set("")
            self.update_idletasks()

            func, _ = get_function_by_name(self.app_state.function_name)
            fig = build_interpolation_figure(
                func=func,
                x_nodes=self.app_state.x_nodes,
                y_nodes=self.app_state.y_nodes,
                a=self.app_state.a,
                b=self.app_state.b,
                x_value=self.app_state.x_value,
                plot_points=self.app_state.plot_points,
            )

            if self.canvas is not None:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

            self.status_var.set("Graph was built successfully")
        except Exception as exc:
            self.status_var.set("Graph was not built")
            self.error_var.set(f"Error: {exc}")

    def apply_theme(self, palette: dict[str, str]) -> None:
        super().apply_theme(palette)

        for card in (self.header_card, self.controls_card, self.output_card, self.plot_card):
            card.configure(
                fg_color=palette["panel"],
                border_color=palette["surface_soft"],
            )

        self.title_label.configure(text_color=palette["text"])
        self.subtitle_label.configure(text_color=palette["muted"])
        self.info_label.configure(text_color=palette["muted"])

        self.build_button.configure(
            fg_color=palette["accent"],
            hover_color=palette["accent_hover"],
            text_color=palette["accent_text"],
        )

        self.status_title.configure(text_color=palette["muted"])
        self.status_label.configure(text_color=palette["text"])
        self.error_label.configure(text_color=palette["error"])


class AlgorithmsApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")

        self.title("AitkenInterpolationApp")
        self.resizable(False, False)
        self.geometry("720x900")

        self.current_page = "main"
        self.nav_buttons: dict[str, ctk.CTkButton] = {}
        self.pages: dict[str, BasePage] = {}
        self.app_state = InterpolationState()

        self.fonts: dict[str, ctk.CTkFont] = {
            "title": ctk.CTkFont(family="Segoe UI", size=27, weight="bold"),
            "subtitle": ctk.CTkFont(family="Segoe UI", size=13),
            "label": ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            "body": ctk.CTkFont(family="Segoe UI", size=12),
            "button": ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            "result": ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            "nav": ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        }

        self.page_configs: tuple[PageConfig, ...] = (
            PageConfig(
                page_id="main",
                nav_title="Main",
                title="Aitken Interpolation",
                subtitle="Обчислення інтерполяції функції та оцінки похибки",
            ),
            PageConfig(
                page_id="graph",
                nav_title="Graph",
                title="Aitken Interpolation Graph",
                subtitle="Графік функції, інтерполяції та абсолютної похибки",
            ),
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_topbar()
        self._build_pages()
        self._apply_theme()
        self.show_page(self.current_page)

    def _build_topbar(self) -> None:
        self.topbar = ctk.CTkFrame(self, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_columnconfigure(0, weight=1)

        self.nav_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.nav_frame.grid(row=0, column=0, sticky="w", padx=20, pady=(18, 12))

        for index, page in enumerate(self.page_configs):
            button = ctk.CTkButton(
                self.nav_frame,
                text=page.nav_title,
                width=110,
                height=36,
                corner_radius=10,
                font=self.fonts["nav"],
                border_width=1,
                command=lambda pid=page.page_id: self.show_page(pid),
            )
            button.grid(row=0, column=index, padx=(0, 8))
            self.nav_buttons[page.page_id] = button

    def _build_pages(self) -> None:
        self.page_host = ctk.CTkFrame(self, corner_radius=0)
        self.page_host.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.page_host.grid_rowconfigure(0, weight=1)
        self.page_host.grid_columnconfigure(0, weight=1)

        main_page = MainPage(
            self.page_host,
            self.page_configs[0],
            self.fonts,
            self.app_state,
        )
        main_page.grid(row=0, column=0, sticky="nsew")
        self.pages["main"] = main_page

        graph_page = GraphPage(
            self.page_host,
            self.page_configs[1],
            self.fonts,
            self.app_state,
        )
        graph_page.grid(row=0, column=0, sticky="nsew")
        self.pages["graph"] = graph_page

    def show_page(self, page_id: str) -> None:
        self.current_page = page_id
        self.pages[page_id].tkraise()
        self._refresh_nav_buttons()

    def _refresh_nav_buttons(self) -> None:
        palette = MAIN_THEME
        for page_id, button in self.nav_buttons.items():
            if page_id == self.current_page:
                button.configure(
                    fg_color=palette["segment_active"],
                    hover_color=palette["segment_active"],
                    text_color=palette["text"],
                    border_color=palette["segment_active"],
                )
            else:
                button.configure(
                    fg_color=palette["segment"],
                    hover_color=palette["segment_hover"],
                    text_color=palette["muted"],
                    border_color=palette["surface_soft"],
                )

    def _apply_theme(self) -> None:
        palette = MAIN_THEME

        self.configure(fg_color=palette["bg"])
        self.topbar.configure(fg_color=palette["topbar"])
        self.page_host.configure(fg_color=palette["bg"])

        for page in self.pages.values():
            page.apply_theme(palette)

        self._refresh_nav_buttons()


def main() -> None:
    app = AlgorithmsApp()
    app.mainloop()
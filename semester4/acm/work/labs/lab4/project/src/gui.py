from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from tkinter import filedialog, ttk

import customtkinter as ctk

from src.bisection import isolate_root_intervals, solve_all_intervals
from src.error_analysis import build_error_rows
from src.functions import get_function_by_name
from src.graph_build import PlotData, build_function_plot_data
from src.io_utils import load_json_config, save_text_report
from src.models import PageConfig, RootInterval, RootResult
from src.report import build_full_report, build_short_result
from src.theme import MAIN_THEME


@dataclass
class BisectionState:
    function_name: str = "target"
    function_title: str = "2^x - 4x = 0"
    left: float = 0.0
    right: float = 4.0
    scan_step: float = 0.1
    epsilon: float = 1e-5
    max_iterations: int = 100
    plot_points: int = 500
    intervals: list[RootInterval] | None = None
    results: list[RootResult] | None = None
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
        app_state: BisectionState,
    ) -> None:
        super().__init__(master, page_config, fonts)
        self.app_state = app_state

        self.result_var = tk.StringVar(value="Готово до обчислень")
        self.error_var = tk.StringVar(value="")

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_form()
        self._build_actions()
        self._build_output()
        self.reset_defaults()

    def _build_header(self) -> None:
        self.header_card = ctk.CTkFrame(self, corner_radius=8, border_width=1)
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
            justify="left",
            wraplength=860,
            font=self.fonts["subtitle"],
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

    def _build_form(self) -> None:
        self.form_card = ctk.CTkFrame(self, corner_radius=8, border_width=1)
        self.form_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        self.form_card.grid_columnconfigure((0, 1, 2), weight=1)

        self.equation_label = ctk.CTkLabel(
            self.form_card,
            text="Рівняння: 2^x - 4x = 0",
            anchor="w",
            font=self.fonts["label"],
        )
        self.equation_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(14, 6))

        self.expected_label = ctk.CTkLabel(
            self.form_card,
            text="Очікувані корені: 0.310 та 4.000",
            anchor="e",
            font=self.fonts["label"],
        )
        self.expected_label.grid(row=0, column=2, sticky="ew", padx=(8, 20), pady=(14, 6))

        self.entry_left = self._build_labeled_entry(self.form_card, 1, 0, "Ліва межа:")
        self.entry_right = self._build_labeled_entry(self.form_card, 1, 1, "Права межа:")
        self.entry_scan_step = self._build_labeled_entry(self.form_card, 1, 2, "Крок:")
        self.entry_epsilon = self._build_labeled_entry(self.form_card, 3, 0, "epsilon:")
        self.entry_max_iterations = self._build_labeled_entry(self.form_card, 3, 1, "Ітерації:")
        self.entry_plot_points = self._build_labeled_entry(self.form_card, 3, 2, "Точки графіка:")

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
            corner_radius=8,
            font=self.fonts["body"],
        )
        entry.grid(row=row + 1, column=column, sticky="ew", padx=20, pady=(0, 12))
        return entry

    def _build_actions(self) -> None:
        self.actions = ctk.CTkFrame(self, fg_color="transparent")
        self.actions.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.actions.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.compute_button = ctk.CTkButton(
            self.actions,
            text="Обчислити",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.compute,
        )
        self.compute_button.grid(row=0, column=0, sticky="ew", padx=(0, 7))

        self.load_button = ctk.CTkButton(
            self.actions,
            text="Завантажити JSON",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.load_json,
        )
        self.load_button.grid(row=0, column=1, sticky="ew", padx=7)

        self.save_button = ctk.CTkButton(
            self.actions,
            text="Зберегти звіт",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.save_report,
        )
        self.save_button.grid(row=0, column=2, sticky="ew", padx=7)

        self.clear_button = ctk.CTkButton(
            self.actions,
            text="Очистити",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.clear_all,
        )
        self.clear_button.grid(row=0, column=3, sticky="ew", padx=(7, 0))

    def _build_output(self) -> None:
        self.output_card = ctk.CTkFrame(self, corner_radius=8, border_width=1)
        self.output_card.grid(row=3, column=0, sticky="nsew")
        self.output_card.grid_columnconfigure(0, weight=1)
        self.output_card.grid_rowconfigure(4, weight=1)

        self.result_title = ctk.CTkLabel(
            self.output_card,
            text="Результат",
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
            text="Таблиця коренів",
            anchor="w",
            font=self.fonts["label"],
        )
        self.table_title.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 6))

        self.table_frame = tk.Frame(self.output_card, bg="#101010")
        self.table_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0, 14))
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        columns = ("index", "interval", "root", "residual", "error", "iterations")
        self.results_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=11,
        )

        self.results_table.heading("index", text="N")
        self.results_table.heading("interval", text="Проміжок")
        self.results_table.heading("root", text="x")
        self.results_table.heading("residual", text="f(x)")
        self.results_table.heading("error", text="Похибка")
        self.results_table.heading("iterations", text="Ітерації")

        self.results_table.column("index", width=45, anchor="center")
        self.results_table.column("interval", width=220, anchor="center")
        self.results_table.column("root", width=140, anchor="center")
        self.results_table.column("residual", width=130, anchor="center")
        self.results_table.column("error", width=130, anchor="center")
        self.results_table.column("iterations", width=80, anchor="center")

        self.table_scrollbar = ttk.Scrollbar(
            self.table_frame,
            orient="vertical",
            command=self.results_table.yview,
        )
        self.results_table.configure(yscrollcommand=self.table_scrollbar.set)

        self.results_table.grid(row=0, column=0, sticky="nsew")
        self.table_scrollbar.grid(row=0, column=1, sticky="ns")

    def _fill_table(self, results: list[RootResult]) -> None:
        for item in self.results_table.get_children():
            self.results_table.delete(item)

        for row in build_error_rows(results):
            self.results_table.insert(
                "",
                "end",
                values=(
                    row.index,
                    row.interval.as_text(),
                    f"{row.root:.10f}",
                    f"{row.function_value:.3e}",
                    f"{row.estimated_error:.3e}",
                    row.iterations,
                ),
            )

    def load_json(self) -> None:
        path = filedialog.askopenfilename(
            title="Вибір JSON-файлу",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            loaded = load_json_config(path)

            self._set_entry_value(self.entry_left, loaded.get("left", 0.0))
            self._set_entry_value(self.entry_right, loaded.get("right", 4.0))
            self._set_entry_value(self.entry_scan_step, loaded.get("scan_step", 0.1))
            self._set_entry_value(self.entry_epsilon, loaded.get("epsilon", 1e-5))
            self._set_entry_value(
                self.entry_max_iterations,
                loaded.get("max_iterations", 100),
            )
            self._set_entry_value(self.entry_plot_points, loaded.get("plot_points", 500))

            self.result_var.set("JSON завантажено. Натисни «Обчислити».")
            self.error_var.set("")
        except Exception as exc:
            self.result_var.set("Дані не завантажено")
            self.error_var.set(f"Помилка: {exc}")

    def _parse_input(self) -> tuple[float, float, float, float, int, int]:
        left = float(self.entry_left.get().strip())
        right = float(self.entry_right.get().strip())
        scan_step = float(self.entry_scan_step.get().strip())
        epsilon = float(self.entry_epsilon.get().strip())
        max_iterations = int(self.entry_max_iterations.get().strip())
        plot_points = int(self.entry_plot_points.get().strip())

        if right <= left:
            raise ValueError("Потрібно, щоб права межа була більшою за ліву.")
        if scan_step <= 0:
            raise ValueError("Крок має бути додатним.")
        if scan_step > right - left:
            raise ValueError("Крок не має перевищувати довжину проміжку пошуку.")
        if epsilon <= 0:
            raise ValueError("epsilon має бути додатним.")
        if max_iterations < 1:
            raise ValueError("Кількість ітерацій має бути не меншою за 1.")
        if plot_points < 50:
            raise ValueError("Кількість точок графіка має бути не меншою за 50.")

        return left, right, scan_step, epsilon, max_iterations, plot_points

    def compute(self) -> None:
        try:
            (
                left,
                right,
                scan_step,
                epsilon,
                max_iterations,
                plot_points,
            ) = self._parse_input()
            function_name = "target"
            func, function_title = get_function_by_name(function_name)

            intervals = isolate_root_intervals(func, left, right, scan_step)
            results = solve_all_intervals(func, intervals, epsilon, max_iterations)
            report = build_full_report(
                function_title=function_title,
                left=left,
                right=right,
                scan_step=scan_step,
                epsilon=epsilon,
                max_iterations=max_iterations,
                intervals=intervals,
                results=results,
            )

            self.app_state.function_name = function_name
            self.app_state.function_title = function_title
            self.app_state.left = left
            self.app_state.right = right
            self.app_state.scan_step = scan_step
            self.app_state.epsilon = epsilon
            self.app_state.max_iterations = max_iterations
            self.app_state.plot_points = plot_points
            self.app_state.intervals = intervals
            self.app_state.results = results
            self.app_state.report = report

            self.result_var.set(build_short_result(results))
            self.error_var.set("")
            self._fill_table(results)
        except Exception as exc:
            self.result_var.set("Обчислення не виконано")
            self.error_var.set(f"Помилка: {exc}")

    def save_report(self) -> None:
        if not self.app_state.report.strip():
            self.result_var.set("Немає звіту")
            self.error_var.set("Помилка: спочатку виконай обчислення.")
            return

        path = filedialog.asksaveasfilename(
            title="Збереження звіту",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            save_text_report(path, self.app_state.report)
            self.error_var.set("")
        except Exception as exc:
            self.error_var.set(f"Помилка: {exc}")

    def clear_all(self) -> None:
        self.reset_defaults()

    def reset_defaults(self) -> None:
        self._set_entry_value(self.entry_left, "0")
        self._set_entry_value(self.entry_right, "4")
        self._set_entry_value(self.entry_scan_step, "0.1")
        self._set_entry_value(self.entry_epsilon, "0.00001")
        self._set_entry_value(self.entry_max_iterations, "100")
        self._set_entry_value(self.entry_plot_points, "500")

        self.result_var.set("Готово до обчислень")
        self.error_var.set("")

        for item in self.results_table.get_children():
            self.results_table.delete(item)

        self.app_state.function_name = "target"
        self.app_state.function_title = "2^x - 4x = 0"
        self.app_state.left = 0.0
        self.app_state.right = 4.0
        self.app_state.scan_step = 0.1
        self.app_state.epsilon = 1e-5
        self.app_state.max_iterations = 100
        self.app_state.plot_points = 500
        self.app_state.intervals = None
        self.app_state.results = None
        self.app_state.report = ""

    def _set_entry_value(self, entry: ctk.CTkEntry, value: object) -> None:
        entry.delete(0, tk.END)
        entry.insert(0, str(value))

    def apply_theme(self, palette: dict[str, str]) -> None:
        super().apply_theme(palette)

        for card in (self.header_card, self.form_card, self.output_card):
            card.configure(
                fg_color=palette["panel"],
                border_color=palette["surface_soft"],
            )

        self.title_label.configure(text_color=palette["text"])
        self.subtitle_label.configure(text_color=palette["muted"])
        self.equation_label.configure(text_color=palette["muted"])
        self.expected_label.configure(text_color=palette["warning"])

        for entry in (
            self.entry_left,
            self.entry_right,
            self.entry_scan_step,
            self.entry_epsilon,
            self.entry_max_iterations,
            self.entry_plot_points,
        ):
            entry.configure(
                fg_color=palette["surface"],
                border_color=palette["surface_soft"],
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
            background="#101010",
            foreground="#F5F7FA",
            fieldbackground="#101010",
            rowheight=28,
            bordercolor="#2A2A2A",
            borderwidth=1,
        )
        style.configure(
            "Treeview.Heading",
            background="#171717",
            foreground="#F5F7FA",
            relief="flat",
        )
        style.map(
            "Treeview",
            background=[("selected", "#1F7A55")],
            foreground=[("selected", "#F5F7FA")],
        )


class GraphPage(BasePage):
    def __init__(
        self,
        master: ctk.CTkFrame,
        page_config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
        app_state: BisectionState,
    ) -> None:
        super().__init__(master, page_config, fonts)
        self.app_state = app_state

        self.status_var = tk.StringVar(value="Графік очікує на обчислення")
        self.error_var = tk.StringVar(value="")
        self.canvas: tk.Canvas | None = None
        self.plot_data: PlotData | None = None
        self.view_left = 0.0
        self.view_right = 1.0
        self.view_y_min = -1.0
        self.view_y_max = 1.0
        self.drag_start: tuple[int, int, float, float, float, float] | None = None

        self.grid_rowconfigure(3, weight=1)

        self._build_header()
        self._build_controls()
        self._build_output()
        self._build_plot_area()

    def _build_header(self) -> None:
        self.header_card = ctk.CTkFrame(self, corner_radius=8, border_width=1)
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
            justify="left",
            wraplength=860,
            font=self.fonts["subtitle"],
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

    def _build_controls(self) -> None:
        self.controls_card = ctk.CTkFrame(self, corner_radius=8, border_width=1)
        self.controls_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        self.controls_card.grid_columnconfigure((0, 1), weight=1)

        self.info_label = ctk.CTkLabel(
            self.controls_card,
            text=(
                "Графік функції f(x)=2^x-4x з відокремленими проміжками "
                "та уточненими коренями. Перетягуй поле графіка мишею, "
                "коліщатко змінює масштаб."
            ),
            anchor="w",
            justify="left",
            wraplength=860,
            font=self.fonts["body"],
        )
        self.info_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(14, 12))

        self.build_button = ctk.CTkButton(
            self.controls_card,
            text="Побудувати графік",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.build_graph,
        )
        self.build_button.grid(row=1, column=0, sticky="ew", padx=(20, 8), pady=(0, 14))

        self.reset_view_button = ctk.CTkButton(
            self.controls_card,
            text="Скинути вид",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.reset_plot_view,
        )
        self.reset_view_button.grid(row=1, column=1, sticky="ew", padx=(8, 20), pady=(0, 14))

    def _build_output(self) -> None:
        self.output_card = ctk.CTkFrame(self, corner_radius=8, border_width=1)
        self.output_card.grid(row=2, column=0, sticky="ew")
        self.output_card.grid_columnconfigure(0, weight=1)

        self.status_title = ctk.CTkLabel(
            self.output_card,
            text="Стан",
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
        self.plot_card = ctk.CTkFrame(self, corner_radius=8, border_width=1)
        self.plot_card.grid(row=3, column=0, sticky="nsew", pady=(14, 0))
        self.plot_card.grid_columnconfigure(0, weight=1)
        self.plot_card.grid_rowconfigure(0, weight=1)

        self.plot_container = ctk.CTkFrame(self.plot_card, fg_color="transparent")
        self.plot_container.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self.plot_container.grid_columnconfigure(0, weight=1)
        self.plot_container.grid_rowconfigure(0, weight=1)

    def build_graph(self) -> None:
        try:
            if self.app_state.intervals is None or self.app_state.results is None:
                raise ValueError("Спочатку виконай обчислення на сторінці «Обчислення».")

            self.status_var.set("Побудова графіка...")
            self.error_var.set("")
            self.update_idletasks()

            func, _ = get_function_by_name(self.app_state.function_name)
            plot_data = build_function_plot_data(
                func=func,
                intervals=self.app_state.intervals,
                results=self.app_state.results,
                left=self.app_state.left,
                right=self.app_state.right,
                plot_points=self.app_state.plot_points,
            )
            self.plot_data = plot_data
            self.reset_plot_view()

            self.status_var.set("Графік побудовано")
        except Exception as exc:
            self.status_var.set("Графік не побудовано")
            self.error_var.set(f"Помилка: {exc}")

    def reset_plot_view(self) -> None:
        if self.plot_data is None:
            self.status_var.set("Немає графіка для скидання виду")
            return

        self.view_left = self.plot_data.left
        self.view_right = self.plot_data.right
        self.view_y_min = self.plot_data.y_min
        self.view_y_max = self.plot_data.y_max
        self.error_var.set("")
        self.status_var.set("Вид скинуто")
        self._draw_plot()

    def _draw_plot(self) -> None:
        if self.plot_data is None:
            return

        plot_data = self.plot_data
        (
            width,
            height,
            left_pad,
            right_pad,
            top_pad,
            bottom_pad,
            plot_width,
            plot_height,
        ) = self._plot_geometry()
        palette = MAIN_THEME

        if self.canvas is None:
            self.canvas = tk.Canvas(
                self.plot_container,
                width=width,
                height=height,
                bg=palette["surface"],
                highlightthickness=0,
                cursor="hand2",
            )
            self.canvas.grid(row=0, column=0, sticky="nsew")
            self.canvas.bind("<ButtonPress-1>", self._start_pan)
            self.canvas.bind("<B1-Motion>", self._pan_plot)
            self.canvas.bind("<ButtonRelease-1>", self._finish_pan)
            self.canvas.bind("<MouseWheel>", self._zoom_plot)
            self.canvas.bind("<Button-4>", self._zoom_plot)
            self.canvas.bind("<Button-5>", self._zoom_plot)
        else:
            self.canvas.delete("all")

        def map_x(x_value: float) -> float:
            return left_pad + (x_value - self.view_left) / (
                self.view_right - self.view_left
            ) * plot_width

        def map_y(y_value: float) -> float:
            return top_pad + (self.view_y_max - y_value) / (
                self.view_y_max - self.view_y_min
            ) * plot_height

        self.canvas.create_rectangle(
            left_pad,
            top_pad,
            width - right_pad,
            height - bottom_pad,
            outline=palette["surface_soft"],
            fill="#141414",
        )

        for index in range(6):
            x_grid = left_pad + index * plot_width / 5
            x_value = self.view_left + index * (self.view_right - self.view_left) / 5
            self.canvas.create_line(
                x_grid,
                top_pad,
                x_grid,
                height - bottom_pad,
                fill="#242424",
            )
            self.canvas.create_text(
                x_grid,
                height - 26,
                text=f"{x_value:.2f}",
                fill=palette["muted"],
                font=("Segoe UI", 9),
            )

            y_grid = top_pad + index * plot_height / 5
            y_value = self.view_y_max - index * (self.view_y_max - self.view_y_min) / 5
            self.canvas.create_line(
                left_pad,
                y_grid,
                width - right_pad,
                y_grid,
                fill="#242424",
            )
            self.canvas.create_text(
                34,
                y_grid,
                text=f"{y_value:.1f}",
                fill=palette["muted"],
                font=("Segoe UI", 9),
            )

        for interval in plot_data.intervals:
            if interval.right < self.view_left or interval.left > self.view_right:
                continue

            x_start = map_x(interval.left)
            x_end = map_x(interval.right)
            if interval.width == 0:
                if not self.view_left <= interval.left <= self.view_right:
                    continue

                self.canvas.create_line(
                    x_start,
                    top_pad,
                    x_start,
                    height - bottom_pad,
                    fill=palette["error"],
                    width=2,
                )
            else:
                x_start = max(left_pad, min(width - right_pad, x_start))
                x_end = max(left_pad, min(width - right_pad, x_end))
                self.canvas.create_rectangle(
                    x_start,
                    top_pad,
                    x_end,
                    height - bottom_pad,
                    fill="#2F2A17",
                    outline="",
                )

        if self.view_y_min <= 0 <= self.view_y_max:
            y_zero = map_y(0.0)
            self.canvas.create_line(
                left_pad,
                y_zero,
                width - right_pad,
                y_zero,
                fill=palette["warning"],
                width=2,
            )

        if self.view_left <= 0 <= self.view_right:
            x_zero = map_x(0.0)
            self.canvas.create_line(
                x_zero,
                top_pad,
                x_zero,
                height - bottom_pad,
                fill="#555555",
                width=1,
            )

        coordinates: list[float] = []
        for x_value, y_value in zip(plot_data.x_values, plot_data.y_values):
            x_position = map_x(x_value)
            y_position = map_y(y_value)
            is_visible = (
                left_pad <= x_position <= width - right_pad
                and top_pad <= y_position <= height - bottom_pad
            )

            if is_visible:
                coordinates.extend([x_position, y_position])
            elif len(coordinates) >= 4:
                self.canvas.create_line(
                    *coordinates,
                    fill=palette["accent"],
                    width=2,
                    smooth=True,
                )
                coordinates = []

        if len(coordinates) >= 4:
            self.canvas.create_line(
                *coordinates,
                fill=palette["accent"],
                width=2,
                smooth=True,
            )

        for result in plot_data.results:
            if not (
                self.view_left <= result.root <= self.view_right
                and self.view_y_min <= 0 <= self.view_y_max
            ):
                continue

            x_root = map_x(result.root)
            y_root = map_y(0.0)
            self.canvas.create_oval(
                x_root - 5,
                y_root - 5,
                x_root + 5,
                y_root + 5,
                fill=palette["error"],
                outline=palette["text"],
                width=1,
            )

        self.canvas.create_text(
            width / 2,
            16,
            text="f(x) = 2^x - 4x",
            fill=palette["text"],
            font=("Segoe UI", 11, "bold"),
        )
        self.canvas.create_text(
            width / 2,
            height - 10,
            text="x",
            fill=palette["muted"],
            font=("Segoe UI", 10),
        )
        self.canvas.create_text(
            16,
            top_pad - 14,
            text="f(x)",
            fill=palette["muted"],
            font=("Segoe UI", 10),
        )

    def _plot_geometry(self) -> tuple[int, int, int, int, int, int, int, int]:
        width = 740
        height = 500
        left_pad = 62
        right_pad = 28
        top_pad = 34
        bottom_pad = 48
        plot_width = width - left_pad - right_pad
        plot_height = height - top_pad - bottom_pad
        return (
            width,
            height,
            left_pad,
            right_pad,
            top_pad,
            bottom_pad,
            plot_width,
            plot_height,
        )

    def _is_inside_plot(self, x_position: int, y_position: int) -> bool:
        (
            width,
            height,
            left_pad,
            right_pad,
            top_pad,
            bottom_pad,
            _plot_width,
            _plot_height,
        ) = self._plot_geometry()
        return (
            left_pad <= x_position <= width - right_pad
            and top_pad <= y_position <= height - bottom_pad
        )

    def _start_pan(self, event: tk.Event) -> None:
        if self.canvas is None or not self._is_inside_plot(event.x, event.y):
            return

        self.drag_start = (
            event.x,
            event.y,
            self.view_left,
            self.view_right,
            self.view_y_min,
            self.view_y_max,
        )
        self.canvas.configure(cursor="fleur")

    def _pan_plot(self, event: tk.Event) -> None:
        if self.drag_start is None:
            return

        (
            _width,
            _height,
            _left_pad,
            _right_pad,
            _top_pad,
            _bottom_pad,
            plot_width,
            plot_height,
        ) = self._plot_geometry()
        start_x, start_y, left, right, y_min, y_max = self.drag_start
        x_shift = (event.x - start_x) / plot_width * (right - left)
        y_shift = (event.y - start_y) / plot_height * (y_max - y_min)

        self.view_left = left - x_shift
        self.view_right = right - x_shift
        self.view_y_min = y_min + y_shift
        self.view_y_max = y_max + y_shift
        self._draw_plot()

    def _finish_pan(self, _event: tk.Event) -> None:
        self.drag_start = None
        if self.canvas is not None:
            self.canvas.configure(cursor="hand2")

    def _zoom_plot(self, event: tk.Event) -> str | None:
        if self.plot_data is None or not self._is_inside_plot(event.x, event.y):
            return None

        (
            _width,
            _height,
            left_pad,
            _right_pad,
            top_pad,
            _bottom_pad,
            plot_width,
            plot_height,
        ) = self._plot_geometry()
        x_span = self.view_right - self.view_left
        y_span = self.view_y_max - self.view_y_min

        if x_span <= 0 or y_span <= 0:
            return None

        scroll_delta = getattr(event, "delta", 0)
        scroll_number = getattr(event, "num", None)
        zoom_in = scroll_delta > 0 or scroll_number == 4
        scale = 0.82 if zoom_in else 1.22

        pointer_x_ratio = (event.x - left_pad) / plot_width
        pointer_y_ratio = (event.y - top_pad) / plot_height
        data_x = self.view_left + pointer_x_ratio * x_span
        data_y = self.view_y_max - pointer_y_ratio * y_span
        new_x_span = max(x_span * scale, 1e-8)
        new_y_span = max(y_span * scale, 1e-8)

        self.view_left = data_x - pointer_x_ratio * new_x_span
        self.view_right = self.view_left + new_x_span
        self.view_y_max = data_y + pointer_y_ratio * new_y_span
        self.view_y_min = self.view_y_max - new_y_span
        self._draw_plot()
        return "break"

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
        self.reset_view_button.configure(
            fg_color=palette["segment"],
            hover_color=palette["segment_hover"],
            text_color=palette["text"],
        )

        self.status_title.configure(text_color=palette["muted"])
        self.status_label.configure(text_color=palette["text"])
        self.error_label.configure(text_color=palette["error"])


class AlgorithmsApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")

        self.title("BisectionMethodApp")
        self.resizable(False, False)
        self.geometry("820x900")

        self.current_page = "main"
        self.nav_buttons: dict[str, ctk.CTkButton] = {}
        self.pages: dict[str, BasePage] = {}
        self.app_state = BisectionState()

        self.fonts: dict[str, ctk.CTkFont] = {
            "title": ctk.CTkFont(family="Segoe UI", size=27, weight="bold"),
            "subtitle": ctk.CTkFont(family="Segoe UI", size=13),
            "label": ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            "body": ctk.CTkFont(family="Segoe UI", size=12),
            "button": ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            "result": ctk.CTkFont(family="Consolas", size=15, weight="bold"),
            "nav": ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        }

        self.page_configs: tuple[PageConfig, ...] = (
            PageConfig(
                page_id="main",
                nav_title="Обчислення",
                title="Метод половинного ділення",
                subtitle=(
                    "Розв'язання рівняння 2^x - 4x = 0. "
                    "Відокремлення коренів і уточнення з точністю epsilon."
                ),
            ),
            PageConfig(
                page_id="graph",
                nav_title="Графік",
                title="Графік функції",
                subtitle="Побудова f(x), проміжків відокремлення та знайдених коренів.",
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
                width=130,
                height=36,
                corner_radius=8,
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

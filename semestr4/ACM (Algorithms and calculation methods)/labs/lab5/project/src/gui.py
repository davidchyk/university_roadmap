from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass, field
from tkinter import filedialog, ttk
from typing import Callable

import customtkinter as ctk

from src.gaussian import build_default_problem, solve_gauss_partial_pivot, validate_problem
from src.io_utils import load_system_config, save_text_report
from src.models import EliminationStep, GaussianResult, MatrixProblem, PageConfig, NumberMatrix, NumberVector
from src.report import build_full_report, build_short_result, format_matrix_for_display
from src.theme import MAIN_THEME


@dataclass
class LinearSystemState:
    problem: MatrixProblem = field(default_factory=build_default_problem)
    result: GaussianResult | None = None
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

    def refresh(self) -> None:
        pass

    def apply_theme(self, palette: dict[str, str]) -> None:
        self.configure(fg_color=palette["bg"])


class MatrixPage(BasePage):
    def __init__(
        self,
        master: ctk.CTkFrame,
        page_config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
        app_state: LinearSystemState,
        on_result_changed: Callable[[], None],
    ) -> None:
        super().__init__(master, page_config, fonts)
        self.app_state = app_state
        self.on_result_changed = on_result_changed

        self.status_var = tk.StringVar(value="Готово до обчислень")
        self.error_var = tk.StringVar(value="")
        self.size_var = tk.StringVar(value=str(self.app_state.problem.size))
        self.matrix_entries: list[list[ctk.CTkEntry]] = []
        self.vector_entries: list[ctk.CTkEntry] = []

        self.grid_rowconfigure(1, weight=1)
        self._build_header()
        self._build_workspace()
        self._set_problem(self.app_state.problem, reset_output=True)

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
            wraplength=1020,
            font=self.fonts["subtitle"],
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 14))

    def _build_workspace(self) -> None:
        self.workspace = ctk.CTkFrame(self, fg_color="transparent")
        self.workspace.grid(row=1, column=0, sticky="nsew")
        self.workspace.grid_columnconfigure(0, weight=5)
        self.workspace.grid_columnconfigure(1, weight=3)
        self.workspace.grid_rowconfigure(0, weight=1)

        self.input_card = ctk.CTkFrame(self.workspace, corner_radius=8, border_width=1)
        self.input_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.input_card.grid_columnconfigure(0, weight=1)
        self.input_card.grid_rowconfigure(2, weight=1)

        self.result_card = ctk.CTkFrame(self.workspace, corner_radius=8, border_width=1)
        self.result_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.result_card.grid_columnconfigure(0, weight=1)
        self.result_card.grid_rowconfigure(5, weight=1)

        self._build_problem_controls()
        self._build_matrix_area()
        self._build_action_bar()
        self._build_result_panel()

    def _build_problem_controls(self) -> None:
        self.controls_frame = ctk.CTkFrame(self.input_card, fg_color="transparent")
        self.controls_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 8))
        self.controls_frame.grid_columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(
            self.controls_frame,
            text="Назва системи",
            anchor="w",
            font=self.fonts["label"],
        )
        self.name_label.grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.name_entry = ctk.CTkEntry(
            self.controls_frame,
            height=40,
            corner_radius=8,
            font=self.fonts["body"],
        )
        self.name_entry.grid(row=1, column=0, sticky="ew", padx=(0, 12))
        self.name_entry.bind("<KeyRelease>", self._mark_dirty)

        self.size_label = ctk.CTkLabel(
            self.controls_frame,
            text="Розмір",
            anchor="w",
            font=self.fonts["label"],
        )
        self.size_label.grid(row=0, column=1, sticky="w", pady=(0, 6))

        self.size_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=[str(value) for value in range(2, 11)],
            variable=self.size_var,
            width=110,
            height=40,
            corner_radius=8,
            font=self.fonts["body"],
            command=self._resize_matrix,
        )
        self.size_menu.grid(row=1, column=1, sticky="ew")

        self.method_label = ctk.CTkLabel(
            self.input_card,
            text="A · x = b, метод Гауса з вибором головного елемента за стовпцем",
            anchor="w",
            font=self.fonts["label"],
        )
        self.method_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))

    def _build_matrix_area(self) -> None:
        self.matrix_area = ctk.CTkScrollableFrame(
            self.input_card,
            corner_radius=8,
            border_width=1,
        )
        self.matrix_area.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 14))
        self.matrix_area.grid_columnconfigure(0, weight=1)

    def _build_action_bar(self) -> None:
        self.action_bar = ctk.CTkFrame(self.input_card, fg_color="transparent")
        self.action_bar.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 18))
        self.action_bar.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.solve_button = ctk.CTkButton(
            self.action_bar,
            text="Розв'язати",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.solve,
        )
        self.solve_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.load_button = ctk.CTkButton(
            self.action_bar,
            text="JSON",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.load_json,
        )
        self.load_button.grid(row=0, column=1, sticky="ew", padx=6)

        self.save_button = ctk.CTkButton(
            self.action_bar,
            text="Звіт",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.save_report,
        )
        self.save_button.grid(row=0, column=2, sticky="ew", padx=6)

        self.default_button = ctk.CTkButton(
            self.action_bar,
            text="Варіант",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.reset_variant,
        )
        self.default_button.grid(row=0, column=3, sticky="ew", padx=6)

        self.clear_button = ctk.CTkButton(
            self.action_bar,
            text="Очистити",
            height=40,
            corner_radius=8,
            font=self.fonts["button"],
            command=self.clear_matrix,
        )
        self.clear_button.grid(row=0, column=4, sticky="ew", padx=(6, 0))

    def _build_result_panel(self) -> None:
        self.result_title = ctk.CTkLabel(
            self.result_card,
            text="Результат",
            anchor="w",
            font=self.fonts["title_small"],
        )
        self.result_title.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 8))

        self.status_label = ctk.CTkLabel(
            self.result_card,
            textvariable=self.status_var,
            anchor="w",
            justify="left",
            wraplength=360,
            font=self.fonts["result"],
        )
        self.status_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))

        self.error_label = ctk.CTkLabel(
            self.result_card,
            textvariable=self.error_var,
            anchor="w",
            justify="left",
            wraplength=360,
            font=self.fonts["body"],
        )
        self.error_label.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 12))

        self.stats_frame = ctk.CTkFrame(self.result_card, corner_radius=8, border_width=1)
        self.stats_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 14))
        self.stats_frame.grid_columnconfigure((0, 1), weight=1)

        self.det_caption = ctk.CTkLabel(
            self.stats_frame,
            text="det(A)",
            font=self.fonts["label"],
            anchor="w",
        )
        self.det_caption.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 2))
        self.det_value = ctk.CTkLabel(
            self.stats_frame,
            text="-",
            font=self.fonts["metric"],
            anchor="w",
        )
        self.det_value.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 12))

        self.residual_caption = ctk.CTkLabel(
            self.stats_frame,
            text="max |Ax - b|",
            font=self.fonts["label"],
            anchor="w",
        )
        self.residual_caption.grid(row=0, column=1, sticky="ew", padx=14, pady=(12, 2))
        self.residual_value = ctk.CTkLabel(
            self.stats_frame,
            text="-",
            font=self.fonts["metric"],
            anchor="w",
        )
        self.residual_value.grid(row=1, column=1, sticky="ew", padx=14, pady=(0, 12))

        self.solution_label = ctk.CTkLabel(
            self.result_card,
            text="Вектор x",
            anchor="w",
            font=self.fonts["label"],
        )
        self.solution_label.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 6))

        self.result_text = ctk.CTkTextbox(
            self.result_card,
            corner_radius=8,
            border_width=1,
            wrap="none",
            font=self.fonts["mono"],
        )
        self.result_text.grid(row=5, column=0, sticky="nsew", padx=20, pady=(0, 18))
        self._set_text(self.result_text, "Після натискання «Розв'язати» тут буде вектор x.")

    def _build_matrix_grid(self, problem: MatrixProblem) -> None:
        for child in self.matrix_area.winfo_children():
            child.destroy()

        size = problem.size
        self.matrix_entries = []
        self.vector_entries = []
        self.matrix_area.grid_columnconfigure(tuple(range(size + 3)), weight=1)

        empty_corner = ctk.CTkLabel(self.matrix_area, text="", width=44)
        empty_corner.grid(row=0, column=0, padx=(0, 8), pady=(6, 8))

        for column in range(size):
            label = ctk.CTkLabel(
                self.matrix_area,
                text=f"x{column + 1}",
                font=self.fonts["label"],
                anchor="center",
            )
            label.grid(row=0, column=column + 1, sticky="ew", padx=4, pady=(6, 8))

        separator = ctk.CTkLabel(self.matrix_area, text="|", font=self.fonts["label"])
        separator.grid(row=0, column=size + 1, padx=8, pady=(6, 8))

        rhs_header = ctk.CTkLabel(
            self.matrix_area,
            text="b",
            font=self.fonts["label"],
            anchor="center",
        )
        rhs_header.grid(row=0, column=size + 2, sticky="ew", padx=4, pady=(6, 8))

        for row in range(size):
            row_label = ctk.CTkLabel(
                self.matrix_area,
                text=f"R{row + 1}",
                width=44,
                font=self.fonts["label"],
                anchor="w",
            )
            row_label.grid(row=row + 1, column=0, sticky="w", padx=(0, 8), pady=5)

            row_entries: list[ctk.CTkEntry] = []
            for column in range(size):
                entry = ctk.CTkEntry(
                    self.matrix_area,
                    width=84,
                    height=38,
                    justify="center",
                    corner_radius=8,
                    font=self.fonts["body"],
                )
                entry.grid(row=row + 1, column=column + 1, sticky="ew", padx=4, pady=5)
                self._set_entry_value(entry, problem.matrix[row][column])
                entry.bind("<KeyRelease>", self._mark_dirty)
                row_entries.append(entry)

            separator = ctk.CTkLabel(self.matrix_area, text="|", font=self.fonts["label"])
            separator.grid(row=row + 1, column=size + 1, padx=8, pady=5)

            rhs_entry = ctk.CTkEntry(
                self.matrix_area,
                width=84,
                height=38,
                justify="center",
                corner_radius=8,
                font=self.fonts["body"],
            )
            rhs_entry.grid(row=row + 1, column=size + 2, sticky="ew", padx=4, pady=5)
            self._set_entry_value(rhs_entry, problem.vector[row])
            rhs_entry.bind("<KeyRelease>", self._mark_dirty)
            self.matrix_entries.append(row_entries)
            self.vector_entries.append(rhs_entry)

        self._style_matrix_cells(MAIN_THEME)

    def _resize_matrix(self, selected: str) -> None:
        old_matrix, old_vector = self._read_entries_loose()
        old_size = len(old_vector)
        new_size = int(selected)
        matrix = [[0.0 for _ in range(new_size)] for _ in range(new_size)]
        vector = [0.0 for _ in range(new_size)]

        for row in range(min(old_size, new_size)):
            vector[row] = old_vector[row]
            for column in range(min(old_size, new_size)):
                matrix[row][column] = old_matrix[row][column]

        self._set_problem(
            MatrixProblem(
                name=self.name_entry.get().strip() or f"Система {new_size}x{new_size}",
                matrix=matrix,
                vector=vector,
            ),
            reset_output=False,
        )
        self.status_var.set("Розмір змінено. Заповни коефіцієнти і розв'яжи систему.")
        self.error_var.set("")
        self.app_state.result = None
        self.app_state.report = ""
        self.on_result_changed()

    def solve(self) -> None:
        try:
            problem = self._parse_problem()
            result = solve_gauss_partial_pivot(problem)
            report = build_full_report(result)

            self.app_state.problem = problem
            self.app_state.result = result
            self.app_state.report = report

            self.status_var.set("Систему розв'язано")
            self.error_var.set("")
            self.det_value.configure(text=f"{result.determinant:.6g}")
            self.residual_value.configure(text=f"{result.residual_norm:.3e}")
            self._set_text(self.result_text, build_short_result(result))
            self.on_result_changed()
        except Exception as exc:
            self.status_var.set("Обчислення не виконано")
            self.error_var.set(f"Помилка: {exc}")
            self.det_value.configure(text="-")
            self.residual_value.configure(text="-")
            self._set_text(self.result_text, "Перевір вхідні дані та повтори обчислення.")

    def load_json(self) -> None:
        path = filedialog.askopenfilename(
            title="Вибір JSON-файлу",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            problem = load_system_config(path)
            validate_problem(problem)
            self._set_problem(problem, reset_output=True)
            self.app_state.problem = problem
            self.app_state.result = None
            self.app_state.report = ""
            self.status_var.set("JSON завантажено. Натисни «Розв'язати».")
            self.error_var.set("")
            self.on_result_changed()
        except Exception as exc:
            self.status_var.set("JSON не завантажено")
            self.error_var.set(f"Помилка: {exc}")

    def save_report(self) -> None:
        if not self.app_state.report.strip():
            self.status_var.set("Немає звіту")
            self.error_var.set("Спочатку виконай обчислення.")
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
            self.status_var.set("Звіт збережено")
            self.error_var.set("")
        except Exception as exc:
            self.status_var.set("Звіт не збережено")
            self.error_var.set(f"Помилка: {exc}")

    def reset_variant(self) -> None:
        problem = build_default_problem()
        self._set_problem(problem, reset_output=True)
        self.app_state.problem = problem
        self.app_state.result = None
        self.app_state.report = ""
        self.status_var.set("Варіант з фото відновлено")
        self.error_var.set("")
        self.on_result_changed()

    def clear_matrix(self) -> None:
        size = int(self.size_var.get())
        problem = MatrixProblem(
            name=f"Система {size}x{size}",
            matrix=[[0.0 for _ in range(size)] for _ in range(size)],
            vector=[0.0 for _ in range(size)],
        )
        self._set_problem(problem, reset_output=True)
        self.app_state.problem = problem
        self.app_state.result = None
        self.app_state.report = ""
        self.status_var.set("Поля очищено")
        self.error_var.set("")
        self.on_result_changed()

    def refresh(self) -> None:
        if self.app_state.result is not None:
            self.status_var.set("Систему розв'язано")
            self.det_value.configure(text=f"{self.app_state.result.determinant:.6g}")
            self.residual_value.configure(text=f"{self.app_state.result.residual_norm:.3e}")
            self._set_text(self.result_text, build_short_result(self.app_state.result))

    def _parse_problem(self) -> MatrixProblem:
        size = int(self.size_var.get())
        matrix: NumberMatrix = []
        vector: NumberVector = []
        for row in range(size):
            matrix_row: list[float] = []
            for column in range(size):
                matrix_row.append(self._parse_number(self.matrix_entries[row][column].get()))
            matrix.append(matrix_row)
            vector.append(self._parse_number(self.vector_entries[row].get()))

        problem = MatrixProblem(
            name=self.name_entry.get().strip() or f"Система {size}x{size}",
            matrix=matrix,
            vector=vector,
        )
        validate_problem(problem)
        return problem

    def _read_entries_loose(self) -> tuple[NumberMatrix, NumberVector]:
        size = len(self.vector_entries)
        matrix = [[0.0 for _ in range(size)] for _ in range(size)]
        vector = [0.0 for _ in range(size)]

        for row in range(size):
            for column in range(size):
                try:
                    matrix[row][column] = self._parse_number(self.matrix_entries[row][column].get())
                except ValueError:
                    matrix[row][column] = 0.0
            try:
                vector[row] = self._parse_number(self.vector_entries[row].get())
            except ValueError:
                vector[row] = 0.0

        return matrix, vector

    def _set_problem(self, problem: MatrixProblem, reset_output: bool) -> None:
        self.size_var.set(str(problem.size))
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, problem.name)
        self._build_matrix_grid(problem)
        if reset_output:
            self.det_value.configure(text="-")
            self.residual_value.configure(text="-")
            self._set_text(self.result_text, "Після натискання «Розв'язати» тут буде вектор x.")

    def _parse_number(self, raw_value: str) -> float:
        normalized = raw_value.strip().replace(",", ".")
        if not normalized:
            raise ValueError("Порожні поля потрібно заповнити числами.")
        return float(normalized)

    def _set_entry_value(self, entry: ctk.CTkEntry, value: object) -> None:
        entry.delete(0, tk.END)
        if isinstance(value, float):
            entry.insert(0, f"{value:g}")
        else:
            entry.insert(0, str(value))

    def _set_text(self, textbox: ctk.CTkTextbox, text: str) -> None:
        textbox.configure(state="normal")
        textbox.delete("1.0", tk.END)
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")

    def _mark_dirty(self, _event: tk.Event | None = None) -> None:
        if self.app_state.result is None and not self.app_state.report:
            return

        self.app_state.result = None
        self.app_state.report = ""
        self.status_var.set("Дані змінено")
        self.error_var.set("Результат застарів. Запусти обчислення ще раз.")
        self.det_value.configure(text="-")
        self.residual_value.configure(text="-")
        self._set_text(self.result_text, "Матрицю змінено. Натисни «Розв'язати», щоб оновити результат.")
        self.on_result_changed()

    def _style_matrix_cells(self, palette: dict[str, str]) -> None:
        for row in self.matrix_entries:
            for entry in row:
                entry.configure(
                    fg_color=palette["panel_alt"],
                    border_color=palette["surface_soft"],
                    text_color=palette["text"],
                )
        for entry in self.vector_entries:
            entry.configure(
                fg_color=palette["panel_alt"],
                border_color=palette["warning"],
                text_color=palette["text"],
            )

    def apply_theme(self, palette: dict[str, str]) -> None:
        super().apply_theme(palette)
        for card in (self.header_card, self.input_card, self.result_card, self.stats_frame):
            card.configure(fg_color=palette["panel"], border_color=palette["surface_soft"])

        self.matrix_area.configure(
            fg_color=palette["surface"],
            border_color=palette["surface_soft"],
            scrollbar_button_color=palette["segment"],
            scrollbar_button_hover_color=palette["segment_hover"],
        )

        for label in (
            self.title_label,
            self.result_title,
            self.det_value,
            self.residual_value,
        ):
            label.configure(text_color=palette["text"])

        for label in (
            self.subtitle_label,
            self.name_label,
            self.size_label,
            self.method_label,
            self.det_caption,
            self.residual_caption,
            self.solution_label,
        ):
            label.configure(text_color=palette["muted"])

        self.status_label.configure(text_color=palette["text"])
        self.error_label.configure(text_color=palette["error"])
        self.name_entry.configure(
            fg_color=palette["surface"],
            border_color=palette["surface_soft"],
            text_color=palette["text"],
        )
        self.size_menu.configure(
            fg_color=palette["segment"],
            button_color=palette["segment"],
            button_hover_color=palette["segment_hover"],
            text_color=palette["text"],
        )
        self.result_text.configure(
            fg_color=palette["surface"],
            border_color=palette["surface_soft"],
            text_color=palette["text"],
        )
        self._style_matrix_cells(palette)

        self.solve_button.configure(
            fg_color=palette["accent"],
            hover_color=palette["accent_hover"],
            text_color=palette["accent_text"],
        )
        for button in (self.load_button, self.save_button, self.default_button, self.clear_button):
            button.configure(
                fg_color=palette["segment"],
                hover_color=palette["segment_hover"],
                text_color=palette["text"],
            )


class StepsPage(BasePage):
    def __init__(
        self,
        master: ctk.CTkFrame,
        page_config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
        app_state: LinearSystemState,
    ) -> None:
        super().__init__(master, page_config, fonts)
        self.app_state = app_state
        self.steps: list[EliminationStep] = []

        self.grid_rowconfigure(1, weight=1)
        self._build_header()
        self._build_body()

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
            wraplength=1020,
            font=self.fonts["subtitle"],
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 14))

    def _build_body(self) -> None:
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.grid(row=1, column=0, sticky="nsew")
        self.body.grid_columnconfigure(0, weight=3)
        self.body.grid_columnconfigure(1, weight=4)
        self.body.grid_rowconfigure(0, weight=1)

        self.table_card = ctk.CTkFrame(self.body, corner_radius=8, border_width=1)
        self.table_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.table_card.grid_columnconfigure(0, weight=1)
        self.table_card.grid_rowconfigure(1, weight=1)

        self.table_title = ctk.CTkLabel(
            self.table_card,
            text="Вибір головних елементів",
            anchor="w",
            font=self.fonts["title_small"],
        )
        self.table_title.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))

        self.step_table_frame = tk.Frame(self.table_card, bg=MAIN_THEME["panel"])
        self.step_table_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.step_table_frame.grid_columnconfigure(0, weight=1)
        self.step_table_frame.grid_rowconfigure(0, weight=1)

        columns = ("step", "column", "row", "pivot", "swap", "ops")
        self.step_table = ttk.Treeview(
            self.step_table_frame,
            columns=columns,
            show="headings",
            height=14,
        )
        headings = {
            "step": "k",
            "column": "Стовпець",
            "row": "Рядок",
            "pivot": "Pivot",
            "swap": "Обмін",
            "ops": "Опер.",
        }
        widths = {
            "step": 44,
            "column": 82,
            "row": 72,
            "pivot": 112,
            "swap": 74,
            "ops": 62,
        }
        for column in columns:
            self.step_table.heading(column, text=headings[column])
            self.step_table.column(column, width=widths[column], anchor="center")

        self.step_scrollbar = ttk.Scrollbar(
            self.step_table_frame,
            orient="vertical",
            command=self.step_table.yview,
        )
        self.step_table.configure(yscrollcommand=self.step_scrollbar.set)
        self.step_table.grid(row=0, column=0, sticky="nsew")
        self.step_scrollbar.grid(row=0, column=1, sticky="ns")
        self.step_table.bind("<<TreeviewSelect>>", self._select_step)

        self.details_card = ctk.CTkFrame(self.body, corner_radius=8, border_width=1)
        self.details_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.details_card.grid_columnconfigure(0, weight=1)
        self.details_card.grid_rowconfigure(1, weight=1)

        self.details_title = ctk.CTkLabel(
            self.details_card,
            text="Матриця після кроку",
            anchor="w",
            font=self.fonts["title_small"],
        )
        self.details_title.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))

        self.details_text = ctk.CTkTextbox(
            self.details_card,
            corner_radius=8,
            border_width=1,
            wrap="none",
            font=self.fonts["mono"],
        )
        self.details_text.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self._set_text("Спочатку розв'яжи систему на сторінці «Система».")

    def refresh(self) -> None:
        for item in self.step_table.get_children():
            self.step_table.delete(item)

        result = self.app_state.result
        self.steps = [] if result is None else result.elimination_steps
        if result is None:
            self._set_text("Спочатку розв'яжи систему на сторінці «Система».")
            return

        for index, step in enumerate(self.steps):
            self.step_table.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    step.step,
                    step.pivot_column + 1,
                    step.selected_row + 1,
                    f"{step.pivot_value:.6g}",
                    "так" if step.did_swap else "ні",
                    len(step.operations),
                ),
            )

        if self.steps:
            first_item = self.step_table.get_children()[0]
            self.step_table.selection_set(first_item)
            self.step_table.focus(first_item)
            self._show_step(self.steps[0])
        else:
            self._set_text("Для системи 1x1 прямий хід не потрібен.")

    def _select_step(self, _event: tk.Event) -> None:
        selected = self.step_table.selection()
        if not selected:
            return
        step_index = int(selected[0])
        if 0 <= step_index < len(self.steps):
            self._show_step(self.steps[step_index])

    def _show_step(self, step: EliminationStep) -> None:
        lines = [
            f"Крок {step.step}",
            f"Стовпець: {step.pivot_column + 1}",
            f"Вибрано рядок: R{step.selected_row + 1}",
            f"Головний елемент: {step.pivot_value:.12g}",
        ]
        if step.did_swap:
            lines.append(f"Перестановка: R{step.pivot_row + 1} <-> R{step.selected_row + 1}")
        else:
            lines.append("Перестановка: не потрібна")

        lines.append("")
        lines.append("Операції занулення:")
        if step.operations:
            lines.extend(operation.as_text() for operation in step.operations)
        else:
            lines.append("Немає")

        lines.append("")
        lines.append(format_matrix_for_display(step.matrix, step.vector))
        self._set_text("\n".join(lines))

    def _set_text(self, text: str) -> None:
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", text)
        self.details_text.configure(state="disabled")

    def apply_theme(self, palette: dict[str, str]) -> None:
        super().apply_theme(palette)
        for card in (self.header_card, self.table_card, self.details_card):
            card.configure(fg_color=palette["panel"], border_color=palette["surface_soft"])

        self.title_label.configure(text_color=palette["text"])
        self.subtitle_label.configure(text_color=palette["muted"])
        self.table_title.configure(text_color=palette["text"])
        self.details_title.configure(text_color=palette["text"])
        self.details_text.configure(
            fg_color=palette["surface"],
            border_color=palette["surface_soft"],
            text_color=palette["text"],
        )


class CheckPage(BasePage):
    def __init__(
        self,
        master: ctk.CTkFrame,
        page_config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
        app_state: LinearSystemState,
    ) -> None:
        super().__init__(master, page_config, fonts)
        self.app_state = app_state

        self.grid_rowconfigure(1, weight=1)
        self._build_header()
        self._build_body()

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
            wraplength=1020,
            font=self.fonts["subtitle"],
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 14))

    def _build_body(self) -> None:
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.grid(row=1, column=0, sticky="nsew")
        self.body.grid_columnconfigure((0, 1), weight=1)
        self.body.grid_rowconfigure(1, weight=1)

        self.solution_card = ctk.CTkFrame(self.body, corner_radius=8, border_width=1)
        self.solution_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 14))
        self.solution_card.grid_columnconfigure(0, weight=1)
        self.solution_card.grid_rowconfigure(1, weight=1)

        self.residual_card = ctk.CTkFrame(self.body, corner_radius=8, border_width=1)
        self.residual_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 14))
        self.residual_card.grid_columnconfigure(0, weight=1)
        self.residual_card.grid_rowconfigure(1, weight=1)

        self.chart_card = ctk.CTkFrame(self.body, corner_radius=8, border_width=1)
        self.chart_card.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.chart_card.grid_columnconfigure(0, weight=1)
        self.chart_card.grid_rowconfigure(1, weight=1)

        self.solution_title = ctk.CTkLabel(
            self.solution_card,
            text="Вектор розв'язку",
            anchor="w",
            font=self.fonts["title_small"],
        )
        self.solution_title.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))

        self.solution_table_frame = tk.Frame(self.solution_card, bg=MAIN_THEME["panel"])
        self.solution_table_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.solution_table_frame.grid_columnconfigure(0, weight=1)
        self.solution_table_frame.grid_rowconfigure(0, weight=1)

        self.solution_table = ttk.Treeview(
            self.solution_table_frame,
            columns=("variable", "value", "rounded"),
            show="headings",
            height=7,
        )
        for column, title, width in (
            ("variable", "Змінна", 80),
            ("value", "Значення", 180),
            ("rounded", "До 4 знаків", 140),
        ):
            self.solution_table.heading(column, text=title)
            self.solution_table.column(column, width=width, anchor="center")
        self.solution_table.grid(row=0, column=0, sticky="nsew")

        self.residual_title = ctk.CTkLabel(
            self.residual_card,
            text="Нев'язки",
            anchor="w",
            font=self.fonts["title_small"],
        )
        self.residual_title.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))

        self.residual_table_frame = tk.Frame(self.residual_card, bg=MAIN_THEME["panel"])
        self.residual_table_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.residual_table_frame.grid_columnconfigure(0, weight=1)
        self.residual_table_frame.grid_rowconfigure(0, weight=1)

        self.residual_table = ttk.Treeview(
            self.residual_table_frame,
            columns=("row", "residual", "absolute"),
            show="headings",
            height=7,
        )
        for column, title, width in (
            ("row", "Рядок", 80),
            ("residual", "Ax - b", 180),
            ("absolute", "|r|", 140),
        ):
            self.residual_table.heading(column, text=title)
            self.residual_table.column(column, width=width, anchor="center")
        self.residual_table.grid(row=0, column=0, sticky="nsew")

        self.chart_title = ctk.CTkLabel(
            self.chart_card,
            text="Графік модулів нев'язки",
            anchor="w",
            font=self.fonts["title_small"],
        )
        self.chart_title.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))

        self.chart_canvas = tk.Canvas(
            self.chart_card,
            height=280,
            bg=MAIN_THEME["surface"],
            highlightthickness=0,
        )
        self.chart_canvas.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))

    def refresh(self) -> None:
        for table in (self.solution_table, self.residual_table):
            for item in table.get_children():
                table.delete(item)

        result = self.app_state.result
        if result is None:
            self._draw_empty_chart("Спочатку розв'яжи систему на сторінці «Система».")
            return

        for index, value in enumerate(result.solution, start=1):
            self.solution_table.insert(
                "",
                "end",
                values=(f"x{index}", f"{value:.10f}", f"{value:.4f}"),
            )

        for index, value in enumerate(result.residuals, start=1):
            self.residual_table.insert(
                "",
                "end",
                values=(f"R{index}", f"{value:.3e}", f"{abs(value):.3e}"),
            )

        self._draw_residual_chart(result.residuals)

    def _draw_empty_chart(self, text: str) -> None:
        palette = MAIN_THEME
        self.chart_canvas.delete("all")
        width = max(self.chart_canvas.winfo_width(), 720)
        height = max(self.chart_canvas.winfo_height(), 260)
        self.chart_canvas.create_rectangle(0, 0, width, height, fill=palette["surface"], outline="")
        self.chart_canvas.create_text(
            width / 2,
            height / 2,
            text=text,
            fill=palette["muted"],
            font=("Segoe UI", 13, "bold"),
        )

    def _draw_residual_chart(self, residuals: NumberVector) -> None:
        palette = MAIN_THEME
        self.chart_canvas.delete("all")
        width = max(self.chart_canvas.winfo_width(), 720)
        height = max(self.chart_canvas.winfo_height(), 260)
        left = 84
        right = 34
        top = 32
        bottom = 42
        plot_width = width - left - right
        plot_height = height - top - bottom

        self.chart_canvas.create_rectangle(0, 0, width, height, fill=palette["surface"], outline="")
        self.chart_canvas.create_rectangle(
            left,
            top,
            width - right,
            height - bottom,
            fill="#141414",
            outline=palette["surface_soft"],
        )

        magnitudes = [abs(value) for value in residuals]
        max_value = max(magnitudes + [1e-16])
        bar_count = len(magnitudes)
        if bar_count == 0:
            return

        slot_width = plot_width / bar_count
        for index, magnitude in enumerate(magnitudes):
            x_center = left + slot_width * index + slot_width / 2
            bar_width = min(72, slot_width * 0.48)
            normalized_height = (magnitude / max_value) * (plot_height - 24)
            y_top = height - bottom - normalized_height

            fill = palette["accent"] if magnitude <= 1e-8 else palette["warning"]
            if magnitude > 1e-5:
                fill = palette["error"]

            self.chart_canvas.create_rectangle(
                x_center - bar_width / 2,
                y_top,
                x_center + bar_width / 2,
                height - bottom,
                fill=fill,
                outline="",
            )
            self.chart_canvas.create_text(
                x_center,
                height - 20,
                text=f"r{index + 1}",
                fill=palette["muted"],
                font=("Segoe UI", 10, "bold"),
            )
            self.chart_canvas.create_text(
                x_center,
                max(top + 14, y_top - 12),
                text=f"{magnitude:.1e}",
                fill=palette["text"],
                font=("Segoe UI", 9),
            )

        self.chart_canvas.create_text(
            left,
            16,
            text=f"max |r| = {max_value:.3e}",
            fill=palette["text"],
            anchor="w",
            font=("Segoe UI", 11, "bold"),
        )

    def apply_theme(self, palette: dict[str, str]) -> None:
        super().apply_theme(palette)
        for card in (self.header_card, self.solution_card, self.residual_card, self.chart_card):
            card.configure(fg_color=palette["panel"], border_color=palette["surface_soft"])

        self.title_label.configure(text_color=palette["text"])
        self.subtitle_label.configure(text_color=palette["muted"])
        self.solution_title.configure(text_color=palette["text"])
        self.residual_title.configure(text_color=palette["text"])
        self.chart_title.configure(text_color=palette["text"])
        self.chart_canvas.configure(bg=palette["surface"])


class AlgorithmsApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.title("Gauss Pivot Lab")
        self.geometry("1180x820")
        self.minsize(1080, 760)

        self.current_page = "matrix"
        self.nav_buttons: dict[str, ctk.CTkButton] = {}
        self.pages: dict[str, BasePage] = {}
        self.app_state = LinearSystemState()

        self.fonts: dict[str, ctk.CTkFont] = {
            "title": ctk.CTkFont(family="Segoe UI", size=27, weight="bold"),
            "title_small": ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            "subtitle": ctk.CTkFont(family="Segoe UI", size=13),
            "label": ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            "body": ctk.CTkFont(family="Segoe UI", size=12),
            "button": ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            "result": ctk.CTkFont(family="Consolas", size=15, weight="bold"),
            "metric": ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            "nav": ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            "mono": ctk.CTkFont(family="Consolas", size=13),
        }

        self.page_configs: tuple[PageConfig, ...] = (
            PageConfig(
                page_id="matrix",
                nav_title="Система",
                title="Метод Гауса з вибором головного елемента",
                subtitle=(
                    "Редагуй коефіцієнти, завантажуй JSON і розв'язуй СЛАР з частковим "
                    "вибором головного елемента для стійкішого прямого ходу."
                ),
            ),
            PageConfig(
                page_id="steps",
                nav_title="Хід методу",
                title="Прямий хід та pivoting",
                subtitle="Кожен крок показує вибраний головний елемент, перестановку рядків та занулення.",
            ),
            PageConfig(
                page_id="check",
                nav_title="Перевірка",
                title="Контроль точності",
                subtitle="Вектор розв'язку, нев'язки Ax - b і швидка візуальна оцінка похибки.",
            ),
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._configure_treeview_style()
        self._build_topbar()
        self._build_pages()
        self._apply_theme()
        self.show_page(self.current_page)

    def _build_topbar(self) -> None:
        self.topbar = ctk.CTkFrame(self, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_columnconfigure(0, weight=1)

        self.brand_label = ctk.CTkLabel(
            self.topbar,
            text="SLAE Solver",
            font=self.fonts["title_small"],
            anchor="w",
        )
        self.brand_label.grid(row=0, column=0, sticky="w", padx=20, pady=(18, 12))

        self.nav_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.nav_frame.grid(row=0, column=1, sticky="e", padx=20, pady=(18, 12))

        for index, page in enumerate(self.page_configs):
            button = ctk.CTkButton(
                self.nav_frame,
                text=page.nav_title,
                width=132,
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
        self.page_host.grid_columnconfigure(0, weight=1)
        self.page_host.grid_rowconfigure(0, weight=1)

        matrix_page = MatrixPage(
            self.page_host,
            self.page_configs[0],
            self.fonts,
            self.app_state,
            self._notify_pages,
        )
        matrix_page.grid(row=0, column=0, sticky="nsew")
        self.pages["matrix"] = matrix_page

        steps_page = StepsPage(
            self.page_host,
            self.page_configs[1],
            self.fonts,
            self.app_state,
        )
        steps_page.grid(row=0, column=0, sticky="nsew")
        self.pages["steps"] = steps_page

        check_page = CheckPage(
            self.page_host,
            self.page_configs[2],
            self.fonts,
            self.app_state,
        )
        check_page.grid(row=0, column=0, sticky="nsew")
        self.pages["check"] = check_page

    def show_page(self, page_id: str) -> None:
        self.current_page = page_id
        self.pages[page_id].refresh()
        self.pages[page_id].tkraise()
        self._refresh_nav_buttons()

    def _notify_pages(self) -> None:
        for page_id, page in self.pages.items():
            if page_id != self.current_page:
                page.refresh()

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

    def _configure_treeview_style(self) -> None:
        palette = MAIN_THEME
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background=palette["surface"],
            foreground=palette["text"],
            fieldbackground=palette["surface"],
            rowheight=30,
            bordercolor=palette["surface_soft"],
            borderwidth=1,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=palette["panel_alt"],
            foreground=palette["text"],
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Treeview",
            background=[("selected", palette["segment_active"])],
            foreground=[("selected", palette["text"])],
        )

    def _apply_theme(self) -> None:
        palette = MAIN_THEME
        self.configure(fg_color=palette["bg"])
        self.topbar.configure(fg_color=palette["topbar"])
        self.brand_label.configure(text_color=palette["text"])
        self.page_host.configure(fg_color=palette["bg"])

        for page in self.pages.values():
            page.apply_theme(palette)
        self._refresh_nav_buttons()


def main() -> None:
    app = AlgorithmsApp()
    app.mainloop()

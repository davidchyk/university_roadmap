from __future__ import annotations

import json
import re
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog
from typing import Callable

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.radix_sort import radix_sort
from src.graph_build import build_actual_vs_theoretical_figure


MAIN_THEME: dict[str, str] = {
    "bg": "#000000",
    "topbar": "#000000",
    "panel": "#090909",
    "surface": "#111111",
    "surface_soft": "#1B1B1B",
    "text": "#F5F7FA",
    "muted": "#97A1AD",
    "accent": "#29A8FF",
    "accent_hover": "#44B4FF",
    "accent_text": "#06121B",
    "segment": "#131313",
    "segment_hover": "#1E1E1E",
    "segment_active": "#1F2D3C",
    "error": "#FF5B71",
}

INT_LIST_SPLIT_PATTERN = re.compile(r"[,\s]+")


@dataclass(frozen=True)
class PageConfig:
    page_id: str
    nav_title: str
    title: str
    subtitle: str


def parse_int_array(raw: str) -> list[int]:
    value = raw.strip()
    if not value:
        raise ValueError("Поле масиву не може бути порожнім")

    parts = [part for part in INT_LIST_SPLIT_PATTERN.split(value) if part]
    if not parts:
        raise ValueError("Не вдалося розпізнати жодного числа")

    try:
        return [int(part) for part in parts]
    except ValueError as exc:
        raise ValueError(
            "Масив має містити лише цілі числа, розділені пробілами або комами"
        ) from exc


class BasePage(ctk.CTkFrame):
    def __init__(
        self,
        master: ctk.CTkFrame,
        config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
    ) -> None:
        super().__init__(master, corner_radius=0)
        self.config_data = config
        self.fonts = fonts

        self.grid_columnconfigure(0, weight=1)

    def apply_theme(self, palette: dict[str, str]) -> None:
        self.configure(fg_color=palette["bg"])


class SortPage(BasePage):
    def __init__(
        self,
        master: ctk.CTkFrame,
        config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
        sort_func: Callable[[list[int]], tuple[list[int], int]],
    ) -> None:
        super().__init__(master, config, fonts)
        self.sort_func = sort_func

        self.result_var = tk.StringVar(value="Ready")
        self.error_var = tk.StringVar(value="")

        self._build_header()
        self._build_form()
        self._build_actions()
        self._build_output()

    def _build_header(self) -> None:
        self.header_card = ctk.CTkFrame(self, corner_radius=14, border_width=1)
        self.header_card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        self.header_card.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_card,
            text=self.config_data.title,
            anchor="w",
            font=self.fonts["title"],
        )
        self.title_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 4))

        self.subtitle_label = ctk.CTkLabel(
            self.header_card,
            text=self.config_data.subtitle,
            anchor="w",
            font=self.fonts["subtitle"],
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

    def _build_form(self) -> None:
        self.form_card = ctk.CTkFrame(self, corner_radius=14, border_width=1)
        self.form_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        self.form_card.grid_columnconfigure(0, weight=1)

        self.array_label = ctk.CTkLabel(
            self.form_card,
            text="Array:",
            anchor="w",
            font=self.fonts["label"],
        )
        self.array_label.grid(row=0, column=0, sticky="w", padx=20, pady=(14, 6))

        self.array_entry = ctk.CTkEntry(
            self.form_card,
            height=40,
            corner_radius=10,
            font=self.fonts["body"],
            placeholder_text="Наприклад: 170, 45, 75, 90, 802, 24, 2, 66",
        )
        self.array_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        self.hint_label = ctk.CTkLabel(
            self.form_card,
            text="Розділювачі: пробіл або кома.",
            anchor="w",
            font=self.fonts["body"],
        )
        self.hint_label.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 14))

    def _build_actions(self) -> None:
        self.actions = ctk.CTkFrame(self, fg_color="transparent")
        self.actions.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.actions.grid_columnconfigure((0, 1, 2), weight=1)

        self.compute_button = ctk.CTkButton(
            self.actions,
            text="Sort",
            height=40,
            corner_radius=11,
            font=self.fonts["button"],
            command=self.compute,
        )
        self.compute_button.grid(row=0, column=0, sticky="ew", padx=(0, 7))

        self.load_button = ctk.CTkButton(
            self.actions,
            text="Load JSON",
            height=40,
            corner_radius=11,
            font=self.fonts["button"],
            command=self.load_json,
        )
        self.load_button.grid(row=0, column=1, sticky="ew", padx=7)

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
        self.output_card.grid(row=3, column=0, sticky="ew")
        self.output_card.grid_columnconfigure(0, weight=1)

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
        self.error_label.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 14))

    def load_json(self) -> None:
        path = filedialog.askopenfilename(
            title="Select JSON file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            raw_data = Path(path).read_text(encoding="utf-8")
            loaded = json.loads(raw_data)

            if not isinstance(loaded, dict):
                raise ValueError("JSON root must be an object")

            if "array" not in loaded:
                raise ValueError("JSON must contain key 'array'")

            array_data = loaded["array"]

            if not isinstance(array_data, list):
                raise TypeError("'array' must be a list")

            if not all(isinstance(x, int) for x in array_data):
                raise TypeError("'array' must contain only integers")

            prepared = ", ".join(str(x) for x in array_data)

            self.array_entry.delete(0, tk.END)
            self.array_entry.insert(0, prepared)

            self.result_var.set("JSON loaded. Press Sort.")
            self.error_var.set("")
        except Exception as exc:
            self.result_var.set("No result")
            self.error_var.set(f"Error: {exc}")

    def compute(self) -> None:
        try:
            raw = self.array_entry.get()
            arr = parse_int_array(raw)
            sorted_arr, ops = self.sort_func(arr.copy())

            self.result_var.set(f"Sorted array: {sorted_arr}\nOperations: {ops}")
            self.error_var.set("")
        except Exception as exc:
            self.result_var.set("No result")
            self.error_var.set(f"Error: {exc}")

    def clear_all(self) -> None:
        self.array_entry.delete(0, tk.END)
        self.result_var.set("Ready")
        self.error_var.set("")

    def apply_theme(self, palette: dict[str, str]) -> None:
        super().apply_theme(palette)

        for card in (self.header_card, self.form_card, self.output_card):
            card.configure(
                fg_color=palette["panel"],
                border_color=palette["surface_soft"],
            )

        self.title_label.configure(text_color=palette["text"])
        self.subtitle_label.configure(text_color=palette["muted"])
        self.array_label.configure(text_color=palette["muted"])
        self.hint_label.configure(text_color=palette["muted"])

        self.array_entry.configure(
            fg_color=palette["surface"],
            border_color=palette["surface_soft"],
            text_color=palette["text"],
            placeholder_text_color=palette["muted"],
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
        self.clear_button.configure(
            fg_color=palette["segment"],
            hover_color=palette["segment_hover"],
            text_color=palette["text"],
        )

        self.result_title.configure(text_color=palette["muted"])
        self.result_label.configure(text_color=palette["text"])
        self.error_label.configure(text_color=palette["error"])


class GraphPage(BasePage):
    def __init__(
        self,
        master: ctk.CTkFrame,
        config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
        graph_func: Callable[[Callable[[list[int]], tuple[list[int], int]]], Figure],
        sort_func: Callable[[list[int]], tuple[list[int], int]],
    ) -> None:
        super().__init__(master, config, fonts)
        self.graph_func = graph_func
        self.sort_func = sort_func

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
            text=self.config_data.title,
            anchor="w",
            font=self.fonts["title"],
        )
        self.title_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 4))

        self.subtitle_label = ctk.CTkLabel(
            self.header_card,
            text=self.config_data.subtitle,
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
                "Побудова графіка фактичної кількості операцій "
                "та теоретичної залежності Radix Sort."
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
            self.status_var.set("Building graph...")
            self.error_var.set("")
            self.update_idletasks()

            fig = self.graph_func(self.sort_func)

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

        self.title("RadixSortApp")
        self.resizable(False, False)
        self.geometry("720x900")

        self.current_page = "sort"
        self.nav_buttons: dict[str, ctk.CTkButton] = {}
        self.pages: dict[str, BasePage] = {}

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
                page_id="sort",
                nav_title="Sort",
                title="Radix Sort",
                subtitle="Сортування масиву цілих чисел та підрахунок кількості операцій",
            ),
            PageConfig(
                page_id="graph",
                nav_title="Graph",
                title="Radix Sort Graph",
                subtitle="Порівняння фактичної та теоретичної залежностей",
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

        sort_page = SortPage(
            self.page_host,
            self.page_configs[0],
            self.fonts,
            radix_sort,
        )
        sort_page.grid(row=0, column=0, sticky="nsew")
        self.pages["sort"] = sort_page

        graph_page = GraphPage(
            self.page_host,
            self.page_configs[1],
            self.fonts,
            build_actual_vs_theoretical_figure,
            radix_sort,
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


if __name__ == "__main__":
    main()
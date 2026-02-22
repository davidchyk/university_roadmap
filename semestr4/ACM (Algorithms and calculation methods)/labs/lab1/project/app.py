from __future__ import annotations

import json
import re
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog
from typing import Callable

import customtkinter as ctk

from src.branched_alg import branched_alg
from src.cyclic_alg import cyclic_alg
from src.linear_alg import linear_alg

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

INT_PATTERN = re.compile(r"^[+-]?\d+$")
EPSILON = 1e-12

@dataclass(frozen=True)
class PageConfig:
    page_id: str
    nav_title: str
    title: str
    subtitle: str
    fields: tuple[str, ...]
    parser: Callable[[dict[str, str]], dict[str, object]]
    compute: Callable[..., object]


def parse_complex_fields(raw_values: dict[str, str]) -> dict[str, complex]:
    parsed: dict[str, complex] = {}
    for key, raw in raw_values.items():
        value = raw.strip()
        if not value:
            raise ValueError(f"'{key}' is required")

        try:
            parsed[key] = complex(value)
        except ValueError as exc:
            raise ValueError(
                f"'{key}' must be a complex-compatible string (examples: '1', '2.5', '1+2j')"
            ) from exc
    return parsed


def parse_cyclic_fields(raw_values: dict[str, str]) -> dict[str, int]:
    parsed: dict[str, int] = {}
    for key in ("n", "p"):
        raw = raw_values[key].strip()
        if not raw:
            raise ValueError(f"'{key}' is required")
        if not INT_PATTERN.fullmatch(raw):
            raise TypeError(f"'{key}' must be an integer string (for example: '0', '5', '12')")

        value = int(raw)
        if value < 0:
            raise ValueError(f"'{key}' must be >= 0")
        parsed[key] = value
    return parsed


def _normalize_zero(value: float) -> float:
    return 0.0 if abs(value) < EPSILON else value


def _format_real(value: float) -> str:
    normalized = _normalize_zero(value)
    if float(normalized).is_integer():
        return str(int(normalized))
    return f"{normalized:.12g}"


def format_output_value(value: object) -> str:
    if isinstance(value, complex):
        real = _normalize_zero(float(value.real))
        imag = _normalize_zero(float(value.imag))

        if imag == 0.0:
            return _format_real(real)

        sign = "+" if imag >= 0 else "-"
        return f"{_format_real(real)} {sign} {_format_real(abs(imag))}j"

    if isinstance(value, float):
        return _format_real(value)

    return str(value)


class AlgorithmPage(ctk.CTkFrame):
    def __init__(
        self,
        master: ctk.CTkFrame,
        config: PageConfig,
        fonts: dict[str, ctk.CTkFont],
    ) -> None:
        super().__init__(master, corner_radius=0)
        self.config_data = config
        self.fonts = fonts
        self.entries: dict[str, ctk.CTkEntry] = {}
        self.field_labels: list[ctk.CTkLabel] = []
        self.result_var = tk.StringVar(value="Ready")
        self.error_var = tk.StringVar(value="")

        self.grid_columnconfigure(0, weight=1)

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
        self.form_card.grid_columnconfigure(1, weight=1)

        for row, field_name in enumerate(self.config_data.fields):
            label = ctk.CTkLabel(
                self.form_card,
                text=f"{field_name}:",
                width=42,
                anchor="w",
                font=self.fonts["label"],
            )
            label.grid(row=row, column=0, sticky="w", padx=(20, 12), pady=9)
            self.field_labels.append(label)

            entry = ctk.CTkEntry(
                self.form_card,
                height=38,
                corner_radius=10,
                font=self.fonts["body"],
            )
            entry.grid(row=row, column=1, sticky="ew", padx=(0, 20), pady=9)
            self.entries[field_name] = entry

    def _build_actions(self) -> None:
        self.actions = ctk.CTkFrame(self, fg_color="transparent")
        self.actions.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.actions.grid_columnconfigure((0, 1), weight=1)

        self.compute_button = ctk.CTkButton(
            self.actions,
            text="Compute",
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
        self.load_button.grid(row=0, column=1, sticky="ew", padx=(7, 0))

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
        self.result_title.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 4))

        self.result_label = ctk.CTkLabel(
            self.output_card,
            textvariable=self.result_var,
            anchor="w",
            font=self.fonts["result"],
        )
        self.result_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 6))

        self.error_label = ctk.CTkLabel(
            self.output_card,
            textvariable=self.error_var,
            anchor="w",
            justify="left",
            wraplength=860,
            font=self.fonts["body"],
        )
        self.error_label.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 14))

    def apply_theme(self, palette: dict[str, str]) -> None:
        self.configure(fg_color=palette["bg"])

        for card in (self.header_card, self.form_card, self.output_card):
            card.configure(
                fg_color=palette["panel"],
                border_color=palette["surface_soft"],
            )

        self.title_label.configure(text_color=palette["text"])
        self.subtitle_label.configure(text_color=palette["muted"])

        for label in self.field_labels:
            label.configure(text_color=palette["muted"])

        for entry in self.entries.values():
            entry.configure(
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

        self.result_title.configure(text_color=palette["muted"])
        self.result_label.configure(text_color=palette["text"])
        self.error_label.configure(text_color=palette["error"])

    def _collect_raw_values(self) -> dict[str, str]:
        return {key: entry.get() for key, entry in self.entries.items()}

    def _show_result(self, value: object) -> None:
        self.result_var.set(format_output_value(value))
        self.error_var.set("")

    def _show_error(self, error: Exception | str) -> None:
        self.result_var.set("No result")
        self.error_var.set(f"Error: {error}")

    def _set_entries_from_dict(self, values: dict[str, str]) -> None:
        for key, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, values[key])

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

            expected_keys = set(self.config_data.fields)
            actual_keys = set(loaded.keys())
            if actual_keys != expected_keys:
                raise ValueError(f"Expected keys exactly: {sorted(expected_keys)}")

            for key in self.config_data.fields:
                if not isinstance(loaded[key], str):
                    raise TypeError(f"JSON value for '{key}' must be a string")

            prepared = {key: loaded[key] for key in self.config_data.fields}
            self._set_entries_from_dict(prepared)
            self.error_var.set("")
            self.result_var.set("JSON loaded. Press Compute.")
        except Exception as exc:
            self._show_error(exc)

    def compute(self) -> None:
        try:
            raw_values = self._collect_raw_values()
            parsed = self.config_data.parser(raw_values)
            result = self.config_data.compute(**parsed)
            self._show_result(result)
        except Exception as exc:
            self._show_error(exc)


class AlgorithmsApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")

        self.title("AlgorithmsDemoApp")
        self.resizable(False, False)
        self.geometry("100x500")
        self.minsize(780, 680)

        self.current_page = "linear_alg"
        self.nav_buttons: dict[str, ctk.CTkButton] = {}
        self.pages: dict[str, AlgorithmPage] = {}

        self.fonts: dict[str, ctk.CTkFont] = {
            "title": ctk.CTkFont(family="Segoe UI", size=27, weight="bold"),
            "subtitle": ctk.CTkFont(family="Segoe UI", size=13),
            "label": ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            "body": ctk.CTkFont(family="Segoe UI", size=12),
            "button": ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            "result": ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            "nav": ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        }

        self.page_configs: tuple[PageConfig, ...] = (
            PageConfig(
                page_id="linear_alg",
                nav_title="Linear",
                title="Linear Algorithm",
                subtitle="Y1 = (d*a)^b + (b*c)^(1/d)",
                fields=("a", "b", "c", "d"),
                parser=parse_complex_fields,
                compute=linear_alg,
            ),
            PageConfig(
                page_id="branched_alg",
                nav_title="Branched",
                title="Branched Algorithm",
                subtitle="y = (4*r - r*x) / (4*x - r*x)",
                fields=("r", "x"),
                parser=parse_complex_fields,
                compute=branched_alg,
            ),
            PageConfig(
                page_id="cyclic_alg",
                nav_title="Cyclic",
                title="Cyclic Algorithm",
                subtitle="f = sum(a^b + b^a), for a in [0..n], b in [0..p]",
                fields=("n", "p"),
                parser=parse_cyclic_fields,
                compute=cyclic_alg,
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

        for config in self.page_configs:
            page = AlgorithmPage(self.page_host, config, self.fonts)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[config.page_id] = page

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
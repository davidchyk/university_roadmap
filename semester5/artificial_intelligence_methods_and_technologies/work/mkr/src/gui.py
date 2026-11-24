"""Tkinter GUI for automatic genetic structural synthesis."""

from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from mkr_core import compile_safe_expression, make_grid, split_dataset
from structure_search import StructureConfig, search_architecture


class StructuralSynthesisApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Структурний синтез нейронної мережі")
        root.geometry("760x520")
        root.minsize(720, 480)
        self.events: queue.Queue = queue.Queue()
        self.fields = {}
        self._build()
        self.root.after(150, self._poll)

    def _entry(self, parent, row, label, default):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=8, pady=6)
        value = tk.StringVar(value=str(default))
        ttk.Entry(parent, textvariable=value, width=30).grid(row=row, column=1, sticky="ew", padx=8, pady=6)
        self.fields[label] = value

    def _build(self):
        frame = ttk.LabelFrame(self.root, text="Вхідні параметри")
        frame.pack(fill="x", padx=14, pady=12)
        frame.columnconfigure(1, weight=1)
        values = [
            ("Функція", "x*sin(abs(y))"),
            ("x мінімум", 0), ("x максимум", 1),
            ("y мінімум", 0), ("y максимум", 1),
            ("Максимум прихованих нейронів", 24),
            ("Максимальна MSE", 0.008),
            ("Популяція структур", 8),
            ("Покоління структур", 8),
        ]
        for row, (label, default) in enumerate(values):
            self._entry(frame, row, label, default)
        self.start_button = ttk.Button(self.root, text="Почати структурний синтез", command=self.start)
        self.start_button.pack(pady=6)
        self.status = tk.StringVar(value="Готово до запуску")
        ttk.Label(self.root, textvariable=self.status, font=("Sans", 11, "bold")).pack(pady=6)
        self.result = tk.Text(self.root, height=5, wrap="word")
        self.result.pack(fill="both", expand=True, padx=14, pady=10)

    def _create_progress_window(self, config):
        self.progress = tk.Toplevel(self.root)
        self.progress.title("Параметри та проміжні результати ГА")
        self.progress.geometry("660x420")
        text = (
            f"Популяція структур: {config.population_size}; покоління: {config.generations}; "
            f"максимум нейронів: {config.max_total_neurons}; цільова MSE: {config.target_mse}"
        )
        ttk.Label(self.progress, text=text, wraplength=620).pack(anchor="w", padx=12, pady=10)
        self.tree = ttk.Treeview(self.progress, columns=("generation", "architecture", "mse"), show="headings")
        self.tree.heading("generation", text="Покоління")
        self.tree.heading("architecture", text="Найкраща структура")
        self.tree.heading("mse", text="MSE")
        self.tree.column("generation", width=90, anchor="center")
        self.tree.column("architecture", width=300, anchor="center")
        self.tree.column("mse", width=160, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=12, pady=10)

    def start(self):
        try:
            function = compile_safe_expression(self.fields["Функція"].get())
            x_interval = (float(self.fields["x мінімум"].get()), float(self.fields["x максимум"].get()))
            y_interval = (float(self.fields["y мінімум"].get()), float(self.fields["y максимум"].get()))
            config = StructureConfig(
                max_total_neurons=int(self.fields["Максимум прихованих нейронів"].get()),
                target_mse=float(self.fields["Максимальна MSE"].get()),
                population_size=int(self.fields["Популяція структур"].get()),
                generations=int(self.fields["Покоління структур"].get()),
            )
        except Exception as error:
            messagebox.showerror("Помилка параметрів", str(error))
            return
        self.start_button.configure(state="disabled")
        self.status.set("Виконується пошук...")
        self.result.delete("1.0", "end")
        self._create_progress_window(config)

        def worker():
            try:
                inputs, targets, _, _ = make_grid(x_interval, y_interval, points=15, function=function)
                train_x, train_y, test_x, test_y = split_dataset(inputs, targets)
                result = search_architecture(
                    train_x,
                    train_y,
                    test_x,
                    test_y,
                    config,
                    callback=lambda generation, architecture, mse: self.events.put(
                        ("progress", generation, architecture, mse)
                    ),
                )
                self.events.put(("done", result))
            except Exception as error:
                self.events.put(("error", str(error)))

        threading.Thread(target=worker, daemon=True).start()

    def _poll(self):
        try:
            while True:
                event = self.events.get_nowait()
                if event[0] == "progress":
                    _, generation, architecture, mse = event
                    self.tree.insert("", "end", values=(generation, "-".join(map(str, architecture)), f"{mse:.6g}"))
                    self.status.set(f"Покоління {generation}: MSE={mse:.6g}")
                elif event[0] == "done":
                    result = event[1]
                    architecture = "-".join(map(str, result["architecture"]))
                    self.result.insert("end", f"Отримана структура: {architecture}\nПохибка MSE: {result['mse']:.8f}\n")
                    self.status.set("Пошук завершено")
                    self.start_button.configure(state="normal")
                elif event[0] == "error":
                    messagebox.showerror("Помилка виконання", event[1])
                    self.status.set("Пошук завершився з помилкою")
                    self.start_button.configure(state="normal")
        except queue.Empty:
            pass
        self.root.after(150, self._poll)


def main():
    root = tk.Tk()
    StructuralSynthesisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

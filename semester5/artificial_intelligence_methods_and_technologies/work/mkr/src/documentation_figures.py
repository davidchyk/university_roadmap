"""Generate explanatory figures used in the report."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def architecture_figure():
    architecture = [2, 4, 8, 10, 6, 6, 1]
    x_positions = np.arange(len(architecture))
    figure, axes = plt.subplots(figsize=(11, 4.8))
    for layer, (x_position, neurons) in enumerate(zip(x_positions, architecture)):
        shown = min(neurons, 10)
        y_positions = np.linspace(-1, 1, shown) if shown > 1 else np.array([0.0])
        if layer < len(architecture) - 1:
            next_shown = min(architecture[layer + 1], 10)
            next_y = np.linspace(-1, 1, next_shown) if next_shown > 1 else np.array([0.0])
            for y_start in y_positions:
                for y_end in next_y:
                    axes.plot([x_position, x_position + 1], [y_start, y_end], color="#aab4c0", linewidth=0.35, alpha=0.42)
        axes.scatter(np.full(shown, x_position), y_positions, s=120, color="#3465a4", edgecolor="white", zorder=3)
        axes.text(x_position, -1.33, str(neurons), ha="center", fontsize=11, fontweight="bold")
    axes.set_xticks(x_positions, ["Вхід", "H1", "H2", "H3", "H4", "H5", "Вихід"])
    axes.set_title("Архітектура нейронної мережі 2-4-8-10-6-6-1")
    axes.text(3, 1.28, "257 ваг і зміщень = 257 генів хромосоми", ha="center", fontsize=11)
    axes.set_xlim(-0.4, 6.4)
    axes.set_ylim(-1.55, 1.5)
    axes.axis("off")
    figure.tight_layout()
    figure.savefig(RESULTS / "architecture.png", dpi=190, bbox_inches="tight")
    plt.close(figure)


def gui_preview():
    figure, axes = plt.subplots(figsize=(9.3, 5.6))
    axes.set_xlim(0, 10)
    axes.set_ylim(0, 7)
    axes.axis("off")
    panel = FancyBboxPatch((0.3, 0.3), 9.4, 6.4, boxstyle="round,pad=0.08", facecolor="#f4f6f8", edgecolor="#6d7785")
    axes.add_patch(panel)
    axes.text(0.65, 6.3, "Структурний синтез нейронної мережі", fontsize=14, fontweight="bold")
    labels = [
        ("Функція", "x*sin(abs(y))"),
        ("Інтервали", "x: 0...1; y: 0...1"),
        ("Максимум нейронів", "24"),
        ("Максимальна MSE", "0.008"),
        ("Параметри ГА", "8 структур, 8 поколінь"),
    ]
    for index, (label, value) in enumerate(labels):
        y = 5.65 - index * 0.78
        axes.text(0.75, y, label, va="center", fontsize=10)
        field = FancyBboxPatch((3.25, y - 0.25), 3.2, 0.5, boxstyle="round,pad=0.03", facecolor="white", edgecolor="#b7bec7")
        axes.add_patch(field)
        axes.text(3.43, y, value, va="center", fontsize=10)
    button = FancyBboxPatch((3.25, 1.25), 3.2, 0.65, boxstyle="round,pad=0.05", facecolor="#3465a4", edgecolor="#294f82")
    axes.add_patch(button)
    axes.text(4.85, 1.57, "Почати структурний синтез", ha="center", va="center", color="white", fontweight="bold")
    axes.text(7.0, 5.65, "Проміжні результати", fontweight="bold", fontsize=11)
    axes.text(7.0, 5.15, "Покоління 1   2-14-1   0.00384", fontsize=9)
    axes.text(7.0, 4.75, "Покоління 2   2-16-1   0.00195", fontsize=9)
    axes.text(7.0, 3.9, "Результат", fontweight="bold", fontsize=11)
    axes.text(7.0, 3.45, "Структура: 2-16-1", fontsize=10)
    axes.text(7.0, 3.05, "MSE: 0.0019517", fontsize=10)
    figure.tight_layout()
    figure.savefig(RESULTS / "gui_preview.png", dpi=190, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    architecture_figure()
    gui_preview()

"""可视化通用工具：Matplotlib 主题、Tkinter 嵌入、导出等"""

import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


# 使用一致的中文/学校主题
matplotlib.rcParams.update(
    {
        "font.sans-serif": ["SimHei", "Microsoft YaHei", "Arial"],
        "axes.unicode_minus": False,
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "axes.edgecolor": "#EEEEEE",
        "axes.grid": True,
        "grid.color": "#E0E0E0",
    }
)


def create_figure(figsize=(6, 4)) -> Figure:
    """创建统一风格的 Matplotlib Figure"""
    fig = Figure(figsize=figsize, dpi=100)
    return fig


def embed_figure_in_toplevel(
    parent: tk.Tk | tk.Toplevel,
    title: str,
    figure: Figure,
    modal: bool = False,
) -> tk.Toplevel:
    """在新的 Toplevel 窗口中嵌入一个 Figure 并返回窗口对象。

    由调用方决定是否保存窗口引用/是否阻塞。
    """
    win = tk.Toplevel(parent)
    win.title(title)
    win.geometry("800x600")

    frame = tk.Frame(win)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = FigureCanvasTkAgg(figure, master=frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar_frame = tk.Frame(frame)
    toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
    NavigationToolbar2Tk(canvas, toolbar_frame)

    if modal:
        win.transient(parent)
        win.grab_set()

    return win


def export_figure_as_image(figure: Figure, parent: Optional[tk.Tk | tk.Toplevel] = None):
    """导出当前图像为 PNG 文件"""
    file_path = filedialog.asksaveasfilename(
        parent=parent,
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
        title="导出图表为图片",
    )
    if not file_path:
        return

    try:
        figure.savefig(file_path, bbox_inches="tight")
        messagebox.showinfo("成功", f"图表已导出到: {file_path}")
    except Exception as e:
        messagebox.showerror("错误", f"导出失败: {e}")


def validate_numeric_series(values, field_name: str = "数值"):
    """简单的数据校验：保证序列中至少有一个有效数字。"""
    nums = [v for v in values if isinstance(v, (int, float))]
    if not nums:
        raise ValueError(f"{field_name}数据为空或无有效数值，无法生成图表。")
    return nums

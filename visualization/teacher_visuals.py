"""教师可视化图表实现"""

from typing import List, Dict, Any

import math
import matplotlib.pyplot as plt

from .visual_utils import create_figure, embed_figure_in_toplevel, validate_numeric_series


def show_course_grade_histogram(parent, grades: List[Dict[str, Any]], course_name: str = "课程"):
    """对某门课程的总评成绩绘制直方图/柱状图。

    grades: 每个元素包含至少 {"final_score": float, "student_id": str, "name": str}
    """
    if not grades:
        raise ValueError("该课程暂无成绩数据，无法生成图表。")

    scores = [g.get("final_score") for g in grades if g.get("final_score") is not None]
    validate_numeric_series(scores, "课程成绩")

    fig = create_figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    ax.hist(scores, bins=10, color="#2196F3", edgecolor="white", alpha=0.85)
    ax.set_title(f"{course_name} 成绩分布")
    ax.set_xlabel("成绩")
    ax.set_ylabel("人数")

    fig.tight_layout()
    embed_figure_in_toplevel(parent, f"{course_name} 成绩直方图", fig)


def show_attendance_vs_score(parent, records: List[Dict[str, Any]], course_name: str = "课程"):
    """成绩 + 出勤率散点图。

    records: 每个元素示例：
        {
            "student_id": "2024001",
            "name": "张三",
            "attendance_rate": 0.92,  # 0-1 之间
            "final_score": 85.0,
        }
    """
    if not records:
        raise ValueError("暂无出勤与成绩数据，无法生成散点图。")

    x = [r.get("attendance_rate") for r in records if r.get("attendance_rate") is not None and r.get("final_score") is not None]
    y = [r.get("final_score") for r in records if r.get("attendance_rate") is not None and r.get("final_score") is not None]

    validate_numeric_series(x, "出勤率")
    validate_numeric_series(y, "成绩")

    fig = create_figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    ax.scatter(x, y, c="#2196F3", alpha=0.7, edgecolors="white")
    ax.set_xlabel("出勤率")
    ax.set_ylabel("总评成绩")
    ax.set_title(f"{course_name} 出勤率与成绩关系")

    # 简单拟合一条趋势线（线性回归）
    try:
        import numpy as np

        arr_x = np.array(x)
        arr_y = np.array(y)
        k, b = np.polyfit(arr_x, arr_y, 1)
        xs = np.linspace(min(arr_x), max(arr_x), 50)
        ys = k * xs + b
        ax.plot(xs, ys, color="#FF5722", linestyle="--", label="趋势线")
        ax.legend(loc="best")
    except Exception:
        # 回归失败时忽略趋势线，不影响主图
        pass

    fig.tight_layout()
    embed_figure_in_toplevel(parent, f"{course_name} 出勤-成绩散点图", fig)


def show_course_knowledge_radar(parent, knowledge_stats: List[Dict[str, Any]], course_name: str = "课程"):
    """单课程知识点掌握雷达图。

    knowledge_stats: 形如：
        [
            {"name": "导数", "avg_score": 78},
            {"name": "积分", "avg_score": 65},
            ...
        ]
    """
    if not knowledge_stats:
        raise ValueError("暂无知识点统计数据，无法生成雷达图。")

    labels = [k.get("name") or "未命名" for k in knowledge_stats]
    scores = [float(k.get("avg_score", 0)) for k in knowledge_stats]
    validate_numeric_series(scores, "知识点得分")

    values = scores + scores[:1]
    angles = [n / float(len(labels)) * 2 * math.pi for n in range(len(labels))]
    angles += angles[:1]

    fig = create_figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)

    ax.plot(angles, values, linewidth=2, color="#9C27B0")
    ax.fill(angles, values, alpha=0.25, color="#9C27B0")

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title(f"{course_name} 知识点掌握情况雷达图")

    ax.set_ylim(0, 100)

    fig.tight_layout()
    embed_figure_in_toplevel(parent, f"{course_name} 知识点雷达图", fig)

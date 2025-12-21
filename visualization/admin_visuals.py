"""管理员可视化图表实现"""

from typing import Dict, Any, List

import numpy as np
import matplotlib.pyplot as plt

from .visual_utils import create_figure, embed_figure_in_toplevel, validate_numeric_series


def show_grade_distribution_bar(parent, distribution: Dict[str, int]):
    """根据管理员端已有的成绩分布数据绘制柱状图。

    distribution: {等级: 人数}
    """
    if not distribution:
        raise ValueError("成绩分布数据为空，无法绘制图表。")

    labels = list(distribution.keys())
    values = [int(distribution[k]) for k in labels]
    validate_numeric_series(values, "成绩分布人数")

    fig = create_figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    bars = ax.bar(labels, values, color=["#4CAF50", "#2196F3", "#FF9800", "#FFC107", "#f44336"][: len(labels)])
    ax.set_title("全校成绩等级分布")
    ax.set_ylabel("人数")

    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, str(value), ha="center", va="bottom", fontsize=9)

    fig.tight_layout()

    embed_figure_in_toplevel(parent, "成绩分布柱状图", fig)


def show_statistics_overview(parent, stats: Dict[str, Any]):
    """一个简单示例：展示学生、教师、课程数量的对比柱状图。"""
    labels = ["学生", "教师", "课程"]
    values = [
        int(stats.get("total_students", 0) or 0),
        int(stats.get("total_teachers", 0) or 0),
        int(stats.get("total_courses", 0) or 0),
    ]

    validate_numeric_series(values, "统计数量")

    fig = create_figure(figsize=(5, 4))
    ax = fig.add_subplot(111)
    bars = ax.bar(labels, values, color=["#4CAF50", "#2196F3", "#FF9800"])
    ax.set_title("全校基础统计概览")
    ax.set_ylabel("数量")

    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, str(value), ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    embed_figure_in_toplevel(parent, "基础统计柱状图", fig)


def show_resource_heatmap(parent, courses: List[Dict[str, Any]]):
    if not courses:
        raise ValueError("暂无课程数据，无法生成资源利用率热力图。")

    classrooms = sorted({c.get("classroom") for c in courses if c.get("classroom")})
    timeslots = sorted({c.get("class_time") for c in courses if c.get("class_time")})

    if not classrooms or not timeslots:
        raise ValueError("课程中缺少教室或时间信息，无法生成热力图。")

    room_index = {room: i for i, room in enumerate(classrooms)}
    time_index = {t: j for j, t in enumerate(timeslots)}

    matrix = np.zeros((len(classrooms), len(timeslots)))

    for c in courses:
        room = c.get("classroom")
        time = c.get("class_time")
        if not room or not time:
            continue
        enrolled = c.get("enrolled_count") or 0
        capacity = c.get("capacity") or 1
        utilization = min(float(enrolled) / float(capacity), 1.0)
        i = room_index[room]
        j = time_index[time]
        matrix[i, j] = max(matrix[i, j], utilization)

    fig = create_figure(figsize=(7, 5))
    ax = fig.add_subplot(111)

    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto", vmin=0, vmax=1)

    ax.set_xticks(range(len(timeslots)))
    ax.set_xticklabels(timeslots, rotation=45, ha="right")
    ax.set_yticks(range(len(classrooms)))
    ax.set_yticklabels(classrooms)

    ax.set_xlabel("时间段")
    ax.set_ylabel("教室/实验室")
    ax.set_title("教室资源利用率热力图")

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="利用率")

    fig.tight_layout()
    embed_figure_in_toplevel(parent, "资源利用率热力图", fig)


def show_grouped_grade_boxplot(parent, grouped_scores: Dict[str, List[float]], title: str = "成绩分布箱线图"):
    """按学院/专业分组的成绩箱线图。

    grouped_scores: 形如 {"计算机学院": [80, 90, 75, ...], "机械学院": [...]} 或
                    {"软件工程": [...], "网络工程": [...]}。
    """
    if not grouped_scores:
        raise ValueError("暂无分组成绩数据，无法生成箱线图。")

    labels = list(grouped_scores.keys())
    data = [grouped_scores[k] for k in labels]

    # 确保每个分组都有至少一个数值
    flat = []
    for arr in data:
        flat.extend(v for v in arr if isinstance(v, (int, float)))
    validate_numeric_series(flat, "成绩")

    fig = create_figure(figsize=(8, 5))
    ax = fig.add_subplot(111)

    bp = ax.boxplot(data, labels=labels, patch_artist=True)

    colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#009688"]
    for patch, color in zip(bp["boxes"], colors * (len(labels) // len(colors) + 1)):
        patch.set_facecolor(color)
        patch.set_alpha(0.4)

    ax.set_ylabel("成绩")
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    embed_figure_in_toplevel(parent, "分组成绩箱线图", fig)


def show_student_risk_trend(parent, timeline: List[Dict[str, Any]]):
    """学生流失/预警趋势堆叠面积图。

    timeline: 时间序列数据，例如：
        [
            {"term": "2023-秋", "warn": 10, "absence": 5, "drop": 1},
            {"term": "2024-春", "warn": 8,  "absence": 3, "drop": 2},
            ...
        ]
    """
    if not timeline:
        raise ValueError("暂无学生预警/流失数据，无法生成趋势图。")

    terms = [item.get("term") or "" for item in timeline]
    warn = [int(item.get("warn", 0) or 0) for item in timeline]
    absence = [int(item.get("absence", 0) or 0) for item in timeline]
    drop = [int(item.get("drop", 0) or 0) for item in timeline]

    total = [w + a + d for w, a, d in zip(warn, absence, drop)]
    validate_numeric_series(total, "人数")

    fig = create_figure(figsize=(8, 4))
    ax = fig.add_subplot(111)

    x = np.arange(len(terms))
    ax.stackplot(
        x,
        warn,
        absence,
        drop,
        labels=["学业预警", "缺勤预警", "退学/休学"],
        colors=["#FFC107", "#03A9F4", "#F44336"],
        alpha=0.8,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(terms, rotation=30, ha="right")
    ax.set_ylabel("人数")
    ax.set_title("学生预警与流失趋势")
    ax.legend(loc="upper left")

    fig.tight_layout()
    embed_figure_in_toplevel(parent, "学生流失趋势堆叠图", fig)


def show_grade_class_overview(parent, grade: str, class_stats: List[Dict[str, Any]]):
    """按年级展示各班级的平均成绩和挂科率等柱状图。

    class_stats: 形如 [{
        "class_name": str,
        "major": str,
        "student_count": int,
        "avg_score": float,
        "fail_rate": float,
        "excellent_rate": float,
        "good_rate": float,
    }, ...]
    """
    if not class_stats:
        raise ValueError("暂无班级统计数据，无法生成图表。")

    labels = [item.get("class_name", "") for item in class_stats]
    avg_scores = [float(item.get("avg_score") or 0) for item in class_stats]
    fail_rates = [float(item.get("fail_rate") or 0) * 100 for item in class_stats]

    validate_numeric_series(avg_scores, "平均成绩")

    x = np.arange(len(labels))
    width = 0.35

    fig = create_figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)

    bars1 = ax1.bar(x - width / 2, avg_scores, width, label="平均成绩", color="#4CAF50")
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width / 2, fail_rates, width, label="挂科率(%)", color="#f44336")

    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha="right")
    ax1.set_ylabel("平均成绩")
    ax2.set_ylabel("挂科率(%)")
    ax1.set_title(f"{grade} 级各班级成绩与挂科率概览")

    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}", ha="center", va="bottom", fontsize=8)

    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}", ha="center", va="bottom", fontsize=8, color="#f44336")

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper right")

    fig.tight_layout()
    embed_figure_in_toplevel(parent, "年级-班级成绩概览", fig)


def show_course_teacher_overview(
    parent,
    course_name: str,
    teacher_name: str,
    overall: Dict[str, Any],
    class_stats: List[Dict[str, Any]],
):
    """课程-教师维度的班级成绩与挂科率柱状图。"""
    if not class_stats:
        raise ValueError("暂无班级统计数据，无法生成图表。")

    labels = [item.get("class_name", "") for item in class_stats]
    avg_scores = [float(item.get("avg_score") or 0) for item in class_stats]
    fail_rates = [float(item.get("fail_rate") or 0) * 100 for item in class_stats]

    validate_numeric_series(avg_scores, "平均成绩")

    x = np.arange(len(labels))
    width = 0.35

    fig = create_figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)

    bars1 = ax1.bar(x - width / 2, avg_scores, width, label="平均成绩", color="#2196F3")
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width / 2, fail_rates, width, label="挂科率(%)", color="#FF5722")

    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha="right")
    ax1.set_ylabel("平均成绩")
    ax2.set_ylabel("挂科率(%)")

    title = f"{course_name} - {teacher_name} 班级成绩与挂科率"
    ax1.set_title(title)

    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}", ha="center", va="bottom", fontsize=8)

    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}", ha="center", va="bottom", fontsize=8, color="#FF5722")

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper right")

    fig.tight_layout()
    embed_figure_in_toplevel(parent, "课程-教师班级成绩概览", fig)


def show_major_rank_bar(parent, grade: str, major: str, ranking: List[Dict[str, Any]], top_n: int = 50):
    """按年级+专业展示学生加权平均成绩排名（前 top_n）条形图。"""
    if not ranking:
        raise ValueError("暂无排名数据，无法生成图表。")

    data = ranking[:top_n]
    labels = [item.get("student_id", "") for item in data]
    avg_scores = [float(item.get("avg_score") or 0) for item in data]

    validate_numeric_series(avg_scores, "平均成绩")

    x = np.arange(len(labels))

    fig = create_figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    bars = ax.bar(x, avg_scores, color="#673AB7")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=75, ha="right")
    ax.set_ylabel("加权平均成绩")
    ax.set_title(f"{grade} 级 {major} 学生加权平均成绩排名 (Top {len(data)})")

    for bar, item in zip(bars, data):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}", ha="center", va="bottom", fontsize=7)

    fig.tight_layout()
    embed_figure_in_toplevel(parent, "专业成绩排名", fig)

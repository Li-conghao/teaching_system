"""学生可视化图表实现"""

from typing import List, Dict, Any

import math

from .visual_utils import create_figure, embed_figure_in_toplevel, validate_numeric_series


def show_personal_score_trend(parent, grades: List[Dict[str, Any]], target_score: float | None = None):
    if not grades:
        raise ValueError("暂无成绩数据，无法生成成绩趋势图。")

    semester_scores = {}
    for g in grades:
        sem = g.get("semester") or "未标明学期"
        score = g.get("final_score")
        if score is None:
            continue
        semester_scores.setdefault(sem, []).append(score)

    if not semester_scores:
        raise ValueError("成绩数据中没有有效的总评成绩，无法生成图表。")

    semesters = sorted(semester_scores.keys())
    avg_scores = [sum(semester_scores[s]) / len(semester_scores[s]) for s in semesters]
    validate_numeric_series(avg_scores, "平均成绩")

    fig = create_figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    ax.plot(semesters, avg_scores, marker="o", color="#4CAF50", label="平均成绩")

    # 目标分数线（若未显式传入，则给一个可调整的默认值，例如 85 分）
    if target_score is None:
        target_score = 85.0

    ax.axhline(y=target_score, color="#FF5722", linestyle="--", linewidth=1.5, label=f"目标线 {target_score:.1f}")

    ax.set_title("学期平均成绩变化趋势")
    ax.set_xlabel("学期")
    ax.set_ylabel("平均成绩")

    for x, y in zip(semesters, avg_scores):
        ax.text(x, y, f"{y:.1f}", ha="center", va="bottom", fontsize=9)

    ax.legend(loc="best")

    fig.autofmt_xdate(rotation=30)
    fig.tight_layout()

    embed_figure_in_toplevel(parent, "成绩成长曲线", fig)


def show_credit_radar(parent, courses: List[Dict[str, Any]]):
    if not courses:
        raise ValueError("暂无课程数据，无法生成学分雷达图。")

    categories = ["专业课", "选修课", "公共课", "实践课"]
    required = {
        "专业课": 80,
        "选修课": 20,
        "公共课": 30,
        "实践课": 10,
    }

    obtained_map = {c: 0.0 for c in categories}

    for c in courses:
        credits = c.get("credits")
        if credits is None:
            continue
        course_id = (c.get("course_id") or "").upper()
        name = c.get("course_name") or ""
        if course_id.startswith(("CS", "SE", "DS", "AI")):
            key = "专业课"
        elif "实验" in name or "实践" in name:
            key = "实践课"
        elif "导论" in name or "基础" in name:
            key = "公共课"
        else:
            key = "选修课"
        obtained_map[key] += float(credits)

    obtained = [min(obtained_map[c], required[c]) for c in categories]
    validate_numeric_series(obtained, "已修学分")

    values_required = [required[c] for c in categories]

    values_obtained = obtained + obtained[:1]
    values_required_closed = values_required + values_required[:1]

    angles = [n / float(len(categories)) * 2 * math.pi for n in range(len(categories))]
    angles += angles[:1]

    fig = create_figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)

    ax.plot(angles, values_required_closed, linewidth=1, linestyle="--", color="#B0BEC5", label="应修学分")
    ax.fill(angles, values_required_closed, alpha=0.05, color="#B0BEC5")

    ax.plot(angles, values_obtained, linewidth=2, color="#4CAF50", label="已修学分")
    ax.fill(angles, values_obtained, alpha=0.25, color="#4CAF50")

    # 对不足阈值的维度进行高亮标记
    threshold_ratio = 0.7  # 学分达成率低于 70% 视为「预警」
    for idx, cat in enumerate(categories):
        ratio = (obtained[idx] / required[cat]) if required[cat] else 1
        if ratio < threshold_ratio:
            ax.text(
                angles[idx],
                required[cat],
                "⚠",
                color="#F44336",
                fontsize=14,
                ha="center",
                va="bottom",
            )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title("学分达成进度雷达图（含预警）")

    max_required = max(values_required) or 1
    ax.set_ylim(0, max_required)

    ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))

    fig.tight_layout()
    embed_figure_in_toplevel(parent, "学分达成雷达图", fig)

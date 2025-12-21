"""可视化核心入口

对外只暴露统一的 show_visual 接口，由原有系统调用。
内部根据角色(role) + 图表类型(chart_type) 分发到对应模块。

设计目标：
- role: "admin" / "teacher" / "student" 等
- chart_type: 针对不同角色的字符串枚举，例如：
  - admin: "grade_distribution", "statistics_overview" 等
  - teacher: "course_grade_histogram" 等
  - student: "personal_score_trend" 等
- data: 上层业务已经准备好的纯数据结构(dict/list)，不在此处做网络/数据库访问。
"""

from __future__ import annotations

from typing import Any, Dict

import tkinter as tk
from tkinter import messagebox

from . import admin_visuals, teacher_visuals, student_visuals


def show_visual(
    parent: tk.Tk | tk.Toplevel,
    role: str,
    chart_type: str,
    data: Dict[str, Any] | None = None,
) -> None:
    """统一可视化入口。

    参数：
    - parent: 当前 Tk 根窗口或子窗口，用于挂载图表窗口；
    - role: 角色标识，如 "admin"/"teacher"/"student"；
    - chart_type: 图表类型字符串，按角色定义；
    - data: 上层准备好的数据字典，例如：
        admin + grade_distribution: {"distribution": {"优秀": 10, "良好": 20, ...}}
        teacher + course_grade_histogram: {"grades": [...], "course_name": "高等数学"}
        student + personal_score_trend: {"grades": [...]} 等。
    """

    role = (role or "").lower()
    chart_type = (chart_type or "").lower()
    data = data or {}

    try:
        if role == "admin":
            _dispatch_admin(parent, chart_type, data)
        elif role == "teacher":
            _dispatch_teacher(parent, chart_type, data)
        elif role == "student":
            _dispatch_student(parent, chart_type, data)
        else:
            raise ValueError(f"未知角色: {role}")

    except ValueError as e:
        messagebox.showerror("可视化错误", str(e), parent=parent)
    except Exception as e:
        messagebox.showerror("可视化异常", f"生成图表失败: {e}", parent=parent)


def _dispatch_admin(parent: tk.Tk | tk.Toplevel, chart_type: str, data: Dict[str, Any]):
    if chart_type == "grade_distribution":
        distribution = data.get("distribution") or data
        admin_visuals.show_grade_distribution_bar(parent, distribution)
    elif chart_type == "statistics_overview":
        stats = data.get("statistics") or data
        admin_visuals.show_statistics_overview(parent, stats)
    elif chart_type == "resource_heatmap":
        courses = data.get("courses") or []
        admin_visuals.show_resource_heatmap(parent, courses)
    elif chart_type == "grouped_grade_boxplot":
        grouped_scores = data.get("grouped_scores") or {}
        title = data.get("title", "成绩分布箱线图")
        admin_visuals.show_grouped_grade_boxplot(parent, grouped_scores, title)
    elif chart_type == "student_risk_trend":
        timeline = data.get("timeline") or []
        admin_visuals.show_student_risk_trend(parent, timeline)
    elif chart_type == "grade_class_overview":
        grade = data.get("grade", "")
        class_stats = data.get("class_stats") or []
        admin_visuals.show_grade_class_overview(parent, grade, class_stats)
    elif chart_type == "course_teacher_overview":
        course_name = data.get("course_name", "")
        teacher_name = data.get("teacher_name", "")
        overall = data.get("overall") or {}
        class_stats = data.get("class_stats") or []
        admin_visuals.show_course_teacher_overview(parent, course_name, teacher_name, overall, class_stats)
    elif chart_type == "major_rank_bar":
        grade = data.get("grade", "")
        major = data.get("major", "")
        ranking = data.get("ranking") or []
        top_n = int(data.get("top_n", 50) or 50)
        admin_visuals.show_major_rank_bar(parent, grade, major, ranking, top_n)
    else:
        raise ValueError(f"管理员暂不支持的图表类型: {chart_type}")


def _dispatch_teacher(parent: tk.Tk | tk.Toplevel, chart_type: str, data: Dict[str, Any]):
    if chart_type == "course_grade_histogram":
        grades = data.get("grades") or []
        course_name = data.get("course_name", "课程")
        teacher_visuals.show_course_grade_histogram(parent, grades, course_name)
    elif chart_type == "attendance_scatter":
        records = data.get("records") or []
        course_name = data.get("course_name", "课程")
        teacher_visuals.show_attendance_vs_score(parent, records, course_name)
    elif chart_type == "knowledge_radar":
        knowledge_stats = data.get("knowledge_stats") or []
        course_name = data.get("course_name", "课程")
        teacher_visuals.show_course_knowledge_radar(parent, knowledge_stats, course_name)
    else:
        raise ValueError(f"教师暂不支持的图表类型: {chart_type}")


def _dispatch_student(parent: tk.Tk | tk.Toplevel, chart_type: str, data: Dict[str, Any]):
    if chart_type == "personal_score_trend":
        grades = data.get("grades") or []
        target_score = data.get("target_score")
        student_visuals.show_personal_score_trend(parent, grades, target_score)
    elif chart_type == "credit_radar":
        courses = data.get("courses") or []
        student_visuals.show_credit_radar(parent, courses)
    else:
        raise ValueError(f"学生暂不支持的图表类型: {chart_type}")

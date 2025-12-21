"""
教师主界面模块
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager


class TeacherWindow:
    """教师主界面类"""
    
    def __init__(self, user_info, login_root):
        self.user_info = user_info
        self.login_root = login_root
        self.db = DatabaseManager()
        
        # 获取教师信息
        self.teacher_info = self.db.get_teacher_by_user_id(user_info['user_id'])
        
        if not self.teacher_info:
            messagebox.showerror("错误", "无法获取教师信息！")
            self.logout()
            return
        
        # 创建主窗口
        self.root = tk.Toplevel()
        self.root.title(f"本科教学管理系统 - 教师端 [{self.teacher_info['name']}]")
        self.root.geometry("1100x750")
        
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
        
        # 创建界面
        self.create_widgets()
        
        # 加载数据
        self.load_info()
    
    def create_widgets(self):
        """创建界面组件"""
        # 顶部标题栏
        top_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        # 标题
        tk.Label(
            top_frame,
            text=f"欢迎：{self.teacher_info['name']} ({self.teacher_info['teacher_id']}) - {self.teacher_info['title']}",
            font=("微软雅黑", 16, "bold"),
            bg='#2196F3',
            fg='white'
        ).pack(side=tk.LEFT, padx=20)
        
        # 注销按钮
        tk.Button(
            top_frame,
            text="注销",
            font=("微软雅黑", 11),
            bg='#f44336',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.logout
        ).pack(side=tk.RIGHT, padx=20)
        
        # 主容器
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧导航
        nav_frame = tk.Frame(main_container, bg='#f5f5f5', width=180)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        nav_frame.pack_propagate(False)
        
        # 导航按钮
        nav_buttons = [
            ("个人信息", self.show_info),
            ("我的课程", self.show_my_courses),
            ("成绩录入", self.show_grade_input),
            ("学生管理", self.show_students),
            ("成绩分析", self.show_grade_analytics),
            ("专业介绍", self.show_major_introduction),
            ("修改密码", self.change_password),
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=("微软雅黑", 11),
                bg='#ffffff',
                fg='#333',
                width=15,
                height=2,
                cursor='hand2',
                relief=tk.FLAT,
                command=command
            )
            btn.pack(pady=5, padx=10)
        
        # 右侧内容区域
        self.content_frame = tk.Frame(main_container, bg='white')
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def clear_content(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_grade_analytics(self):
        """显示成绩分析（挂科名单、成绩排名）"""
        self.clear_content()

        teacher_id = self.teacher_info['teacher_id']
        
        # 标题
        tk.Label(
            self.content_frame,
            text="成绩分析",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 创建 Notebook
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 三个 Tab
        tab_fail = tk.Frame(notebook, bg='white')
        tab_rank = tk.Frame(notebook, bg='white')
        tab_hist = tk.Frame(notebook, bg='white')
        
        notebook.add(tab_fail, text="挂科名单")
        notebook.add(tab_rank, text="各科成绩排名")
        notebook.add(tab_hist, text="成绩分布直方图")
        
        # ==================== Tab 1: 挂科名单 ====================
        fail_tool_frame = tk.Frame(tab_fail, bg='white')
        fail_tool_frame.pack(fill=tk.X, padx=10, pady=10)

        # 学期筛选
        tk.Label(fail_tool_frame, text="学期:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.fail_semester_var = tk.StringVar()
        fail_semester_combo = ttk.Combobox(
            fail_tool_frame,
            textvariable=self.fail_semester_var,
            font=("微软雅黑", 11),
            width=12,
            state='readonly'
        )
        fail_semester_combo.pack(side=tk.LEFT, padx=5)

        # 加载学期数据
        semester_values = ["全部"]
        try:
            with self.db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT semester FROM courses WHERE teacher_id = ? ORDER BY semester DESC", (teacher_id,))
                semester_values.extend([r[0] for r in cur.fetchall()])
        except Exception:
            pass
        fail_semester_combo['values'] = semester_values
        if len(semester_values) > 1:
             fail_semester_combo.current(1)
        else:
             fail_semester_combo.current(0)
        
        # 课程筛选
        tk.Label(fail_tool_frame, text="课程:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.fail_course_var = tk.StringVar()
        fail_course_combo = ttk.Combobox(
            fail_tool_frame, 
            textvariable=self.fail_course_var,
            font=("微软雅黑", 11), 
            width=15, 
            state='readonly'
        )
        fail_course_combo.pack(side=tk.LEFT, padx=5)
        
        # 班级筛选
        tk.Label(fail_tool_frame, text="班级:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.fail_class_var = tk.StringVar()
        fail_class_combo = ttk.Combobox(
            fail_tool_frame, 
            textvariable=self.fail_class_var,
            font=("微软雅黑", 11), 
            width=15, 
            state='readonly'
        )
        fail_class_combo.pack(side=tk.LEFT, padx=5)
        
        # 联动逻辑：学期 -> 课程 -> 班级
        def update_fail_courses(event=None):
            sel_semester = self.fail_semester_var.get().strip()
            
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    sql = "SELECT DISTINCT course_name FROM courses WHERE teacher_id = ?"
                    params = [teacher_id]
                    if sel_semester and sel_semester != "全部":
                        sql += " AND semester = ?"
                        params.append(sel_semester)
                    sql += " ORDER BY course_name"
                    cur.execute(sql, params)
                    courses = [r[0] for r in cur.fetchall()]
            except Exception:
                courses = []
                
            fail_course_combo['values'] = ["全部"] + courses
            fail_course_combo.current(0)
            update_fail_classes()

        def update_fail_classes(event=None):
            sel_semester = self.fail_semester_var.get().strip()
            sel_course = self.fail_course_var.get().strip()
            
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    sql = """
                        SELECT DISTINCT s.class_name 
                        FROM enrollments e
                        JOIN courses c ON e.course_id = c.course_id
                        JOIN students s ON e.student_id = s.student_id
                        WHERE c.teacher_id = ?
                    """
                    params = [teacher_id]
                    
                    if sel_semester and sel_semester != "全部":
                        sql += " AND c.semester = ?"
                        params.append(sel_semester)
                        
                    if sel_course and sel_course != "全部":
                        sql += " AND c.course_name = ?"
                        params.append(sel_course)
                        
                    sql += " ORDER BY s.class_name"
                    
                    cur.execute(sql, params)
                    classes = [r[0] for r in cur.fetchall()]
            except Exception:
                classes = []
            
            fail_class_combo['values'] = ["全部"] + classes
            fail_class_combo.current(0)
        
        fail_semester_combo.bind("<<ComboboxSelected>>", update_fail_courses)
        fail_course_combo.bind("<<ComboboxSelected>>", update_fail_classes)
        
        # 初始化
        update_fail_courses()
        
        # 挂科列表 Treeview
        fail_tree_frame = tk.Frame(tab_fail, bg='white')
        fail_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        fail_scroll = ttk.Scrollbar(fail_tree_frame)
        fail_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        fail_columns = ('student_id', 'name', 'class_name', 'course_name', 'score', 'semester')
        fail_tree = ttk.Treeview(
            fail_tree_frame, 
            columns=fail_columns, 
            show='headings',
            yscrollcommand=fail_scroll.set
        )
        
        fail_headers = ['学号', '姓名', '班级', '课程名称', '成绩', '学期']
        fail_widths = [100, 80, 100, 150, 60, 100]
        
        for col, h, w in zip(fail_columns, fail_headers, fail_widths):
            fail_tree.heading(col, text=h)
            fail_tree.column(col, width=w, anchor='center')
            
        fail_tree.pack(fill=tk.BOTH, expand=True)
        fail_scroll.config(command=fail_tree.yview)
        
        def load_fail_list():
            for item in fail_tree.get_children():
                fail_tree.delete(item)
                
            sel_semester = self.fail_semester_var.get().strip()
            sel_course = self.fail_course_var.get().strip()
            sel_class = self.fail_class_var.get().strip()
            
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    
                    sql = """
                        SELECT s.student_id, s.name, s.class_name, c.course_name, 
                               TRUNCATE(g.final_score, 2), 
                               c.semester
                        FROM grades g
                        JOIN courses c ON g.course_id = c.course_id
                        JOIN students s ON g.student_id = s.student_id
                        WHERE c.teacher_id = ? AND g.final_score < 60
                    """
                    params = [teacher_id]
                    
                    if sel_semester and sel_semester != "全部":
                        sql += " AND c.semester = ?"
                        params.append(sel_semester)

                    if sel_course and sel_course != "全部":
                        sql += " AND c.course_name = ?"
                        params.append(sel_course)
                        
                    if sel_class and sel_class != "全部":
                        sql += " AND s.class_name = ?"
                        params.append(sel_class)
                        
                    sql += " ORDER BY c.course_name, s.class_name, s.student_id"
                    
                    cur.execute(sql, params)
                    rows = cur.fetchall()
                    
                    for row in rows:
                        # 格式化成绩，确保显示两位小数
                        score = row[4]
                        formatted_score = f"{score:.2f}" if score is not None else ""

                        fail_tree.insert('', tk.END, values=(
                            row[0], row[1], row[2], row[3], formatted_score, row[5]
                        ))
            except Exception as e:
                messagebox.showerror("错误", f"加载挂科名单失败: {e}")

        tk.Button(
            fail_tool_frame,
            text="查询",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=10,
            cursor='hand2',
            command=load_fail_list
        ).pack(side=tk.LEFT, padx=10)
        
        # 默认加载一次
        load_fail_list()
        
        # ==================== Tab 2: 成绩排名 ====================
        rank_tool_frame = tk.Frame(tab_rank, bg='white')
        rank_tool_frame.pack(fill=tk.X, padx=10, pady=10)

        # 学期筛选
        tk.Label(rank_tool_frame, text="学期:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.rank_semester_var = tk.StringVar()
        rank_semester_combo = ttk.Combobox(
            rank_tool_frame,
            textvariable=self.rank_semester_var,
            font=("微软雅黑", 11),
            width=12,
            state='readonly'
        )
        rank_semester_combo.pack(side=tk.LEFT, padx=5)

        # 复用 Fail Tab 的学期数据逻辑，或者重新加载
        # 这里为了简单直接使用前面加载过的 semester_values (如果它们是通用的，通常是)
        # 但为了稳健，最好重新设置或复用变量
        rank_semester_combo['values'] = semester_values
        if len(semester_values) > 1:
             rank_semester_combo.current(1)
        else:
             rank_semester_combo.current(0)
        
        # 课程选择
        tk.Label(rank_tool_frame, text="课程:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.rank_course_var = tk.StringVar()
        rank_course_combo = ttk.Combobox(
            rank_tool_frame, 
            textvariable=self.rank_course_var,
            font=("微软雅黑", 11), 
            width=20, 
            state='readonly'
        )
        rank_course_combo.pack(side=tk.LEFT, padx=5)
        
        # 班级筛选
        tk.Label(rank_tool_frame, text="班级:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.rank_class_var = tk.StringVar()
        rank_class_combo = ttk.Combobox(
            rank_tool_frame, 
            textvariable=self.rank_class_var,
            font=("微软雅黑", 11), 
            width=15, 
            state='readonly'
        )
        rank_class_combo.pack(side=tk.LEFT, padx=5)
        
        # 排名列表 Treeview
        rank_tree_frame = tk.Frame(tab_rank, bg='white')
        rank_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        rank_scroll = ttk.Scrollbar(rank_tree_frame)
        rank_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        rank_columns = ('rank', 'student_id', 'name', 'class_name', 'course_name', 'score', 'level')
        rank_tree = ttk.Treeview(
            rank_tree_frame, 
            columns=rank_columns, 
            show='headings',
            yscrollcommand=rank_scroll.set
        )
        
        rank_headers = ['排名', '学号', '姓名', '班级', '课程名称', '成绩', '等级']
        rank_widths = [60, 100, 80, 100, 150, 80, 80]
        
        for col, h, w in zip(rank_columns, rank_headers, rank_widths):
            rank_tree.heading(col, text=h)
            rank_tree.column(col, width=w, anchor='center')
            
        rank_tree.pack(fill=tk.BOTH, expand=True)
        rank_scroll.config(command=rank_tree.yview)
        
        # 联动逻辑
        def update_rank_courses(event=None):
            sel_semester = self.rank_semester_var.get().strip()
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    sql = "SELECT DISTINCT course_name FROM courses WHERE teacher_id = ?"
                    params = [teacher_id]
                    if sel_semester and sel_semester != "全部":
                        sql += " AND semester = ?"
                        params.append(sel_semester)
                    sql += " ORDER BY course_name"
                    cur.execute(sql, params)
                    courses = [r[0] for r in cur.fetchall()]
            except Exception:
                courses = []
            
            rank_course_combo['values'] = ["全部"] + courses
            rank_course_combo.current(0)
            update_rank_classes()

        def update_rank_classes(event=None):
            sel_semester = self.rank_semester_var.get().strip()
            sel_course = self.rank_course_var.get().strip()
            
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    sql = """
                        SELECT DISTINCT s.class_name 
                        FROM enrollments e
                        JOIN courses c ON e.course_id = c.course_id
                        JOIN students s ON e.student_id = s.student_id
                        WHERE c.teacher_id = ?
                    """
                    params = [teacher_id]
                    
                    if sel_semester and sel_semester != "全部":
                        sql += " AND c.semester = ?"
                        params.append(sel_semester)
                        
                    if sel_course and sel_course != "全部":
                        sql += " AND c.course_name = ?"
                        params.append(sel_course)
                        
                    sql += " ORDER BY s.class_name"
                    
                    cur.execute(sql, params)
                    classes = [r[0] for r in cur.fetchall()]
            except Exception:
                classes = []
            
            rank_class_combo['values'] = ["全部"] + classes
            rank_class_combo.current(0)
            
        rank_semester_combo.bind("<<ComboboxSelected>>", update_rank_courses)
        rank_course_combo.bind("<<ComboboxSelected>>", update_rank_classes)
        
        # 初始化
        update_rank_courses()
        
        def load_rank_list():
            for item in rank_tree.get_children():
                rank_tree.delete(item)
            
            sel_semester = self.rank_semester_var.get().strip()
            sel_course = self.rank_course_var.get().strip()
            sel_class = self.rank_class_var.get().strip()
            
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    
                    sql = """
                        SELECT s.student_id, s.name, s.class_name, c.course_name, g.final_score, g.grade_level
                        FROM grades g
                        JOIN courses c ON g.course_id = c.course_id
                        JOIN students s ON g.student_id = s.student_id
                        WHERE c.teacher_id = ? AND g.final_score IS NOT NULL
                    """
                    params = [teacher_id]
                    
                    if sel_semester and sel_semester != "全部":
                        sql += " AND c.semester = ?"
                        params.append(sel_semester)

                    if sel_course and sel_course != "全部":
                        sql += " AND c.course_name = ?"
                        params.append(sel_course)
                        
                    if sel_class and sel_class != "全部":
                        sql += " AND s.class_name = ?"
                        params.append(sel_class)
                    
                    # 按成绩降序排列
                    sql += " ORDER BY c.course_name, g.final_score DESC"
                    
                    cur.execute(sql, params)
                    rows = cur.fetchall()
                    
                    for idx, row in enumerate(rows, start=1):
                        # 处理成绩显示：保留两位小数
                        score = row[4]
                        formatted_score = f"{score:.2f}" if score is not None else ""
                        
                        rank_tree.insert('', tk.END, values=(
                            idx, row[0], row[1], row[2], row[3], formatted_score, row[5]
                        ))
                        
            except Exception as e:
                messagebox.showerror("错误", f"加载排名失败: {e}")
        
        tk.Button(
            rank_tool_frame,
            text="查询排名",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=10,
            cursor='hand2',
            command=load_rank_list
        ).pack(side=tk.LEFT, padx=10)
        
        # 默认查询一次
        load_rank_list()

        # ==================== Tab 3: 成绩分布直方图 ====================
        hist_tool_frame = tk.Frame(tab_hist, bg='white')
        hist_tool_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(hist_tool_frame, text="课程:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.hist_course_var = tk.StringVar()
        hist_course_combo = ttk.Combobox(
            hist_tool_frame,
            textvariable=self.hist_course_var,
            font=("微软雅黑", 11),
            width=30,
            state='readonly',
        )
        hist_course_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(hist_tool_frame, text="班级:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.hist_class_var = tk.StringVar()
        hist_class_combo = ttk.Combobox(
            hist_tool_frame,
            textvariable=self.hist_class_var,
            font=("微软雅黑", 11),
            width=15,
            state='readonly',
        )
        hist_class_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(hist_tool_frame, text="指标:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.hist_metric_var = tk.StringVar()
        metric_map = {
            "期末成绩": "exam_score",
            "最终成绩": "final_score",
        }
        hist_metric_combo = ttk.Combobox(
            hist_tool_frame,
            textvariable=self.hist_metric_var,
            font=("微软雅黑", 11),
            width=10,
            state='readonly',
            values=list(metric_map.keys()),
        )
        hist_metric_combo.pack(side=tk.LEFT, padx=5)
        hist_metric_combo.current(0)

        hist_chart_frame = tk.Frame(tab_hist, bg='white')
        hist_chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._hist_canvas = None
        self._hist_course_id_map = {}

        def refresh_hist_course_options():
            courses = []
            try:
                courses = self.db.get_teacher_courses(teacher_id)
            except Exception:
                courses = []

            labels = []
            self._hist_course_id_map = {}
            for c in courses:
                cid = c.get('course_id')
                cname = c.get('course_name')
                if not cid:
                    continue
                label = f"{cid} - {cname}" if cname else str(cid)
                labels.append(label)
                self._hist_course_id_map[label] = cid

            hist_course_combo['values'] = labels
            if labels:
                if self.hist_course_var.get().strip() not in labels:
                    self.hist_course_var.set(labels[0])
            else:
                self.hist_course_var.set("")

            refresh_hist_class_options()

        def refresh_hist_class_options(event=None):
            label = self.hist_course_var.get().strip()
            course_id = self._hist_course_id_map.get(label)
            classes = ["全部"]
            if not course_id:
                hist_class_combo['values'] = classes
                self.hist_class_var.set("全部")
                return
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute(
                        """
                        SELECT DISTINCT s.class_name
                        FROM enrollments e
                        JOIN students s ON e.student_id = s.student_id
                        WHERE e.course_id = ? AND s.class_name IS NOT NULL AND s.class_name <> ''
                        ORDER BY s.class_name
                        """,
                        (course_id,),
                    )
                    classes.extend([r[0] for r in cur.fetchall()])
            except Exception:
                classes = ["全部"]
            hist_class_combo['values'] = classes
            if self.hist_class_var.get().strip() not in classes:
                self.hist_class_var.set("全部")

        hist_course_combo.bind("<<ComboboxSelected>>", refresh_hist_class_options)

        def draw_histogram():
            course_label = self.hist_course_var.get().strip()
            course_id = self._hist_course_id_map.get(course_label)
            metric_text = self.hist_metric_var.get().strip()
            metric_field = metric_map.get(metric_text)
            sel_class = self.hist_class_var.get().strip()

            if not course_id:
                messagebox.showwarning("提示", "请选择课程！")
                return
            if not metric_field:
                messagebox.showwarning("提示", "请选择指标！")
                return

            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    sql = f"""
                        SELECT g.{metric_field}
                        FROM grades g
                        JOIN courses c ON g.course_id = c.course_id
                        JOIN students s ON g.student_id = s.student_id
                        WHERE c.teacher_id = ?
                          AND c.course_id = ?
                          AND g.{metric_field} IS NOT NULL
                    """
                    params = [teacher_id, course_id]
                    if sel_class and sel_class != "全部":
                        sql += " AND s.class_name = ?"
                        params.append(sel_class)

                    cur.execute(sql, params)
                    scores = [float(r[0]) for r in cur.fetchall() if r[0] is not None]
            except Exception as e:
                messagebox.showerror("错误", f"加载成绩数据失败: {e}")
                return

            if not scores:
                messagebox.showinfo("提示", "该条件下暂无成绩数据。")
                return

            for widget in hist_chart_frame.winfo_children():
                widget.destroy()

            bins = np.arange(0, 101, 10)
            counts, edges = np.histogram(scores, bins=bins)
            labels = [f"{int(edges[i])}-{int(edges[i+1]-1)}" for i in range(len(edges) - 2)] + ["90-100"]

            fig, ax = plt.subplots(figsize=(9, 4.5))
            x = np.arange(len(counts))
            bars = ax.bar(x, counts, color="#2196F3", alpha=0.85)

            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=0)
            ax.set_ylabel("人数")
            title_parts = ["成绩分布直方图", metric_text, course_label]
            if sel_class and sel_class != "全部":
                title_parts.append(f"班级:{sel_class}")
            ax.set_title(" ".join(title_parts))

            for rect, cnt in zip(bars, counts):
                ax.text(
                    rect.get_x() + rect.get_width() / 2,
                    rect.get_height(),
                    str(int(cnt)),
                    ha='center',
                    va='bottom',
                    fontsize=9,
                )

            fig.tight_layout()
            self._hist_canvas = FigureCanvasTkAgg(fig, master=hist_chart_frame)
            self._hist_canvas.draw()
            self._hist_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        tk.Button(
            hist_tool_frame,
            text="生成直方图",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=10,
            cursor='hand2',
            command=draw_histogram,
        ).pack(side=tk.LEFT, padx=10)

        refresh_hist_course_options()

    def _get_project_root(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _extract_major_from_filename(self, filename):
        name = os.path.splitext(filename)[0]
        if '（' in name:
            name = name.split('（', 1)[0]
        if '专业' in name:
            name = name.split('专业', 1)[0]
        return name.strip()

    def _infer_teacher_major(self):
        department = (self.teacher_info.get('department') or '').strip()
        if not department:
            return ''
        majors = ['物联网工程', '电信工程及管理', '智能科学与技术', '电子信息工程']
        for m in majors:
            if m in department:
                return m
        return ''

    def _pick_latest_major_file(self, major):
        base_dir = os.path.join(self._get_project_root(), 'bupt_news_content')
        if not os.path.isdir(base_dir):
            return None

        candidates = []
        for fn in os.listdir(base_dir):
            if not fn.lower().endswith('.txt'):
                continue
            if self._extract_major_from_filename(fn) != major:
                continue
            candidates.append(fn)

        if not candidates:
            return None

        def _date_key(fn):
            stem = os.path.splitext(fn)[0]
            parts = stem.rsplit('-', 2)
            if len(parts) == 3:
                try:
                    return (int(parts[0][-4:]), int(parts[1]), int(parts[2]))
                except Exception:
                    return (0, 0, 0)
            return (0, 0, 0)

        latest = sorted(candidates, key=_date_key)[-1]
        return os.path.join(base_dir, latest)

    def show_major_introduction(self):
        """显示教师所属院系对应的专业介绍"""
        self.clear_content()

        major = self._infer_teacher_major()
        title = f"专业介绍 - {major}" if major else "专业介绍"

        tk.Label(
            self.content_frame,
            text=title,
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)

        if not major:
            messagebox.showinfo("提示", "无法从教师院系信息推导出专业（示例：物联网工程系 -> 物联网工程）")
            return

        fp = self._pick_latest_major_file(major)
        if not fp or not os.path.isfile(fp):
            messagebox.showinfo("提示", f"未找到专业【{major}】对应的介绍文件")
            return

        try:
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("错误", f"读取专业介绍失败: {e}")
            return

        text_frame = tk.Frame(self.content_frame, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(
            text_frame,
            font=("微软雅黑", 11),
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
    
    def show_info(self):
        """显示个人信息"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="个人信息",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 信息框架
        info_frame = tk.Frame(self.content_frame, bg='white')
        info_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # 信息列表
        info_items = [
            ("工号", self.teacher_info['teacher_id']),
            ("姓名", self.teacher_info['name']),
            ("性别", self.teacher_info['gender']),
            ("出生日期", self.teacher_info['birth_date']),
            ("院系", self.teacher_info['department']),
            ("职称", self.teacher_info['title']),
            ("电话", self.teacher_info['phone']),
            ("邮箱", self.teacher_info['email']),
            ("办公室", self.teacher_info['office']),
            ("入职日期", self.teacher_info['hire_date']),
        ]
        
        for label, value in info_items:
            row_frame = tk.Frame(info_frame, bg='white')
            row_frame.pack(fill=tk.X, pady=8)
            
            tk.Label(
                row_frame,
                text=f"{label}:",
                font=("微软雅黑", 12, "bold"),
                bg='white',
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row_frame,
                text=str(value) if value else "未填写",
                font=("微软雅黑", 12),
                bg='white',
                anchor='w'
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def show_my_courses(self):
        """显示我的课程"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="我的课程",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 按钮框架
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="查看选课学生",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=12,
            cursor='hand2',
            command=self.view_course_students
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="刷新",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.load_my_courses
        ).pack(side=tk.LEFT, padx=5)
        
        # 树形视图
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('course_id', 'course_name', 'credits', 'hours', 'semester', 
                   'time', 'classroom', 'capacity', 'enrolled')
        self.course_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        headers = ['课程编号', '课程名称', '学分', '学时', '学期', 
                   '上课时间', '教室', '容量', '已选人数']
        widths = [90, 130, 60, 60, 90, 140, 90, 60, 80]
        
        for col, header, width in zip(columns, headers, widths):
            self.course_tree.heading(col, text=header)
            self.course_tree.column(col, width=width, anchor='center')
        
        self.course_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.course_tree.yview)
        
        # 加载数据
        self.load_my_courses()
    
    def load_my_courses(self):
        """加载我的课程"""
        # 清空现有数据
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        # 获取课程
        courses = self.db.get_teacher_courses(self.teacher_info['teacher_id'])
        
        for course in courses:
            self.course_tree.insert('', tk.END, values=(
                course['course_id'],
                course['course_name'],
                course['credits'],
                course['hours'],
                course['semester'],
                course['class_time'],
                course['classroom'],
                course['capacity'],
                course['enrolled_count']
            ))
    
    def view_course_students(self):
        """查看课程选课学生"""
        selection = self.course_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择课程！")
            return
        
        item = self.course_tree.item(selection[0])
        course_id = item['values'][0]
        course_name = item['values'][1]
        
        # 创建新窗口
        student_win = tk.Toplevel(self.root)
        student_win.title(f"{course_name} - 选课学生")
        student_win.geometry("800x500")
        
        tk.Label(
            student_win,
            text=f"{course_name} - 选课学生列表",
            font=("微软雅黑", 14, "bold")
        ).pack(pady=10)
        
        # 树形视图
        tree_frame = tk.Frame(student_win)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('student_id', 'name', 'class_name', 'enrollment_date')
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        headers = ['学号', '姓名', '班级', '选课日期']
        widths = [120, 100, 150, 180]
        
        for col, header, width in zip(columns, headers, widths):
            tree.heading(col, text=header)
            tree.column(col, width=width, anchor='center')
        
        tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=tree.yview)
        
        # 加载学生数据
        students = self.db.get_course_enrollments(course_id)
        for student in students:
            tree.insert('', tk.END, values=(
                student['student_id'],
                student['name'],
                student['class_name'],
                student['enrollment_date']
            ))
        
        tk.Label(
            student_win,
            text=f"共 {len(students)} 名学生选课",
            font=("微软雅黑", 11)
        ).pack(pady=10)
    
    def show_grade_input(self):
        """显示成绩录入"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="成绩录入",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 选择课程框架
        select_frame = tk.Frame(self.content_frame, bg='white')
        select_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            select_frame,
            text="选择课程:",
            font=("微软雅黑", 12),
            bg='white'
        ).pack(side=tk.LEFT, padx=10)
        
        # 课程下拉框
        self.course_combo = ttk.Combobox(
            select_frame,
            font=("微软雅黑", 11),
            width=30,
            state='readonly'
        )
        self.course_combo.pack(side=tk.LEFT, padx=10)
        
        # 加载课程列表
        courses = self.db.get_teacher_courses(self.teacher_info['teacher_id'])
        self.course_list = courses
        self.course_combo['values'] = [f"{c['course_id']} - {c['course_name']}" for c in courses]
        
        tk.Button(
            select_frame,
            text="加载学生",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.load_course_students
        ).pack(side=tk.LEFT, padx=10)
        
        # 学生成绩列表
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('student_id', 'name', 'class_name', 'usual', 'exam', 'final', 'level')
        self.grade_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        headers = ['学号', '姓名', '班级', '平时成绩', '考试成绩', '总评成绩', '等级']
        widths = [100, 80, 120, 80, 80, 80, 80]
        
        for col, header, width in zip(columns, headers, widths):
            self.grade_tree.heading(col, text=header)
            self.grade_tree.column(col, width=width, anchor='center')
        
        self.grade_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.grade_tree.yview)
        
        # 操作按钮
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="录入/编辑成绩",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.edit_grade
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="批量导入",
            font=("微软雅黑", 11),
            bg='#FF9800',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.batch_import_grades
        ).pack(side=tk.LEFT, padx=5)
    
    def load_course_students(self):
        """加载课程学生"""
        if not self.course_combo.get():
            messagebox.showwarning("提示", "请先选择课程！")
            return
        
        # 获取选中的课程
        index = self.course_combo.current()
        course = self.course_list[index]
        course_id = course['course_id']
        semester = course['semester']
        
        # 清空现有数据
        for item in self.grade_tree.get_children():
            self.grade_tree.delete(item)
        
        # 获取选课学生
        students = self.db.get_course_enrollments(course_id)
        
        # 获取成绩
        grades_dict = {}
        grades = self.db.get_course_grades(course_id)
        for grade in grades:
            grades_dict[grade['student_id']] = grade
        
        # 显示数据
        for student in students:
            student_id = student['student_id']
            grade = grades_dict.get(student_id, {})
            
            self.grade_tree.insert('', tk.END, values=(
                student_id,
                student['name'],
                student['class_name'],
                f"{grade.get('usual_score', 0):.1f}" if grade.get('usual_score') else '-',
                f"{grade.get('exam_score', 0):.1f}" if grade.get('exam_score') else '-',
                f"{grade.get('final_score', 0):.1f}" if grade.get('final_score') else '-',
                grade.get('grade_level', '-')
            ))
    
    def edit_grade(self):
        """编辑成绩"""
        if not self.course_combo.get():
            messagebox.showwarning("提示", "请先选择课程！")
            return
        
        selection = self.grade_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择学生！")
            return
        
        item = self.grade_tree.item(selection[0])
        student_id = item['values'][0]
        student_name = item['values'][1]
        usual_score = item['values'][3]
        exam_score = item['values'][4]
        
        # 获取当前课程
        index = self.course_combo.current()
        course = self.course_list[index]
        
        # 创建编辑窗口
        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"录入成绩 - {student_name}")
        edit_win.geometry("400x300")
        
        tk.Label(
            edit_win,
            text=f"学生：{student_name} ({student_id})",
            font=("微软雅黑", 12, "bold")
        ).pack(pady=20)
        
        tk.Label(
            edit_win,
            text=f"课程：{course['course_name']}",
            font=("微软雅黑", 11)
        ).pack(pady=5)
        
        # 输入框架
        input_frame = tk.Frame(edit_win)
        input_frame.pack(pady=20)
        
        tk.Label(
            input_frame,
            text="平时成绩:",
            font=("微软雅黑", 11),
            width=10
        ).grid(row=0, column=0, pady=10, padx=10)
        
        usual_entry = ttk.Entry(input_frame, font=("微软雅黑", 11), width=15)
        usual_entry.grid(row=0, column=1, pady=10, padx=10)
        if usual_score != '-':
            usual_entry.insert(0, usual_score)
        
        tk.Label(
            input_frame,
            text="考试成绩:",
            font=("微软雅黑", 11),
            width=10
        ).grid(row=1, column=0, pady=10, padx=10)
        
        exam_entry = ttk.Entry(input_frame, font=("微软雅黑", 11), width=15)
        exam_entry.grid(row=1, column=1, pady=10, padx=10)
        if exam_score != '-':
            exam_entry.insert(0, exam_score)
        
        # 提交按钮
        def submit():
            try:
                usual = float(usual_entry.get().strip())
                exam = float(exam_entry.get().strip())
                
                if not (0 <= usual <= 100 and 0 <= exam <= 100):
                    messagebox.showerror("错误", "成绩必须在0-100之间！")
                    return
                
                grade_data = {
                    'student_id': student_id,
                    'course_id': course['course_id'],
                    'usual_score': usual,
                    'exam_score': exam,
                    'semester': course['semester']
                }
                
                if self.db.add_grade(grade_data):
                    messagebox.showinfo("成功", "成绩录入成功！")
                    edit_win.destroy()
                    self.load_course_students()
                else:
                    messagebox.showerror("错误", "成绩录入失败！")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字！")
        
        tk.Button(
            edit_win,
            text="提交",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=15,
            cursor='hand2',
            command=submit
        ).pack(pady=20)
    
    def batch_import_grades(self):
        """批量导入成绩"""
        messagebox.showinfo("提示", "批量导入功能开发中...")
    
    def show_students(self):
        """显示学生管理"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="学生管理",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 搜索框架
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            search_frame,
            text="搜索:",
            font=("微软雅黑", 11),
            bg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        search_entry = ttk.Entry(search_frame, font=("微软雅黑", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        def search():
            keyword = search_entry.get().strip()
            # 获取选了该教师课程的学生
            all_teacher_students = self.db.get_teacher_students(self.teacher_info['teacher_id'])
            
            # 如果有搜索关键词，则过滤
            if keyword:
                students = [s for s in all_teacher_students 
                           if keyword in s['student_id'] 
                           or keyword in s['name'] 
                           or keyword in s.get('major', '')]
            else:
                students = all_teacher_students
            
            # 清空并重新加载
            for item in student_tree.get_children():
                student_tree.delete(item)
            
            for student in students:
                student_tree.insert('', tk.END, values=(
                    student['student_id'],
                    student['name'],
                    student['gender'],
                    student['major'],
                    student['grade'],
                    student['class_name'],
                    student['phone'],
                    student.get('courses', '-')
                ))
        
        tk.Button(
            search_frame,
            text="搜索",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=8,
            cursor='hand2',
            command=search
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            search_frame,
            text="显示全部",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=8,
            cursor='hand2',
            command=lambda: (search_entry.delete(0, tk.END), search())
        ).pack(side=tk.LEFT, padx=5)
        
        # 学生列表
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('student_id', 'name', 'gender', 'major', 'grade', 'class', 'phone', 'courses')
        student_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        headers = ['学号', '姓名', '性别', '专业', '年级', '班级', '电话', '选课课程']
        widths = [100, 80, 60, 120, 60, 80, 110, 200]
        
        for col, header, width in zip(columns, headers, widths):
            student_tree.heading(col, text=header)
            student_tree.column(col, width=width, anchor='center')
        
        student_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=student_tree.yview)
        
        # 加载所有学生
        search()
    
    def change_password(self):
        """修改密码"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="修改密码",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=30)
        
        # 输入框架
        input_frame = tk.Frame(self.content_frame, bg='white')
        input_frame.pack(expand=True)
        
        # 旧密码
        tk.Label(
            input_frame,
            text="旧密码:",
            font=("微软雅黑", 12),
            bg='white',
            width=10,
            anchor='w'
        ).grid(row=0, column=0, pady=10, padx=10)
        
        old_pwd_entry = ttk.Entry(input_frame, font=("微软雅黑", 11), width=25, show='●')
        old_pwd_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # 新密码
        tk.Label(
            input_frame,
            text="新密码:",
            font=("微软雅黑", 12),
            bg='white',
            width=10,
            anchor='w'
        ).grid(row=1, column=0, pady=10, padx=10)
        
        new_pwd_entry = ttk.Entry(input_frame, font=("微软雅黑", 11), width=25, show='●')
        new_pwd_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # 确认密码
        tk.Label(
            input_frame,
            text="确认密码:",
            font=("微软雅黑", 12),
            bg='white',
            width=10,
            anchor='w'
        ).grid(row=2, column=0, pady=10, padx=10)
        
        confirm_pwd_entry = ttk.Entry(input_frame, font=("微软雅黑", 11), width=25, show='●')
        confirm_pwd_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # 提交按钮
        def submit():
            old_pwd = old_pwd_entry.get().strip()
            new_pwd = new_pwd_entry.get().strip()
            confirm_pwd = confirm_pwd_entry.get().strip()
            
            if not all([old_pwd, new_pwd, confirm_pwd]):
                messagebox.showwarning("提示", "请填写所有字段！")
                return
            
            if new_pwd != confirm_pwd:
                messagebox.showerror("错误", "两次输入的新密码不一致！")
                return
            
            if len(new_pwd) < 6:
                messagebox.showerror("错误", "新密码长度至少6位！")
                return
            
            if self.db.change_password(self.user_info['user_id'], old_pwd, new_pwd):
                messagebox.showinfo("成功", "密码修改成功！请重新登录。")
                self.logout()
            else:
                messagebox.showerror("错误", "旧密码错误！")
        
        tk.Button(
            input_frame,
            text="提交",
            font=("微软雅黑", 12),
            bg='#2196F3',
            fg='white',
            width=15,
            height=2,
            cursor='hand2',
            command=submit
        ).grid(row=3, column=0, columnspan=2, pady=30)
    
    def load_info(self):
        """加载初始信息"""
        self.show_info()
    
    def logout(self):
        """注销"""
        if messagebox.askyesno("确认", "确定要注销吗？"):
            self.root.destroy()
            self.login_root.deiconify()


if __name__ == '__main__':
    pass
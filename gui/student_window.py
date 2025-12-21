"""
学生主界面模块
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from visualization.visual_utils import create_figure


class StudentWindow:
    """学生主界面类"""
    
    def __init__(self, user_info, login_root):
        self.user_info = user_info
        self.login_root = login_root
        self.db = DatabaseManager()
        
        # 获取学生信息
        self.student_info = self.db.get_student_by_user_id(user_info['user_id'])
        
        if not self.student_info:
            messagebox.showerror("错误", "无法获取学生信息！")
            self.logout()
            return
        
        # 创建主窗口
        self.root = tk.Toplevel()
        self.root.title(f"本科教学管理系统 - 学生端 [{self.student_info['name']}]")
        self.root.geometry("1000x700")
        
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
            text=f"欢迎：{self.student_info['name']} ({self.student_info['student_id']})",
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
            ("成绩分析", self.show_grade_analytics),
            ("我的课程", self.show_courses),
            ("选课管理", self.show_enrollment),
            ("我的成绩", self.show_grades),
            ("专业介绍", self.show_major_introduction),
            ("师资介绍", self.show_faculty_introduction),
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

    def _get_project_root(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _extract_major_from_filename(self, filename):
        name = os.path.splitext(filename)[0]
        if '（' in name:
            name = name.split('（', 1)[0]
        if '专业' in name:
            name = name.split('专业', 1)[0]
        return name.strip()

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
        """显示本专业介绍（按学生专业过滤）"""
        self.clear_content()

        major = (self.student_info.get('major') or '').strip()
        tk.Label(
            self.content_frame,
            text=f"专业介绍 - {major}" if major else "专业介绍",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)

        if not major:
            messagebox.showwarning("提示", "未获取到学生专业信息！")
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

    def show_faculty_introduction(self):
        """显示师资介绍（图片列表，双击打开）"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="师资介绍",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)

        img_dir = os.path.join(self._get_project_root(), 'images')
        if not os.path.isdir(img_dir):
            messagebox.showinfo("提示", "未找到 images 文件夹")
            return

        files = [
            fn for fn in os.listdir(img_dir)
            if fn.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))
        ]
        files.sort()

        if not files:
            messagebox.showinfo("提示", "images 文件夹下暂无图片")
            return

        list_frame = tk.Frame(self.content_frame, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(
            list_frame,
            text="双击图片文件名可打开查看",
            font=("微软雅黑", 11),
            bg='white',
            fg='#666'
        ).pack(anchor='w', pady=(0, 10))

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        lb = tk.Listbox(
            list_frame,
            font=("微软雅黑", 11),
            yscrollcommand=scrollbar.set
        )
        lb.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=lb.yview)

        for fn in files:
            lb.insert(tk.END, fn)

        def _open_selected(_event=None):
            sel = lb.curselection()
            if not sel:
                return
            fn = lb.get(sel[0])
            path = os.path.join(img_dir, fn)
            try:
                os.startfile(path)
            except Exception as e:
                messagebox.showerror("错误", f"打开图片失败: {e}")

        lb.bind('<Double-Button-1>', _open_selected)
    
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
            ("学号", self.student_info['student_id']),
            ("姓名", self.student_info['name']),
            ("性别", self.student_info['gender']),
            ("出生日期", self.student_info['birth_date']),
            ("专业", self.student_info['major']),
            ("年级", self.student_info['grade']),
            ("班级", self.student_info['class_name']),
            ("电话", self.student_info['phone']),
            ("邮箱", self.student_info['email']),
            ("地址", self.student_info['address']),
        ]
        
        for i, (label, value) in enumerate(info_items):
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
    
    def show_courses(self):
        """显示我的课程"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="我的课程",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 树形视图框架
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 树形视图
        columns = ('course_id', 'course_name', 'teacher', 'credits', 'time', 'classroom')
        self.course_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        # 列标题
        headers = ['课程编号', '课程名称', '任课教师', '学分', '上课时间', '教室']
        widths = [100, 150, 100, 80, 180, 100]
        
        for col, header, width in zip(columns, headers, widths):
            self.course_tree.heading(col, text=header)
            self.course_tree.column(col, width=width, anchor='center')
        
        self.course_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.course_tree.yview)
        
        # 加载数据
        enrollments = self.db.get_student_enrollments(self.student_info['student_id'])
        for enroll in enrollments:
            self.course_tree.insert('', tk.END, values=(
                enroll['course_id'],
                enroll['course_name'],
                enroll['teacher_name'],
                enroll['credits'],
                enroll['class_time'],
                enroll['classroom']
            ))
    
    def show_enrollment(self):
        """显示选课管理"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="选课管理",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 按钮框架
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="选课",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.enroll_course
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="退课",
            font=("微软雅黑", 11),
            bg='#f44336',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.drop_course
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="刷新",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.load_available_courses
        ).pack(side=tk.LEFT, padx=5)
        
        # 可选课程列表
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('course_id', 'course_name', 'teacher', 'credits', 'capacity', 'enrolled')
        self.enroll_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        headers = ['课程编号', '课程名称', '任课教师', '学分', '容量', '已选人数']
        widths = [100, 150, 100, 80, 80, 100]
        
        for col, header, width in zip(columns, headers, widths):
            self.enroll_tree.heading(col, text=header)
            self.enroll_tree.column(col, width=width, anchor='center')
        
        self.enroll_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.enroll_tree.yview)
        
        # 加载可选课程
        self.load_available_courses()
    
    def load_available_courses(self):
        """加载可选课程"""
        # 清空现有数据
        for item in self.enroll_tree.get_children():
            self.enroll_tree.delete(item)
        
        # 获取所有开放的课程
        all_courses = self.db.get_all_courses()
        
        # 获取已选课程
        enrolled = self.db.get_student_enrollments(self.student_info['student_id'])
        enrolled_ids = {e['course_id'] for e in enrolled}

        # 获取已修过课程（已有成绩记录的课程）
        taken = self.db.get_student_grades(self.student_info['student_id'])
        taken_ids = {g['course_id'] for g in taken}
        
        # 显示未选且未修过的课程（不再限制 status）
        for course in all_courses:
            if course['course_id'] not in enrolled_ids and course['course_id'] not in taken_ids:
                self.enroll_tree.insert('', tk.END, values=(
                    course['course_id'],
                    course['course_name'],
                    course['teacher_name'] if course['teacher_name'] else '待定',
                    course['credits'],
                    course['capacity'],
                    course['enrolled_count']
                ))
    
    def enroll_course(self):
        """选课"""
        selection = self.enroll_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要选的课程！")
            return
        
        item = self.enroll_tree.item(selection[0])
        course_id = item['values'][0]
        course_name = item['values'][1]
        
        # 确认
        if not messagebox.askyesno("确认", f"确定要选 {course_name} 吗？"):
            return
        
        # 选课
        success, message = self.db.enroll_course(self.student_info['student_id'], course_id)
        
        if success:
            messagebox.showinfo("成功", message)
            self.load_available_courses()
        else:
            messagebox.showerror("失败", message)
    
    def drop_course(self):
        """退课"""
        # 打开已选课程列表
        drop_win = tk.Toplevel(self.root)
        drop_win.title("退课")
        drop_win.geometry("700x400")
        
        tk.Label(
            drop_win,
            text="选择要退的课程",
            font=("微软雅黑", 14, "bold")
        ).pack(pady=10)
        
        # 课程列表
        tree_frame = tk.Frame(drop_win)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('course_id', 'course_name', 'teacher')
        drop_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        for col, header in zip(columns, ['课程编号', '课程名称', '任课教师']):
            drop_tree.heading(col, text=header)
            drop_tree.column(col, width=150, anchor='center')
        
        drop_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=drop_tree.yview)
        
        # 加载已选课程
        enrolled = self.db.get_student_enrollments(self.student_info['student_id'])
        for enroll in enrolled:
            drop_tree.insert('', tk.END, values=(
                enroll['course_id'],
                enroll['course_name'],
                enroll['teacher_name']
            ))
        
        # 退课按钮
        def confirm_drop():
            selection = drop_tree.selection()
            if not selection:
                messagebox.showwarning("提示", "请先选择要退的课程！")
                return
            
            item = drop_tree.item(selection[0])
            course_id = item['values'][0]
            course_name = item['values'][1]
            
            if not messagebox.askyesno("确认", f"确定要退 {course_name} 吗？"):
                return
            
            success, message = self.db.drop_course(self.student_info['student_id'], course_id)
            
            if success:
                messagebox.showinfo("成功", message)
                drop_win.destroy()
                self.load_available_courses()
            else:
                messagebox.showerror("失败", message)
        
        tk.Button(
            drop_win,
            text="确认退课",
            font=("微软雅黑", 11),
            bg='#f44336',
            fg='white',
            width=15,
            cursor='hand2',
            command=confirm_drop
        ).pack(pady=10)
    
    def show_grades(self):
        """显示成绩"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="我的成绩",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 树形视图
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('course_name', 'teacher', 'usual', 'exam', 'final', 'level', 'semester')
        self.grade_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        headers = ['课程名称', '任课教师', '平时成绩', '考试成绩', '总评成绩', '等级', '学期']
        widths = [150, 100, 80, 80, 80, 80, 100]
        
        for col, header, width in zip(columns, headers, widths):
            self.grade_tree.heading(col, text=header)
            self.grade_tree.column(col, width=width, anchor='center')
        
        self.grade_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.grade_tree.yview)
        
        # 加载成绩
        grades = self.db.get_student_grades(self.student_info['student_id'])
        total_score = 0
        count = 0
        
        for grade in grades:
            self.grade_tree.insert('', tk.END, values=(
                grade['course_name'],
                grade['teacher_name'],
                f"{grade['usual_score']:.1f}" if grade['usual_score'] else '-',
                f"{grade['exam_score']:.1f}" if grade['exam_score'] else '-',
                f"{grade['final_score']:.1f}" if grade['final_score'] else '-',
                grade['grade_level'],
                grade['semester']
            ))
            if grade['final_score']:
                total_score += grade['final_score']
                count += 1
        
        # 统计信息
        if count > 0:
            avg_score = total_score / count
            tk.Label(
                self.content_frame,
                text=f"平均分: {avg_score:.2f}",
                font=("微软雅黑", 12, "bold"),
                bg='white',
                fg='#2196F3'
            ).pack(pady=10)

    def show_grade_analytics(self):
        """显示成绩分析"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="成绩分析",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=12)

        notebook = ttk.Notebook(self.content_frame)
        tab_trend = tk.Frame(notebook, bg='white')
        tab_radar = tk.Frame(notebook, bg='white')
        notebook.add(tab_trend, text="个人成绩趋势")
        notebook.add(tab_radar, text="个人成绩雷达图")
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        student_id = self.student_info['student_id']

        # ==================== Tab 1: Trend ====================
        trend_controls = tk.Frame(tab_trend, bg='white')
        trend_controls.pack(fill=tk.X, padx=10, pady=(10, 6))

        tk.Label(
            trend_controls,
            text="按学期平均分趋势（总评成绩）",
            font=("微软雅黑", 12, "bold"),
            bg='white'
        ).pack(side=tk.LEFT)

        trend_canvas_frame = tk.Frame(tab_trend, bg='white')
        trend_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        trend_fig = create_figure(figsize=(8, 4.5))
        trend_ax = trend_fig.add_subplot(111)
        trend_canvas = FigureCanvasTkAgg(trend_fig, master=trend_canvas_frame)
        trend_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def _plot_trend():
            try:
                trend_ax.clear()
                data = self.db.get_student_semester_trend(student_id)
                student_series = data.get('student') or []
                major_series = data.get('major') or []
                class_series = data.get('class') or []
                meta = data.get('student_meta') or {}

                if not student_series:
                    trend_ax.text(0.5, 0.5, '暂无成绩数据', ha='center', va='center')
                    trend_canvas.draw()
                    return

                semesters = [d['semester'] for d in student_series]

                def _series_to_map(series):
                    return {d['semester']: d['avg_score'] for d in series if d.get('semester')}

                student_map = _series_to_map(student_series)
                major_map = _series_to_map(major_series)
                class_map = _series_to_map(class_series)

                y_student = [student_map.get(s) for s in semesters]
                y_major = [major_map.get(s) for s in semesters]
                y_class = [class_map.get(s) for s in semesters]

                trend_ax.plot(semesters, y_student, marker='o', linewidth=2.0, label='个人平均分')
                if any(v is not None for v in y_major):
                    trend_ax.plot(
                        semesters,
                        y_major,
                        marker='o',
                        linewidth=1.6,
                        linestyle='--',
                        label=f"专业平均分({meta.get('major') or ''})",
                    )
                if any(v is not None for v in y_class):
                    trend_ax.plot(
                        semesters,
                        y_class,
                        marker='o',
                        linewidth=1.6,
                        linestyle='--',
                        label=f"班级平均分({meta.get('class_name') or ''})",
                    )

                trend_ax.set_title('按学期平均分趋势')
                trend_ax.set_xlabel('学期')
                trend_ax.set_ylabel('平均分')

                # Y 轴范围：根据当前显示数据自适应（避免固定 0-100）
                y_candidates = [v for v in (y_student + y_major + y_class) if isinstance(v, (int, float))]
                if y_candidates:
                    ymin = min(y_candidates)
                    ymax = max(y_candidates)
                    pad = max(2.0, (ymax - ymin) * 0.1)
                    trend_ax.set_ylim(max(0, ymin - pad), min(100, ymax + pad))
                trend_ax.tick_params(axis='x', rotation=30)
                trend_ax.legend(loc='best')
                trend_ax.grid(True, linestyle='--', alpha=0.3)
                trend_fig.tight_layout()
                trend_canvas.draw()
            except Exception as e:
                messagebox.showerror('错误', f'生成趋势图失败: {e}')

        tk.Button(
            trend_controls,
            text="刷新",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=10,
            cursor='hand2',
            command=_plot_trend,
        ).pack(side=tk.RIGHT)

        _plot_trend()

        # ==================== Tab 2: Radar ====================
        radar_controls = tk.Frame(tab_radar, bg='white')
        radar_controls.pack(fill=tk.X, padx=10, pady=(10, 6))

        tk.Label(
            radar_controls,
            text="学期(必选):",
            font=("微软雅黑", 11),
            bg='white'
        ).pack(side=tk.LEFT)

        semester_var = tk.StringVar()
        semester_cb = ttk.Combobox(
            radar_controls,
            textvariable=semester_var,
            width=18,
            state='readonly'
        )
        semester_cb.pack(side=tk.LEFT, padx=(6, 14))

        hint = tk.Label(
            radar_controls,
            text="说明：雷达图按该学期各课程（学科）总评成绩绘制",
            font=("微软雅黑", 10),
            bg='white',
            fg='#666'
        )
        hint.pack(side=tk.LEFT, fill=tk.X, expand=True)

        radar_canvas_frame = tk.Frame(tab_radar, bg='white')
        radar_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        radar_fig = create_figure(figsize=(8, 4.5))
        radar_ax = radar_fig.add_subplot(111, polar=True)
        radar_canvas = FigureCanvasTkAgg(radar_fig, master=radar_canvas_frame)
        radar_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def _plot_radar():
            try:
                semester = (semester_var.get() or '').strip()
                if not semester:
                    messagebox.showwarning('提示', '请选择学期！')
                    return

                radar_ax.clear()

                rows = self.db.get_student_semester_course_scores(student_id, semester)
                if not rows:
                    radar_ax.text(0.5, 0.5, '该学期暂无成绩数据', ha='center', va='center', transform=radar_ax.transAxes)
                    radar_canvas.draw()
                    return

                # 1) 偏科结构：按课程名（学科）逐门课绘制
                course_scores = []
                for r in rows:
                    cn = r.get('course_name')
                    sc = r.get('final_score')
                    if cn is None or sc is None:
                        continue
                    try:
                        course_scores.append((str(cn), float(sc)))
                    except Exception:
                        continue

                if not course_scores:
                    radar_ax.text(0.5, 0.5, '无有效成绩', ha='center', va='center', transform=radar_ax.transAxes)
                    radar_canvas.draw()
                    return

                # 课程名过长时做截断显示，避免标签挤压
                def _short(name: str, max_len: int = 8) -> str:
                    return name if len(name) <= max_len else (name[: max_len - 1] + '…')

                # 课程数较多/名称较长时：采用编号标签，并在下方输出“编号-课程名”映射
                full_names = [n for n, _ in course_scores]
                values = [v for _, v in course_scores]
                max_name_len = max((len(n) for n in full_names), default=0)
                use_numeric_labels = len(course_scores) >= 8 or max_name_len >= 10
                if use_numeric_labels:
                    categories = [str(i + 1) for i in range(len(course_scores))]
                else:
                    categories = [_short(n) for n in full_names]

                # 闭合
                import math

                angles = [i / float(len(categories)) * 2 * math.pi for i in range(len(categories))]
                angles += angles[:1]
                plot_values = values + values[:1]

                radar_ax.set_theta_offset(math.pi / 2)
                radar_ax.set_theta_direction(-1)
                radar_ax.set_thetagrids([a * 180 / math.pi for a in angles[:-1]], categories)

                # 字体/刻度自适应
                n = len(categories)
                label_fontsize = 11 if n <= 5 else 10 if n <= 7 else 9 if n <= 10 else 8
                value_fontsize = 10 if n <= 7 else 9 if n <= 10 else 8

                # 旋转并对齐每个标签，减少重叠
                for lbl, ang in zip(radar_ax.get_xticklabels(), angles[:-1]):
                    ang_deg = ang * 180 / math.pi
                    rotation = ang_deg - 90
                    if ang_deg >= 180:
                        rotation = ang_deg + 90
                        lbl.set_horizontalalignment('right')
                    else:
                        lbl.set_horizontalalignment('left')
                    lbl.set_rotation(rotation)
                    lbl.set_rotation_mode('anchor')
                    lbl.set_fontsize(label_fontsize)

                radar_ax.set_ylim(0, 100)

                radar_ax.plot(angles, plot_values, linewidth=2)
                radar_ax.fill(angles, plot_values, alpha=0.15)

                # 标注数值
                for a, v in zip(angles[:-1], values):
                    radar_ax.text(
                        a,
                        min(100, v + 2),
                        f"{v:.1f}",
                        ha='center',
                        va='center',
                        fontsize=value_fontsize,
                        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.8),
                    )

                radar_ax.set_title("")
                radar_fig.tight_layout()
                radar_canvas.draw()
            except Exception as e:
                messagebox.showerror('错误', f'生成雷达图失败: {e}')

        def _load_semesters():
            semesters = self.db.get_student_semesters(student_id)
            semester_cb['values'] = semesters
            if semesters:
                semester_var.set(semesters[-1])
            else:
                semester_var.set('')

        tk.Button(
            radar_controls,
            text="生成雷达图",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=12,
            cursor='hand2',
            command=_plot_radar,
        ).pack(side=tk.RIGHT, padx=(8, 0))

        _load_semesters()
    
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
    # 测试代码
    pass
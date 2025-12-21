import tkinter as tk
from tkinter import ttk, messagebox

import os

from visualization.visualization_core import show_visual


class NetworkTeacherWindow:
    """教师主界面（网络模式）"""

    def __init__(self, user_info, login_root, client):
        self.user_info = user_info
        self.login_root = login_root
        self.client = client

        # 通过网络获取教师信息
        resp = self.client.get_teacher_info(self.user_info['user_id'])
        if not resp.get('success') or not resp.get('data') or not resp['data'].get('teacher'):
            messagebox.showerror("错误", resp.get('message', '无法获取教师信息！'))
            self.login_root.deiconify()
            return

        self.teacher_info = resp['data']['teacher']

        # 创建主窗口
        self.root = tk.Toplevel()
        self.root.title(
            f"本科教学管理系统 - 网络教师端 [{self.teacher_info['name']}]"
        )
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
        top_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)

        # 标题
        tk.Label(
            top_frame,
            text=(
                f"欢迎：{self.teacher_info['name']} "
                f"({self.teacher_info['teacher_id']}) - {self.teacher_info.get('title', '')}"
            ),
            font=("微软雅黑", 16, "bold"),
            bg="#2196F3",
            fg="white",
        ).pack(side=tk.LEFT, padx=20)

        # 注销按钮
        tk.Button(
            top_frame,
            text="注销",
            font=("微软雅黑", 11),
            bg="#f44336",
            fg="white",
            width=8,
            cursor="hand2",
            command=self.logout,
        ).pack(side=tk.RIGHT, padx=20)

        # 主容器
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧导航
        nav_frame = tk.Frame(main_container, bg="#f5f5f5", width=180)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        nav_frame.pack_propagate(False)

        # 导航按钮
        nav_buttons = [
            ("个人信息", self.show_info),
            ("我的课程", self.show_my_courses),
            ("成绩录入", self.show_grade_input),
            ("学生管理", self.show_students),
            ("专业介绍", self.show_major_introduction),
            ("修改密码", self.change_password),
        ]

        for text, command in nav_buttons:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=("微软雅黑", 11),
                bg="#ffffff",
                fg="#333",
                width=15,
                height=2,
                cursor="hand2",
                relief=tk.FLAT,
                command=command,
            )
            btn.pack(pady=5, padx=10)

        # 右侧内容区域
        self.content_frame = tk.Frame(main_container, bg="white")
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
            bg="white",
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

        text_frame = tk.Frame(self.content_frame, bg="white")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(
            text_frame,
            font=("微软雅黑", 11),
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

    def show_info(self):
        """显示个人信息"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="个人信息",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        info_frame = tk.Frame(self.content_frame, bg="white")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        info_items = [
            ("工号", self.teacher_info.get('teacher_id')),
            ("姓名", self.teacher_info.get('name')),
            ("性别", self.teacher_info.get('gender')),
            ("出生日期", self.teacher_info.get('birth_date')),
            ("院系", self.teacher_info.get('department')),
            ("职称", self.teacher_info.get('title')),
            ("电话", self.teacher_info.get('phone')),
            ("邮箱", self.teacher_info.get('email')),
            ("办公室", self.teacher_info.get('office')),
            ("入职日期", self.teacher_info.get('hire_date')),
        ]

        for label, value in info_items:
            row_frame = tk.Frame(info_frame, bg="white")
            row_frame.pack(fill=tk.X, pady=8)

            tk.Label(
                row_frame,
                text=f"{label}:",
                font=("微软雅黑", 12, "bold"),
                bg="white",
                width=12,
                anchor="w",
            ).pack(side=tk.LEFT)

            tk.Label(
                row_frame,
                text=str(value) if value else "未填写",
                font=("微软雅黑", 12),
                bg="white",
                anchor="w",
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

    # ==================== 我的课程 ====================

    def show_my_courses(self):
        """显示我的课程（通过服务器）"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="我的课程",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        btn_frame = tk.Frame(self.content_frame, bg="white")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            btn_frame,
            text="查看选课学生",
            font=("微软雅黑", 11),
            bg="#2196F3",
            fg="white",
            width=12,
            cursor="hand2",
            command=self.view_course_students,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="刷新",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.load_my_courses,
        ).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self.content_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = (
            "course_id",
            "course_name",
            "credits",
            "hours",
            "semester",
            "time",
            "classroom",
            "capacity",
            "enrolled",
        )
        self.course_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        headers = [
            "课程编号",
            "课程名称",
            "学分",
            "学时",
            "学期",
            "上课时间",
            "教室",
            "容量",
            "已选人数",
        ]
        widths = [90, 130, 60, 60, 90, 140, 90, 60, 80]

        for col, header, width in zip(columns, headers, widths):
            self.course_tree.heading(col, text=header)
            self.course_tree.column(col, width=width, anchor="center")

        self.course_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.course_tree.yview)

        self.load_my_courses()

    def load_my_courses(self):
        """加载我的课程（通过服务器）"""
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)

        resp = self.client.get_teacher_courses(self.teacher_info['teacher_id'])
        if not resp.get('success'):
            messagebox.showerror("错误", resp.get('message', '获取课程失败'))
            return

        courses = resp['data'].get('courses', [])
        self.course_list = courses

        for course in courses:
            self.course_tree.insert(
                "",
                tk.END,
                values=(
                    course.get('course_id'),
                    course.get('course_name'),
                    course.get('credits'),
                    course.get('hours'),
                    course.get('semester'),
                    course.get('class_time'),
                    course.get('classroom'),
                    course.get('capacity'),
                    course.get('enrolled_count', 0),
                ),
            )

    def view_course_students(self):
        """查看课程选课学生（通过服务器）"""
        selection = self.course_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择课程！")
            return

        item = self.course_tree.item(selection[0])
        course_id = item['values'][0]
        course_name = item['values'][1]

        student_win = tk.Toplevel(self.root)
        student_win.title(f"{course_name} - 选课学生")
        student_win.geometry("800x500")

        tk.Label(
            student_win,
            text=f"{course_name} - 选课学生列表",
            font=("微软雅黑", 14, "bold"),
        ).pack(pady=10)

        tree_frame = tk.Frame(student_win)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("student_id", "name", "class_name", "enrollment_date")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        headers = ["学号", "姓名", "班级", "选课日期"]
        widths = [120, 100, 150, 180]

        for col, header, width in zip(columns, headers, widths):
            tree.heading(col, text=header)
            tree.column(col, width=width, anchor="center")

        tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=tree.yview)

        resp = self.client.get_course_students(course_id)
        if not resp.get('success'):
            messagebox.showerror("错误", resp.get('message', '获取学生列表失败'))
            student_win.destroy()
            return

        students = resp['data'].get('students', [])
        for student in students:
            tree.insert(
                "",
                tk.END,
                values=(
                    student.get('student_id'),
                    student.get('name'),
                    student.get('class_name'),
                    student.get('enrollment_date'),
                ),
            )

        tk.Label(
            student_win,
            text=f"共 {len(students)} 名学生选课",
            font=("微软雅黑", 11),
        ).pack(pady=10)

    # ==================== 成绩录入 ====================

    def show_grade_input(self):
        """显示成绩录入（通过服务器）"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="成绩录入",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        select_frame = tk.Frame(self.content_frame, bg="white")
        select_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            select_frame,
            text="选择课程:",
            font=("微软雅黑", 12),
            bg="white",
        ).pack(side=tk.LEFT, padx=10)

        self.course_combo = ttk.Combobox(
            select_frame,
            font=("微软雅黑", 11),
            width=30,
            state="readonly",
        )
        self.course_combo.pack(side=tk.LEFT, padx=10)

        # 加载课程列表
        resp = self.client.get_teacher_courses(self.teacher_info['teacher_id'])
        if not resp.get('success'):
            messagebox.showerror("错误", resp.get('message', '获取课程失败'))
            return
        courses = resp['data'].get('courses', [])
        self.course_list = courses
        self.course_combo['values'] = [
            f"{c.get('course_id')} - {c.get('course_name')}" for c in courses
        ]

        tk.Button(
            select_frame,
            text="加载学生",
            font=("微软雅黑", 11),
            bg="#2196F3",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.load_course_students,
        ).pack(side=tk.LEFT, padx=10)

        tree_frame = tk.Frame(self.content_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("student_id", "name", "class_name", "usual", "exam", "final", "level")
        self.grade_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        headers = ["学号", "姓名", "班级", "平时成绩", "考试成绩", "总评成绩", "等级"]
        widths = [100, 80, 120, 80, 80, 80, 80]

        for col, header, width in zip(columns, headers, widths):
            self.grade_tree.heading(col, text=header)
            self.grade_tree.column(col, width=width, anchor="center")

        self.grade_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.grade_tree.yview)

        btn_frame = tk.Frame(self.content_frame, bg="white")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            btn_frame,
            text="录入/编辑成绩",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=15,
            cursor="hand2",
            command=self.edit_grade,
        ).pack(side=tk.LEFT, padx=5)

        def show_course_grade_distribution():
            """显示当前选中课程的成绩分布直方图"""
            if not getattr(self, "current_course_grades", None):
                messagebox.showwarning("提示", "请先选择课程并加载学生成绩！")
                return

            course_name = getattr(self, "current_course_name", "课程")
            show_visual(
                parent=self.root,
                role="teacher",
                chart_type="course_grade_histogram",
                data={
                    "course_name": course_name,
                    "grades": self.current_course_grades,
                },
            )

        tk.Button(
            btn_frame,
            text="成绩分布分析",
            font=("微软雅黑", 11),
            bg="#2196F3",
            fg="white",
            width=15,
            cursor="hand2",
            command=show_course_grade_distribution,
        ).pack(side=tk.LEFT, padx=5)

    def load_course_students(self):
        """加载课程学生及成绩（通过服务器）"""
        if not self.course_combo.get():
            messagebox.showwarning("提示", "请先选择课程！")
            return

        index = self.course_combo.current()
        course = self.course_list[index]
        course_id = course.get('course_id')

        for item in self.grade_tree.get_children():
            self.grade_tree.delete(item)

        # 获取选课学生
        resp_students = self.client.get_course_students(course_id)
        if not resp_students.get('success'):
            messagebox.showerror("错误", resp_students.get('message', '获取学生失败'))
            return
        students = resp_students['data'].get('students', [])

        # 获取成绩
        resp_grades = self.client.get_course_grades(course_id)
        if not resp_grades.get('success'):
            messagebox.showerror("错误", resp_grades.get('message', '获取成绩失败'))
            return
        grades = resp_grades['data'].get('grades', [])
        grades_dict = {g.get('student_id'): g for g in grades}

        # 缓存当前课程和其成绩，供可视化使用
        self.current_course_grades = grades
        self.current_course_name = course.get('course_name')

        for student in students:
            sid = student.get('student_id')
            grade = grades_dict.get(sid, {})
            usual = grade.get('usual_score')
            exam = grade.get('exam_score')
            final_score = grade.get('final_score')

            self.grade_tree.insert(
                "",
                tk.END,
                values=(
                    sid,
                    student.get('name'),
                    student.get('class_name'),
                    f"{usual:.1f}" if usual is not None else "-",
                    f"{exam:.1f}" if exam is not None else "-",
                    f"{final_score:.1f}" if final_score is not None else "-",
                    grade.get('grade_level', '-'),
                ),
            )

    def edit_grade(self):
        """编辑成绩（通过服务器）"""
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

        index = self.course_combo.current()
        course = self.course_list[index]

        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"录入成绩 - {student_name}")
        edit_win.geometry("400x300")

        tk.Label(
            edit_win,
            text=f"学生：{student_name} ({student_id})",
            font=("微软雅黑", 12, "bold"),
        ).pack(pady=20)

        tk.Label(
            edit_win,
            text=f"课程：{course.get('course_name')}",
            font=("微软雅黑", 11),
        ).pack(pady=5)

        input_frame = tk.Frame(edit_win)
        input_frame.pack(pady=20)

        tk.Label(
            input_frame,
            text="平时成绩:",
            font=("微软雅黑", 11),
            width=10,
        ).grid(row=0, column=0, pady=10, padx=10)

        usual_entry = ttk.Entry(input_frame, font=("微软雅黑", 11), width=15)
        usual_entry.grid(row=0, column=1, pady=10, padx=10)
        if usual_score != "-":
            usual_entry.insert(0, usual_score)

        tk.Label(
            input_frame,
            text="考试成绩:",
            font=("微软雅黑", 11),
            width=10,
        ).grid(row=1, column=0, pady=10, padx=10)

        exam_entry = ttk.Entry(input_frame, font=("微软雅黑", 11), width=15)
        exam_entry.grid(row=1, column=1, pady=10, padx=10)
        if exam_score != "-":
            exam_entry.insert(0, exam_score)

        def submit():
            try:
                usual = float(usual_entry.get().strip())
                exam = float(exam_entry.get().strip())

                if not (0 <= usual <= 100 and 0 <= exam <= 100):
                    messagebox.showerror("错误", "成绩必须在0-100之间！")
                    return

                grade_data = {
                    'student_id': student_id,
                    'course_id': course.get('course_id'),
                    'usual_score': usual,
                    'exam_score': exam,
                    'semester': course.get('semester'),
                }

                resp = self.client.add_or_update_grade(grade_data)
                if resp.get('success'):
                    messagebox.showinfo("成功", resp.get('message', '成绩录入成功'))
                    edit_win.destroy()
                    self.load_course_students()
                else:
                    messagebox.showerror("错误", resp.get('message', '成绩录入失败'))
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字！")

        tk.Button(
            edit_win,
            text="提交",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=15,
            cursor="hand2",
            command=submit,
        ).pack(pady=20)

    # ==================== 学生管理（通过服务器） ====================

    def show_students(self):
        """显示学生管理（网络版）"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="学生管理",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        search_frame = tk.Frame(self.content_frame, bg="white")
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            search_frame,
            text="搜索:",
            font=("微软雅黑", 11),
            bg="white",
        ).pack(side=tk.LEFT, padx=5)

        search_entry = ttk.Entry(search_frame, font=("微软雅黑", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self.content_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = (
            "student_id",
            "name",
            "gender",
            "major",
            "grade",
            "class",
            "phone",
            "courses",
        )
        self.student_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        headers = ["学号", "姓名", "性别", "专业", "年级", "班级", "电话", "选课课程"]
        widths = [100, 80, 60, 120, 60, 80, 110, 200]

        for col, header, width in zip(columns, headers, widths):
            self.student_tree.heading(col, text=header)
            self.student_tree.column(col, width=width, anchor="center")

        self.student_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.student_tree.yview)

        def load_and_filter():
            resp = self.client.get_teacher_students(self.teacher_info['teacher_id'])
            if not resp.get('success'):
                messagebox.showerror("错误", resp.get('message', '获取学生列表失败'))
                return
            all_students = resp['data'].get('students', [])

            keyword = search_entry.get().strip()
            if keyword:
                students = [
                    s for s in all_students
                    if keyword in s.get('student_id', '')
                    or keyword in s.get('name', '')
                    or keyword in s.get('major', '')
                ]
            else:
                students = all_students

            for item in self.student_tree.get_children():
                self.student_tree.delete(item)

            for s in students:
                self.student_tree.insert(
                    "",
                    tk.END,
                    values=(
                        s.get('student_id'),
                        s.get('name'),
                        s.get('gender'),
                        s.get('major'),
                        s.get('grade'),
                        s.get('class_name'),
                        s.get('phone'),
                        s.get('courses', '-'),
                    ),
                )

        tk.Button(
            search_frame,
            text="搜索",
            font=("微软雅黑", 11),
            bg="#2196F3",
            fg="white",
            width=8,
            cursor="hand2",
            command=load_and_filter,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            search_frame,
            text="显示全部",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=8,
            cursor="hand2",
            command=lambda: (search_entry.delete(0, tk.END), load_and_filter()),
        ).pack(side=tk.LEFT, padx=5)

        # 初始加载
        load_and_filter()

    # ==================== 修改密码（通过服务器） ====================

    def change_password(self):
        """修改密码（网络版）"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="修改密码",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=30)

        input_frame = tk.Frame(self.content_frame, bg="white")
        input_frame.pack(expand=True)

        tk.Label(
            input_frame,
            text="旧密码:",
            font=("微软雅黑", 12),
            bg="white",
            width=10,
            anchor="w",
        ).grid(row=0, column=0, pady=10, padx=10)

        old_pwd_entry = ttk.Entry(input_frame, font=("微软雅黑", 11), width=25, show="●")
        old_pwd_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(
            input_frame,
            text="新密码:",
            font=("微软雅黑", 12),
            bg="white",
            width=10,
            anchor="w",
        ).grid(row=1, column=0, pady=10, padx=10)

        new_pwd_entry = ttk.Entry(input_frame, font=("微软雅黑", 11), width=25, show="●")
        new_pwd_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(
            input_frame,
            text="确认密码:",
            font=("微软雅黑", 12),
            bg="white",
            width=10,
            anchor="w",
        ).grid(row=2, column=0, pady=10, padx=10)

        confirm_pwd_entry = ttk.Entry(input_frame, font=("微软雅黑", 11), width=25, show="●")
        confirm_pwd_entry.grid(row=2, column=1, pady=10, padx=10)

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

            resp = self.client.change_password(
                self.user_info['username'], old_pwd, new_pwd
            )
            if resp.get('success'):
                messagebox.showinfo("成功", resp.get('message', '密码修改成功！请重新登录。'))
                self.logout()
            else:
                messagebox.showerror("错误", resp.get('message', '旧密码错误或修改失败！'))

        tk.Button(
            input_frame,
            text="提交",
            font=("微软雅黑", 12),
            bg="#2196F3",
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            command=submit,
        ).grid(row=3, column=0, columnspan=2, pady=30)

    def load_info(self):
        """加载初始信息"""
        self.show_info()

    def logout(self):
        """注销并返回登录窗口"""
        if messagebox.askyesno("确认", "确定要注销并返回登录界面吗？"):
            try:
                self.root.destroy()
            except Exception:
                pass
            try:
                self.login_root.deiconify()
            except Exception:
                pass


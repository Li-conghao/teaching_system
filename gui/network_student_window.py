import tkinter as tk
from tkinter import ttk, messagebox

import os

from visualization.visualization_core import show_visual


class NetworkStudentWindow:
    """学生主界面（网络模式）"""

    def __init__(self, user_info, login_root, client):
        self.user_info = user_info
        self.login_root = login_root
        self.client = client

        # 通过网络获取学生信息
        resp = self.client.get_student_info(self.user_info['user_id'])
        if not resp.get('success') or not resp.get('data') or not resp['data'].get('student'):
            messagebox.showerror("错误", resp.get('message', '无法获取学生信息！'))
            self.login_root.deiconify()
            return

        self.student_info = resp['data']['student']

        # 创建主窗口
        self.root = tk.Toplevel()
        self.root.title(f"本科教学管理系统 - 网络学生端 [{self.student_info['name']}]")
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
        top_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)

        # 标题
        tk.Label(
            top_frame,
            text=f"欢迎：{self.student_info['name']} ({self.student_info['student_id']})",
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
            ("我的课程", self.show_courses),
            ("选课管理", self.show_enrollment),
            ("我的成绩", self.show_grades),
            ("专业介绍", self.show_major_introduction),
            ("师资介绍", self.show_faculty_introduction),
            ("修改密码", self.change_password_placeholder),
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
            bg="white",
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

    def show_faculty_introduction(self):
        """显示师资介绍（图片列表，双击打开）"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="师资介绍",
            font=("微软雅黑", 18, "bold"),
            bg="white",
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

        list_frame = tk.Frame(self.content_frame, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(
            list_frame,
            text="双击图片文件名可打开查看",
            font=("微软雅黑", 11),
            bg="white",
            fg="#666",
        ).pack(anchor='w', pady=(0, 10))

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        lb = tk.Listbox(list_frame, font=("微软雅黑", 11), yscrollcommand=scrollbar.set)
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

        tk.Label(
            self.content_frame,
            text="个人信息",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        info_frame = tk.Frame(self.content_frame, bg="white")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        info_items = [
            ("学号", self.student_info.get('student_id')),
            ("姓名", self.student_info.get('name')),
            ("性别", self.student_info.get('gender')),
            ("出生日期", self.student_info.get('birth_date')),
            ("专业", self.student_info.get('major')),
            ("年级", self.student_info.get('grade')),
            ("班级", self.student_info.get('class_name')),
            ("电话", self.student_info.get('phone')),
            ("邮箱", self.student_info.get('email')),
            ("地址", self.student_info.get('address')),
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

    def show_courses(self):
        """显示我的课程"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="我的课程",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        btn_frame = tk.Frame(self.content_frame, bg="white")
        btn_frame.pack(fill=tk.X, padx=20, pady=(10, 0))

        tree_frame = tk.Frame(self.content_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("course_id", "course_name", "teacher", "credits", "time", "classroom")
        self.course_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        headers = ["课程编号", "课程名称", "任课教师", "学分", "上课时间", "教室"]
        widths = [100, 150, 100, 80, 180, 100]

        for col, header, width in zip(columns, headers, widths):
            self.course_tree.heading(col, text=header)
            self.course_tree.column(col, width=width, anchor="center")

        self.course_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.course_tree.yview)

        # 从服务器加载已选课程
        resp = self.client.get_student_courses(self.student_info['student_id'])
        if not resp.get('success'):
            messagebox.showerror("错误", resp.get('message', '获取课程失败'))
            return

        courses = resp['data'].get('courses', [])

        def show_credit_radar_chart():
            if not courses:
                messagebox.showwarning("提示", "当前暂无选课，无法生成学分雷达图！")
                return
            show_visual(
                parent=self.root,
                role="student",
                chart_type="credit_radar",
                data={"courses": courses},
            )

        tk.Button(
            btn_frame,
            text="学分雷达图",
            font=("微软雅黑", 11),
            bg="#2196F3",
            fg="white",
            width=14,
            cursor="hand2",
            command=show_credit_radar_chart,
        ).pack(side=tk.LEFT, padx=5)

        for enroll in courses:
            self.course_tree.insert(
                "",
                tk.END,
                values=(
                    enroll.get('course_id'),
                    enroll.get('course_name'),
                    enroll.get('teacher_name'),
                    enroll.get('credits'),
                    enroll.get('class_time'),
                    enroll.get('classroom'),
                ),
            )

    def show_enrollment(self):
        """显示选课管理"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="选课管理",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        btn_frame = tk.Frame(self.content_frame, bg="white")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            btn_frame,
            text="选课",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.enroll_course,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="退课",
            font=("微软雅黑", 11),
            bg="#f44336",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.drop_course,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="刷新",
            font=("微软雅黑", 11),
            bg="#2196F3",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.load_available_courses,
        ).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self.content_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("course_id", "course_name", "teacher", "credits", "capacity", "enrolled")
        self.enroll_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        headers = ["课程编号", "课程名称", "任课教师", "学分", "容量", "已选人数"]
        widths = [100, 150, 100, 80, 80, 100]

        for col, header, width in zip(columns, headers, widths):
            self.enroll_tree.heading(col, text=header)
            self.enroll_tree.column(col, width=width, anchor="center")

        self.enroll_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.enroll_tree.yview)

        self.load_available_courses()

    def load_available_courses(self):
        """加载可选课程（通过服务器）"""
        for item in self.enroll_tree.get_children():
            self.enroll_tree.delete(item)

        # 所有课程
        resp_all = self.client.get_all_courses()
        if not resp_all.get('success'):
            messagebox.showerror("错误", resp_all.get('message', '获取课程列表失败'))
            return
        all_courses = resp_all['data'].get('courses', [])

        # 已选课程
        resp_enrolled = self.client.get_student_courses(self.student_info['student_id'])
        if not resp_enrolled.get('success'):
            messagebox.showerror("错误", resp_enrolled.get('message', '获取已选课程失败'))
            return
        enrolled_courses = resp_enrolled['data'].get('courses', [])
        enrolled_ids = {c.get('course_id') for c in enrolled_courses}

        # 已修课程（成绩表里出现过的课程）
        resp_grades = self.client.get_student_grades(self.student_info['student_id'])
        if not resp_grades.get('success'):
            messagebox.showerror("错误", resp_grades.get('message', '获取成绩失败'))
            return
        grade_rows = resp_grades.get('data', {}).get('grades', [])
        taken_ids = {g.get('course_id') for g in grade_rows}

        for course in all_courses:
            cid = course.get('course_id')
            if cid and cid not in enrolled_ids and cid not in taken_ids:
                self.enroll_tree.insert(
                    "",
                    tk.END,
                    values=(
                        course.get('course_id'),
                        course.get('course_name'),
                        course.get('teacher_name') or "待定",
                        course.get('credits'),
                        course.get('capacity'),
                        course.get('enrolled_count'),
                    ),
                )

    def enroll_course(self):
        """选课（通过服务器）"""
        selection = self.enroll_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要选的课程！")
            return

        item = self.enroll_tree.item(selection[0])
        course_id = item['values'][0]
        course_name = item['values'][1]

        if not messagebox.askyesno("确认", f"确定要选 {course_name} 吗？"):
            return

        resp = self.client.enroll_course(self.student_info['student_id'], course_id)
        if resp.get('success'):
            messagebox.showinfo("成功", resp.get('message', '选课成功'))
            self.load_available_courses()
        else:
            messagebox.showerror("失败", resp.get('message', '选课失败'))

    def drop_course(self):
        """退课（通过服务器）"""
        drop_win = tk.Toplevel(self.root)
        drop_win.title("退课")
        drop_win.geometry("700x400")

        tk.Label(
            drop_win,
            text="选择要退的课程",
            font=("微软雅黑", 14, "bold"),
        ).pack(pady=10)

        tree_frame = tk.Frame(drop_win)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("course_id", "course_name", "teacher")
        drop_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        for col, header in zip(columns, ["课程编号", "课程名称", "任课教师"]):
            drop_tree.heading(col, text=header)
            drop_tree.column(col, width=150, anchor="center")

        drop_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=drop_tree.yview)

        # 已选课程
        resp = self.client.get_student_courses(self.student_info['student_id'])
        if not resp.get('success'):
            messagebox.showerror("错误", resp.get('message', '获取已选课程失败'))
            drop_win.destroy()
            return
        enrolled = resp['data'].get('courses', [])

        for enroll in enrolled:
            drop_tree.insert(
                "",
                tk.END,
                values=(
                    enroll.get('course_id'),
                    enroll.get('course_name'),
                    enroll.get('teacher_name'),
                ),
            )

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

            resp_drop = self.client.drop_course(self.student_info['student_id'], course_id)
            if resp_drop.get('success'):
                messagebox.showinfo("成功", resp_drop.get('message', '退课成功'))
                drop_win.destroy()
                self.load_available_courses()
            else:
                messagebox.showerror("失败", resp_drop.get('message', '退课失败'))

        tk.Button(
            drop_win,
            text="确认退课",
            font=("微软雅黑", 11),
            bg="#f44336",
            fg="white",
            width=15,
            cursor="hand2",
            command=confirm_drop,
        ).pack(pady=10)

    def show_grades(self):
        """显示成绩（通过服务器）"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="我的成绩",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        tree_frame = tk.Frame(self.content_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("course_name", "teacher", "usual", "exam", "final", "level", "semester")
        self.grade_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        headers = ["课程名称", "任课教师", "平时成绩", "考试成绩", "总评成绩", "等级", "学期"]
        widths = [150, 100, 80, 80, 80, 80, 100]

        for col, header, width in zip(columns, headers, widths):
            self.grade_tree.heading(col, text=header)
            self.grade_tree.column(col, width=width, anchor="center")

        self.grade_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.grade_tree.yview)

        resp = self.client.get_student_grades(self.student_info['student_id'])
        if not resp.get('success'):
            messagebox.showerror("错误", resp.get('message', '获取成绩失败'))
            return

        grades = resp['data'].get('grades', [])

        # 按钮：成绩成长曲线（学期平均成绩变化）
        def show_score_trend():
            show_visual(
                parent=self.root,
                role="student",
                chart_type="personal_score_trend",
                data={"grades": grades},
            )

        btn_frame = tk.Frame(self.content_frame, bg="white")
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Button(
            btn_frame,
            text="成绩成长曲线",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=14,
            cursor="hand2",
            command=show_score_trend,
        ).pack(side=tk.LEFT, padx=5)
        total_score = 0
        count = 0

        for grade in grades:
            final_score = grade.get('final_score')
            usual_score = grade.get('usual_score')
            exam_score = grade.get('exam_score')

            self.grade_tree.insert(
                "",
                tk.END,
                values=(
                    grade.get('course_name'),
                    grade.get('teacher_name'),
                    f"{usual_score:.1f}" if usual_score is not None else "-",
                    f"{exam_score:.1f}" if exam_score is not None else "-",
                    f"{final_score:.1f}" if final_score is not None else "-",
                    grade.get('grade_level'),
                    grade.get('semester'),
                ),
            )

            if final_score is not None:
                total_score += final_score
                count += 1

        if count > 0:
            avg_score = total_score / count
            tk.Label(
                self.content_frame,
                text=f"平均分: {avg_score:.2f}",
                font=("微软雅黑", 12, "bold"),
                bg="white",
                fg="#2196F3",
            ).pack(pady=10)

    def change_password_placeholder(self):
        """修改密码占位（暂未实现网络接口）"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="修改密码功能暂未在网络模式下开放，请使用本地模式或联系管理员。",
            font=("微软雅黑", 12),
            bg="white",
            fg="#f57c00",
            wraplength=600,
            justify="left",
        ).pack(pady=40)

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


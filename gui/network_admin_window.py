import tkinter as tk
from tkinter import ttk, messagebox

import os

from visualization.visualization_core import show_visual


class NetworkAdminWindow:
    """管理员主界面（网络模式，数据通过 Client 获取）"""

    def __init__(self, user_info, login_root, client):
        self.user_info = user_info
        self.login_root = login_root
        self.client = client

        self.root = tk.Toplevel()
        self.root.title(f"本科教学管理系统 - 网络管理员端 [{self.user_info['username']}]")
        self.root.geometry("1200x800")

        self.root.protocol("WM_DELETE_WINDOW", self.logout)

        self.create_widgets()
        self.show_dashboard()

    def create_widgets(self):
        """创建界面组件"""
        top_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)

        tk.Label(
            top_frame,
            text=f"网络管理员控制台 - {self.user_info['username']}",
            font=("微软雅黑", 16, "bold"),
            bg="#2196F3",
            fg="white",
        ).pack(side=tk.LEFT, padx=20)

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

        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        nav_frame = tk.Frame(main_container, bg="#f5f5f5", width=180)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        nav_frame.pack_propagate(False)

        nav_buttons = [
            ("数据总览", self.show_dashboard),
            ("学生管理", self.show_student_management),
            ("教师管理", self.show_teacher_management),
            ("课程管理", self.show_course_management),
            ("专业介绍", self.show_major_introduction_management),
            ("师资介绍", self.show_faculty_introduction),
            ("系统日志", self.show_logs),
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

        self.content_frame = tk.Frame(main_container, bg="white")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _get_project_root(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _list_major_files(self):
        base_dir = os.path.join(self._get_project_root(), 'bupt_news_content')
        if not os.path.isdir(base_dir):
            return []
        files = [fn for fn in os.listdir(base_dir) if fn.lower().endswith('.txt')]
        files.sort()
        return [os.path.join(base_dir, fn) for fn in files]

    def show_major_introduction_management(self):
        """管理员查看全部专业介绍（网络模式：内容本地读取）"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="专业介绍",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        files = self._list_major_files()
        if not files:
            messagebox.showinfo("提示", "未找到 bupt_news_content 专业介绍文件")
            return

        container = tk.Frame(self.content_frame, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left = tk.Frame(container, bg="white", width=260)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        right = tk.Frame(container, bg="white")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(
            left,
            text="文件列表",
            font=("微软雅黑", 12, "bold"),
            bg="white",
        ).pack(anchor='w', pady=(0, 10))

        lb_scroll = ttk.Scrollbar(left)
        lb_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        lb = tk.Listbox(left, font=("微软雅黑", 11), yscrollcommand=lb_scroll.set)
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        lb_scroll.config(command=lb.yview)

        display_names = [os.path.basename(p) for p in files]
        for n in display_names:
            lb.insert(tk.END, n)

        tk.Label(
            right,
            text="内容预览",
            font=("微软雅黑", 12, "bold"),
            bg="white",
        ).pack(anchor='w', pady=(0, 10))

        text_frame = tk.Frame(right, bg="white")
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_scroll = ttk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(
            text_frame,
            font=("微软雅黑", 11),
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set,
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_scroll.config(command=text_widget.yview)

        def _load_selected(_event=None):
            sel = lb.curselection()
            if not sel:
                return
            path = files[sel[0]]
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                messagebox.showerror("错误", f"读取文件失败: {e}")
                return

            text_widget.config(state=tk.NORMAL)
            text_widget.delete('1.0', tk.END)
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)

        lb.bind('<<ListboxSelect>>', _load_selected)
        if display_names:
            lb.selection_set(0)
            _load_selected()

    def show_faculty_introduction(self):
        """管理员查看师资介绍（网络模式：图片列表本地读取）"""
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

    # ==================== 数据总览 ====================

    def show_dashboard(self):
        """显示数据总览（通过网络获取统计和成绩分布）"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="数据总览",
            font=("微软雅黑", 20, "bold"),
            bg="white",
        ).pack(pady=20)

        # 统计数据
        stats_resp = self.client.get_statistics()
        if not stats_resp.get('success'):
            messagebox.showerror("错误", stats_resp.get('message', '获取统计数据失败'))
            return
        stats = stats_resp['data'].get('statistics', {})

        cards_frame = tk.Frame(self.content_frame, bg="white")
        cards_frame.pack(pady=20)

        cards = [
            ("学生总数", stats.get('total_students', 0), "#4CAF50"),
            ("教师总数", stats.get('total_teachers', 0), "#2196F3"),
            ("课程总数", stats.get('total_courses', 0), "#FF9800"),
        ]

        for i, (title, value, color) in enumerate(cards):
            card = tk.Frame(cards_frame, bg=color, width=250, height=150)
            card.grid(row=0, column=i, padx=20, pady=10)
            card.pack_propagate(False)

            tk.Label(
                card,
                text=title,
                font=("微软雅黑", 14),
                bg=color,
                fg="white",
            ).pack(pady=20)

            tk.Label(
                card,
                text=str(value),
                font=("微软雅黑", 36, "bold"),
                bg=color,
                fg="white",
            ).pack()

        # 成绩分布
        tk.Label(
            self.content_frame,
            text="成绩分布统计",
            font=("微软雅黑", 16, "bold"),
            bg="white",
        ).pack(pady=(30, 10))

        dist_resp = self.client.get_grade_distribution()
        if not dist_resp.get('success'):
            messagebox.showerror("错误", dist_resp.get('message', '获取成绩分布失败'))
            return

        dist_list = dist_resp['data'].get('distribution', [])
        distribution = {item['grade_level']: item['count'] for item in dist_list}

        # 可视化按钮区域
        btn_frame = tk.Frame(self.content_frame, bg="white")
        btn_frame.pack(pady=(0, 10))

        def show_grade_distribution_chart():
            # 使用统一可视化接口绘制全校成绩等级分布柱状图
            show_visual(
                parent=self.root,
                role="admin",
                chart_type="grade_distribution",
                data={"distribution": distribution},
            )

        def show_statistics_overview_chart():
            # 使用统一可视化接口绘制学生/教师/课程数量对比图
            show_visual(
                parent=self.root,
                role="admin",
                chart_type="statistics_overview",
                data={"statistics": stats},
            )

        def show_resource_heatmap_chart():
            resp = self.client.get_all_courses()
            if not resp.get('success'):
                messagebox.showerror("错误", resp.get('message', '获取课程数据失败'))
                return
            courses = resp['data'].get('courses', [])
            show_visual(
                parent=self.root,
                role="admin",
                chart_type="resource_heatmap",
                data={"courses": courses},
            )

        tk.Button(
            btn_frame,
            text="成绩分布柱状图",
            font=("微软雅黑", 11),
            bg="#2196F3",
            fg="white",
            width=14,
            cursor="hand2",
            command=show_grade_distribution_chart,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="数据总览对比图",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=14,
            cursor="hand2",
            command=show_statistics_overview_chart,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="资源利用率热力图",
            font=("微软雅黑", 11),
            bg="#FF9800",
            fg="white",
            width=16,
            cursor="hand2",
            command=show_resource_heatmap_chart,
        ).pack(side=tk.LEFT, padx=5)

        dist_frame = tk.Frame(self.content_frame, bg="white")
        dist_frame.pack(fill=tk.X, padx=50, pady=20)

        colors = {
            '优秀': '#4CAF50',
            '良好': '#2196F3',
            '中等': '#FF9800',
            '及格': '#FFC107',
            '不及格': '#f44336',
        }

        total = sum(distribution.values()) or 1

        for level, count in distribution.items():
            item_frame = tk.Frame(dist_frame, bg="white")
            item_frame.pack(fill=tk.X, pady=5)

            tk.Label(
                item_frame,
                text=f"{level}:",
                font=("微软雅黑", 12),
                bg="white",
                width=10,
                anchor="w",
            ).pack(side=tk.LEFT, padx=10)

            canvas = tk.Canvas(
                item_frame, width=400, height=30, bg="white", highlightthickness=0
            )
            canvas.pack(side=tk.LEFT, padx=10)

            width = int(400 * count / total)
            canvas.create_rectangle(0, 5, width, 25, fill=colors.get(level, '#999'), outline="")

            tk.Label(
                item_frame,
                text=f"{count} 人",
                font=("微软雅黑", 12),
                bg="white",
            ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            self.content_frame,
            text=f"平均分: {stats.get('average_score', 0)}",
            font=("微软雅黑", 14, "bold"),
            bg="white",
            fg="#2196F3",
        ).pack(pady=20)

    # ==================== 学生管理（增删改查，网络模式） ====================

    def show_student_management(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="学生管理",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        # 工具栏
        toolbar = tk.Frame(self.content_frame, bg="white")
        toolbar.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            toolbar,
            text="搜索:",
            font=("微软雅黑", 11),
            bg="white",
        ).pack(side=tk.LEFT, padx=5)

        search_entry = ttk.Entry(toolbar, font=("微软雅黑", 11), width=25)
        search_entry.pack(side=tk.LEFT, padx=5)

        def search_students():
            keyword = search_entry.get().strip()
            if keyword:
                resp = self.client.search_students(keyword)
            else:
                resp = self.client.get_all_students()
            if not resp.get('success'):
                messagebox.showerror("错误", resp.get('message', '搜索学生失败'))
                return
            students = resp['data'].get('students', [])
            self.load_students(students)

        tk.Button(
            toolbar,
            text="搜索",
            font=("微软雅黑", 10),
            bg="#2196F3",
            fg="white",
            width=8,
            cursor="hand2",
            command=search_students,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="添加学生",
            font=("微软雅黑", 10),
            bg="#4CAF50",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.add_student,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="编辑",
            font=("微软雅黑", 10),
            bg="#FF9800",
            fg="white",
            width=8,
            cursor="hand2",
            command=self.edit_student,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="删除",
            font=("微软雅黑", 10),
            bg="#f44336",
            fg="white",
            width=8,
            cursor="hand2",
            command=self.delete_student,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="刷新",
            font=("微软雅黑", 10),
            bg="#9E9E9E",
            fg="white",
            width=8,
            cursor="hand2",
            command=lambda: self.load_students(),
        ).pack(side=tk.LEFT, padx=5)

        # 学生列表
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
            "class_name",
            "phone",
            "email",
        )
        self.student_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        headers = ["学号", "姓名", "性别", "专业", "年级", "班级", "电话", "邮箱"]
        widths = [100, 80, 60, 150, 60, 80, 110, 160]

        for col, header, width in zip(columns, headers, widths):
            self.student_tree.heading(col, text=header)
            self.student_tree.column(col, width=width, anchor="center")

        self.student_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.student_tree.yview)

        self.load_students()

    def load_students(self, students=None):
        """加载学生数据到树形视图（可传入现成列表，否则从服务器获取）"""
        if students is None:
            resp = self.client.get_all_students()
            if not resp.get('success'):
                messagebox.showerror("错误", resp.get('message', '获取学生数据失败'))
                return
            students = resp['data'].get('students', [])

        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        for stu in students:
            self.student_tree.insert(
                "",
                tk.END,
                values=(
                    stu.get('student_id'),
                    stu.get('name'),
                    stu.get('gender'),
                    stu.get('major'),
                    stu.get('grade'),
                    stu.get('class_name'),
                    stu.get('phone'),
                    stu.get('email'),
                ),
            )

    def add_student(self):
        """添加学生（管理员，通过网络接口）"""
        add_win = tk.Toplevel(self.root)
        add_win.title("添加学生")
        add_win.geometry("550x750")

        tk.Label(
            add_win,
            text="添加学生信息",
            font=("微软雅黑", 14, "bold"),
        ).pack(pady=15)

        input_frame = tk.Frame(add_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        fields = [
            ("学号", "student_id"),
            ("用户名", "username"),
            ("密码", "password"),
            ("姓名", "name"),
            ("性别", "gender"),
            ("出生日期", "birth_date"),
            ("专业", "major"),
            ("年级", "grade"),
            ("班级", "class_name"),
            ("电话", "phone"),
            ("邮箱", "email"),
            ("地址", "address"),
            ("入学日期", "enrollment_date"),
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(
                input_frame,
                text=f"{label}:",
                font=("微软雅黑", 10),
                width=10,
                anchor="w",
            ).grid(row=i, column=0, pady=8, padx=5, sticky="w")

            if key == "gender":
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=["男", "女"],
                    state="readonly",
                )
                combo.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = combo
            elif key == "password":
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30, show="●")
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30)
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry

        def submit():
            try:
                username = entries["username"].get().strip()
                password = entries["password"].get().strip()

                if not username or not password:
                    messagebox.showerror("错误", "用户名和密码不能为空！")
                    return

                student_data = {
                    "student_id": entries["student_id"].get().strip(),
                    "name": entries["name"].get().strip(),
                    "gender": entries["gender"].get(),
                    "birth_date": entries["birth_date"].get().strip(),
                    "major": entries["major"].get().strip(),
                    "grade": int(entries["grade"].get().strip()) if entries["grade"].get().strip() else None,
                    "class_name": entries["class_name"].get().strip(),
                    "phone": entries["phone"].get().strip(),
                    "email": entries["email"].get().strip(),
                    "address": entries["address"].get().strip(),
                    "enrollment_date": entries["enrollment_date"].get().strip(),
                }

                resp = self.client.add_student(student_data, username, password)
                if resp.get('success'):
                    messagebox.showinfo("成功", resp.get('message', '学生添加成功！'))
                    add_win.destroy()
                    self.load_students()
                else:
                    messagebox.showerror("错误", resp.get('message', '学生添加失败！'))
            except ValueError as e:
                messagebox.showerror("错误", f"输入格式错误: {e}")
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {e}")

        tk.Button(
            add_win,
            text="提交",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=15,
            cursor="hand2",
            command=submit,
        ).pack(pady=15)

    def edit_student(self):
        """编辑学生（管理员，通过网络接口）"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要编辑的学生！")
            return

        item = self.student_tree.item(selection[0])
        values = item["values"]

        edit_win = tk.Toplevel(self.root)
        edit_win.title("编辑学生信息")
        edit_win.geometry("500x550")

        tk.Label(
            edit_win,
            text=f"编辑学生: {values[0]}",
            font=("微软雅黑", 14, "bold"),
        ).pack(pady=15)

        input_frame = tk.Frame(edit_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        fields = [
            ("姓名", "name", values[1]),
            ("性别", "gender", values[2]),
            ("专业", "major", values[3]),
            ("年级", "grade", values[4]),
            ("班级", "class", values[5]),
            ("电话", "phone", values[6]),
            ("邮箱", "email", values[7]),
        ]

        entries = {}
        for i, (label, key, value) in enumerate(fields):
            tk.Label(
                input_frame,
                text=f"{label}:",
                font=("微软雅黑", 10),
                width=10,
                anchor="w",
            ).grid(row=i, column=0, pady=10, padx=5, sticky="w")

            if key == "gender":
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=["男", "女"],
                    state="readonly",
                )
                combo.set(value)
                combo.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = combo
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30)
                entry.insert(0, value)
                entry.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = entry

        def submit():
            try:
                student_data = {
                    "name": entries["name"].get().strip(),
                    "gender": entries["gender"].get(),
                    "birth_date": "",  # 简化，不在此处修改
                    "major": entries["major"].get().strip(),
                    "grade": int(entries["grade"].get().strip()),
                    "class_name": entries["class"].get().strip(),
                    "phone": entries["phone"].get().strip(),
                    "email": entries["email"].get().strip(),
                    "address": "",  # 简化
                }

                resp = self.client.update_student(values[0], student_data)
                if resp.get('success'):
                    messagebox.showinfo("成功", resp.get('message', '学生信息更新成功！'))
                    edit_win.destroy()
                    self.load_students()
                else:
                    messagebox.showerror("错误", resp.get('message', '更新失败！'))
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {e}")

        tk.Button(
            edit_win,
            text="保存",
            font=("微软雅黑", 11),
            bg="#2196F3",
            fg="white",
            width=15,
            cursor="hand2",
            command=submit,
        ).pack(pady=15)

    def delete_student(self):
        """删除学生（管理员，通过网络接口）"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要删除的学生！")
            return

        item = self.student_tree.item(selection[0])
        student_id = item["values"][0]
        student_name = item["values"][1]

        if not messagebox.askyesno("确认", f"确定要删除学生 {student_name} ({student_id}) 吗？\n此操作将删除该学生的所有相关数据！"):
            return

        resp = self.client.delete_student(student_id)
        if resp.get('success'):
            messagebox.showinfo("成功", resp.get('message', '学生删除成功！'))
            self.load_students()
        else:
            messagebox.showerror("错误", resp.get('message', '删除失败！'))

    # ==================== 教师管理（增删改查，网络模式） ====================

    def show_teacher_management(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="教师管理",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        # 工具栏
        toolbar = tk.Frame(self.content_frame, bg="white")
        toolbar.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            toolbar,
            text="添加教师",
            font=("微软雅黑", 10),
            bg="#4CAF50",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.add_teacher,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="编辑",
            font=("微软雅黑", 10),
            bg="#FF9800",
            fg="white",
            width=8,
            cursor="hand2",
            command=self.edit_teacher,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="删除",
            font=("微软雅黑", 10),
            bg="#f44336",
            fg="white",
            width=8,
            cursor="hand2",
            command=self.delete_teacher,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="刷新",
            font=("微软雅黑", 10),
            bg="#2196F3",
            fg="white",
            width=8,
            cursor="hand2",
            command=lambda: self.load_teachers(),
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            toolbar,
            text="搜索:",
            font=("微软雅黑", 10),
            bg="white",
        ).pack(side=tk.LEFT, padx=(20, 5))

        self.teacher_search_var = tk.StringVar()
        search_entry = ttk.Entry(
            toolbar,
            textvariable=self.teacher_search_var,
            font=("微软雅黑", 10),
            width=20,
        )
        search_entry.pack(side=tk.LEFT, padx=5)

        def search_teachers():
            keyword = self.teacher_search_var.get().strip()
            if not keyword:
                self.load_teachers()
                return
            resp = self.client.search_teachers(keyword)
            if not resp.get('success'):
                messagebox.showerror("错误", resp.get('message', '搜索教师失败'))
                return
            teachers = resp['data'].get('teachers', [])
            self.load_teachers(teachers)

        tk.Button(
            toolbar,
            text="搜索",
            font=("微软雅黑", 10),
            bg="#607D8B",
            fg="white",
            width=8,
            cursor="hand2",
            command=search_teachers,
        ).pack(side=tk.LEFT, padx=5)

        # 教师列表
        tree_frame = tk.Frame(self.content_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = (
            "teacher_id",
            "name",
            "gender",
            "department",
            "title",
            "phone",
            "email",
            "office",
        )
        self.teacher_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        headers = ["工号", "姓名", "性别", "院系", "职称", "电话", "邮箱", "办公室"]
        widths = [90, 80, 50, 150, 80, 110, 140, 100]

        for col, header, width in zip(columns, headers, widths):
            self.teacher_tree.heading(col, text=header)
            self.teacher_tree.column(col, width=width, anchor="center")

        self.teacher_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.teacher_tree.yview)

        self.load_teachers()

    def load_teachers(self, teachers=None):
        if teachers is None:
            resp = self.client.get_all_teachers()
            if not resp.get('success'):
                messagebox.showerror("错误", resp.get('message', '获取教师数据失败'))
                return
            teachers = resp['data'].get('teachers', [])

        for item in self.teacher_tree.get_children():
            self.teacher_tree.delete(item)

        for t in teachers:
            self.teacher_tree.insert(
                "",
                tk.END,
                values=(
                    t.get('teacher_id'),
                    t.get('name'),
                    t.get('gender'),
                    t.get('department'),
                    t.get('title'),
                    t.get('phone'),
                    t.get('email'),
                    t.get('office'),
                ),
            )

    def add_teacher(self):
        """添加教师（管理员，通过网络接口）"""
        add_win = tk.Toplevel(self.root)
        add_win.title("添加教师")
        add_win.geometry("500x650")

        tk.Label(
            add_win,
            text="添加教师信息",
            font=("微软雅黑", 14, "bold"),
        ).pack(pady=15)

        input_frame = tk.Frame(add_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        fields = [
            ("工号", "teacher_id"),
            ("用户名", "username"),
            ("密码", "password"),
            ("姓名", "name"),
            ("性别", "gender"),
            ("出生日期", "birth_date"),
            ("院系", "department"),
            ("职称", "title"),
            ("电话", "phone"),
            ("邮箱", "email"),
            ("办公室", "office"),
            ("入职日期", "hire_date"),
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(
                input_frame,
                text=f"{label}:",
                font=("微软雅黑", 10),
                width=10,
                anchor="w",
            ).grid(row=i, column=0, pady=8, padx=5, sticky="w")

            if key == "gender":
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=["男", "女"],
                    state="readonly",
                )
                combo.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = combo
            elif key == "title":
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=["教授", "副教授", "讲师", "助教"],
                    state="readonly",
                )
                combo.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = combo
            elif key == "password":
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30, show="●")
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30)
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry

        def submit():
            try:
                username = entries["username"].get().strip()
                password = entries["password"].get().strip()

                if not username or not password:
                    messagebox.showerror("错误", "用户名和密码不能为空！")
                    return

                teacher_data = {
                    "teacher_id": entries["teacher_id"].get().strip(),
                    "name": entries["name"].get().strip(),
                    "gender": entries["gender"].get(),
                    "birth_date": entries["birth_date"].get().strip(),
                    "department": entries["department"].get().strip(),
                    "title": entries["title"].get(),
                    "phone": entries["phone"].get().strip(),
                    "email": entries["email"].get().strip(),
                    "office": entries["office"].get().strip(),
                    "hire_date": entries["hire_date"].get().strip(),
                }

                resp = self.client.add_teacher(teacher_data, username, password)
                if resp.get('success'):
                    messagebox.showinfo("成功", resp.get('message', '教师添加成功！'))
                    add_win.destroy()
                    self.load_teachers()
                else:
                    messagebox.showerror("错误", resp.get('message', '教师添加失败！'))
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {e}")

        tk.Button(
            add_win,
            text="提交",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=15,
            cursor="hand2",
            command=submit,
        ).pack(pady=15)

    def edit_teacher(self):
        """编辑教师（管理员，通过网络接口）"""
        selection = self.teacher_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要编辑的教师！")
            return

        item = self.teacher_tree.item(selection[0])
        values = item["values"]

        edit_win = tk.Toplevel(self.root)
        edit_win.title("编辑教师信息")
        edit_win.geometry("500x550")

        tk.Label(
            edit_win,
            text=f"编辑教师: {values[0]}",
            font=("微软雅黑", 14, "bold"),
        ).pack(pady=15)

        input_frame = tk.Frame(edit_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        fields = [
            ("姓名", "name", values[1]),
            ("性别", "gender", values[2]),
            ("院系", "department", values[3]),
            ("职称", "title", values[4]),
            ("电话", "phone", values[5]),
            ("邮箱", "email", values[6]),
            ("办公室", "office", values[7]),
        ]

        entries = {}
        for i, (label, key, value) in enumerate(fields):
            tk.Label(
                input_frame,
                text=f"{label}:",
                font=("微软雅黑", 10),
                width=10,
                anchor="w",
            ).grid(row=i, column=0, pady=10, padx=5, sticky="w")

            if key == "gender":
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=["男", "女"],
                    state="readonly",
                )
                combo.set(value)
                combo.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = combo
            elif key == "title":
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=["教授", "副教授", "讲师", "助教"],
                    state="readonly",
                )
                combo.set(value)
                combo.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = combo
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30)
                entry.insert(0, value)
                entry.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = entry

        def submit():
            try:
                teacher_data = {
                    "name": entries["name"].get().strip(),
                    "gender": entries["gender"].get(),
                    "department": entries["department"].get().strip(),
                    "title": entries["title"].get(),
                    "phone": entries["phone"].get().strip(),
                    "email": entries["email"].get().strip(),
                    "office": entries["office"].get().strip(),
                }

                resp = self.client.update_teacher(values[0], teacher_data)
                if resp.get('success'):
                    messagebox.showinfo("成功", resp.get('message', '教师信息更新成功！'))
                    edit_win.destroy()
                    self.load_teachers()
                else:
                    messagebox.showerror("错误", resp.get('message', '更新失败！'))
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {e}")

        tk.Button(
            edit_win,
            text="保存",
            font=("微软雅黑", 11),
            bg="#2196F3",
            fg="white",
            width=15,
            cursor="hand2",
            command=submit,
        ).pack(pady=15)

    def delete_teacher(self):
        """删除教师（管理员，通过网络接口）"""
        selection = self.teacher_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要删除的教师！")
            return

        item = self.teacher_tree.item(selection[0])
        teacher_id = item["values"][0]
        teacher_name = item["values"][1]

        if not messagebox.askyesno("确认", f"确定要删除教师 {teacher_name} ({teacher_id}) 吗？\n此操作将删除该教师的所有相关数据！"):
            return

        resp = self.client.delete_teacher(teacher_id)
        if resp.get('success'):
            messagebox.showinfo("成功", resp.get('message', '教师删除成功！'))
            self.load_teachers()
        else:
            messagebox.showerror("错误", resp.get('message', '删除失败！'))

    # ==================== 课程管理（增删改查，网络模式） ====================

    def show_course_management(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="课程管理",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        # 工具栏
        toolbar = tk.Frame(self.content_frame, bg="white")
        toolbar.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            toolbar,
            text="添加课程",
            font=("微软雅黑", 10),
            bg="#4CAF50",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.add_course,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="编辑",
            font=("微软雅黑", 10),
            bg="#FF9800",
            fg="white",
            width=8,
            cursor="hand2",
            command=self.edit_course,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="删除",
            font=("微软雅黑", 10),
            bg="#f44336",
            fg="white",
            width=8,
            cursor="hand2",
            command=self.delete_course,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="刷新",
            font=("微软雅黑", 10),
            bg="#2196F3",
            fg="white",
            width=8,
            cursor="hand2",
            command=lambda: self.load_courses(),
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            toolbar,
            text="搜索:",
            font=("微软雅黑", 10),
            bg="white",
        ).pack(side=tk.LEFT, padx=(20, 5))

        self.course_search_var = tk.StringVar()
        search_entry = ttk.Entry(
            toolbar,
            textvariable=self.course_search_var,
            font=("微软雅黑", 10),
            width=20,
        )
        search_entry.pack(side=tk.LEFT, padx=5)

        def search_courses():
            keyword = self.course_search_var.get().strip()
            if not keyword:
                self.load_courses()
                return
            resp = self.client.search_courses(keyword)
            if not resp.get('success'):
                messagebox.showerror("错误", resp.get('message', '搜索课程失败'))
                return
            courses = resp['data'].get('courses', [])
            self.load_courses(courses)

        tk.Button(
            toolbar,
            text="搜索",
            font=("微软雅黑", 10),
            bg="#607D8B",
            fg="white",
            width=8,
            cursor="hand2",
            command=search_courses,
        ).pack(side=tk.LEFT, padx=5)

        # 课程列表
        tree_frame = tk.Frame(self.content_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = (
            "course_id",
            "course_name",
            "teacher_name",
            "credits",
            "hours",
            "semester",
            "capacity",
            "enrolled",
            "status",
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
            "任课教师",
            "学分",
            "学时",
            "学期",
            "容量",
            "已选",
            "状态",
        ]
        widths = [90, 140, 90, 60, 60, 90, 60, 60, 70]

        for col, header, width in zip(columns, headers, widths):
            self.course_tree.heading(col, text=header)
            self.course_tree.column(col, width=width, anchor="center")

        self.course_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.course_tree.yview)

        self.load_courses()

    def load_courses(self, courses=None):
        if courses is None:
            resp = self.client.get_all_courses()
            if not resp.get('success'):
                messagebox.showerror("错误", resp.get('message', '获取课程数据失败'))
                return
            courses = resp['data'].get('courses', [])

        for item in self.course_tree.get_children():
            self.course_tree.delete(item)

        for c in courses:
            self.course_tree.insert(
                "",
                tk.END,
                values=(
                    c.get('course_id'),
                    c.get('course_name'),
                    c.get('teacher_name'),
                    c.get('credits'),
                    c.get('hours'),
                    c.get('semester'),
                    c.get('capacity'),
                    c.get('enrolled_count', 0),
                    c.get('status'),
                ),
            )

    def add_course(self):
        """添加课程（管理员，通过网络接口）"""
        add_win = tk.Toplevel(self.root)
        add_win.title("添加课程")
        add_win.geometry("500x600")

        tk.Label(
            add_win,
            text="添加课程信息",
            font=("微软雅黑", 14, "bold"),
        ).pack(pady=15)

        input_frame = tk.Frame(add_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        fields = [
            ("课程编号", "course_id"),
            ("课程名称", "course_name"),
            ("任课教师工号", "teacher_id"),
            ("学分", "credits"),
            ("学时", "hours"),
            ("学期", "semester"),
            ("上课时间", "class_time"),
            ("教室", "classroom"),
            ("容量", "capacity"),
            ("状态", "status"),
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(
                input_frame,
                text=f"{label}:",
                font=("微软雅黑", 10),
                width=12,
                anchor="w",
            ).grid(row=i, column=0, pady=8, padx=5, sticky="w")

            if key == "status":
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=26,
                    values=["open", "closed"],
                    state="readonly",
                )
                combo.set("open")
                combo.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = combo
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=28)
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry

        def submit():
            try:
                course_data = {
                    "course_id": entries["course_id"].get().strip(),
                    "course_name": entries["course_name"].get().strip(),
                    "teacher_id": entries["teacher_id"].get().strip() or None,
                    "credits": int(entries["credits"].get().strip()),
                    "hours": int(entries["hours"].get().strip()),
                    "semester": entries["semester"].get().strip(),
                    "class_time": entries["class_time"].get().strip(),
                    "classroom": entries["classroom"].get().strip(),
                    "capacity": int(entries["capacity"].get().strip() or 50),
                    "status": entries["status"].get() or "open",
                }

                resp = self.client.add_course(course_data)
                if resp.get('success'):
                    messagebox.showinfo("成功", resp.get('message', '课程添加成功！'))
                    add_win.destroy()
                    self.load_courses()
                else:
                    messagebox.showerror("错误", resp.get('message', '课程添加失败！'))
            except ValueError as e:
                messagebox.showerror("错误", f"输入格式错误: {e}")
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {e}")

        tk.Button(
            add_win,
            text="提交",
            font=("微软雅黑", 11),
            bg="#4CAF50",
            fg="white",
            width=15,
            cursor="hand2",
            command=submit,
        ).pack(pady=15)

    def edit_course(self):
        """编辑课程（管理员，通过网络接口）"""
        selection = self.course_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要编辑的课程！")
            return

        item = self.course_tree.item(selection[0])
        values = item["values"]

        edit_win = tk.Toplevel(self.root)
        edit_win.title("编辑课程信息")
        edit_win.geometry("500x550")

        tk.Label(
            edit_win,
            text=f"编辑课程: {values[0]}",
            font=("微软雅黑", 14, "bold"),
        ).pack(pady=15)

        input_frame = tk.Frame(edit_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        fields = [
            ("课程名称", "course_name", values[1]),
            ("任课教师工号", "teacher_id", ""),
            ("学分", "credits", values[3]),
            ("学时", "hours", values[4]),
            ("学期", "semester", values[5]),
            ("容量", "capacity", values[6]),
            ("状态", "status", values[8]),
        ]

        entries = {}
        for i, (label, key, value) in enumerate(fields):
            tk.Label(
                input_frame,
                text=f"{label}:",
                font=("微软雅黑", 10),
                width=12,
                anchor="w",
            ).grid(row=i, column=0, pady=8, padx=5, sticky="w")

            if key == "status":
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=26,
                    values=["open", "closed"],
                    state="readonly",
                )
                combo.set(value)
                combo.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = combo
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=28)
                if value is not None:
                    entry.insert(0, value)
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry

        def submit():
            try:
                course_data = {
                    "course_name": entries["course_name"].get().strip(),
                    "teacher_id": entries["teacher_id"].get().strip() or None,
                    "credits": int(entries["credits"].get().strip()),
                    "hours": int(entries["hours"].get().strip()),
                    "semester": entries["semester"].get().strip(),
                    "capacity": int(entries["capacity"].get().strip() or 50),
                    "status": entries["status"].get() or "open",
                    "class_time": None,
                    "classroom": None,
                }

                resp = self.client.update_course(values[0], course_data)
                if resp.get('success'):
                    messagebox.showinfo("成功", resp.get('message', '课程信息更新成功！'))
                    edit_win.destroy()
                    self.load_courses()
                else:
                    messagebox.showerror("错误", resp.get('message', '更新失败！'))
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {e}")

        tk.Button(
            edit_win,
            text="保存",
            font=("微软雅黑", 11),
            bg="#2196F3",
            fg="white",
            width=15,
            cursor="hand2",
            command=submit,
        ).pack(pady=15)

    def delete_course(self):
        """删除课程（管理员，通过网络接口）"""
        selection = self.course_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要删除的课程！")
            return

        item = self.course_tree.item(selection[0])
        course_id = item["values"][0]
        course_name = item["values"][1]

        if not messagebox.askyesno("确认", f"确定要删除课程 {course_name} ({course_id}) 吗？\n此操作将删除该课程的所有相关选课和成绩记录！"):
            return

        resp = self.client.delete_course(course_id)
        if resp.get('success'):
            messagebox.showinfo("成功", resp.get('message', '课程删除成功！'))
            self.load_courses()
        else:
            messagebox.showerror("错误", resp.get('message', '删除失败！'))

    # ==================== 系统日志 ====================

    def show_logs(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="系统日志",
            font=("微软雅黑", 18, "bold"),
            bg="white",
        ).pack(pady=20)

        toolbar = tk.Frame(self.content_frame, bg="white")
        toolbar.pack(fill=tk.X, padx=20, pady=5)

        tk.Button(
            toolbar,
            text="刷新",
            font=("微软雅黑", 10),
            bg="#2196F3",
            fg="white",
            width=8,
            cursor="hand2",
            command=self.load_logs,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="清空日志",
            font=("微软雅黑", 10),
            bg="#f44336",
            fg="white",
            width=8,
            cursor="hand2",
            command=self.clear_logs,
        ).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(self.content_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("timestamp", "username", "action", "description")
        self.log_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        headers = ["时间", "用户", "操作", "描述"]
        widths = [160, 100, 120, 500]

        for col, header, width in zip(columns, headers, widths):
            self.log_tree.heading(col, text=header)
            self.log_tree.column(col, width=width, anchor="w")

        self.log_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_tree.yview)

        self.load_logs()

    def load_logs(self):
        resp = self.client.get_logs(limit=200)
        if not resp.get('success'):
            messagebox.showerror("错误", resp.get('message', '获取日志失败'))
            return
        logs = resp['data'].get('logs', [])

        for item in self.log_tree.get_children():
            self.log_tree.delete(item)

        for log in logs:
            self.log_tree.insert(
                "",
                tk.END,
                values=(
                    log.get('timestamp'),
                    log.get('username'),
                    log.get('action'),
                    log.get('description'),
                ),
            )

    def clear_logs(self):
        if not messagebox.askyesno("确认", "确定要清空所有日志吗？"):
            return
        resp = self.client.clear_logs()
        if resp.get('success'):
            messagebox.showinfo("成功", resp.get('message', '日志已清空'))
            self.load_logs()
        else:
            messagebox.showerror("错误", resp.get('message', '清空日志失败'))

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



"""
管理员主界面模块
包含用户管理、学生管理、教师管理、课程管理、数据统计等功能
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from visualization.visualization_core import show_visual


class AdminWindow:
    """管理员主界面类"""
    
    def __init__(self, user_info, login_root):
        self.user_info = user_info
        self.login_root = login_root
        self.db = DatabaseManager()
        
        # 创建主窗口
        self.root = tk.Toplevel()
        self.root.title("本科教学管理系统 - 管理员端")
        self.root.geometry("1200x800")
        
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
        
        # 创建界面
        self.create_widgets()
        
        # 加载数据
        self.show_dashboard()
    
    def create_widgets(self):
        """创建界面组件"""
        # 顶部标题栏
        top_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        # 标题
        tk.Label(
            top_frame,
            text=f"管理员控制台 - {self.user_info['username']}",
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
            ("数据总览", self.show_dashboard),
            ("学生管理", self.show_student_management),
            ("教师管理", self.show_teacher_management),
            ("课程管理", self.show_course_management),
            ("成绩统计", self.show_grade_statistics),
            ("用户管理", self.show_user_management),
            ("专业介绍", self.show_major_introduction_management),
            ("师资介绍", self.show_faculty_introduction),
            ("系统日志", self.show_logs),
            ("数据导出", self.show_export),
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

    def _list_major_files(self):
        base_dir = os.path.join(self._get_project_root(), 'bupt_news_content')
        if not os.path.isdir(base_dir):
            return []
        files = [fn for fn in os.listdir(base_dir) if fn.lower().endswith('.txt')]
        files.sort()
        return [os.path.join(base_dir, fn) for fn in files]

    def show_major_introduction_management(self):
        """管理员查看全部专业介绍"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="专业介绍",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)

        files = self._list_major_files()
        if not files:
            messagebox.showinfo("提示", "未找到 bupt_news_content 专业介绍文件")
            return

        container = tk.Frame(self.content_frame, bg='white')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left = tk.Frame(container, bg='white', width=260)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        right = tk.Frame(container, bg='white')
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(
            left,
            text="文件列表",
            font=("微软雅黑", 12, "bold"),
            bg='white'
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
            bg='white'
        ).pack(anchor='w', pady=(0, 10))

        text_frame = tk.Frame(right, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_scroll = ttk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(
            text_frame,
            font=("微软雅黑", 11),
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set
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
        """管理员查看师资介绍（图片列表）"""
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
    
    def show_dashboard(self):
        """显示数据总览"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="数据总览",
            font=("微软雅黑", 20, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 获取统计数据
        stats = self.db.get_statistics()
        
        # 卡片容器
        cards_frame = tk.Frame(self.content_frame, bg='white')
        cards_frame.pack(pady=20)
        
        # 统计卡片（只保留学生、教师、课程三个）
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
                fg='white'
            ).pack(pady=20)
            
            tk.Label(
                card,
                text=str(value),
                font=("微软雅黑", 36, "bold"),
                bg=color,
                fg='white'
            ).pack()
        
        # 成绩分布
        tk.Label(
            self.content_frame,
            text="成绩分布统计",
            font=("微软雅黑", 16, "bold"),
            bg='white'
        ).pack(pady=(30, 10))
        
        # 获取成绩分布（列表 -> 字典）
        dist_list = self.db.get_grade_distribution()
        distribution = {item['grade_level']: item['count'] for item in dist_list}
        
        # 成绩分布框架
        dist_frame = tk.Frame(self.content_frame, bg='white')
        dist_frame.pack(fill=tk.X, padx=50, pady=20)
        
        colors = {
            '优秀': '#4CAF50',
            '良好': '#2196F3',
            '中等': '#FF9800',
            '及格': '#FFC107',
            '不及格': '#f44336'
        }
        
        for i, (level, count) in enumerate(distribution.items()):
            item_frame = tk.Frame(dist_frame, bg='white')
            item_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                item_frame,
                text=f"{level}:",
                font=("微软雅黑", 12),
                bg='white',
                width=10,
                anchor='w'
            ).pack(side=tk.LEFT, padx=10)
            
            # 进度条
            canvas = tk.Canvas(item_frame, width=400, height=30, bg='white', highlightthickness=0)
            canvas.pack(side=tk.LEFT, padx=10)
            
            total = sum(distribution.values())
            if total > 0:
                width = int(400 * count / total)
                canvas.create_rectangle(0, 5, width, 25, fill=colors[level], outline='')
            
            tk.Label(
                item_frame,
                text=f"{count} 人",
                font=("微软雅黑", 12),
                bg='white'
            ).pack(side=tk.LEFT, padx=10)
        
        # 平均分
        tk.Label(
            self.content_frame,
            text=f"平均分: {stats.get('average_score', 0)}",
            font=("微软雅黑", 14, "bold"),
            bg='white',
            fg='#2196F3'
        ).pack(pady=20)
        
        # 可视化按钮
        tk.Button(
            self.content_frame,
            text="查看详细图表",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.show_charts
        ).pack(pady=10)
    
    def show_charts(self):
        """显示数据可视化图表"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import matplotlib
            matplotlib.use('TkAgg')
            
            # 创建新窗口
            chart_win = tk.Toplevel(self.root)
            chart_win.title("数据可视化")
            chart_win.geometry("900x600")
            
            # 获取成绩分布数据
            distribution = self.db.get_grade_distribution()
            
            # 创建图表
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # 饼图
            labels = list(distribution.keys())
            sizes = list(distribution.values())
            colors = ['#4CAF50', '#2196F3', '#FF9800', '#FFC107', '#f44336']
            
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title('成绩分布饼图', fontproperties='SimHei', fontsize=14)
            
            # 柱状图
            ax2.bar(labels, sizes, color=colors)
            ax2.set_title('成绩分布柱状图', fontproperties='SimHei', fontsize=14)
            ax2.set_ylabel('人数', fontproperties='SimHei')
            ax2.set_xlabel('等级', fontproperties='SimHei')
            
            plt.tight_layout()
            
            # 嵌入到Tkinter窗口
            canvas = FigureCanvasTkAgg(fig, master=chart_win)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except ImportError:
            messagebox.showwarning("提示", "未安装matplotlib库，无法显示图表")
    
    def show_student_management(self):
        """显示学生管理"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="学生管理",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 工具栏
        toolbar = tk.Frame(self.content_frame, bg='white')
        toolbar.pack(fill=tk.X, padx=20, pady=10)
        
        # 搜索框
        tk.Label(
            toolbar,
            text="搜索:",
            font=("微软雅黑", 11),
            bg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        search_entry = ttk.Entry(toolbar, font=("微软雅黑", 11), width=25)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        def search_students():
            keyword = search_entry.get().strip()
            if keyword:
                students = self.db.search_students(keyword)
            else:
                students = self.db.get_all_students()
            self.load_students(students)
        
        tk.Button(
            toolbar,
            text="搜索",
            font=("微软雅黑", 10),
            bg='#2196F3',
            fg='white',
            width=8,
            cursor='hand2',
            command=search_students
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="添加学生",
            font=("微软雅黑", 10),
            bg='#4CAF50',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.add_student
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="编辑",
            font=("微软雅黑", 10),
            bg='#FF9800',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.edit_student
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="删除",
            font=("微软雅黑", 10),
            bg='#f44336',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.delete_student
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="刷新",
            font=("微软雅黑", 10),
            bg='#9E9E9E',
            fg='white',
            width=8,
            cursor='hand2',
            command=lambda: self.load_students(self.db.get_all_students())
        ).pack(side=tk.LEFT, padx=5)
        
        # 学生列表
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建树形视图
        columns = ('student_id', 'name', 'gender', 'major', 'grade', 'class', 'phone', 'email')
        self.student_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        # 设置列标题
        headers = ['学号', '姓名', '性别', '专业', '年级', '班级', '电话', '邮箱']
        widths = [100, 80, 50, 130, 60, 100, 110, 140]
        
        for col, header, width in zip(columns, headers, widths):
            self.student_tree.heading(col, text=header)
            self.student_tree.column(col, width=width, anchor='center')
        
        self.student_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.student_tree.yview)
        
        # 加载学生数据
        self.load_students(self.db.get_all_students())
    
    def load_students(self, students):
        """加载学生数据到树形视图"""
        # 清空现有数据
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        # 插入新数据
        for student in students:
            self.student_tree.insert('', tk.END, values=(
                student['student_id'],
                student['name'],
                student['gender'],
                student['major'],
                student['grade'],
                student['class_name'],
                student['phone'],
                student['email']
            ))
    
    def add_student(self):
        """添加学生"""
        add_win = tk.Toplevel(self.root)
        add_win.title("添加学生")
        add_win.geometry("550x750")
        
        tk.Label(
            add_win,
            text="添加学生信息",
            font=("微软雅黑", 14, "bold")
        ).pack(pady=15)
        
        # 输入框架
        input_frame = tk.Frame(add_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        fields = [
            ('学号', 'student_id'),
            ('用户名', 'username'),
            ('密码', 'password'),
            ('姓名', 'name'),
            ('性别', 'gender'),
            ('出生日期', 'birth_date'),
            ('专业', 'major'),
            ('年级', 'grade'),
            ('班级', 'class_name'),
            ('电话', 'phone'),
            ('邮箱', 'email'),
            ('地址', 'address'),
            ('入学日期', 'enrollment_date'),
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(
                input_frame,
                text=f"{label}:",
                font=("微软雅黑", 10),
                width=10,
                anchor='w'
            ).grid(row=i, column=0, pady=8, padx=5, sticky='w')
            
            if key == 'gender':
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=['男', '女'],
                    state='readonly'
                )
                combo.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = combo
            elif key == 'password':
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30, show='●')
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30)
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry
        
        # 提交按钮
        def submit():
            try:
                username = entries['username'].get().strip()
                password = entries['password'].get().strip()
                
                if not username or not password:
                    messagebox.showerror("错误", "用户名和密码不能为空！")
                    return
                
                student_data = {
                    'student_id': entries['student_id'].get().strip(),
                    'name': entries['name'].get().strip(),
                    'gender': entries['gender'].get(),
                    'birth_date': entries['birth_date'].get().strip(),
                    'major': entries['major'].get().strip(),
                    'grade': int(entries['grade'].get().strip()) if entries['grade'].get().strip() else None,
                    'class_name': entries['class_name'].get().strip(),
                    'phone': entries['phone'].get().strip(),
                    'email': entries['email'].get().strip(),
                    'address': entries['address'].get().strip(),
                    'enrollment_date': entries['enrollment_date'].get().strip(),
                }
                
                if self.db.add_student(student_data, username, password):
                    messagebox.showinfo("成功", "学生添加成功！")
                    add_win.destroy()
                    self.load_students(self.db.get_all_students())
                else:
                    messagebox.showerror("错误", "学生添加失败！可能学号或用户名已存在。")
            except ValueError as e:
                messagebox.showerror("错误", f"输入格式错误: {e}")
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {e}")
        
        tk.Button(
            add_win,
            text="提交",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=15,
            cursor='hand2',
            command=submit
        ).pack(pady=15)
    
    def edit_student(self):
        """编辑学生"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要编辑的学生！")
            return
        
        item = self.student_tree.item(selection[0])
        values = item['values']
        
        # 创建编辑窗口
        edit_win = tk.Toplevel(self.root)
        edit_win.title("编辑学生信息")
        edit_win.geometry("500x550")
        
        tk.Label(
            edit_win,
            text=f"编辑学生: {values[0]}",
            font=("微软雅黑", 14, "bold")
        ).pack(pady=15)
        
        # 输入框架
        input_frame = tk.Frame(edit_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        fields = [
            ('姓名', 'name', values[1]),
            ('性别', 'gender', values[2]),
            ('专业', 'major', values[3]),
            ('年级', 'grade', values[4]),
            ('班级', 'class', values[5]),
            ('电话', 'phone', values[6]),
            ('邮箱', 'email', values[7]),
        ]
        
        entries = {}
        for i, (label, key, value) in enumerate(fields):
            tk.Label(
                input_frame,
                text=f"{label}:",
                font=("微软雅黑", 10),
                width=10,
                anchor='w'
            ).grid(row=i, column=0, pady=10, padx=5, sticky='w')
            
            if key == 'gender':
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=['男', '女'],
                    state='readonly'
                )
                combo.set(value)
                combo.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = combo
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30)
                entry.insert(0, value)
                entry.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = entry
        
        # 提交按钮
        def submit():
            try:
                student_data = {
                    'name': entries['name'].get().strip(),
                    'gender': entries['gender'].get(),
                    'birth_date': '',  # 简化，不修改出生日期
                    'major': entries['major'].get().strip(),
                    'grade': int(entries['grade'].get().strip()),
                    'class_name': entries['class'].get().strip(),
                    'phone': entries['phone'].get().strip(),
                    'email': entries['email'].get().strip(),
                    'address': '',  # 简化
                }
                
                if self.db.update_student(values[0], student_data):
                    messagebox.showinfo("成功", "学生信息更新成功！")
                    edit_win.destroy()
                    self.load_students(self.db.get_all_students())
                else:
                    messagebox.showerror("错误", "更新失败！")
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {e}")
        
        tk.Button(
            edit_win,
            text="保存",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=15,
            cursor='hand2',
            command=submit
        ).pack(pady=15)
    
    def delete_student(self):
        """删除学生"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要删除的学生！")
            return
        
        item = self.student_tree.item(selection[0])
        student_id = item['values'][0]
        student_name = item['values'][1]
        
        if messagebox.askyesno("确认", f"确定要删除学生 {student_name} ({student_id}) 吗？\n此操作将删除该学生的所有相关数据！"):
            if self.db.delete_student(student_id):
                messagebox.showinfo("成功", "学生删除成功！")
                self.load_students(self.db.get_all_students())
            else:
                messagebox.showerror("错误", "删除失败！")
    
    def show_teacher_management(self):
        """显示教师管理"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="教师管理",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 工具栏
        toolbar = tk.Frame(self.content_frame, bg='white')
        toolbar.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            toolbar,
            text="添加教师",
            font=("微软雅黑", 10),
            bg='#4CAF50',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.add_teacher
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="编辑",
            font=("微软雅黑", 10),
            bg='#FF9800',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.edit_teacher
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="删除",
            font=("微软雅黑", 10),
            bg='#f44336',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.delete_teacher
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="刷新",
            font=("微软雅黑", 10),
            bg='#2196F3',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.load_teachers
        ).pack(side=tk.LEFT, padx=5)
        
        # 搜索框
        tk.Label(
            toolbar,
            text="搜索:",
            font=("微软雅黑", 10),
            bg='white'
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.teacher_search_var = tk.StringVar()
        search_entry = ttk.Entry(
            toolbar,
            textvariable=self.teacher_search_var,
            font=("微软雅黑", 10),
            width=20
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="搜索",
            font=("微软雅黑", 10),
            bg='#607D8B',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.search_teachers
        ).pack(side=tk.LEFT, padx=5)
        
        # 教师列表
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('teacher_id', 'name', 'gender', 'department', 'title', 'phone', 'email', 'office')
        self.teacher_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        headers = ['工号', '姓名', '性别', '院系', '职称', '电话', '邮箱', '办公室']
        widths = [90, 80, 50, 150, 80, 110, 140, 100]
        
        for col, header, width in zip(columns, headers, widths):
            self.teacher_tree.heading(col, text=header)
            self.teacher_tree.column(col, width=width, anchor='center')
        
        self.teacher_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.teacher_tree.yview)
        
        # 加载教师数据
        self.load_teachers()
    
    def load_teachers(self):
        """加载教师数据"""
        # 清空现有数据
        for item in self.teacher_tree.get_children():
            self.teacher_tree.delete(item)
        
        # 获取所有教师
        teachers = self.db.get_all_teachers()
        
        for teacher in teachers:
            self.teacher_tree.insert('', tk.END, values=(
                teacher['teacher_id'],
                teacher['name'],
                teacher['gender'],
                teacher['department'],
                teacher['title'],
                teacher['phone'],
                teacher['email'],
                teacher['office']
            ))
    
    def search_teachers(self):
        """搜索教师"""
        keyword = self.teacher_search_var.get().strip()
        if not keyword:
            self.load_teachers()
            return
        
        # 清空现有数据
        for item in self.teacher_tree.get_children():
            self.teacher_tree.delete(item)
        
        # 获取所有教师并过滤
        teachers = self.db.get_all_teachers()
        for teacher in teachers:
            if (keyword.lower() in teacher['teacher_id'].lower() or
                keyword in teacher['name'] or
                keyword in teacher['department']):
                self.teacher_tree.insert('', tk.END, values=(
                    teacher['teacher_id'],
                    teacher['name'],
                    teacher['gender'],
                    teacher['department'],
                    teacher['title'],
                    teacher['phone'],
                    teacher['email'],
                    teacher['office']
                ))
    
    def add_teacher(self):
        """添加教师"""
        add_win = tk.Toplevel(self.root)
        add_win.title("添加教师")
        add_win.geometry("500x650")
        
        tk.Label(
            add_win,
            text="添加教师信息",
            font=("微软雅黑", 14, "bold")
        ).pack(pady=15)
        
        # 输入框架
        input_frame = tk.Frame(add_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        fields = [
            ('工号', 'teacher_id'),
            ('用户名', 'username'),
            ('密码', 'password'),
            ('姓名', 'name'),
            ('性别', 'gender'),
            ('出生日期', 'birth_date'),
            ('院系', 'department'),
            ('职称', 'title'),
            ('电话', 'phone'),
            ('邮箱', 'email'),
            ('办公室', 'office'),
            ('入职日期', 'hire_date'),
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(
                input_frame,
                text=f"{label}:",
                font=("微软雅黑", 10),
                width=10,
                anchor='w'
            ).grid(row=i, column=0, pady=8, padx=5, sticky='w')
            
            if key == 'gender':
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=['男', '女'],
                    state='readonly'
                )
                combo.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = combo
            elif key == 'title':
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=['教授', '副教授', '讲师', '助教'],
                    state='readonly'
                )
                combo.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = combo
            elif key == 'password':
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30, show='●')
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30)
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry
        
        # 提交按钮
        def submit():
            try:
                username = entries['username'].get().strip()
                password = entries['password'].get().strip()
                
                if not username or not password:
                    messagebox.showerror("错误", "用户名和密码不能为空！")
                    return
                
                teacher_data = {
                    'teacher_id': entries['teacher_id'].get().strip(),
                    'name': entries['name'].get().strip(),
                    'gender': entries['gender'].get(),
                    'birth_date': entries['birth_date'].get().strip(),
                    'department': entries['department'].get().strip(),
                    'title': entries['title'].get(),
                    'phone': entries['phone'].get().strip(),
                    'email': entries['email'].get().strip(),
                    'office': entries['office'].get().strip(),
                    'hire_date': entries['hire_date'].get().strip(),
                }
                
                if self.db.add_teacher(teacher_data, username, password):
                    messagebox.showinfo("成功", "教师添加成功！")
                    add_win.destroy()
                    self.load_teachers()
                else:
                    messagebox.showerror("错误", "教师添加失败！可能工号或用户名已存在。")
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {e}")
        
        tk.Button(
            add_win,
            text="提交",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=15,
            cursor='hand2',
            command=submit
        ).pack(pady=15)
    
    def edit_teacher(self):
        """编辑教师"""
        selection = self.teacher_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要编辑的教师！")
            return
        
        item = self.teacher_tree.item(selection[0])
        values = item['values']
        
        # 创建编辑窗口
        edit_win = tk.Toplevel(self.root)
        edit_win.title("编辑教师信息")
        edit_win.geometry("500x550")
        
        tk.Label(
            edit_win,
            text=f"编辑教师: {values[0]}",
            font=("微软雅黑", 14, "bold")
        ).pack(pady=15)
        
        # 输入框架
        input_frame = tk.Frame(edit_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        fields = [
            ('姓名', 'name', values[1]),
            ('性别', 'gender', values[2]),
            ('院系', 'department', values[3]),
            ('职称', 'title', values[4]),
            ('电话', 'phone', values[5]),
            ('邮箱', 'email', values[6]),
            ('办公室', 'office', values[7]),
        ]
        
        entries = {}
        for i, (label, key, value) in enumerate(fields):
            tk.Label(
                input_frame,
                text=f"{label}:",
                font=("微软雅黑", 10),
                width=10,
                anchor='w'
            ).grid(row=i, column=0, pady=10, padx=5, sticky='w')
            
            if key == 'gender':
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=['男', '女'],
                    state='readonly'
                )
                combo.set(value)
                combo.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = combo
            elif key == 'title':
                combo = ttk.Combobox(
                    input_frame,
                    font=("微软雅黑", 10),
                    width=28,
                    values=['教授', '副教授', '讲师', '助教'],
                    state='readonly'
                )
                combo.set(value)
                combo.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = combo
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30)
                entry.insert(0, value)
                entry.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = entry
        
        # 提交按钮
        def submit():
            try:
                teacher_data = {
                    'name': entries['name'].get().strip(),
                    'gender': entries['gender'].get(),
                    'department': entries['department'].get().strip(),
                    'title': entries['title'].get(),
                    'phone': entries['phone'].get().strip(),
                    'email': entries['email'].get().strip(),
                    'office': entries['office'].get().strip(),
                }
                
                if self.db.update_teacher(values[0], teacher_data):
                    messagebox.showinfo("成功", "教师信息更新成功！")
                    edit_win.destroy()
                    self.load_teachers()
                else:
                    messagebox.showerror("错误", "更新失败！")
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {e}")
        
        tk.Button(
            edit_win,
            text="保存",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=15,
            cursor='hand2',
            command=submit
        ).pack(pady=15)
    
    def delete_teacher(self):
        """删除教师"""
        selection = self.teacher_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要删除的教师！")
            return
        
        item = self.teacher_tree.item(selection[0])
        teacher_id = item['values'][0]
        teacher_name = item['values'][1]
        
        if messagebox.askyesno("确认", f"确定要删除教师 {teacher_name} ({teacher_id}) 吗？\n此操作将删除该教师的所有相关数据！"):
            if self.db.delete_teacher(teacher_id):
                messagebox.showinfo("成功", "教师删除成功！")
                self.load_teachers()
            else:
                messagebox.showerror("错误", "删除失败！")
    
    def show_course_management(self):
        """显示课程管理"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="课程管理",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 工具栏
        toolbar = tk.Frame(self.content_frame, bg='white')
        toolbar.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            toolbar,
            text="添加课程",
            font=("微软雅黑", 10),
            bg='#4CAF50',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.add_course
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="编辑",
            font=("微软雅黑", 10),
            bg='#FF9800',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.edit_course
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="删除",
            font=("微软雅黑", 10),
            bg='#f44336',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.delete_course
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="刷新",
            font=("微软雅黑", 10),
            bg='#2196F3',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.load_courses
        ).pack(side=tk.LEFT, padx=5)
        
        # 搜索框
        tk.Label(
            toolbar,
            text="搜索:",
            font=("微软雅黑", 10),
            bg='white'
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.course_search_var = tk.StringVar()
        search_entry = ttk.Entry(
            toolbar,
            textvariable=self.course_search_var,
            font=("微软雅黑", 10),
            width=20
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="搜索",
            font=("微软雅黑", 10),
            bg='#607D8B',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.search_courses
        ).pack(side=tk.LEFT, padx=5)
        
        # 课程列表
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('course_id', 'course_name', 'teacher', 'credits', 'hours', 
                   'semester', 'capacity', 'enrolled', 'status')
        self.course_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        headers = ['课程编号', '课程名称', '任课教师', '学分', '学时', 
                   '学期', '容量', '已选', '状态']
        widths = [90, 140, 90, 60, 60, 90, 60, 60, 70]
        
        for col, header, width in zip(columns, headers, widths):
            self.course_tree.heading(col, text=header)
            self.course_tree.column(col, width=width, anchor='center')
        
        self.course_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.course_tree.yview)
        
        # 加载课程数据
        self.load_courses()
    
    def load_courses(self):
        """加载课程数据"""
        # 清空现有数据
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        # 获取所有课程
        courses = self.db.get_all_courses()
        
        for course in courses:
            self.course_tree.insert('', tk.END, values=(
                course['course_id'],
                course['course_name'],
                course.get('teacher_name', '待定'),
                course['credits'],
                course['hours'],
                course['semester'],
                course['capacity'],
                course.get('enrolled_count', 0),
                '开放' if course.get('status', 'open') == 'open' else '关闭'
            ))
    
    def search_courses(self):
        """搜索课程"""
        keyword = self.course_search_var.get().strip()
        if not keyword:
            self.load_courses()
            return
        
        # 清空现有数据
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        # 获取所有课程并过滤
        courses = self.db.get_all_courses()
        for course in courses:
            teacher_name = course.get('teacher_name', '')
            if (keyword.lower() in course['course_id'].lower() or
                keyword in course['course_name'] or
                (teacher_name and keyword in teacher_name)):
                self.course_tree.insert('', tk.END, values=(
                    course['course_id'],
                    course['course_name'],
                    teacher_name if teacher_name else '待定',
                    course['credits'],
                    course['hours'],
                    course['semester'],
                    course['capacity'],
                    course.get('enrolled_count', 0),
                    '开放' if course.get('status', 'open') == 'open' else '关闭'
                ))
    
    def add_course(self):
        """添加课程"""
        add_win = tk.Toplevel(self.root)
        add_win.title("添加课程")
        add_win.geometry("500x700")
        
        tk.Label(add_win, text="添加课程信息", font=("微软雅黑", 14, "bold")).pack(pady=15)
        
        input_frame = tk.Frame(add_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        teachers = self.db.get_all_teachers()
        teacher_options = ['待定'] + [f"{t['teacher_id']} - {t['name']}" for t in teachers]
        
        fields = [
            ('课程编号', 'course_id'), ('课程名称', 'course_name'), ('任课教师', 'teacher'),
            ('学分', 'credits'), ('学时', 'hours'), ('学期', 'semester'),
            ('上课时间', 'class_time'), ('教室', 'classroom'), ('容量', 'capacity'), ('状态', 'status')
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(input_frame, text=f"{label}:", font=("微软雅黑", 10), width=10, anchor='w').grid(row=i, column=0, pady=8, padx=5, sticky='w')
            
            if key == 'teacher':
                combo = ttk.Combobox(input_frame, font=("微软雅黑", 10), width=28, values=teacher_options, state='readonly')
                combo.current(0)
                combo.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = combo
            elif key == 'status':
                combo = ttk.Combobox(input_frame, font=("微软雅黑", 10), width=28, values=['开放', '关闭'], state='readonly')
                combo.current(0)
                combo.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = combo
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30)
                entry.grid(row=i, column=1, pady=8, padx=5)
                entries[key] = entry
        
        def submit():
            try:
                teacher_str = entries['teacher'].get()
                teacher_id = None if teacher_str == '待定' else teacher_str.split(' - ')[0]
                
                course_data = {
                    'course_id': entries['course_id'].get().strip(),
                    'course_name': entries['course_name'].get().strip(),
                    'teacher_id': teacher_id,
                    'credits': float(entries['credits'].get().strip()),
                    'hours': int(entries['hours'].get().strip()),
                    'semester': entries['semester'].get().strip(),
                    'class_time': entries['class_time'].get().strip(),
                    'classroom': entries['classroom'].get().strip(),
                    'capacity': int(entries['capacity'].get().strip()),
                    'status': 'open' if entries['status'].get() == '开放' else 'closed',
                }
                
                if self.db.add_course(course_data):
                    messagebox.showinfo("成功", "课程添加成功！")
                    add_win.destroy()
                    self.load_courses()
                else:
                    messagebox.showerror("错误", "课程添加失败！")
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {e}")
        
        tk.Button(add_win, text="提交", font=("微软雅黑", 11), bg='#4CAF50', fg='white', width=15, cursor='hand2', command=submit).pack(pady=15)
    
    def edit_course(self):
        """编辑课程"""
        selection = self.course_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要编辑的课程！")
            return
        
        item = self.course_tree.item(selection[0])
        values = item['values']
        
        edit_win = tk.Toplevel(self.root)
        edit_win.title("编辑课程信息")
        edit_win.geometry("500x600")
        
        tk.Label(edit_win, text=f"编辑课程: {values[0]}", font=("微软雅黑", 14, "bold")).pack(pady=15)
        
        input_frame = tk.Frame(edit_win)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        teachers = self.db.get_all_teachers()
        teacher_options = ['待定'] + [f"{t['teacher_id']} - {t['name']}" for t in teachers]
        
        fields = [
            ('课程名称', 'course_name', values[1]), ('任课教师', 'teacher', values[2]),
            ('学分', 'credits', values[3]), ('学时', 'hours', values[4]),
            ('学期', 'semester', values[5]), ('容量', 'capacity', values[6]), ('状态', 'status', values[8])
        ]
        
        entries = {}
        for i, (label, key, value) in enumerate(fields):
            tk.Label(input_frame, text=f"{label}:", font=("微软雅黑", 10), width=10, anchor='w').grid(row=i, column=0, pady=10, padx=5, sticky='w')
            
            if key == 'teacher':
                combo = ttk.Combobox(input_frame, font=("微软雅黑", 10), width=28, values=teacher_options, state='readonly')
                if value == '待定':
                    combo.current(0)
                else:
                    for idx, opt in enumerate(teacher_options):
                        if value in opt:
                            combo.current(idx)
                            break
                combo.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = combo
            elif key == 'status':
                combo = ttk.Combobox(input_frame, font=("微软雅黑", 10), width=28, values=['开放', '关闭'], state='readonly')
                combo.current(0 if value == '开放' else 1)
                combo.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = combo
            else:
                entry = ttk.Entry(input_frame, font=("微软雅黑", 10), width=30)
                entry.insert(0, value)
                entry.grid(row=i, column=1, pady=10, padx=5)
                entries[key] = entry
        
        def submit():
            try:
                teacher_str = entries['teacher'].get()
                teacher_id = None if teacher_str == '待定' else teacher_str.split(' - ')[0]
                
                course_data = {
                    'course_name': entries['course_name'].get().strip(),
                    'teacher_id': teacher_id,
                    'credits': float(entries['credits'].get().strip()),
                    'hours': int(entries['hours'].get().strip()),
                    'semester': entries['semester'].get().strip(),
                    'capacity': int(entries['capacity'].get().strip()),
                    'status': 'open' if entries['status'].get() == '开放' else 'closed',
                }
                
                if self.db.update_course(values[0], course_data):
                    messagebox.showinfo("成功", "课程信息更新成功！")
                    edit_win.destroy()
                    self.load_courses()
                else:
                    messagebox.showerror("错误", "更新失败！")
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {e}")
        
        tk.Button(edit_win, text="保存", font=("微软雅黑", 11), bg='#2196F3', fg='white', width=15, cursor='hand2', command=submit).pack(pady=15)
    
    def delete_course(self):
        """删除课程"""
        selection = self.course_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要删除的课程！")
            return
        
        item = self.course_tree.item(selection[0])
        course_id = item['values'][0]
        course_name = item['values'][1]
        
        if messagebox.askyesno("确认", f"确定要删除课程 {course_name} ({course_id}) 吗？"):
            if self.db.delete_course(course_id):
                messagebox.showinfo("成功", "课程删除成功！")
                self.load_courses()
            else:
                messagebox.showerror("错误", "删除失败！")
    
    def show_grade_statistics(self):
        """显示成绩统计"""
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="成绩统计分析",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)

        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tab_grade_class = tk.Frame(notebook, bg='white')
        tab_course_teacher = tk.Frame(notebook, bg='white')
        tab_fail_list = tk.Frame(notebook, bg='white')
        tab_major_rank = tk.Frame(notebook, bg='white')
        tab_semester_trend = tk.Frame(notebook, bg='white')

        notebook.add(tab_grade_class, text="年级-班级概览")
        notebook.add(tab_course_teacher, text="课程-教师分析")
        notebook.add(tab_fail_list, text="挂科名单")
        notebook.add(tab_major_rank, text="专业成绩排名")
        notebook.add(tab_semester_trend, text="学期趋势")

        top_frame_gc = tk.Frame(tab_grade_class, bg='white')
        top_frame_gc.pack(fill=tk.X, padx=20, pady=10)

        chart_container_gc = tk.Frame(tab_grade_class, bg='white')
        chart_container_gc.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self._gc_chart_canvas = None

        tk.Label(top_frame_gc, text="学期:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.semester_gc_var = tk.StringVar()
        semester_combo_gc = ttk.Combobox(top_frame_gc, textvariable=self.semester_gc_var, font=("微软雅黑", 11), width=12, state='readonly')
        semester_combo_gc.pack(side=tk.LEFT, padx=5)
        
        # 加载所有学期
        semester_values_gc = ["全部"]
        try:
            with self.db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT semester FROM grades WHERE semester IS NOT NULL AND semester <> '' ORDER BY semester DESC")
                semester_values_gc.extend([r[0] for r in cur.fetchall()])
        except Exception:
            pass
        semester_combo_gc['values'] = semester_values_gc
        if semester_values_gc:
            semester_combo_gc.current(0)

        tk.Label(top_frame_gc, text="年级:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        grade_values = []
        try:
            with self.db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT grade FROM students WHERE grade IS NOT NULL AND grade <> '' ORDER BY grade")
                rows = cur.fetchall()
                grade_values = [str(r[0]) for r in rows]
        except Exception:
            grade_values = []

        self.grade_gc_var = tk.StringVar()
        grade_combo_gc = ttk.Combobox(top_frame_gc, textvariable=self.grade_gc_var, font=("微软雅黑", 11), width=10, state='readonly', values=grade_values)
        grade_combo_gc.pack(side=tk.LEFT, padx=5)
        if grade_values:
            grade_combo_gc.current(0)

        def refresh_gc_grade_options(event=None):
            """学期改变后刷新年级下拉框（只显示该学期有成绩数据的年级）"""
            sel_semester = self.semester_gc_var.get().strip()
            current_grade = self.grade_gc_var.get().strip()

            grades = []
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    if sel_semester and sel_semester != "全部":
                        cur.execute(
                            """
                            SELECT DISTINCT s.grade
                            FROM students s
                            JOIN grades g ON s.student_id = g.student_id
                            WHERE g.semester = ? AND s.grade IS NOT NULL AND s.grade <> ''
                            ORDER BY s.grade
                            """,
                            (sel_semester,),
                        )
                    else:
                        cur.execute(
                            "SELECT DISTINCT grade FROM students WHERE grade IS NOT NULL AND grade <> '' ORDER BY grade"
                        )
                    grades = [str(r[0]) for r in cur.fetchall()]
            except Exception:
                grades = grade_values

            grade_combo_gc['values'] = grades
            if current_grade and current_grade in grades:
                self.grade_gc_var.set(current_grade)
            elif grades:
                self.grade_gc_var.set(grades[0])
            else:
                self.grade_gc_var.set("")

        semester_combo_gc.bind("<<ComboboxSelected>>", refresh_gc_grade_options)
        refresh_gc_grade_options()

        def on_show_grade_class_overview():
            import math
            grade = self.grade_gc_var.get().strip()
            semester = self.semester_gc_var.get().strip()
            
            if not grade:
                messagebox.showwarning("提示", "请先选择年级！")
                return
            class_stats = []
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    
                    conditions = ["s.grade = ?"]
                    params = [grade]
                    
                    if semester and semester != "全部":
                        conditions.append("g.semester = ?")
                        params.append(semester)
                        
                    where_clause = " AND ".join(conditions)
                    
                    sql = f"""
                        SELECT s.class_name,
                               s.major,
                               COUNT(DISTINCT s.student_id) AS student_count,
                               AVG(g.final_score) AS avg_score,
                               SUM(CASE WHEN g.final_score < 60 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS fail_rate,
                               SUM(CASE WHEN g.final_score >= 90 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS excellent_rate,
                               SUM(CASE WHEN g.final_score >= 80 AND g.final_score < 90 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS good_rate
                        FROM students s
                        JOIN grades g ON s.student_id = g.student_id
                        WHERE {where_clause}
                        GROUP BY s.class_name, s.major
                        ORDER BY s.class_name
                    """
                    
                    cur.execute(sql, params)
                    for row in cur.fetchall():
                        raw_avg = row[3] or 0
                        # 保留两位小数向下取整
                        avg_score = math.floor(raw_avg * 100) / 100
                        class_stats.append(
                            {
                                "class_name": row[0],
                                "major": row[1],
                                "student_count": row[2],
                                "avg_score": avg_score,
                                "fail_rate": row[4] or 0,
                                "excellent_rate": row[5] or 0,
                                "good_rate": row[6] or 0,
                            }
                        )
            except Exception as e:
                messagebox.showerror("错误", f"获取班级统计数据失败: {e}")
                return

            if not class_stats:
                messagebox.showinfo("提示", "所选年级暂无成绩数据。")
                return

            for widget in chart_container_gc.winfo_children():
                widget.destroy()

            labels = []
            avg_scores = []
            fail_rates = []
            for item in class_stats:
                cname = item.get("class_name") or ""
                if len(cname) > 2:
                    cname_display = cname[-2:]
                else:
                    cname_display = cname
                labels.append(cname_display)
                avg_scores.append(float(item.get("avg_score") or 0))
                fail_rates.append(float(item.get("fail_rate") or 0) * 100)

            if not labels:
                messagebox.showinfo("提示", "所选年级暂无可用班级数据。")
                return

            x = list(range(len(labels)))
            width = 0.35

            fig, ax1 = plt.subplots(figsize=(8, 4))
            bars1 = ax1.bar([i - width / 2 for i in x], avg_scores, width, label="平均成绩", color="#4CAF50")
            ax2 = ax1.twinx()
            bars2 = ax2.bar([i + width / 2 for i in x], fail_rates, width, label="挂科率(%)", color="#f44336")

            ax1.set_xticks(x)
            ax1.set_xticklabels(labels, rotation=45, ha="right")
            ax1.set_ylabel("平均成绩")
            ax2.set_ylabel("挂科率(%)")
            
            title_text = f"{grade} 级"
            if semester and semester != "全部":
                title_text += f" {semester}"
            title_text += " 各班级成绩与挂科率概览"
            ax1.set_title(title_text)

            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}", ha="center", va="bottom", fontsize=8)

            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}", ha="center", va="bottom", fontsize=8, color="#f44336")

            handles1, labels1 = ax1.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper right")

            fig.tight_layout()

            self._gc_chart_canvas = FigureCanvasTkAgg(fig, master=chart_container_gc)
            self._gc_chart_canvas.draw()
            self._gc_chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        tk.Button(
            top_frame_gc,
            text="查看班级统计柱状图",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=18,
            cursor='hand2',
            command=on_show_grade_class_overview,
        ).pack(side=tk.LEFT, padx=10)

        top_frame_ct = tk.Frame(tab_course_teacher, bg='white')
        top_frame_ct.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(top_frame_ct, text="学期:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.semester_ct_var = tk.StringVar()
        semester_combo_ct = ttk.Combobox(
            top_frame_ct,
            textvariable=self.semester_ct_var,
            font=("微软雅黑", 11),
            width=12,
            state='readonly'
        )
        semester_combo_ct.pack(side=tk.LEFT, padx=5)

        # 加载学期选项
        ct_semester_values = ["全部"]
        try:
            with self.db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT semester FROM courses WHERE semester IS NOT NULL AND semester <> '' ORDER BY semester DESC")
                ct_semester_values.extend([r[0] for r in cur.fetchall()])
        except Exception:
            pass
        semester_combo_ct['values'] = ct_semester_values
        if len(ct_semester_values) > 1:
            semester_combo_ct.current(1) # 默认选中最新的学期
        else:
            semester_combo_ct.current(0)

        tk.Label(top_frame_ct, text="课程:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        
        # 数据缓存
        self._ct_all_courses = []
        self._ct_all_teachers = []
        self._ct_course_to_teachers = {} # course_name -> set(teacher_label)
        self._ct_teacher_to_courses = {} # teacher_label -> set(course_name)
        self._teacher_id_map = {} # label -> id

        self.course_ct_var = tk.StringVar()
        course_combo_ct = ttk.Combobox(
            top_frame_ct,
            textvariable=self.course_ct_var,
            font=("微软雅黑", 11),
            width=20,
            state='readonly'
        )
        course_combo_ct.pack(side=tk.LEFT, padx=5)

        tk.Label(top_frame_ct, text="教师:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.teacher_ct_var = tk.StringVar()
        teacher_combo_ct = ttk.Combobox(
            top_frame_ct,
            textvariable=self.teacher_ct_var,
            font=("微软雅黑", 11),
            width=20,
            state='readonly'
        )
        teacher_combo_ct.pack(side=tk.LEFT, padx=5)

        def refresh_ct_relations(event=None):
            """根据选定的学期刷新课程和教师列表"""
            semester = self.semester_ct_var.get().strip()
            
            # 清空缓存
            self._ct_course_to_teachers = {}
            self._ct_teacher_to_courses = {}
            self._teacher_id_map = {}
            course_set = set()
            teacher_set = set()
            
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    sql = """
                        SELECT c.course_name, t.teacher_id, t.name
                        FROM courses c
                        JOIN teachers t ON c.teacher_id = t.teacher_id
                    """
                    params = []
                    if semester and semester != "全部":
                        sql += " WHERE c.semester = ?"
                        params.append(semester)
                    
                    cur.execute(sql, params)
                    relations = cur.fetchall()
                    
                    for cname, tid, tname in relations:
                        t_label = f"{tid} - {tname}"
                        self._teacher_id_map[t_label] = tid
                        
                        course_set.add(cname)
                        teacher_set.add(t_label)
                        
                        if cname not in self._ct_course_to_teachers:
                            self._ct_course_to_teachers[cname] = set()
                        self._ct_course_to_teachers[cname].add(t_label)
                        
                        if t_label not in self._ct_teacher_to_courses:
                            self._ct_teacher_to_courses[t_label] = set()
                        self._ct_teacher_to_courses[t_label].add(cname)
            except Exception as e:
                print(f"Error loading course-teacher data: {e}")
            
            self._ct_all_courses = sorted(list(course_set))
            self._ct_all_teachers = sorted(list(teacher_set))
            
            course_combo_ct['values'] = ["全部"] + self._ct_all_courses
            teacher_combo_ct['values'] = ["全部"] + self._ct_all_teachers
            
            self.course_ct_var.set("全部")
            self.teacher_ct_var.set("全部")

        semester_combo_ct.bind("<<ComboboxSelected>>", refresh_ct_relations)
        
        # 联动逻辑
        def on_course_select(event=None):
            sel_course = self.course_ct_var.get()
            current_teacher = self.teacher_ct_var.get()
            
            if sel_course == "全部":
                teacher_combo_ct['values'] = ["全部"] + self._ct_all_teachers
            else:
                valid_teachers = sorted(list(self._ct_course_to_teachers.get(sel_course, set())))
                teacher_combo_ct['values'] = ["全部"] + valid_teachers
                if current_teacher != "全部" and current_teacher not in valid_teachers:
                    teacher_combo_ct.current(0)

        def on_teacher_select(event=None):
            sel_teacher = self.teacher_ct_var.get()
            current_course = self.course_ct_var.get()
            
            if sel_teacher == "全部":
                course_combo_ct['values'] = ["全部"] + self._ct_all_courses
            else:
                valid_courses = sorted(list(self._ct_teacher_to_courses.get(sel_teacher, set())))
                course_combo_ct['values'] = ["全部"] + valid_courses
                if current_course != "全部" and current_course not in valid_courses:
                    course_combo_ct.current(0)

        course_combo_ct.bind("<<ComboboxSelected>>", on_course_select)
        teacher_combo_ct.bind("<<ComboboxSelected>>", on_teacher_select)
        
        # 初始化加载
        refresh_ct_relations()

        table_frame_ct = tk.Frame(tab_course_teacher, bg='white')
        table_frame_ct.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar_ct = ttk.Scrollbar(table_frame_ct)
        scrollbar_ct.pack(side=tk.RIGHT, fill=tk.Y)

        columns_ct = (
            'teacher_id',
            'teacher_name',
            'course_name',
            'total',
            'avg_score',
            'fail_rate',
            'excellent_rate',
            'good_rate',
        )
        self.course_teacher_tree = ttk.Treeview(
            table_frame_ct,
            columns=columns_ct,
            show='headings',
            yscrollcommand=scrollbar_ct.set,
        )
        headers_ct = ['教师工号', '教师姓名', '课程名称', '人数', '平均成绩', '挂科率', '优秀率', '良好率']
        widths_ct = [90, 90, 160, 60, 80, 80, 80, 80]
        for col, header, width in zip(columns_ct, headers_ct, widths_ct):
            self.course_teacher_tree.heading(col, text=header)
            self.course_teacher_tree.column(col, width=width, anchor='center')
        self.course_teacher_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar_ct.config(command=self.course_teacher_tree.yview)

        def load_course_teacher_stats():
            import math
            for item in self.course_teacher_tree.get_children():
                self.course_teacher_tree.delete(item)

            semester = self.semester_ct_var.get().strip()
            course_name = self.course_ct_var.get().strip()
            if course_name == "全部":
                course_name = ""

            teacher_label = self.teacher_ct_var.get().strip()
            if teacher_label == "全部":
                teacher_id = None
            else:
                teacher_id = self._teacher_id_map.get(teacher_label)

            conditions = ["g.final_score IS NOT NULL"]
            params = []
            if semester and semester != "全部":
                conditions.append("c.semester = ?")
                params.append(semester)
            if course_name:
                conditions.append("c.course_name = ?")
                params.append(course_name)
            if teacher_id:
                conditions.append("t.teacher_id = ?")
                params.append(teacher_id)

            where_clause = " AND ".join(conditions)

            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute(
                        f"""
                        SELECT t.teacher_id,
                               t.name,
                               c.course_name,
                               COUNT(*) AS total,
                               AVG(g.final_score) AS avg_score,
                               SUM(CASE WHEN g.final_score < 60 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS fail_rate,
                               SUM(CASE WHEN g.final_score >= 90 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS excellent_rate,
                               SUM(CASE WHEN g.final_score >= 80 AND g.final_score < 90 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS good_rate
                        FROM grades g
                        JOIN courses c ON g.course_id = c.course_id
                        JOIN teachers t ON c.teacher_id = t.teacher_id
                        WHERE {where_clause}
                        GROUP BY t.teacher_id, t.name, c.course_name
                        ORDER BY t.teacher_id, c.course_name
                        """,
                        params,
                    )
                    rows = cur.fetchall()
                    for row in rows:
                        tid, tname, cname, total, avg_score, fail_rate, excellent_rate, good_rate = row
                        
                        # 应用两位小数向下取整
                        display_avg = math.floor((avg_score or 0) * 100) / 100
                        
                        self.course_teacher_tree.insert(
                            '',
                            tk.END,
                            values=(
                                tid,
                                tname,
                                cname,
                                total or 0,
                                f"{display_avg:.2f}",
                                f"{((fail_rate or 0) * 100):.2f}%",
                                f"{((excellent_rate or 0) * 100):.2f}%",
                                f"{((good_rate or 0) * 100):.2f}%",
                            ),
                        )
            except Exception as e:
                messagebox.showerror("错误", f"加载课程-教师统计失败: {e}")

        tk.Button(
            top_frame_ct,
            text="加载课程-教师统计表",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=22,
            cursor='hand2',
            command=load_course_teacher_stats,
        ).pack(side=tk.LEFT, padx=10)

        top_frame_fl = tk.Frame(tab_fail_list, bg='white')
        top_frame_fl.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(top_frame_fl, text="学期:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=0)
        semester_values = ["全部"]
        try:
            with self.db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT DISTINCT semester FROM grades WHERE semester IS NOT NULL AND semester <> '' ORDER BY semester DESC"
                )
                semester_values.extend([r[0] for r in cur.fetchall()])
        except Exception:
            semester_values = ["全部"]

        self.semester_fl_var = tk.StringVar()
        semester_combo_fl = ttk.Combobox(
            top_frame_fl,
            textvariable=self.semester_fl_var,
            font=("微软雅黑", 11),
            width=11,
            state='readonly',
            values=semester_values,
        )
        semester_combo_fl.pack(side=tk.LEFT, padx=2)
        semester_combo_fl.current(0)

        tk.Label(top_frame_fl, text="年级:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=0)
        
        grade_values_fl = ["全部"]
        try:
            with self.db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT grade FROM students WHERE grade IS NOT NULL AND grade <> '' ORDER BY grade")
                grade_values_fl.extend([str(r[0]) for r in cur.fetchall()])
        except Exception:
            pass
        self.grade_fl_var = tk.StringVar()
        grade_combo_fl = ttk.Combobox(
            top_frame_fl,
            textvariable=self.grade_fl_var,
            font=("微软雅黑", 11),
            width=5,
            state='readonly',
            values=grade_values_fl,
        )
        grade_combo_fl.pack(side=tk.LEFT, padx=2)
        grade_combo_fl.current(0)

        tk.Label(top_frame_fl, text="专业:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=0)
        
        major_values_fl = ["全部"]
        try:
            with self.db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT DISTINCT major FROM students WHERE major IS NOT NULL AND major <> '' ORDER BY major"
                )
                major_values_fl.extend([r[0] for r in cur.fetchall()])
        except Exception:
            pass
        self.major_fl_var = tk.StringVar()
        major_combo_fl = ttk.Combobox(
            top_frame_fl,
            textvariable=self.major_fl_var,
            font=("微软雅黑", 11),
            width=13,
            state='readonly',
            values=major_values_fl,
        )
        major_combo_fl.pack(side=tk.LEFT, padx=2)
        major_combo_fl.current(0)

        tk.Label(top_frame_fl, text="班级:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=0)
        
        class_values_fl = ["全部"]
        try:
            with self.db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT DISTINCT class_name FROM students WHERE class_name IS NOT NULL AND class_name <> '' ORDER BY class_name"
                )
                class_values_fl.extend([r[0] for r in cur.fetchall()])
        except Exception:
            pass
        self.class_fl_var = tk.StringVar()
        class_combo_fl = ttk.Combobox(
            top_frame_fl,
            textvariable=self.class_fl_var,
            font=("微软雅黑", 11),
            width=10,
            state='readonly',
            values=class_values_fl,
        )
        class_combo_fl.pack(side=tk.LEFT, padx=2)
        class_combo_fl.current(0)

        self._updating_fail_filters = False

        def refresh_fail_filter_options(changed=None):
            """挂科名单：级联刷新下拉框选项，只保留当前筛选条件下真实存在的数据"""
            if self._updating_fail_filters:
                return
            self._updating_fail_filters = True
            try:
                sel_semester = self.semester_fl_var.get().strip()
                sel_grade = self.grade_fl_var.get().strip()
                sel_major = self.major_fl_var.get().strip()
                sel_class = self.class_fl_var.get().strip()

                def _fetch_distinct(field_sql, ignore_field=None):
                    conditions = ["g.final_score < 60"]
                    params = []

                    if ignore_field != 'semester' and sel_semester and sel_semester != '全部':
                        conditions.append("g.semester = ?")
                        params.append(sel_semester)
                    if ignore_field != 'grade' and sel_grade and sel_grade != '全部':
                        conditions.append("s.grade = ?")
                        params.append(sel_grade)
                    if ignore_field != 'major' and sel_major and sel_major != '全部':
                        conditions.append("s.major = ?")
                        params.append(sel_major)
                    if ignore_field != 'class' and sel_class and sel_class != '全部':
                        conditions.append("s.class_name = ?")
                        params.append(sel_class)

                    where_clause = " AND ".join(conditions)
                    sql = f"""
                        SELECT DISTINCT {field_sql}
                        FROM grades g
                        JOIN students s ON g.student_id = s.student_id
                        WHERE {where_clause}
                        ORDER BY 1
                    """
                    with self.db.get_connection() as conn:
                        cur = conn.cursor()
                        cur.execute(sql, params)
                        return [r[0] for r in cur.fetchall() if r[0] is not None and str(r[0]).strip() != ""]

                try:
                    semesters = ["全部"] + [str(x) for x in _fetch_distinct("g.semester", ignore_field='semester')]
                except Exception:
                    semesters = ["全部"]
                try:
                    grades = ["全部"] + [str(x) for x in _fetch_distinct("s.grade", ignore_field='grade')]
                except Exception:
                    grades = ["全部"]
                try:
                    majors = ["全部"] + [str(x) for x in _fetch_distinct("s.major", ignore_field='major')]
                except Exception:
                    majors = ["全部"]
                try:
                    classes = ["全部"] + [str(x) for x in _fetch_distinct("s.class_name", ignore_field='class')]
                except Exception:
                    classes = ["全部"]

                semester_combo_fl['values'] = semesters
                grade_combo_fl['values'] = grades
                major_combo_fl['values'] = majors
                class_combo_fl['values'] = classes

                if sel_semester not in semesters:
                    self.semester_fl_var.set("全部")
                if sel_grade not in grades:
                    self.grade_fl_var.set("全部")
                if sel_major not in majors:
                    self.major_fl_var.set("全部")
                if sel_class not in classes:
                    self.class_fl_var.set("全部")
            finally:
                self._updating_fail_filters = False

        semester_combo_fl.bind("<<ComboboxSelected>>", lambda e: refresh_fail_filter_options('semester'))
        grade_combo_fl.bind("<<ComboboxSelected>>", lambda e: refresh_fail_filter_options('grade'))
        major_combo_fl.bind("<<ComboboxSelected>>", lambda e: refresh_fail_filter_options('major'))
        class_combo_fl.bind("<<ComboboxSelected>>", lambda e: refresh_fail_filter_options('class'))
        refresh_fail_filter_options()

        tk.Button(
            top_frame_fl,
            text="生成名单",
            font=("微软雅黑", 11),
            bg='#FF9800',
            fg='white',
            width=8,
            cursor='hand2',
            command=lambda: load_fail_list(),
        ).pack(side=tk.LEFT, padx=5)

        tree_frame_fl = tk.Frame(tab_fail_list, bg='white')
        tree_frame_fl.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar_fl = ttk.Scrollbar(tree_frame_fl)
        scrollbar_fl.pack(side=tk.RIGHT, fill=tk.Y)

        columns_fl = (
            'student_id',
            'name',
            'grade',
            'major',
            'class_name',
            'course_id',
            'course_name',
            'final_score',
            'grade_level',
            'semester',
        )
        self.fail_tree = ttk.Treeview(
            tree_frame_fl,
            columns=columns_fl,
            show='headings',
            yscrollcommand=scrollbar_fl.set,
        )
        headers_fl = ['学号', '姓名', '年级', '专业', '班级', '课程ID', '课程名', '成绩', '等级', '学期']
        widths_fl = [90, 80, 60, 130, 110, 90, 140, 60, 70, 100]
        for col, header, width in zip(columns_fl, headers_fl, widths_fl):
            self.fail_tree.heading(col, text=header)
            self.fail_tree.column(col, width=width, anchor='center')
        self.fail_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar_fl.config(command=self.fail_tree.yview)

        def load_fail_list():
            import math
            for item in self.fail_tree.get_children():
                self.fail_tree.delete(item)
            semester = self.semester_fl_var.get().strip()
            grade_sel = self.grade_fl_var.get().strip()
            major_sel = self.major_fl_var.get().strip()
            class_sel = self.class_fl_var.get().strip()

            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    conditions = ["g.final_score < 60"]
                    params = []
                    
                    if semester and semester != "全部":
                        conditions.append("g.semester = ?")
                        params.append(semester)

                    if grade_sel and grade_sel != "全部":
                        conditions.append("s.grade = ?")
                        params.append(grade_sel)

                    if major_sel and major_sel != "全部":
                        conditions.append("s.major = ?")
                        params.append(major_sel)

                    if class_sel and class_sel != "全部":
                        conditions.append("s.class_name = ?")
                        params.append(class_sel)

                    where_clause = " AND ".join(conditions)

                    cur.execute(
                        f"""
                        SELECT s.student_id, s.name, s.grade, s.major, s.class_name,
                               g.course_id, c.course_name, 
                               TRUNCATE(g.final_score, 2), 
                               g.grade_level, g.semester
                        FROM grades g
                        JOIN students s ON g.student_id = s.student_id
                        JOIN courses c ON g.course_id = c.course_id
                        WHERE {where_clause}
                        ORDER BY s.student_id, g.course_id
                        """,
                        params,
                    )
                    for row in cur.fetchall():
                        # 处理成绩显示：确保显示两位小数
                        r = list(row)
                        score = r[7]
                        if score is not None:
                            r[7] = f"{score:.2f}"
                        
                        self.fail_tree.insert('', tk.END, values=tuple(r))
            except Exception as e:
                messagebox.showerror("错误", f"加载挂科名单失败: {e}")

        # 默认不加载，等待用户点击
        # load_fail_list()

        top_frame_mr = tk.Frame(tab_major_rank, bg='white')
        top_frame_mr.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(top_frame_mr, text="学期:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.semester_mr_var = tk.StringVar()
        semester_combo_mr = ttk.Combobox(top_frame_mr, textvariable=self.semester_mr_var, font=("微软雅黑", 11), width=12, state='readonly')
        semester_combo_mr.pack(side=tk.LEFT, padx=5)
        
        # 加载所有学期
        semester_values_mr = ["全部"]
        try:
            with self.db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT semester FROM grades WHERE semester IS NOT NULL AND semester <> '' ORDER BY semester DESC")
                semester_values_mr.extend([r[0] for r in cur.fetchall()])
        except Exception:
            pass
        semester_combo_mr['values'] = semester_values_mr
        if semester_values_mr:
            semester_combo_mr.current(0)

        tk.Label(top_frame_mr, text="年级:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        grade_values_mr = grade_values
        self.grade_mr_var = tk.StringVar()
        grade_combo_mr = ttk.Combobox(
            top_frame_mr,
            textvariable=self.grade_mr_var,
            font=("微软雅黑", 11),
            width=10,
            state='readonly',
            values=grade_values_mr,
        )
        grade_combo_mr.pack(side=tk.LEFT, padx=5)
        if grade_values_mr:
            grade_combo_mr.current(0)

        def refresh_mr_grade_options(event=None):
            """学期改变后刷新专业成绩排名的年级下拉框（只显示该学期有成绩数据的年级）"""
            sel_semester = self.semester_mr_var.get().strip()
            current_grade = self.grade_mr_var.get().strip()

            grades = []
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    if sel_semester and sel_semester != "全部":
                        cur.execute(
                            """
                            SELECT DISTINCT s.grade
                            FROM students s
                            JOIN grades g ON s.student_id = g.student_id
                            WHERE g.semester = ? AND s.grade IS NOT NULL AND s.grade <> ''
                            ORDER BY s.grade
                            """,
                            (sel_semester,),
                        )
                    else:
                        cur.execute(
                            "SELECT DISTINCT grade FROM students WHERE grade IS NOT NULL AND grade <> '' ORDER BY grade"
                        )
                    grades = [str(r[0]) for r in cur.fetchall()]
            except Exception:
                grades = grade_values_mr

            grade_combo_mr['values'] = grades
            if current_grade and current_grade in grades:
                self.grade_mr_var.set(current_grade)
            elif grades:
                self.grade_mr_var.set(grades[0])
            else:
                self.grade_mr_var.set("")

            try:
                refresh_class_mr()
            except NameError:
                pass

        semester_combo_mr.bind("<<ComboboxSelected>>", refresh_mr_grade_options)

        tk.Label(top_frame_mr, text="专业:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        major_values = []
        try:
            with self.db.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT DISTINCT major FROM students WHERE major IS NOT NULL AND major <> '' ORDER BY major"
                )
                major_values = [r[0] for r in cur.fetchall()]
        except Exception:
            major_values = []

        self.major_mr_var = tk.StringVar()
        major_combo_mr = ttk.Combobox(
            top_frame_mr,
            textvariable=self.major_mr_var,
            font=("微软雅黑", 11),
            width=20,
            state='readonly',
            values=major_values,
        )
        major_combo_mr.pack(side=tk.LEFT, padx=5)
        if major_values:
            major_combo_mr.current(0)

        tk.Label(top_frame_mr, text="班级:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.class_mr_var = tk.StringVar()
        self.class_mr_combo = ttk.Combobox(
            top_frame_mr,
            textvariable=self.class_mr_var,
            font=("微软雅黑", 11),
            width=12,
            state='readonly',
            values=[],
        )
        self.class_mr_combo.pack(side=tk.LEFT, padx=5)

        btn_frame_mr = tk.Frame(tab_major_rank, bg='white')
        btn_frame_mr.pack(fill=tk.X, padx=20, pady=(0, 10))

        def refresh_class_mr(event=None):
            grade = self.grade_mr_var.get().strip()
            major = self.major_mr_var.get().strip()
            classes = ["全部"]
            if not grade or not major:
                self.class_mr_combo["values"] = classes
                self.class_mr_var.set("全部")
                return
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute(
                        """
                        SELECT DISTINCT class_name
                        FROM students
                        WHERE grade = ? AND major = ? AND class_name IS NOT NULL AND class_name <> ''
                        ORDER BY class_name
                        """,
                        (grade, major),
                    )
                    for (cname,) in cur.fetchall():
                        classes.append(cname)
            except Exception:
                classes = ["全部"]
            self.class_mr_combo["values"] = classes
            self.class_mr_var.set(classes[0] if classes else "")

        grade_combo_mr.bind("<<ComboboxSelected>>", refresh_class_mr)
        major_combo_mr.bind("<<ComboboxSelected>>", refresh_class_mr)

        refresh_mr_grade_options()
        refresh_class_mr()

        tree_frame_mr = tk.Frame(tab_major_rank, bg='white')
        tree_frame_mr.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar_mr = ttk.Scrollbar(tree_frame_mr)
        scrollbar_mr.pack(side=tk.RIGHT, fill=tk.Y)

        columns_mr = ('rank', 'student_id', 'name', 'class_name', 'avg_score')
        self.rank_tree = ttk.Treeview(
            tree_frame_mr,
            columns=columns_mr,
            show='headings',
            yscrollcommand=scrollbar_mr.set,
        )
        headers_mr = ['排名', '学号', '姓名', '班级', '加权平均成绩']
        widths_mr = [60, 100, 80, 110, 120]
        for col, header, width in zip(columns_mr, headers_mr, widths_mr):
            self.rank_tree.heading(col, text=header)
            self.rank_tree.column(col, width=width, anchor='center')
        self.rank_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar_mr.config(command=self.rank_tree.yview)

        def load_ranking():
            for item in self.rank_tree.get_children():
                self.rank_tree.delete(item)
            grade = self.grade_mr_var.get().strip()
            major = self.major_mr_var.get().strip()
            semester = self.semester_mr_var.get().strip()
            
            if not grade or not major:
                messagebox.showwarning("提示", "请先选择年级和专业！")
                return
            class_name = self.class_mr_var.get().strip()
            ranking = []
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    conditions = ["s.grade = ?", "s.major = ?"]
                    params = [grade, major]
                    if class_name and class_name != "全部":
                        conditions.append("s.class_name = ?")
                        params.append(class_name)
                    
                    if semester and semester != "全部":
                        conditions.append("g.semester = ?")
                        params.append(semester)

                    where_clause = " AND ".join(conditions)

                    cur.execute(
                        f"""
                        SELECT s.student_id, s.name, s.class_name,
                               SUM(g.final_score * c.credits) AS weighted_sum,
                               SUM(c.credits) AS credit_sum
                        FROM students s
                        JOIN grades g ON s.student_id = g.student_id
                        JOIN courses c ON g.course_id = c.course_id
                        WHERE {where_clause}
                        GROUP BY s.student_id, s.name, s.class_name
                        HAVING credit_sum > 0
                        ORDER BY weighted_sum * 1.0 / credit_sum DESC
                        """,
                        params,
                    )
                    for row in cur.fetchall():
                        student_id, name, class_name, weighted_sum, credit_sum = row
                        avg_score = (weighted_sum or 0) / (credit_sum or 1)
                        ranking.append(
                            {
                                "student_id": student_id,
                                "name": name,
                                "class_name": class_name,
                                "avg_score": avg_score,
                            }
                        )
            except Exception as e:
                messagebox.showerror("错误", f"获取排名数据失败: {e}")
                return

            if not ranking:
                messagebox.showinfo("提示", "该条件下暂无成绩数据。")
                return

            for idx, item in enumerate(ranking, start=1):
                self.rank_tree.insert(
                    '',
                    tk.END,
                    values=(idx, item["student_id"], item["name"], item["class_name"], f"{item['avg_score']:.2f}"),
                )

        tk.Button(
            btn_frame_mr,
            text="加载专业/班级成绩排名",
            font=("微软雅黑", 11),
            bg='#2196F3',
            fg='white',
            width=22,
            cursor='hand2',
            command=load_ranking,
        ).pack(side=tk.LEFT, padx=10)

        top_frame_tr = tk.Frame(tab_semester_trend, bg='white')
        top_frame_tr.pack(fill=tk.X, padx=20, pady=10)

        chart_container_tr = tk.Frame(tab_semester_trend, bg='white')
        chart_container_tr.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self._trend_chart_canvas = None

        tk.Label(top_frame_tr, text="年级:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.trend_grade_var = tk.StringVar()
        trend_grade_combo = ttk.Combobox(
            top_frame_tr,
            textvariable=self.trend_grade_var,
            font=("微软雅黑", 11),
            width=10,
            state='readonly',
            values=grade_values,
        )
        trend_grade_combo.pack(side=tk.LEFT, padx=5)
        if grade_values:
            trend_grade_combo.current(0)

        tk.Label(top_frame_tr, text="专业:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.trend_major_var = tk.StringVar()
        trend_major_combo = ttk.Combobox(
            top_frame_tr,
            textvariable=self.trend_major_var,
            font=("微软雅黑", 11),
            width=18,
            state='readonly',
            values=["全部"],
        )
        trend_major_combo.pack(side=tk.LEFT, padx=5)
        trend_major_combo.current(0)

        tk.Label(top_frame_tr, text="班级:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.trend_class_var = tk.StringVar()
        trend_class_combo = ttk.Combobox(
            top_frame_tr,
            textvariable=self.trend_class_var,
            font=("微软雅黑", 11),
            width=14,
            state='readonly',
            values=["全部"],
        )
        trend_class_combo.pack(side=tk.LEFT, padx=5)
        trend_class_combo.current(0)

        tk.Label(top_frame_tr, text="指标:", font=("微软雅黑", 11), bg='white').pack(side=tk.LEFT, padx=5)
        self.trend_metric_var = tk.StringVar()
        metric_map = {
            "平均分趋势": "avg",
            "挂科率趋势": "fail_rate",
            "优秀率趋势": "excellent_rate",
        }
        metric_values = list(metric_map.keys())
        trend_metric_combo = ttk.Combobox(
            top_frame_tr,
            textvariable=self.trend_metric_var,
            font=("微软雅黑", 11),
            width=12,
            state='readonly',
            values=metric_values,
        )
        trend_metric_combo.pack(side=tk.LEFT, padx=5)
        if metric_values:
            trend_metric_combo.current(0)

        def refresh_trend_major_options(event=None):
            grade = self.trend_grade_var.get().strip()
            majors = ["全部"]
            if not grade:
                trend_major_combo['values'] = majors
                self.trend_major_var.set("全部")
                refresh_trend_class_options()
                return
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute(
                        """
                        SELECT DISTINCT major
                        FROM students
                        WHERE grade = ? AND major IS NOT NULL AND major <> ''
                        ORDER BY major
                        """,
                        (grade,),
                    )
                    majors.extend([r[0] for r in cur.fetchall()])
            except Exception:
                majors = ["全部"]
            trend_major_combo['values'] = majors
            if self.trend_major_var.get().strip() not in majors:
                self.trend_major_var.set("全部")
            refresh_trend_class_options()

        def refresh_trend_class_options(event=None):
            grade = self.trend_grade_var.get().strip()
            major = self.trend_major_var.get().strip()
            classes = ["全部"]
            if not grade or not major or major == "全部":
                trend_class_combo['values'] = classes
                self.trend_class_var.set("全部")
                return
            try:
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute(
                        """
                        SELECT DISTINCT class_name
                        FROM students
                        WHERE grade = ? AND major = ? AND class_name IS NOT NULL AND class_name <> ''
                        ORDER BY class_name
                        """,
                        (grade, major),
                    )
                    classes.extend([r[0] for r in cur.fetchall()])
            except Exception:
                classes = ["全部"]
            trend_class_combo['values'] = classes
            if self.trend_class_var.get().strip() not in classes:
                self.trend_class_var.set("全部")

        trend_grade_combo.bind("<<ComboboxSelected>>", refresh_trend_major_options)
        trend_major_combo.bind("<<ComboboxSelected>>", refresh_trend_class_options)
        refresh_trend_major_options()

        def _metric_label(metric_key):
            if metric_key == 'avg':
                return '平均分'
            if metric_key == 'fail_rate':
                return '挂科率(%)'
            if metric_key == 'excellent_rate':
                return '优秀率(%)'
            return metric_key

        def _value_transform(metric_key, v):
            if v is None:
                v = 0
            if metric_key in ('fail_rate', 'excellent_rate'):
                return float(v) * 100
            return float(v)

        def draw_semester_trend():
            import math
            grade = self.trend_grade_var.get().strip()
            major = self.trend_major_var.get().strip()
            class_name = self.trend_class_var.get().strip()
            metric_text = self.trend_metric_var.get().strip()
            metric_key = metric_map.get(metric_text)

            if not metric_key:
                messagebox.showwarning("提示", "请选择指标！")
                return
            if not grade:
                messagebox.showwarning("提示", "请先选择年级！")
                return
            if class_name and class_name != "全部" and (not major or major == "全部"):
                messagebox.showwarning("提示", "选择班级前请先选择年级和专业！")
                return

            base_conditions = ["g.final_score IS NOT NULL", "s.grade = ?"]
            base_params = [grade]

            if major and major != "全部":
                base_conditions.append("s.major = ?")
                base_params.append(major)
            if class_name and class_name != "全部":
                base_conditions.append("s.class_name = ?")
                base_params.append(class_name)

            where_base = " AND ".join(base_conditions)

            def query_series(group_field=None):
                select_metric = {
                    'avg': "AVG(g.final_score)",
                    'fail_rate': "SUM(CASE WHEN g.final_score < 60 THEN 1 ELSE 0 END) * 1.0 / COUNT(*)",
                    'excellent_rate': "SUM(CASE WHEN g.final_score >= 90 THEN 1 ELSE 0 END) * 1.0 / COUNT(*)",
                }[metric_key]

                group_select = ""
                group_by = "c.semester"
                if group_field:
                    group_select = f", {group_field}"
                    group_by = f"c.semester, {group_field}"

                sql = f"""
                    SELECT c.semester{group_select}, {select_metric} AS val
                    FROM grades g
                    JOIN courses c ON g.course_id = c.course_id
                    JOIN students s ON g.student_id = s.student_id
                    WHERE {where_base} AND c.semester IS NOT NULL AND c.semester <> ''
                    GROUP BY {group_by}
                    ORDER BY c.semester
                """
                with self.db.get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute(sql, base_params)
                    rows = cur.fetchall()

                series = {}
                semesters = []
                if not group_field:
                    for sem, val in rows:
                        semesters.append(sem)
                        series.setdefault("平均", {})[sem] = val
                else:
                    for sem, gval, val in rows:
                        semesters.append(sem)
                        series.setdefault(str(gval), {})[sem] = val
                semesters = sorted(list({s for s in semesters}))
                return semesters, series

            try:
                if class_name and class_name != "全部":
                    semesters, series = query_series(group_field=None)
                    plot_series = {f"{grade}-{major}-{class_name}": series.get("平均", {})}
                elif major and major != "全部":
                    semesters, major_series = query_series(group_field=None)
                    semesters2, class_series = query_series(group_field="s.class_name")
                    semesters = sorted(list(set(semesters) | set(semesters2)))
                    plot_series = {f"{grade}-{major}-平均": major_series.get("平均", {})}
                    for cname, data in class_series.items():
                        plot_series[f"{cname}"] = data
                else:
                    semesters, grade_series = query_series(group_field=None)
                    semesters2, major_series = query_series(group_field="s.major")
                    semesters = sorted(list(set(semesters) | set(semesters2)))
                    plot_series = {f"{grade}-平均": grade_series.get("平均", {})}
                    for mname, data in major_series.items():
                        plot_series[f"{mname}"] = data
            except Exception as e:
                messagebox.showerror("错误", f"加载学期趋势数据失败: {e}")
                return

            if not semesters:
                messagebox.showinfo("提示", "该条件下暂无趋势数据。")
                return

            for widget in chart_container_tr.winfo_children():
                widget.destroy()

            fig, ax = plt.subplots(figsize=(9, 4.5))
            x = list(range(len(semesters)))
            for label, data in plot_series.items():
                y = [_value_transform(metric_key, data.get(sem)) for sem in semesters]
                if metric_key == 'avg':
                    y = [math.floor(v * 100) / 100 for v in y]
                ax.plot(x, y, marker='o', linewidth=2, label=label)

            ax.set_xticks(x)
            ax.set_xticklabels(semesters, rotation=30, ha='right')
            ax.set_ylabel(_metric_label(metric_key))
            title_parts = ["学期趋势", metric_text, f"年级:{grade}"]
            if major and major != "全部":
                title_parts.append(f"专业:{major}")
            if class_name and class_name != "全部":
                title_parts.append(f"班级:{class_name}")
            ax.set_title(" ".join(title_parts))
            ax.grid(True, linestyle='--', alpha=0.3)
            ax.legend(fontsize=9)
            fig.tight_layout()

            self._trend_chart_canvas = FigureCanvasTkAgg(fig, master=chart_container_tr)
            self._trend_chart_canvas.draw()
            self._trend_chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        tk.Button(
            top_frame_tr,
            text="生成趋势图",
            font=("微软雅黑", 11),
            bg='#4CAF50',
            fg='white',
            width=10,
            cursor='hand2',
            command=draw_semester_trend,
        ).pack(side=tk.LEFT, padx=10)
    
    def show_user_management(self):
        """显示用户管理"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="用户管理",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 工具栏
        toolbar = tk.Frame(self.content_frame, bg='white')
        toolbar.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            toolbar,
            text="激活用户",
            font=("微软雅黑", 10),
            bg='#4CAF50',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.activate_user
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="禁用用户",
            font=("微软雅黑", 10),
            bg='#FF9800',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.deactivate_user
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="重置密码",
            font=("微软雅黑", 10),
            bg='#2196F3',
            fg='white',
            width=10,
            cursor='hand2',
            command=self.reset_user_password
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            toolbar,
            text="刷新",
            font=("微软雅黑", 10),
            bg='#9E9E9E',
            fg='white',
            width=8,
            cursor='hand2',
            command=self.load_users
        ).pack(side=tk.LEFT, padx=5)
        
        # 用户列表
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('user_id', 'username', 'role', 'status', 'created_at')
        self.user_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        headers = ['用户ID', '用户名', '角色', '状态', '创建时间']
        widths = [80, 150, 100, 100, 180]
        
        for col, header, width in zip(columns, headers, widths):
            self.user_tree.heading(col, text=header)
            self.user_tree.column(col, width=width, anchor='center')
        
        self.user_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.user_tree.yview)
        
        # 加载用户数据
        self.load_users()
    
    def load_users(self):
        """加载用户数据"""
        # 清空现有数据
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # 获取所有用户
        users = self.db.get_all_users()
        
        # 角色映射
        role_map = {
            'admin': '管理员',
            'teacher': '教师',
            'student': '学生'
        }
        
        # 状态映射
        status_map = {
            'active': '✓ 激活',
            'inactive': '✗ 禁用'
        }
        
        for user in users:
            # 设置标签以便根据状态显示不同颜色
            tags = ('inactive',) if user['status'] == 'inactive' else ()
            
            self.user_tree.insert('', tk.END, values=(
                user['user_id'],
                user['username'],
                role_map.get(user['role'], user['role']),
                status_map.get(user['status'], user['status']),
                user['created_at']
            ), tags=tags)
        
        # 设置标签样式
        self.user_tree.tag_configure('inactive', foreground='gray')
    
    def activate_user(self):
        """激活用户"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要激活的用户！")
            return
        
        item = self.user_tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        # 不能操作管理员账号
        if username == 'admin':
            messagebox.showwarning("提示", "不能操作管理员账号！")
            return
        
        if messagebox.askyesno("确认", f"确定要激活用户 {username} 吗？"):
            if self.db.update_user_status(user_id, 'active'):
                messagebox.showinfo("成功", "用户激活成功！")
                self.load_users()
            else:
                messagebox.showerror("错误", "用户激活失败！")
    
    def deactivate_user(self):
        """禁用用户"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要禁用的用户！")
            return
        
        item = self.user_tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        # 不能操作管理员账号
        if username == 'admin':
            messagebox.showwarning("提示", "不能操作管理员账号！")
            return
        
        if messagebox.askyesno("确认", f"确定要禁用用户 {username} 吗？\n禁用后该用户将无法登录系统。"):
            if self.db.update_user_status(user_id, 'inactive'):
                messagebox.showinfo("成功", "用户禁用成功！")
                self.load_users()
            else:
                messagebox.showerror("错误", "用户禁用失败！")
    
    def reset_user_password(self):
        """重置用户密码为默认密码"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要重置密码的用户！")
            return
        
        item = self.user_tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]
        role = item['values'][2]
        
        # 不能操作管理员账号
        if username == 'admin':
            messagebox.showwarning("提示", "不能操作管理员账号！")
            return
        
        # 根据角色确定默认密码
        if role == '教师':
            default_password = 'teacher123'
        elif role == '学生':
            default_password = 'student123'
        else:
            messagebox.showerror("错误", "未知的用户角色！")
            return
        
        # 确认重置
        confirm_msg = f"确定要重置用户 {username} 的密码吗？\n\n" \
                      f"用户名: {username}\n" \
                      f"角色: {role}\n" \
                      f"默认密码: {default_password}"
        
        if messagebox.askyesno("确认重置密码", confirm_msg):
            if self.db.reset_password(user_id, default_password):
                messagebox.showinfo("成功", f"用户 {username} 的密码已重置为默认密码！\n新密码: {default_password}")
                self.load_users()
            else:
                messagebox.showerror("错误", "密码重置失败！")
    
    def show_logs(self):
        """显示系统日志"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="系统日志",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 日志列表
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('username', 'action', 'description', 'timestamp')
        log_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        headers = ['用户', '操作', '描述', '时间']
        widths = [100, 120, 300, 180]
        
        for col, header, width in zip(columns, headers, widths):
            log_tree.heading(col, text=header)
            log_tree.column(col, width=width, anchor='center')
        
        log_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=log_tree.yview)
        
        # 加载日志
        logs = self.db.get_logs(100)
        for log in logs:
            log_tree.insert('', tk.END, values=(
                log['username'] if log['username'] else 'System',
                log['action'],
                log['description'],
                log['timestamp']
            ))
    
    def show_export(self):
        """显示数据导出"""
        self.clear_content()
        
        # 标题
        tk.Label(
            self.content_frame,
            text="数据导出",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=30)
        
        # 导出选项
        export_frame = tk.Frame(self.content_frame, bg='white')
        export_frame.pack(expand=True)
        
        buttons = [
            ("导出学生数据", self.export_students),
            ("导出教师数据", self.export_teachers),
            ("导出课程数据", self.export_courses),
            ("导出成绩数据", self.export_grades),
        ]
        
        for text, command in buttons:
            tk.Button(
                export_frame,
                text=text,
                font=("微软雅黑", 12),
                bg='#4CAF50',
                fg='white',
                width=20,
                height=2,
                cursor='hand2',
                command=command
            ).pack(pady=10)
    
    def export_students(self):
        """导出学生数据"""
        try:
            import csv
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
            )
            
            if filename:
                students = self.db.get_all_students()
                
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['学号', '姓名', '性别', '专业', '年级', '班级', '电话', '邮箱'])
                    
                    for s in students:
                        writer.writerow([
                            s['student_id'], s['name'], s['gender'],
                            s['major'], s['grade'], s['class_name'],
                            s['phone'], s['email']
                        ])
                
                messagebox.showinfo("成功", f"学生数据已导出到:\n{filename}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")
    
    def export_teachers(self):
        """导出教师数据"""
        messagebox.showinfo("提示", "导出教师数据功能类似")
    
    def export_courses(self):
        """导出课程数据"""
        messagebox.showinfo("提示", "导出课程数据功能类似")
    
    def export_grades(self):
        """导出成绩数据"""
        messagebox.showinfo("提示", "导出成绩数据功能类似")
    
    def logout(self):
        """注销"""
        if messagebox.askyesno("确认", "确定要注销吗？"):
            self.root.destroy()
            self.login_root.deiconify()


if __name__ == '__main__':
    pass
"""
管理员主界面模块
包含用户管理、学生管理、教师管理、课程管理、数据统计等功能
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager


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
        
        # 获取成绩分布
        distribution = self.db.get_grade_distribution()
        
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
        
        # 标题
        tk.Label(
            self.content_frame,
            text="成绩统计分析",
            font=("微软雅黑", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # 统计信息框架
        stats_frame = tk.Frame(self.content_frame, bg='white')
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # 获取统计数据
        stats = self.db.get_statistics()
        distribution = self.db.get_grade_distribution()
        
        # 显示统计
        tk.Label(
            stats_frame,
            text=f"平均分: {stats.get('avg_score', 0)}",
            font=("微软雅黑", 16, "bold"),
            bg='white',
            fg='#2196F3'
        ).pack(pady=10)
        
        # 成绩分布
        for level, count in distribution.items():
            tk.Label(
                stats_frame,
                text=f"{level}: {count} 人",
                font=("微软雅黑", 14),
                bg='white'
            ).pack(pady=5)
        
        # 可视化按钮
        tk.Button(
            stats_frame,
            text="查看图表",
            font=("微软雅黑", 12),
            bg='#2196F3',
            fg='white',
            width=15,
            cursor='hand2',
            command=self.show_charts
        ).pack(pady=20)
    
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
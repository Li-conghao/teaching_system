"""
教师主界面模块
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

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
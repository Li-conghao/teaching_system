"""
学生主界面模块
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager


class StudentWindow:
    """学生主界面类"""

    def __init__(self, user_info, login_root, client=None):
        self.user_info = user_info
        self.login_root = login_root
        self.client = client
        self.db = None if client else DatabaseManager()

        # 获取学生信息
        self.student_info = self._load_student_info(user_info['user_id'])

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
            ("我的课程", self.show_courses),
            ("选课管理", self.show_enrollment),
            ("我的成绩", self.show_grades),
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

    def _load_student_info(self, user_id):
        """从网络或本地加载学生信息"""
        if self.client:
            result = self.client.get_student_info(user_id)
            if result.get('success'):
                return result['data']['student']
            messagebox.showerror("错误", result.get('message', '获取学生信息失败'))
            return None

        return self.db.get_student_by_user_id(user_id)

    def _get_student_courses(self):
        """获取学生选课列表"""
        if self.client:
            result = self.client.get_student_enrollments(self.student_info['student_id'])
            if result.get('success'):
                return result['data']['courses']
            messagebox.showerror("错误", result.get('message', '获取课程失败'))
            return []

        return self.db.get_student_enrollments(self.student_info['student_id'])

    def _get_all_courses(self):
        """获取全部课程"""
        if self.client:
            result = self.client.get_all_courses()
            if result.get('success'):
                return result['data']['courses']
            messagebox.showerror("错误", result.get('message', '获取课程失败'))
            return []

        return self.db.get_all_courses()

    def _get_student_grades(self):
        """获取学生成绩"""
        if self.client:
            result = self.client.get_student_grades(self.student_info['student_id'])
            if result.get('success'):
                return result['data']['grades']
            messagebox.showerror("错误", result.get('message', '获取成绩失败'))
            return []

        return self.db.get_student_grades(self.student_info['student_id'])
    
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
        enrollments = self._get_student_courses()
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
        all_courses = self._get_all_courses()

        # 获取已选课程
        enrolled = self._get_student_courses()
        enrolled_ids = {e['course_id'] for e in enrolled}
        
        # 显示未选且开放的课程
        for course in all_courses:
            if course['status'] == 'open' and course['course_id'] not in enrolled_ids:
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
        if self.client:
            result = self.client.enroll_course(self.student_info['student_id'], course_id)
            success = result.get('success', False)
            message = result.get('message', '')
        else:
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
        enrolled = self._get_student_courses()
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
            
            if self.client:
                result = self.client.drop_course(self.student_info['student_id'], course_id)
                success = result.get('success', False)
                message = result.get('message', '')
            else:
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
        grades = self._get_student_grades()
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
            
            if self.client:
                result = self.client.change_password(self.user_info['username'], old_pwd, new_pwd)
                success = result.get('success', False)
            else:
                success = self.db.change_password(self.user_info['username'], old_pwd, new_pwd)

            if success:
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
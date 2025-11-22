"""
登录窗口模块
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager


class LoginWindow:
    """登录窗口类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("本科教学管理系统 - 登录")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 居中显示
        self.center_window()
        
        # 数据库管理器
        self.db = DatabaseManager()
        
        # 当前用户信息
        self.current_user = None
        
        # 创建界面
        self.create_widgets()
    
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题框架
        title_frame = tk.Frame(self.root, bg='#2196F3', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        # 标题
        title_label = tk.Label(
            title_frame, 
            text="本科教学管理系统",
            font=("华文行楷", 28, "bold"),
            bg='#2196F3',
            fg='white'
        )
        title_label.pack(expand=True)
        
        # 主框架
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        # 用户名
        username_frame = tk.Frame(main_frame, bg='white')
        username_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            username_frame, 
            text="用户名:",
            font=("微软雅黑", 12),
            bg='white',
            width=8,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.username_entry = ttk.Entry(
            username_frame,
            font=("微软雅黑", 11),
            width=25
        )
        self.username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.username_entry.focus()
        
        # 密码
        password_frame = tk.Frame(main_frame, bg='white')
        password_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            password_frame, 
            text="密码:",
            font=("微软雅黑", 12),
            bg='white',
            width=8,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.password_entry = ttk.Entry(
            password_frame,
            font=("微软雅黑", 11),
            width=25,
            show='●'
        )
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 角色选择
        role_frame = tk.Frame(main_frame, bg='white')
        role_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            role_frame, 
            text="登录身份:",
            font=("微软雅黑", 12),
            bg='white',
            width=8,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.role_var = tk.StringVar(value="student")
        roles = [("管理员", "admin"), ("教师", "teacher"), ("学生", "student")]
        
        role_radio_frame = tk.Frame(role_frame, bg='white')
        role_radio_frame.pack(side=tk.LEFT)
        
        for text, value in roles:
            tk.Radiobutton(
                role_radio_frame,
                text=text,
                variable=self.role_var,
                value=value,
                font=("微软雅黑", 10),
                bg='white'
            ).pack(side=tk.LEFT, padx=10)
        
        # 按钮框架
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=30)
        
        # 登录按钮
        login_btn = tk.Button(
            button_frame,
            text="登录",
            font=("微软雅黑", 12, "bold"),
            bg='#2196F3',
            fg='white',
            width=12,
            height=2,
            cursor='hand2',
            command=self.login
        )
        login_btn.pack(side=tk.LEFT, expand=True, padx=10)
        
        # 退出按钮
        exit_btn = tk.Button(
            button_frame,
            text="退出",
            font=("微软雅黑", 12),
            bg='#f44336',
            fg='white',
            width=12,
            height=2,
            cursor='hand2',
            command=self.root.quit
        )
        exit_btn.pack(side=tk.LEFT, expand=True, padx=10)
        
        # 提示信息
        tip_frame = tk.Frame(self.root, bg='#f5f5f5', height=40)
        tip_frame.pack(fill=tk.X, side=tk.BOTTOM)
        tip_frame.pack_propagate(False)
        
        tip_text = "默认账户 - 管理员: admin/admin123  教师: teacher001/teacher123  学生: student001/student123"
        tk.Label(
            tip_frame,
            text=tip_text,
            font=("微软雅黑", 9),
            bg='#f5f5f5',
            fg='#666'
        ).pack(expand=True)
        
        # 绑定回车键
        self.root.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """登录处理"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        expected_role = self.role_var.get()
        
        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码！")
            return
        
        # 验证用户
        user = self.db.authenticate_user(username, password)
        
        if not user:
            messagebox.showerror("错误", "用户名或密码错误！")
            return
        
        # 验证角色
        if user['role'] != expected_role:
            messagebox.showerror("错误", f"该账号不是{self.get_role_name(expected_role)}账号！")
            return
        
        self.current_user = user
        messagebox.showinfo("成功", f"欢迎您，{username}！")
        
        # 关闭登录窗口，打开主窗口
        self.root.withdraw()
        self.open_main_window()
    
    def get_role_name(self, role):
        """获取角色中文名"""
        role_names = {
            'admin': '管理员',
            'teacher': '教师',
            'student': '学生'
        }
        return role_names.get(role, '未知')
    
    def open_main_window(self):
        """打开主窗口"""
        role = self.current_user['role']
        
        if role == 'admin':
            from gui.admin_window import AdminWindow
            admin_win = AdminWindow(self.current_user, self.root)
            
        elif role == 'teacher':
            from gui.teacher_window import TeacherWindow
            teacher_win = TeacherWindow(self.current_user, self.root)
            
        elif role == 'student':
            from gui.student_window import StudentWindow
            student_win = StudentWindow(self.current_user, self.root)
    
    def run(self):
        """运行主循环"""
        self.root.mainloop()


if __name__ == '__main__':
    app = LoginWindow()
    app.run()
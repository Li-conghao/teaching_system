#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本科教学管理系统 - 客户端启动文件
连接到远程服务器
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from network.client import Client
from gui.login_window import LoginWindow


class NetworkLoginWindow(LoginWindow):
    """网络模式登录窗口"""
    
    def __init__(self, client):
        self.client = client
        super().__init__()
        self.root.title("本科教学管理系统 - 网络模式")
    
    def login(self):
        """登录处理（网络版本）"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        expected_role = self.role_var.get()
        
        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码！")
            return
        
        # 通过网络验证用户
        result = self.client.login(username, password)
        
        if not result['success']:
            messagebox.showerror("错误", result.get('message', '登录失败'))
            return
        
        user = result['data']['user']
        
        # 验证角色
        if user['role'] != expected_role:
            messagebox.showerror("错误", f"该账号不是{self.get_role_name(expected_role)}账号！")
            return
        
        self.current_user = user
        messagebox.showinfo("成功", f"欢迎您，{username}！")
        
        # 关闭登录窗口，打开主窗口
        self.root.withdraw()
        self.open_main_window()


class ConnectionDialog:
    """连接对话框"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("连接到服务器")
        self.root.geometry("450x250")
        self.root.resizable(False, False)
        
        self.client = None
        self.connected = False
        
        # 居中显示
        self.center_window()
        
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
        # 标题
        title_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="连接到服务器",
            font=("微软雅黑", 16, "bold"),
            bg='#2196F3',
            fg='white'
        ).pack(expand=True)
        
        # 主框架
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # 服务器地址
        address_frame = tk.Frame(main_frame, bg='white')
        address_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            address_frame,
            text="服务器地址:",
            font=("微软雅黑", 11),
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.host_entry = ttk.Entry(
            address_frame,
            font=("微软雅黑", 11),
            width=25
        )
        self.host_entry.insert(0, "127.0.0.1")
        self.host_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 端口
        port_frame = tk.Frame(main_frame, bg='white')
        port_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            port_frame,
            text="端口:",
            font=("微软雅黑", 11),
            bg='white',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        self.port_entry = ttk.Entry(
            port_frame,
            font=("微软雅黑", 11),
            width=25
        )
        self.port_entry.insert(0, "8888")
        self.port_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 按钮框架
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=20)
        
        # 连接按钮
        tk.Button(
            button_frame,
            text="连接",
            font=("微软雅黑", 11, "bold"),
            bg='#4CAF50',
            fg='white',
            width=12,
            height=2,
            cursor='hand2',
            command=self.connect
        ).pack(side=tk.LEFT, expand=True, padx=5)
        
        # 退出按钮
        tk.Button(
            button_frame,
            text="退出",
            font=("微软雅黑", 11),
            bg='#f44336',
            fg='white',
            width=12,
            height=2,
            cursor='hand2',
            command=self.root.quit
        ).pack(side=tk.LEFT, expand=True, padx=5)
        
        # 提示
        tk.Label(
            self.root,
            text="提示：请确保服务器已启动并且网络连接正常",
            font=("微软雅黑", 9),
            bg='#f5f5f5',
            fg='#666'
        ).pack(fill=tk.X, side=tk.BOTTOM, pady=5)
    
    def connect(self):
        """连接到服务器"""
        host = self.host_entry.get().strip()
        port_str = self.port_entry.get().strip()
        
        if not host or not port_str:
            messagebox.showwarning("提示", "请输入服务器地址和端口！")
            return
        
        try:
            port = int(port_str)
            
            # 创建客户端
            self.client = Client(host, port)
            
            # 尝试连接
            messagebox.showinfo("提示", "正在连接服务器，请稍候...")
            
            if self.client.connect():
                messagebox.showinfo("成功", "连接服务器成功！")
                self.connected = True
                self.root.destroy()
            else:
                messagebox.showerror("错误", "连接服务器失败！\n请检查：\n1. 服务器是否已启动\n2. 地址和端口是否正确\n3. 网络连接是否正常")
        
        except ValueError:
            messagebox.showerror("错误", "端口号必须是数字！")
        except Exception as e:
            messagebox.showerror("错误", f"连接失败: {e}")
    
    def run(self):
        """运行对话框"""
        self.root.mainloop()
        return self.connected, self.client


def main():
    """主函数"""
    print("="*60)
    print("本科教学管理系统 - 网络客户端")
    print("="*60)
    print("启动中...")
    
    # 显示连接对话框
    dialog = ConnectionDialog()
    connected, client = dialog.run()
    
    if not connected or not client:
        print("未连接到服务器，程序退出")
        return
    
    # 创建并运行登录窗口（网络版本）
    app = NetworkLoginWindow(client)
    app.run()
    
    # 断开连接
    client.disconnect()
    print("系统已关闭")


if __name__ == '__main__':
    main()
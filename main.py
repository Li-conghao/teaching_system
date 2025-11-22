#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本科教学管理系统 - 本地模式启动文件
直接在本地运行，不需要网络连接
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.login_window import LoginWindow


def main():
    """主函数"""
    print("="*60)
    print("本科教学管理系统 - 本地模式")
    print("="*60)
    print("启动中...")
    
    # 创建并运行登录窗口
    app = LoginWindow()
    app.run()
    
    print("系统已关闭")


if __name__ == '__main__':
    main()
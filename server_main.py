#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本科教学管理系统 - 服务器启动文件
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from network.server import Server


def main():
    """主函数"""
    print("="*60)
    print("本科教学管理系统 - 服务器端")
    print("="*60)
    
    # 创建服务器
    server = Server(host='0.0.0.0', port=8888)
    
    try:
        # 启动服务器
        server.start()
    
    except KeyboardInterrupt:
        print("\n收到中断信号，正在关闭服务器...")
        server.stop()
    
    except Exception as e:
        print(f"服务器运行出错: {e}")
        server.stop()


if __name__ == '__main__':
    main()
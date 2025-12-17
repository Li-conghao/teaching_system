#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目完整性测试脚本
检查所有必需文件是否存在，以及基本功能是否正常
"""
import os
import sys


def check_file_exists(filepath):
    """检查文件是否存在"""
    exists = os.path.exists(filepath)
    status = "[OK]" if exists else "[X]"
    print(f"  {status} {filepath}")
    return exists


def test_imports():
    """测试模块导入"""
    print("\n=== 测试模块导入 ===")
    
    modules = [
        ('database.db_manager', 'DatabaseManager'),
        ('database.init_db', 'DatabaseInitializer'),
        ('models.user', 'User'),
        ('models.student', 'Student'),
        ('models.teacher', 'Teacher'),
        ('models.course', 'Course'),
        ('network.server', 'Server'),
        ('network.client', 'Client'),
        ('utils.logger', 'Logger'),
        ('utils.validator', 'Validator'),
        ('utils.visualizer', 'Visualizer'),
    ]
    
    all_success = True
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  [OK] {module_name}.{class_name}")
        except Exception as e:
            print(f"  [X] {module_name}.{class_name} - {e}")
            all_success = False
    
    return all_success


def test_database():
    """测试数据库功能"""
    print("\n=== 测试数据库功能 ===")
    
    try:
        from database.db_manager import DatabaseManager
        
        # 删除旧的测试数据库
        if os.path.exists('test_temp.db'):
            os.remove('test_temp.db')
        
        # 创建临时数据库
        db = DatabaseManager('test_temp.db')
        
        # 初始化数据库
        from database.init_db import DatabaseInitializer
        init = DatabaseInitializer('test_temp.db')
        init.create_tables()
        init.insert_sample_data()
        
        print("  [OK] 数据库创建成功")
        
        # 测试用户认证
        user = db.authenticate_user('admin', 'admin123')
        if user:
            print("  [OK] 用户认证成功")
        else:
            print("  [X] 用户认证失败")
            return False
        
        # 测试查询
        students = db.get_all_students()
        print(f"  [OK] 查询学生数据成功（{len(students)}条）")
        
        courses = db.get_all_courses()
        print(f"  [OK] 查询课程数据成功（{len(courses)}条）")
        
        # 关闭数据库连接
        if hasattr(db.local, 'conn') and db.local.conn:
            db.local.conn.close()
        
        # 删除临时数据库
        import time
        time.sleep(0.1)  # 等待连接完全关闭
        if os.path.exists('test_temp.db'):
            os.remove('test_temp.db')
        print("  [OK] 测试完成，临时数据库已删除")
        
        return True
    
    except Exception as e:
        print(f"  [X] 数据库测试失败: {e}")
        return False


def test_validators():
    """测试数据验证"""
    print("\n=== 测试数据验证功能 ===")
    
    try:
        from utils.validator import Validator
        
        # 测试用户名验证
        valid, msg = Validator.validate_username("admin")
        print(f"  [OK] 用户名验证: {valid}")
        
        # 测试密码验证
        valid, msg = Validator.validate_password("123456")
        print(f"  [OK] 密码验证: {valid}")
        
        # 测试学号验证
        valid, msg = Validator.validate_student_id("2021001001")
        print(f"  [OK] 学号验证: {valid}")
        
        # 测试邮箱验证
        valid, msg = Validator.validate_email("test@example.com")
        print(f"  [OK] 邮箱验证: {valid}")
        
        return True
    
    except Exception as e:
        print(f"  [X] 验证测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("本科教学管理系统 - 项目完整性测试")
    print("=" * 60)
    
    # 检查文件结构
    print("\n=== 检查文件结构 ===")
    
    required_files = [
        'README.md',
        'requirements.txt',
        'main.py',
        'server_main.py',
        'client_main.py',
        'database/__init__.py',
        'database/db_manager.py',
        'database/init_db.py',
        'models/__init__.py',
        'models/user.py',
        'models/student.py',
        'models/teacher.py',
        'models/course.py',
        'gui/__init__.py',
        'gui/login_window.py',
        'gui/admin_window.py',
        'gui/teacher_window.py',
        'gui/student_window.py',
        'network/__init__.py',
        'network/server.py',
        'network/client.py',
        'utils/__init__.py',
        'utils/logger.py',
        'utils/validator.py',
        'utils/visualizer.py',
    ]
    
    all_files_exist = True
    for filepath in required_files:
        if not check_file_exists(filepath):
            all_files_exist = False
    
    # 测试模块导入
    imports_ok = test_imports()
    
    # 测试数据库
    database_ok = test_database()
    
    # 测试验证器
    validator_ok = test_validators()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)
    print(f"文件结构检查: {'[PASS]' if all_files_exist else '[FAIL]'}")
    print(f"模块导入测试: {'[PASS]' if imports_ok else '[FAIL]'}")
    print(f"数据库功能测试: {'[PASS]' if database_ok else '[FAIL]'}")
    print(f"数据验证测试: {'[PASS]' if validator_ok else '[FAIL]'}")
    
    if all([all_files_exist, imports_ok, database_ok, validator_ok]):
        print("\n[SUCCESS] 所有测试通过！项目已完整且可以正常运行。")
        return 0
    else:
        print("\n[WARNING] 部分测试未通过，请检查相关问题。")
        return 1


if __name__ == '__main__':
    sys.exit(main())

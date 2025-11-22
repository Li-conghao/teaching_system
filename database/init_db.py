"""
数据库初始化模块
创建表结构并插入示例数据
"""
import sqlite3
import hashlib
from datetime import datetime


class DatabaseInitializer:
    """数据库初始化类"""
    
    def __init__(self, db_path='teaching_system.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def _hash_password(self, password):
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_tables(self):
        """创建所有表"""
        print("正在创建数据库表...")
        
        # 用户表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'teacher', 'student')),
                status TEXT DEFAULT 'active' CHECK(status IN ('active', 'inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 学生表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL,
                name TEXT NOT NULL,
                gender TEXT CHECK(gender IN ('男', '女')),
                birth_date DATE,
                major TEXT,
                grade TEXT,
                class_name TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # 教师表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id TEXT PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL,
                name TEXT NOT NULL,
                gender TEXT CHECK(gender IN ('男', '女')),
                birth_date DATE,
                department TEXT,
                title TEXT,
                phone TEXT,
                email TEXT,
                office TEXT,
                hire_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # 课程表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                course_name TEXT NOT NULL,
                teacher_id TEXT,
                credits REAL NOT NULL,
                hours INTEGER NOT NULL,
                semester TEXT,
                class_time TEXT,
                classroom TEXT,
                capacity INTEGER DEFAULT 50,
                status TEXT DEFAULT 'open' CHECK(status IN ('open', 'closed')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
            )
        ''')
        
        # 选课表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                course_id TEXT NOT NULL,
                enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        ''')
        
        # 成绩表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                course_id TEXT NOT NULL,
                usual_score REAL,
                exam_score REAL,
                final_score REAL,
                grade_level TEXT,
                semester TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        ''')
        
        # 日志表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                action TEXT NOT NULL,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("[OK] 数据库表创建完成")
    
    def insert_sample_data(self):
        """插入示例数据"""
        # 检查是否已有数据
        self.cursor.execute('SELECT COUNT(*) FROM users')
        user_count = self.cursor.fetchone()[0]
        
        if user_count > 0:
            print(f"[警告] 数据库中已存在 {user_count} 个用户")
            response = input("是否清空现有数据并重新初始化？(y/n): ")
            if response.lower() != 'y':
                print("[取消] 已取消数据初始化")
                self.conn.close()
                return
            
            # 清空所有表的数据
            print("正在清空现有数据...")
            tables = ['grades', 'enrollments', 'courses', 'teachers', 'students', 'users', 'logs']
            for table in tables:
                self.cursor.execute(f'DELETE FROM {table}')
            self.conn.commit()
            print("[OK] 现有数据已清空")
        
        print("正在插入示例数据...")
        
        # 插入管理员
        self._insert_admin()
        
        # 插入教师
        self._insert_teachers()
        
        # 插入学生
        self._insert_students()
        
        # 插入课程
        self._insert_courses()
        
        # 插入选课记录
        self._insert_enrollments()
        
        # 插入成绩
        self._insert_grades()
        
        self.conn.commit()
        print("[OK] 示例数据插入完成")
        self.conn.close()
    
    def _insert_admin(self):
        """插入管理员账号"""
        admin_password = self._hash_password('admin123')
        
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password_hash, role, status)
                VALUES ('admin', ?, 'admin', 'active')
            ''', (admin_password,))
            print("  - 管理员账号: admin / admin123")
        except Exception as e:
            print(f"  [警告] 管理员账号已存在，跳过")
    
    def _insert_teachers(self):
        """插入教师数据"""
        teachers = [
            ('teacher001', '张教授', '男', '1975-03-15', '计算机科学', '教授', '13800001001', 'zhang@university.edu', 'A101', '2000-09-01'),
            ('teacher002', '李副教授', '女', '1980-07-20', '计算机科学', '副教授', '13800001002', 'li@university.edu', 'A102', '2005-09-01'),
            ('teacher003', '王讲师', '男', '1985-11-10', '软件工程', '讲师', '13800001003', 'wang@university.edu', 'B201', '2010-09-01'),
            ('teacher004', '赵副教授', '女', '1978-05-25', '数据科学', '副教授', '13800001004', 'zhao@university.edu', 'B202', '2003-09-01'),
            ('teacher005', '刘讲师', '男', '1988-09-08', '人工智能', '讲师', '13800001005', 'liu@university.edu', 'C301', '2015-09-01'),
        ]
        
        for i, teacher_data in enumerate(teachers):
            teacher_id = teacher_data[0]
            password = self._hash_password('teacher123')
            
            # 创建用户账号
            self.cursor.execute('''
                INSERT INTO users (username, password_hash, role, status)
                VALUES (?, ?, 'teacher', 'active')
            ''', (teacher_id, password))
            
            user_id = self.cursor.lastrowid
            
            # 插入教师信息
            self.cursor.execute('''
                INSERT INTO teachers (
                    teacher_id, user_id, name, gender, birth_date,
                    department, title, phone, email, office, hire_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (teacher_id, user_id, *teacher_data[1:]))
        
        print(f"  - 插入了 {len(teachers)} 个教师账号 (密码: teacher123)")
    
    def _insert_students(self):
        """插入学生数据"""
        students = [
            ('2021001001', '张三', '男', '2003-01-15', '计算机科学与技术', '2021', '1班', '13900001001', 'zhangsan@student.edu', '北京市'),
            ('2021001002', '李四', '女', '2003-02-20', '计算机科学与技术', '2021', '1班', '13900001002', 'lisi@student.edu', '上海市'),
            ('2021001003', '王五', '男', '2003-03-10', '计算机科学与技术', '2021', '1班', '13900001003', 'wangwu@student.edu', '广州市'),
            ('2021002001', '赵六', '女', '2003-04-05', '软件工程', '2021', '2班', '13900002001', 'zhaoliu@student.edu', '深圳市'),
            ('2021002002', '钱七', '男', '2003-05-12', '软件工程', '2021', '2班', '13900002002', 'qianqi@student.edu', '杭州市'),
            ('2022001001', '孙八', '女', '2004-06-18', '计算机科学与技术', '2022', '1班', '13900003001', 'sunba@student.edu', '南京市'),
            ('2022001002', '周九', '男', '2004-07-22', '计算机科学与技术', '2022', '1班', '13900003002', 'zhoujiu@student.edu', '武汉市'),
            ('2022002001', '吴十', '女', '2004-08-30', '数据科学与大数据技术', '2022', '2班', '13900004001', 'wushi@student.edu', '成都市'),
            ('2022002002', '郑一', '男', '2004-09-14', '数据科学与大数据技术', '2022', '2班', '13900004002', 'zhengyi@student.edu', '重庆市'),
            ('2023001001', '陈二', '女', '2005-10-08', '人工智能', '2023', '1班', '13900005001', 'chener@student.edu', '西安市'),
        ]
        
        for i, student_data in enumerate(students):
            student_id = student_data[0]
            password = self._hash_password('student123')
            
            # 创建用户账号
            self.cursor.execute('''
                INSERT INTO users (username, password_hash, role, status)
                VALUES (?, ?, 'student', 'active')
            ''', (student_id, password))
            
            user_id = self.cursor.lastrowid
            
            # 插入学生信息
            self.cursor.execute('''
                INSERT INTO students (
                    student_id, user_id, name, gender, birth_date,
                    major, grade, class_name, phone, email, address
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, user_id, *student_data[1:]))
        
        print(f"  - 插入了 {len(students)} 个学生账号 (密码: student123)")
    
    def _insert_courses(self):
        """插入课程数据"""
        courses = [
            ('CS101', 'Python程序设计', 'teacher001', 3.0, 48, '2024-2025-1', '周一 1-2节', 'A301', 50, 'open'),
            ('CS102', '数据结构与算法', 'teacher001', 4.0, 64, '2024-2025-1', '周二 3-4节', 'A302', 50, 'open'),
            ('CS201', '操作系统原理', 'teacher002', 3.5, 56, '2024-2025-1', '周三 1-2节', 'B201', 45, 'open'),
            ('CS202', '计算机网络', 'teacher002', 3.5, 56, '2024-2025-1', '周四 3-4节', 'B202', 45, 'open'),
            ('SE101', '软件工程', 'teacher003', 3.0, 48, '2024-2025-1', '周五 1-2节', 'C101', 40, 'open'),
            ('SE201', '数据库系统', 'teacher003', 4.0, 64, '2024-2025-1', '周一 3-4节', 'C102', 40, 'open'),
            ('DS101', '数据分析基础', 'teacher004', 3.0, 48, '2024-2025-1', '周二 1-2节', 'D201', 35, 'open'),
            ('DS201', '机器学习', 'teacher004', 4.0, 64, '2024-2025-1', '周三 3-4节', 'D202', 35, 'open'),
            ('AI101', '人工智能导论', 'teacher005', 3.0, 48, '2024-2025-1', '周四 1-2节', 'E301', 30, 'open'),
            ('AI201', '深度学习', 'teacher005', 4.0, 64, '2024-2025-1', '周五 3-4节', 'E302', 30, 'open'),
        ]
        
        for course_data in courses:
            self.cursor.execute('''
                INSERT INTO courses (
                    course_id, course_name, teacher_id, credits, hours,
                    semester, class_time, classroom, capacity, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', course_data)
        
        print(f"  - 插入了 {len(courses)} 门课程")
    
    def _insert_enrollments(self):
        """插入选课记录"""
        enrollments = [
            # 学生 2021001001 的选课
            ('2021001001', 'CS101'),
            ('2021001001', 'CS102'),
            ('2021001001', 'CS201'),
            ('2021001001', 'SE101'),
            
            # 学生 2021001002 的选课
            ('2021001002', 'CS101'),
            ('2021001002', 'CS102'),
            ('2021001002', 'CS202'),
            ('2021001002', 'SE201'),
            
            # 学生 2021001003 的选课
            ('2021001003', 'CS101'),
            ('2021001003', 'CS201'),
            ('2021001003', 'SE101'),
            
            # 学生 2021002001 的选课
            ('2021002001', 'SE101'),
            ('2021002001', 'SE201'),
            ('2021002001', 'CS102'),
            
            # 学生 2021002002 的选课
            ('2021002002', 'SE101'),
            ('2021002002', 'CS101'),
            
            # 学生 2022001001 的选课
            ('2022001001', 'CS101'),
            ('2022001001', 'CS102'),
            ('2022001001', 'DS101'),
            
            # 学生 2022001002 的选课
            ('2022001002', 'CS101'),
            ('2022001002', 'CS201'),
            
            # 学生 2022002001 的选课
            ('2022002001', 'DS101'),
            ('2022002001', 'DS201'),
            ('2022002001', 'CS101'),
            
            # 学生 2022002002 的选课
            ('2022002002', 'DS101'),
            ('2022002002', 'CS102'),
            
            # 学生 2023001001 的选课
            ('2023001001', 'AI101'),
            ('2023001001', 'CS101'),
        ]
        
        for enrollment in enrollments:
            self.cursor.execute('''
                INSERT INTO enrollments (student_id, course_id)
                VALUES (?, ?)
            ''', enrollment)
        
        print(f"  - 插入了 {len(enrollments)} 条选课记录")
    
    def _insert_grades(self):
        """插入成绩数据"""
        grades = [
            # 学生 2021001001 的成绩
            ('2021001001', 'CS101', 85.0, 88.0, '2024-2025-1'),
            ('2021001001', 'CS102', 90.0, 92.0, '2024-2025-1'),
            ('2021001001', 'CS201', 78.0, 82.0, '2024-2025-1'),
            ('2021001001', 'SE101', 88.0, 86.0, '2024-2025-1'),
            
            # 学生 2021001002 的成绩
            ('2021001002', 'CS101', 92.0, 95.0, '2024-2025-1'),
            ('2021001002', 'CS102', 88.0, 90.0, '2024-2025-1'),
            ('2021001002', 'CS202', 85.0, 87.0, '2024-2025-1'),
            
            # 学生 2021001003 的成绩
            ('2021001003', 'CS101', 75.0, 78.0, '2024-2025-1'),
            ('2021001003', 'CS201', 80.0, 82.0, '2024-2025-1'),
            
            # 学生 2021002001 的成绩
            ('2021002001', 'SE101', 90.0, 88.0, '2024-2025-1'),
            ('2021002001', 'CS102', 82.0, 85.0, '2024-2025-1'),
            
            # 学生 2022001001 的成绩
            ('2022001001', 'CS101', 88.0, 90.0, '2024-2025-1'),
            ('2022001001', 'CS102', 85.0, 88.0, '2024-2025-1'),
            
            # 学生 2022002001 的成绩
            ('2022002001', 'DS101', 92.0, 94.0, '2024-2025-1'),
            ('2022002001', 'CS101', 80.0, 83.0, '2024-2025-1'),
        ]
        
        for grade_data in grades:
            student_id, course_id, usual_score, exam_score, semester = grade_data
            
            # 计算总评成绩
            final_score = usual_score * 0.4 + exam_score * 0.6
            
            # 计算等级
            if final_score >= 90:
                grade_level = '优秀'
            elif final_score >= 80:
                grade_level = '良好'
            elif final_score >= 70:
                grade_level = '中等'
            elif final_score >= 60:
                grade_level = '及格'
            else:
                grade_level = '不及格'
            
            self.cursor.execute('''
                INSERT INTO grades (
                    student_id, course_id, usual_score, exam_score,
                    final_score, grade_level, semester
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, course_id, usual_score, exam_score, 
                  final_score, grade_level, semester))
        
        print(f"  - 插入了 {len(grades)} 条成绩记录")


def main():
    """主函数"""
    print("="*60)
    print("本科教学管理系统 - 数据库初始化")
    print("="*60)
    
    initializer = DatabaseInitializer()
    initializer.create_tables()
    initializer.insert_sample_data()
    
    print("="*60)
    print("数据库初始化完成！")
    print("="*60)
    print("\n默认账号信息:")
    print("  管理员: admin / admin123")
    print("  教师: teacher001 / teacher123")
    print("  学生: 2021001001 / student123")
    print()


if __name__ == '__main__':
    main()
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
        teachers = []
        departments = ['物联网工程系', '电信工程及管理系', '智能科学与技术系', '电子信息工程系']
        titles = ['教授', '副教授', '讲师']
        for i in range(30):
            idx = i + 1
            teacher_id = f"teacher{idx:03d}"
            name = f"教师{idx:02d}"
            gender = '男' if idx % 2 == 1 else '女'
            birth_year = 1970 + (idx % 10)
            birth_date = f"{birth_year}-01-01"
            department = departments[i % len(departments)]
            title = titles[i % len(titles)]
            phone = f"1380000{idx:04d}"
            email = f"{teacher_id}@university.edu"
            office = f"T{(i % 10) + 1:03d}"
            hire_year = 2000 + (i % 20)
            hire_date = f"{hire_year}-09-01"
            teachers.append((teacher_id, name, gender, birth_date, department, title, phone, email, office, hire_date))

        for teacher_data in teachers:
            teacher_id = teacher_data[0]
            password = self._hash_password('teacher123')

            self.cursor.execute('''
                INSERT INTO users (username, password_hash, role, status)
                VALUES (?, ?, 'teacher', 'active')
            ''', (teacher_id, password))

            user_id = self.cursor.lastrowid

            self.cursor.execute('''
                INSERT INTO teachers (
                    teacher_id, user_id, name, gender, birth_date,
                    department, title, phone, email, office, hire_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (teacher_id, user_id, *teacher_data[1:]))

        print(f"  - 插入了 {len(teachers)} 个教师账号 (密码: teacher123)")
    
    def _insert_students(self):
        """插入学生数据"""
        majors = ['物联网工程', '电信工程及管理', '智能科学与技术', '电子信息工程']
        years = ['2022', '2023', '2024', '2025']
        total_students = 2000
        classes = []
        for year in years:
            for major_index, major in enumerate(majors):
                for c in range(3):
                    seq = major_index * 3 + c + 1
                    class_code = f"{seq:02d}"
                    class_name = f"{year}2151{class_code}"
                    classes.append((year, major, class_name))

        num_classes = len(classes)
        base_per_class = total_students // num_classes
        extra = total_students % num_classes

        students = []
        student_counter = 1
        surnames = ['张', '李', '王', '赵', '钱', '孙', '周', '吴', '郑', '冯', '陈', '褚', '卫']
        names2 = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

        for idx, (year, major, class_name) in enumerate(classes):
            count = base_per_class + (1 if idx < extra else 0)
            for i in range(count):
                student_id = f"{year}{student_counter:04d}"
                student_counter += 1
                fullname = surnames[(student_counter + i) % len(surnames)] + names2[i % len(names2)]
                gender = '男' if (student_counter + i) % 2 == 0 else '女'
                birth_year = int(year) - 18
                birth_date = f"{birth_year}-09-01"
                phone = f"139{int(year) % 100:02d}{idx:02d}{i:02d}"
                email = f"{student_id}@student.edu"
                address = f"{major}{year}级{class_name}"
                students.append((student_id, fullname, gender, birth_date, major, year, class_name, phone, email, address))

        for student_data in students:
            student_id = student_data[0]
            password = self._hash_password('student123')

            self.cursor.execute('''
                INSERT INTO users (username, password_hash, role, status)
                VALUES (?, ?, 'student', 'active')
            ''', (student_id, password))

            user_id = self.cursor.lastrowid

            self.cursor.execute('''
                INSERT INTO students (
                    student_id, user_id, name, gender, birth_date,
                    major, grade, class_name, phone, email, address
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, user_id, *student_data[1:]))

        print(f"  - 插入了 {len(students)} 个学生账号 (密码: student123)")
    
    def _insert_courses(self):
        """插入课程数据"""
        majors = ['物联网工程', '电信工程及管理', '智能科学与技术', '电子信息工程']
        years = ['2022', '2023', '2024', '2025']
        curriculum = {
            '物联网工程': {
                '2022': ['物联网导论', '高等数学A', 'Python程序设计', '电路分析基础', '大学物理'],
                '2023': ['传感器原理', '离散数学', 'C语言程序设计', '数字电路', '线性代数'],
                '2024': ['嵌入式系统', '数据结构与算法', '信号与系统', '概率论与数理统计', '物联网通信技术'],
                '2025': ['无线传感网络', '操作系统', '数据库系统', '计算机网络', '物联网项目实践'],
            },
            '电信工程及管理': {
                '2022': ['通信工程导论', '高等数学B', '管理学原理', 'Python程序设计', '大学英语'],
                '2023': ['信号与系统', '市场营销', 'C语言程序设计', '电子电路', '线性代数'],
                '2024': ['数字通信原理', '数据结构与算法', '运筹学', '概率论与数理统计', '通信网络管理'],
                '2025': ['移动通信', '网络规划与设计', '数据库系统', '计算机网络', '通信工程项目管理'],
            },
            '智能科学与技术': {
                '2022': ['智能科学导论', '高等数学A', 'Python程序设计', '线性代数', '大学物理'],
                '2023': ['数据结构与算法', '概率论与数理统计', 'C语言程序设计', '离散数学', '机器学习基础'],
                '2024': ['人工智能', '模式识别', '数据库系统', '计算机网络', '最优化方法'],
                '2025': ['深度学习', '自然语言处理', '智能系统设计', '大数据分析', '强化学习'],
            },
            '电子信息工程': {
                '2022': ['电子信息工程导论', '高等数学B', 'C语言程序设计', '电路分析基础', '大学物理'],
                '2023': ['数字电路', '信号与系统', 'Python程序设计', '线性代数', '模拟电子技术'],
                '2024': ['数字信号处理', '嵌入式系统', '通信原理', '概率论与数理统计', '单片机原理'],
                '2025': ['无线通信', '射频技术', '集成电路设计', '计算机网络', '电子系统设计'],
            },
        }

        teacher_ids = []
        self.cursor.execute('SELECT teacher_id FROM teachers ORDER BY teacher_id')
        for row in self.cursor.fetchall():
            teacher_ids.append(row[0])

        courses = []
        class_courses = {}
        class_index = 0
        for year in years:
            for major_index, major in enumerate(majors):
                for c in range(3):
                    seq = major_index * 3 + c + 1
                    class_code = f"{seq:02d}"
                    class_name = f"{year}2151{class_code}"
                    key = (year, major, class_name)
                    class_courses[key] = []
                    course_names = curriculum[major][year]
                    for ci, cname in enumerate(course_names):
                        course_id = f"C{year}{major_index+1}{c+1}{ci+1:02d}"
                        teacher_id = teacher_ids[(class_index + ci) % len(teacher_ids)] if teacher_ids else None
                        credits = 3.0
                        hours = 48
                        semester = f"{year}-1"
                        class_time = f"周{(ci % 5) + 1} {1 + (ci % 4)}- {2 + (ci % 4)}节"
                        classroom = f"{chr(65 + (major_index % 4))}{(c+1)*100 + ci}"
                        capacity = 100
                        status = 'open'
                        courses.append((course_id, cname, teacher_id, credits, hours, semester, class_time, classroom, capacity, status))
                        class_courses[key].append(course_id)
                    class_index += 1

        for course_data in courses:
            self.cursor.execute('''
                INSERT INTO courses (
                    course_id, course_name, teacher_id, credits, hours,
                    semester, class_time, classroom, capacity, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', course_data)

        self.class_courses = class_courses

        print(f"  - 插入了 {len(courses)} 门课程")
    
    def _insert_enrollments(self):
        """插入选课记录"""
        enrollments = []
        self.cursor.execute('SELECT student_id, grade, major, class_name FROM students')
        student_rows = self.cursor.fetchall()
        for row in student_rows:
            student_id, grade, major, class_name = row
            key = (grade, major, class_name)
            if not hasattr(self, 'class_courses') or key not in self.class_courses:
                continue
            course_ids = self.class_courses[key]
            for course_id in course_ids:
                enrollments.append((student_id, course_id))

        for enrollment in enrollments:
            self.cursor.execute('''
                INSERT INTO enrollments (student_id, course_id)
                VALUES (?, ?)
            ''', enrollment)

        print(f"  - 插入了 {len(enrollments)} 条选课记录")
    
    def _insert_grades(self):
        """插入成绩数据"""
        grades = []
        self.cursor.execute('SELECT student_id, course_id FROM enrollments')
        rows = self.cursor.fetchall()
        for idx, row in enumerate(rows):
            student_id, course_id = row
            usual_score = 60 + (idx % 41)
            exam_score = 55 + (idx % 46)
            if usual_score > 100:
                usual_score = 100
            if exam_score > 100:
                exam_score = 100
            semester = '2024-2025-1'
            final_score = usual_score * 0.4 + exam_score * 0.6
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
            grades.append((student_id, course_id, usual_score, exam_score, final_score, grade_level, semester))

        for grade_data in grades:
            self.cursor.execute('''
                INSERT INTO grades (
                    student_id, course_id, usual_score, exam_score,
                    final_score, grade_level, semester
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', grade_data)

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
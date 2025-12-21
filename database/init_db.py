"""
数据库初始化模块
创建表结构并插入示例数据
"""
import sqlite3
import hashlib
import random
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
            # 自动清空以便重新生成
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
        
        # 插入课程并生成选课和成绩
        self._insert_courses_and_grades()
        
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
        # 调整年级：2021级（大四）、2022级（大三）、2023级（大二）、2024级（大一）
        # 假设现在是2025年上半年
        years = ['2021', '2022', '2023', '2024']
        total_students = 2000
        classes = []
        
        # 生成班级列表
        for year in years:
            for major_index, major in enumerate(majors):
                for c in range(3): # 每个专业每个年级3个班
                    seq = major_index * 3 + c + 1
                    class_code = f"{seq:02d}"
                    class_name = f"{year}2151{class_code}"
                    classes.append((year, major, class_name))

        num_classes = len(classes)
        base_per_class = total_students // num_classes
        extra = total_students % num_classes

        students = []
        year_counters = {y: 1 for y in years}
        surnames = ['张', '李', '王', '赵', '钱', '孙', '周', '吴', '郑', '冯', '陈', '褚', '卫']
        names2 = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

        for idx, (year, major, class_name) in enumerate(classes):
            count = base_per_class + (1 if idx < extra else 0)
            for i in range(count):
                seq = year_counters.get(year, 1)
                student_id = f"{year}{seq:04d}"
                year_counters[year] = seq + 1
                fullname = surnames[(seq + i) % len(surnames)] + names2[i % len(names2)]
                gender = '男' if (seq + i) % 2 == 0 else '女'
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
    
    def _insert_courses_and_grades(self):
        """插入课程并生成选课和成绩数据"""
        
        # 定义专业课程体系 (按学期 1-8)
        curriculum = {
            '物联网工程': {
                1: ['物联网导论', '高等数学A(1)', '大学英语(1)', '计算机导论'],
                2: ['高等数学A(2)', '大学英语(2)', 'C语言程序设计', '线性代数'],
                3: ['数据结构', '电路分析基础', '概率论与数理统计', '离散数学'],
                4: ['操作系统', '数字电子技术', '模拟电子技术', '计算机网络'],
                5: ['数据库系统原理', '传感器原理及应用', '无线传感器网络', 'Java程序设计'],
                6: ['嵌入式系统设计', 'RFID原理及应用', '物联网通信技术', '软件工程'],
                7: ['物联网信息安全', '云计算与大数据', '人工智能基础', '移动应用开发'],
                8: ['毕业设计', '物联网工程实践']
            },
            '电信工程及管理': {
                1: ['通信工程导论', '高等数学B(1)', '大学英语(1)', '管理学原理'],
                2: ['高等数学B(2)', '大学英语(2)', 'C语言程序设计', '宏微观经济学'],
                3: ['电路分析基础', '概率论与数理统计', '线性代数', '市场营销学'],
                4: ['信号与系统', '模拟电子技术', '数字电子技术', '通信电子线路'],
                5: ['数字信号处理', '通信原理', '电磁场与电磁波', '现代交换技术'],
                6: ['移动通信', '光纤通信', '数据通信与计算机网络', '通信网规划'],
                7: ['4G/5G移动通信技术', '电信项目管理', '网络优化', '宽带接入技术'],
                8: ['毕业设计', '电信工程综合实践']
            },
            '智能科学与技术': {
                1: ['智能科学导论', '高等数学A(1)', '大学英语(1)', 'Python程序设计'],
                2: ['高等数学A(2)', '大学英语(2)', '线性代数', 'C++程序设计'],
                3: ['数据结构与算法', '概率论与数理统计', '离散数学', '数字逻辑'],
                4: ['计算机组成原理', '操作系统', '人工智能基础', '矩阵论'],
                5: ['机器学习', '模式识别', '数字图像处理', '数据库系统'],
                6: ['深度学习', '自然语言处理', '计算机视觉', '智能机器人'],
                7: ['强化学习', '知识图谱', '类脑计算', '智能系统设计'],
                8: ['毕业设计', '智能科学综合实践']
            },
            '电子信息工程': {
                1: ['电子信息导论', '高等数学A(1)', '大学英语(1)', '工程制图'],
                2: ['高等数学A(2)', '大学英语(2)', 'C语言程序设计', '线性代数'],
                3: ['电路分析基础', '复变函数与积分变换', '大学物理(1)', '概率论'],
                4: ['模拟电子技术', '数字电子技术', '信号与系统', '大学物理(2)'],
                5: ['数字信号处理', '电磁场与电磁波', '微机原理与接口', '通信原理'],
                6: ['信息论与编码', 'DSP技术及应用', '单片机原理', '天线与电波传播'],
                7: ['雷达原理', '图像传输技术', '微波技术', 'FPGA设计基础'],
                8: ['毕业设计', '电子系统综合设计']
            }
        }
        
        # 获取所有教师ID
        teacher_ids = []
        self.cursor.execute('SELECT teacher_id FROM teachers ORDER BY teacher_id')
        for row in self.cursor.fetchall():
            teacher_ids.append(row[0])
            
        # 获取所有学生信息: (id, grade, major, class_name)
        self.cursor.execute('SELECT student_id, grade, major, class_name FROM students')
        all_students = self.cursor.fetchall()
        
        # 按班级分组学生
        class_students = {}
        for s in all_students:
            key = (s[1], s[2], s[3]) # (grade, major, class_name)
            if key not in class_students:
                class_students[key] = []
            class_students[key].append(s[0])
            
        # 当前年份 (假设2025年上半年，即2024-2025学年第2学期正在进行或刚结束，
        # 为了有完整成绩，我们生成到 2024-2025-1 学期)
        # 2021级: 2021-1, 2021-2, 2022-1, 2022-2, 2023-1, 2023-2, 2024-1 (共7个学期)
        # 2022级: 2022-1, 2022-2, 2023-1, 2023-2, 2024-1 (共5个学期)
        # 2023级: 2023-1, 2023-2, 2024-1 (共3个学期)
        # 2024级: 2024-1 (共1个学期)
        
        grades_map = {
            '2021': 7,
            '2022': 5,
            '2023': 3,
            '2024': 1
        }
        
        course_counter = 0
        total_enrollments = 0
        total_grades = 0
        
        # 遍历所有班级
        for (grade_year, major, class_name), students in class_students.items():
            if grade_year not in grades_map:
                continue
                
            max_terms = grades_map[grade_year]
            
            # 遍历该年级应该有的学期
            for term in range(1, max_terms + 1):
                # 计算学期名称
                year_offset = (term - 1) // 2
                is_second_semester = (term % 2 == 0)
                
                start_year = int(grade_year) + year_offset
                semester_name = f"{start_year}-{start_year+1}-{2 if is_second_semester else 1}"
                
                # 获取该学期的课程列表
                term_courses = curriculum.get(major, {}).get(term, [])
                
                for c_name in term_courses:
                    # 创建课程实例
                    course_counter += 1
                    # course_id: C + year + term + counter
                    course_id = f"C{grade_year}{term}{course_counter:05d}"
                    
                    # 随机分配老师
                    teacher_id = random.choice(teacher_ids)
                    
                    # 插入课程
                    self.cursor.execute('''
                        INSERT INTO courses (
                            course_id, course_name, teacher_id, credits, hours,
                            semester, class_time, classroom, capacity, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        course_id, c_name, teacher_id, 
                        3.0 if '实验' not in c_name else 1.5, 
                        48 if '实验' not in c_name else 24,
                        semester_name, 
                        f"周{random.randint(1,5)}", 
                        f"教{random.randint(101, 505)}", 
                        60, 'closed'
                    ))
                    
                    # 确定该课程的挂科率 (10% - 20%)
                    num_students = len(students)
                    fail_rate = random.uniform(0.10, 0.20)
                    fail_count = int(num_students * fail_rate)
                    
                    # 随机打乱学生列表以分配成绩
                    student_list = list(students)
                    random.shuffle(student_list)
                    
                    fail_students = student_list[:fail_count]
                    pass_students = student_list[fail_count:]
                    
                    # 生成成绩
                    for sid in students:
                        if sid in fail_students:
                            # 挂科: 总评 30-59
                            final_score_target = random.uniform(30, 59.9)
                        else:
                            # 通过: 总评 60-98
                            r = random.random()
                            if r < 0.2: final_score_target = random.uniform(60, 70)
                            elif r < 0.6: final_score_target = random.uniform(70, 85)
                            elif r < 0.9: final_score_target = random.uniform(85, 92)
                            else: final_score_target = random.uniform(92, 98)
                        
                        # 反推平时分和期末分 (final = 0.4*usual + 0.6*exam)
                        usual_score = random.uniform(70, 95)
                        exam_score = (final_score_target - 0.4 * usual_score) / 0.6
                        
                        # 边界修正
                        if exam_score < 0: exam_score = 0
                        if exam_score > 100: exam_score = 100
                        
                        # 重新计算 final 以保持一致性
                        final_score = usual_score * 0.4 + exam_score * 0.6
                        
                        if final_score >= 90: grade_level = '优秀'
                        elif final_score >= 80: grade_level = '良好'
                        elif final_score >= 70: grade_level = '中等'
                        elif final_score >= 60: grade_level = '及格'
                        else: grade_level = '不及格'
                        
                        # 插入选课
                        self.cursor.execute('''
                            INSERT INTO enrollments (student_id, course_id)
                            VALUES (?, ?)
                        ''', (sid, course_id))
                        total_enrollments += 1
                        
                        # 插入成绩
                        self.cursor.execute('''
                            INSERT INTO grades (
                                student_id, course_id, usual_score, exam_score,
                                final_score, grade_level, semester
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (sid, course_id, usual_score, exam_score, final_score, grade_level, semester_name))
                        total_grades += 1
                        
        print(f"  - 插入了 {course_counter} 门课程")
        print(f"  - 插入了 {total_enrollments} 条选课记录")
        print(f"  - 插入了 {total_grades} 条成绩记录")


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
    print("  学生: 20210001 / student123")
    print()


if __name__ == '__main__':
    main()
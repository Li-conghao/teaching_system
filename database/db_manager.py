"""
数据库管理模块
提供所有数据库操作的接口
"""
import sqlite3
import hashlib
import threading
from datetime import datetime
from contextlib import contextmanager


class DatabaseManager:
    """数据库管理类"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, db_path='teaching_system.db'):
        if not hasattr(self, 'initialized'):
            self.db_path = db_path
            self.local = threading.local()
            self.initialized = True
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接（线程安全）"""
        if not hasattr(self.local, 'conn') or self.local.conn is None:
            self.local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.local.conn.row_factory = sqlite3.Row
        
        try:
            yield self.local.conn
        except Exception as e:
            self.local.conn.rollback()
            raise e
    
    def _hash_password(self, password):
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _dict_from_row(self, row):
        """将Row对象转换为字典"""
        if row is None:
            return None
        return dict(row)
    
    # ==================== 用户认证相关 ====================
    
    def authenticate_user(self, username, password):
        """验证用户登录"""
        password_hash = self._hash_password(password)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users 
                WHERE username = ? AND password_hash = ? AND status = 'active'
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            
            if user:
                # 记录登录日志
                self.add_log(username, 'login', f'用户 {username} 登录系统')
                return self._dict_from_row(user)
            
            return None
    
    def add_log(self, username, action, description):
        """添加日志"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs (username, action, description)
                VALUES (?, ?, ?)
            ''', (username, action, description))
            conn.commit()
    
    # ==================== 用户管理 ====================
    
    def get_all_users(self):
        """获取所有用户"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users ORDER BY user_id')
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    def add_user(self, username, password, role):
        """添加用户"""
        password_hash = self._hash_password(password)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (username, password_hash, role, status)
                    VALUES (?, ?, ?, 'active')
                ''', (username, password_hash, role))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
    
    def update_user_status(self, user_id, status):
        """更新用户状态"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (status, user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_user(self, user_id):
        """删除用户"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def change_password(self, username, old_password, new_password):
        """修改密码"""
        # 先验证旧密码
        user = self.authenticate_user(username, old_password)
        if not user:
            return False
        
        new_password_hash = self._hash_password(new_password)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP
                WHERE username = ?
            ''', (new_password_hash, username))
            conn.commit()
            return True
    
    def reset_password(self, user_id, new_password):
        """管理员重置用户密码（不需要旧密码）"""
        new_password_hash = self._hash_password(new_password)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (new_password_hash, user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    # ==================== 学生管理 ====================
    
    def get_all_students(self):
        """获取所有学生"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.*, u.username, u.status 
                FROM students s
                JOIN users u ON s.user_id = u.user_id
                ORDER BY s.student_id
            ''')
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    def get_student_by_id(self, student_id):
        """根据学号获取学生信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.*, u.username, u.status 
                FROM students s
                JOIN users u ON s.user_id = u.user_id
                WHERE s.student_id = ?
            ''', (student_id,))
            return self._dict_from_row(cursor.fetchone())
    
    def get_student_by_user_id(self, user_id):
        """根据用户ID获取学生信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students WHERE user_id = ?', (user_id,))
            return self._dict_from_row(cursor.fetchone())
    
    def add_student(self, student_data):
        """添加学生"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO students (
                        student_id, user_id, name, gender, birth_date,
                        major, grade, class_name, phone, email, address
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    student_data['student_id'], student_data['user_id'],
                    student_data['name'], student_data.get('gender'),
                    student_data.get('birth_date'), student_data.get('major'),
                    student_data.get('grade'), student_data.get('class_name'),
                    student_data.get('phone'), student_data.get('email'),
                    student_data.get('address')
                ))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    
    def update_student(self, student_id, student_data):
        """更新学生信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE students SET
                    name = ?, gender = ?, birth_date = ?,
                    major = ?, grade = ?, class_name = ?,
                    phone = ?, email = ?, address = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE student_id = ?
            ''', (
                student_data['name'], student_data.get('gender'),
                student_data.get('birth_date'), student_data.get('major'),
                student_data.get('grade'), student_data.get('class_name'),
                student_data.get('phone'), student_data.get('email'),
                student_data.get('address'), student_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_student(self, student_id):
        """删除学生"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 先删除相关的选课和成绩记录
            cursor.execute('DELETE FROM enrollments WHERE student_id = ?', (student_id,))
            cursor.execute('DELETE FROM grades WHERE student_id = ?', (student_id,))
            cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def search_students(self, keyword):
        """搜索学生"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            search_pattern = f'%{keyword}%'
            cursor.execute('''
                SELECT s.*, u.username, u.status 
                FROM students s
                JOIN users u ON s.user_id = u.user_id
                WHERE s.student_id LIKE ? OR s.name LIKE ? 
                   OR s.major LIKE ? OR s.grade LIKE ?
                ORDER BY s.student_id
            ''', (search_pattern, search_pattern, search_pattern, search_pattern))
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    # ==================== 教师管理 ====================
    
    def get_all_teachers(self):
        """获取所有教师"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.*, u.username, u.status 
                FROM teachers t
                JOIN users u ON t.user_id = u.user_id
                ORDER BY t.teacher_id
            ''')
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    def get_teacher_by_id(self, teacher_id):
        """根据教师ID获取教师信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.*, u.username, u.status 
                FROM teachers t
                JOIN users u ON t.user_id = u.user_id
                WHERE t.teacher_id = ?
            ''', (teacher_id,))
            return self._dict_from_row(cursor.fetchone())
    
    def get_teacher_by_user_id(self, user_id):
        """根据用户ID获取教师信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM teachers WHERE user_id = ?', (user_id,))
            return self._dict_from_row(cursor.fetchone())
    
    def add_teacher(self, teacher_data):
        """添加教师"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO teachers (
                        teacher_id, user_id, name, gender, birth_date,
                        department, title, phone, email, office, hire_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    teacher_data['teacher_id'], teacher_data['user_id'],
                    teacher_data['name'], teacher_data.get('gender'),
                    teacher_data.get('birth_date'), teacher_data.get('department'),
                    teacher_data.get('title'), teacher_data.get('phone'),
                    teacher_data.get('email'), teacher_data.get('office'),
                    teacher_data.get('hire_date')
                ))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    
    def update_teacher(self, teacher_id, teacher_data):
        """更新教师信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE teachers SET
                    name = ?, gender = ?, birth_date = ?,
                    department = ?, title = ?, phone = ?,
                    email = ?, office = ?, hire_date = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE teacher_id = ?
            ''', (
                teacher_data['name'], teacher_data.get('gender'),
                teacher_data.get('birth_date'), teacher_data.get('department'),
                teacher_data.get('title'), teacher_data.get('phone'),
                teacher_data.get('email'), teacher_data.get('office'),
                teacher_data.get('hire_date'), teacher_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_teacher(self, teacher_id):
        """删除教师"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM teachers WHERE teacher_id = ?', (teacher_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def search_teachers(self, keyword):
        """搜索教师"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            search_pattern = f'%{keyword}%'
            cursor.execute('''
                SELECT t.*, u.username, u.status 
                FROM teachers t
                JOIN users u ON t.user_id = u.user_id
                WHERE t.teacher_id LIKE ? OR t.name LIKE ? 
                   OR t.department LIKE ? OR t.title LIKE ?
                ORDER BY t.teacher_id
            ''', (search_pattern, search_pattern, search_pattern, search_pattern))
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    # ==================== 课程管理 ====================
    
    def get_all_courses(self):
        """获取所有课程（包含教师名和已选人数）"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, t.name as teacher_name,
                    (SELECT COUNT(*) FROM enrollments WHERE course_id = c.course_id) as enrolled_count
                FROM courses c
                LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
                ORDER BY c.course_id
            ''')
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    def get_course_by_id(self, course_id):
        """根据课程ID获取课程信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, t.name as teacher_name
                FROM courses c
                LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
                WHERE c.course_id = ?
            ''', (course_id,))
            return self._dict_from_row(cursor.fetchone())
    
    def get_courses_by_teacher(self, teacher_id):
        """获取教师的所有课程"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, t.name as teacher_name
                FROM courses c
                LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
                WHERE c.teacher_id = ?
                ORDER BY c.course_id
            ''', (teacher_id,))
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    def add_course(self, course_data):
        """添加课程"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO courses (
                        course_id, course_name, teacher_id, credits, hours,
                        semester, class_time, classroom, capacity, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    course_data['course_id'], course_data['course_name'],
                    course_data.get('teacher_id'), course_data['credits'],
                    course_data['hours'], course_data.get('semester'),
                    course_data.get('class_time'), course_data.get('classroom'),
                    course_data.get('capacity', 50), course_data.get('status', 'open')
                ))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    
    def update_course(self, course_id, course_data):
        """更新课程信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE courses SET
                    course_name = ?, teacher_id = ?, credits = ?, hours = ?,
                    semester = ?, class_time = ?, classroom = ?,
                    capacity = ?, status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE course_id = ?
            ''', (
                course_data['course_name'], course_data.get('teacher_id'),
                course_data['credits'], course_data['hours'],
                course_data.get('semester'), course_data.get('class_time'),
                course_data.get('classroom'), course_data.get('capacity', 50),
                course_data.get('status', 'open'), course_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_course(self, course_id):
        """删除课程"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 先删除相关的选课和成绩记录
            cursor.execute('DELETE FROM enrollments WHERE course_id = ?', (course_id,))
            cursor.execute('DELETE FROM grades WHERE course_id = ?', (course_id,))
            cursor.execute('DELETE FROM courses WHERE course_id = ?', (course_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def search_courses(self, keyword):
        """搜索课程"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            search_pattern = f'%{keyword}%'
            cursor.execute('''
                SELECT c.*, t.name as teacher_name
                FROM courses c
                LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
                WHERE c.course_id LIKE ? OR c.course_name LIKE ? 
                   OR c.semester LIKE ?
                ORDER BY c.course_id
            ''', (search_pattern, search_pattern, search_pattern))
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    # ==================== 选课管理 ====================
    
    def enroll_course(self, student_id, course_id):
        """学生选课"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # 检查是否已选
                cursor.execute('''
                    SELECT * FROM enrollments 
                    WHERE student_id = ? AND course_id = ?
                ''', (student_id, course_id))
                if cursor.fetchone():
                    return False, "已经选过该课程"
                
                # 检查课程是否开放
                course = self.get_course_by_id(course_id)
                if not course or course['status'] != 'open':
                    return False, "课程未开放选课"
                
                # 检查是否已满
                cursor.execute('''
                    SELECT COUNT(*) as count FROM enrollments WHERE course_id = ?
                ''', (course_id,))
                enrolled_count = cursor.fetchone()[0]
                if enrolled_count >= course['capacity']:
                    return False, "课程已满"
                
                # 选课
                cursor.execute('''
                    INSERT INTO enrollments (student_id, course_id)
                    VALUES (?, ?)
                ''', (student_id, course_id))
                conn.commit()
                return True, "选课成功"
            except Exception as e:
                return False, str(e)
    
    def drop_course(self, student_id, course_id):
        """退课"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM enrollments 
                WHERE student_id = ? AND course_id = ?
            ''', (student_id, course_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_student_courses(self, student_id):
        """获取学生的所有选课"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, t.name as teacher_name, e.enrollment_date
                FROM enrollments e
                JOIN courses c ON e.course_id = c.course_id
                LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
                WHERE e.student_id = ?
                ORDER BY c.course_id
            ''', (student_id,))
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    def get_course_students(self, course_id):
        """获取课程的所有学生"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.*, e.enrollment_date
                FROM enrollments e
                JOIN students s ON e.student_id = s.student_id
                WHERE e.course_id = ?
                ORDER BY s.student_id
            ''', (course_id,))
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    # ==================== 成绩管理 ====================
    
    def add_or_update_grade(self, grade_data):
        """添加或更新成绩"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 计算总评成绩和等级
            usual_score = grade_data.get('usual_score', 0)
            exam_score = grade_data.get('exam_score', 0)
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
            
            # 检查是否已有成绩
            cursor.execute('''
                SELECT grade_id FROM grades 
                WHERE student_id = ? AND course_id = ?
            ''', (grade_data['student_id'], grade_data['course_id']))
            
            existing = cursor.fetchone()
            
            if existing:
                # 更新
                cursor.execute('''
                    UPDATE grades SET
                        usual_score = ?, exam_score = ?, final_score = ?,
                        grade_level = ?, semester = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE student_id = ? AND course_id = ?
                ''', (
                    usual_score, exam_score, final_score, grade_level,
                    grade_data.get('semester'), grade_data['student_id'],
                    grade_data['course_id']
                ))
            else:
                # 插入
                cursor.execute('''
                    INSERT INTO grades (
                        student_id, course_id, usual_score, exam_score,
                        final_score, grade_level, semester
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    grade_data['student_id'], grade_data['course_id'],
                    usual_score, exam_score, final_score, grade_level,
                    grade_data.get('semester')
                ))
            
            conn.commit()
            return True
    
    def get_student_grades(self, student_id):
        """获取学生的所有成绩"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT g.*, c.course_name, c.credits, t.name as teacher_name
                FROM grades g
                JOIN courses c ON g.course_id = c.course_id
                LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
                WHERE g.student_id = ?
                ORDER BY g.semester DESC, c.course_id
            ''', (student_id,))
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    def get_course_grades(self, course_id):
        """获取课程的所有成绩"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT g.*, s.name as student_name, s.student_id
                FROM grades g
                JOIN students s ON g.student_id = s.student_id
                WHERE g.course_id = ?
                ORDER BY g.final_score DESC
            ''', (course_id,))
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    def delete_grade(self, student_id, course_id):
        """删除成绩"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM grades 
                WHERE student_id = ? AND course_id = ?
            ''', (student_id, course_id))
            conn.commit()
            return cursor.rowcount > 0
    
    # ==================== 统计分析 ====================
    
    def get_statistics(self):
        """获取统计数据"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # 学生总数
            cursor.execute('SELECT COUNT(*) FROM students')
            stats['total_students'] = cursor.fetchone()[0]
            
            # 教师总数
            cursor.execute('SELECT COUNT(*) FROM teachers')
            stats['total_teachers'] = cursor.fetchone()[0]
            
            # 课程总数
            cursor.execute('SELECT COUNT(*) FROM courses')
            stats['total_courses'] = cursor.fetchone()[0]
            
            # 选课总数
            cursor.execute('SELECT COUNT(*) FROM enrollments')
            stats['total_enrollments'] = cursor.fetchone()[0]
            
            # 成绩记录数
            cursor.execute('SELECT COUNT(*) FROM grades')
            stats['total_grades'] = cursor.fetchone()[0]
            
            # 平均分
            cursor.execute('SELECT AVG(final_score) FROM grades')
            avg = cursor.fetchone()[0]
            stats['average_score'] = round(avg, 2) if avg else 0
            
            return stats
    
    def get_grade_distribution(self, course_id=None):
        """获取成绩分布"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if course_id:
                cursor.execute('''
                    SELECT grade_level, COUNT(*) as count
                    FROM grades
                    WHERE course_id = ?
                    GROUP BY grade_level
                    ORDER BY 
                        CASE grade_level
                            WHEN '优秀' THEN 1
                            WHEN '良好' THEN 2
                            WHEN '中等' THEN 3
                            WHEN '及格' THEN 4
                            WHEN '不及格' THEN 5
                        END
                ''', (course_id,))
            else:
                cursor.execute('''
                    SELECT grade_level, COUNT(*) as count
                    FROM grades
                    GROUP BY grade_level
                    ORDER BY 
                        CASE grade_level
                            WHEN '优秀' THEN 1
                            WHEN '良好' THEN 2
                            WHEN '中等' THEN 3
                            WHEN '及格' THEN 4
                            WHEN '不及格' THEN 5
                        END
                ''')
            
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    # ==================== 日志管理 ====================
    
    def get_logs(self, limit=100):
        """获取日志"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    def clear_logs(self):
        """清空日志"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM logs')
            conn.commit()
            return True
    
    # ==================== 教师端方法别名 ====================
    
    def get_teacher_courses(self, teacher_id):
        """获取教师的所有课程（别名方法）"""
        courses = self.get_courses_by_teacher(teacher_id)
        # 为每个课程添加已选人数
        for course in courses:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT COUNT(*) FROM enrollments WHERE course_id = ?
                ''', (course['course_id'],))
                course['enrolled_count'] = cursor.fetchone()[0]
        return courses
    
    def get_course_enrollments(self, course_id):
        """获取课程的选课学生列表（别名方法）"""
        return self.get_course_students(course_id)
    
    def add_grade(self, grade_data):
        """添加成绩（别名方法）"""
        return self.add_or_update_grade(grade_data)
    
    def get_teacher_students(self, teacher_id):
        """获取选了该教师课程的所有学生（去重），包含选课信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.*, u.status,
                    GROUP_CONCAT(c.course_id || ': ' || c.course_name, ', ') as courses
                FROM students s
                JOIN enrollments e ON s.student_id = e.student_id
                JOIN courses c ON e.course_id = c.course_id
                JOIN users u ON s.user_id = u.user_id
                WHERE c.teacher_id = ?
                GROUP BY s.student_id
                ORDER BY s.student_id
            ''', (teacher_id,))
            return [self._dict_from_row(row) for row in cursor.fetchall()]
    
    def get_student_enrollments(self, student_id):
        """获取学生的选课列表（别名方法）"""
        return self.get_student_courses(student_id)

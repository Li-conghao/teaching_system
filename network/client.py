"""
网络客户端模块
连接服务器并发送请求
"""
import socket
import json


class Client:
    """客户端类"""
    
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        """连接到服务器"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"连接服务器成功: {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"连接服务器失败: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.connected = False
        print("已断开服务器连接")
    
    def send_request(self, action, data=None):
        """发送请求"""
        if not self.connected:
            return {
                'success': False,
                'message': '未连接到服务器'
            }
        
        try:
            # 构造请求
            request = {
                'action': action,
                'data': data or {}
            }
            
            # 发送请求
            self.socket.send(json.dumps(request).encode('utf-8'))
            
            # 接收响应
            response_data = self.socket.recv(4096)
            response = json.loads(response_data.decode('utf-8'))
            
            return response
        
        except Exception as e:
            return {
                'success': False,
                'message': f'请求失败: {str(e)}'
            }
    
    # ==================== 用户操作 ====================
    
    def login(self, username, password):
        """登录"""
        return self.send_request('login', {
            'username': username,
            'password': password
        })
    
    # ==================== 学生操作 ====================
    
    def get_student_info(self, user_id):
        """获取学生信息"""
        return self.send_request('get_student_info', {
            'user_id': user_id
        })
    
    def get_student_courses(self, student_id):
        """获取学生选课"""
        return self.send_request('get_student_courses', {
            'student_id': student_id
        })
    
    def enroll_course(self, student_id, course_id):
        """选课"""
        return self.send_request('enroll_course', {
            'student_id': student_id,
            'course_id': course_id
        })
    
    def drop_course(self, student_id, course_id):
        """退课"""
        return self.send_request('drop_course', {
            'student_id': student_id,
            'course_id': course_id
        })
    
    def get_student_grades(self, student_id):
        """获取学生成绩"""
        return self.send_request('get_student_grades', {
            'student_id': student_id
        })
    
    # ==================== 教师操作 ====================
    
    def get_teacher_info(self, user_id):
        """获取教师信息"""
        return self.send_request('get_teacher_info', {
            'user_id': user_id
        })
    
    def get_teacher_courses(self, teacher_id):
        """获取教师课程"""
        return self.send_request('get_teacher_courses', {
            'teacher_id': teacher_id
        })
    
    def get_course_students(self, course_id):
        """获取课程学生"""
        return self.send_request('get_course_students', {
            'course_id': course_id
        })
    
    def get_course_grades(self, course_id):
        """获取课程成绩"""
        return self.send_request('get_course_grades', {
            'course_id': course_id
        })

    def get_teacher_students(self, teacher_id):
        """获取选了该教师课程的所有学生"""
        return self.send_request('get_teacher_students', {
            'teacher_id': teacher_id
        })
    
    def add_or_update_grade(self, grade_data):
        """录入成绩"""
        return self.send_request('add_or_update_grade', {
            'grade_data': grade_data
        })
    
    # ==================== 公共操作 ====================
    
    def get_all_courses(self):
        """获取所有课程"""
        return self.send_request('get_courses')

    # ==================== 管理员操作 ====================

    def get_statistics(self):
        """获取统计数据"""
        return self.send_request('get_statistics')

    def get_grade_distribution(self):
        """获取成绩分布"""
        return self.send_request('get_grade_distribution')

    def get_logs(self, limit=100):
        """获取系统日志"""
        return self.send_request('get_logs', {'limit': limit})

    def clear_logs(self):
        """清空系统日志"""
        return self.send_request('clear_logs')

    def get_all_students(self):
        """获取所有学生"""
        return self.send_request('get_all_students')

    def get_all_teachers(self):
        """获取所有教师"""
        return self.send_request('get_all_teachers')

    def get_all_users(self):
        """获取所有用户"""
        return self.send_request('get_all_users')

    def add_student(self, student_data, username, password):
        """添加学生（管理员）"""
        return self.send_request('add_student', {
            'student_data': student_data,
            'username': username,
            'password': password,
        })

    def update_student(self, student_id, student_data):
        """更新学生信息（管理员）"""
        return self.send_request('update_student', {
            'student_id': student_id,
            'student_data': student_data,
        })

    def delete_student(self, student_id):
        """删除学生（管理员）"""
        return self.send_request('delete_student', {
            'student_id': student_id,
        })

    def search_students(self, keyword):
        """搜索学生（管理员）"""
        return self.send_request('search_students', {
            'keyword': keyword,
        })

    def add_teacher(self, teacher_data, username, password):
        """添加教师（管理员）"""
        return self.send_request('add_teacher', {
            'teacher_data': teacher_data,
            'username': username,
            'password': password,
        })

    def update_teacher(self, teacher_id, teacher_data):
        """更新教师信息（管理员）"""
        return self.send_request('update_teacher', {
            'teacher_id': teacher_id,
            'teacher_data': teacher_data,
        })

    def delete_teacher(self, teacher_id):
        """删除教师（管理员）"""
        return self.send_request('delete_teacher', {
            'teacher_id': teacher_id,
        })

    def search_teachers(self, keyword):
        """搜索教师（管理员）"""
        return self.send_request('search_teachers', {
            'keyword': keyword,
        })

    def add_course(self, course_data):
        """添加课程（管理员）"""
        return self.send_request('add_course', {
            'course_data': course_data,
        })

    def update_course(self, course_id, course_data):
        """更新课程信息（管理员）"""
        return self.send_request('update_course', {
            'course_id': course_id,
            'course_data': course_data,
        })

    def delete_course(self, course_id):
        """删除课程（管理员）"""
        return self.send_request('delete_course', {
            'course_id': course_id,
        })

    def search_courses(self, keyword):
        """搜索课程（管理员）"""
        return self.send_request('search_courses', {
            'keyword': keyword,
        })

    # ==================== 通用账号操作 ====================

    def change_password(self, username, old_password, new_password):
        """修改密码（用户自助）"""
        return self.send_request('change_password', {
            'username': username,
            'old_password': old_password,
            'new_password': new_password,
        })


if __name__ == '__main__':
    # 测试连接
    client = Client()
    if client.connect():
        print("连接成功，测试登录...")
        result = client.login('admin', 'admin123')
        print(f"登录结果: {result}")
        client.disconnect()

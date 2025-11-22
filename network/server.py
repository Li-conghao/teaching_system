"""
网络服务器模块
处理客户端请求
"""
import socket
import threading
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager


class Server:
    """服务器类"""
    
    def __init__(self, host='0.0.0.0', port=8888):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.clients = []
        self.db = DatabaseManager()
    
    def start(self):
        """启动服务器"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"服务器启动成功")
            print(f"监听地址: {self.host}:{self.port}")
            print("等待客户端连接...")
            print("-" * 60)
            
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"新客户端连接: {address}")
                    
                    # 为每个客户端创建一个线程
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                    self.clients.append(client_socket)
                
                except Exception as e:
                    if self.running:
                        print(f"接受连接时出错: {e}")
        
        except Exception as e:
            print(f"服务器启动失败: {e}")
        
        finally:
            self.stop()
    
    def stop(self):
        """停止服务器"""
        self.running = False
        
        # 关闭所有客户端连接
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        
        # 关闭服务器socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("服务器已停止")
    
    def handle_client(self, client_socket, address):
        """处理客户端请求"""
        print(f"开始处理客户端 {address} 的请求")
        
        try:
            while self.running:
                # 接收请求
                data = client_socket.recv(4096)
                if not data:
                    break
                
                # 解析请求
                try:
                    request = json.loads(data.decode('utf-8'))
                    print(f"收到请求: {request.get('action')} from {address}")
                    
                    # 处理请求
                    response = self.process_request(request)
                    
                    # 发送响应
                    client_socket.send(json.dumps(response).encode('utf-8'))
                
                except json.JSONDecodeError:
                    error_response = {
                        'success': False,
                        'message': '无效的请求格式'
                    }
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
        
        except Exception as e:
            print(f"处理客户端 {address} 时出错: {e}")
        
        finally:
            print(f"客户端 {address} 断开连接")
            try:
                client_socket.close()
                self.clients.remove(client_socket)
            except:
                pass
    
    def process_request(self, request):
        """处理具体的请求"""
        action = request.get('action')
        data = request.get('data', {})
        
        try:
            # 用户认证
            if action == 'login':
                user = self.db.authenticate_user(
                    data.get('username'),
                    data.get('password')
                )
                if user:
                    return {
                        'success': True,
                        'data': {'user': user}
                    }
                else:
                    return {
                        'success': False,
                        'message': '用户名或密码错误'
                    }
            
            # 获取学生信息
            elif action == 'get_student_info':
                student = self.db.get_student_by_user_id(data.get('user_id'))
                if student:
                    return {
                        'success': True,
                        'data': {'student': student}
                    }
                else:
                    return {
                        'success': False,
                        'message': '未找到学生信息'
                    }
            
            # 获取教师信息
            elif action == 'get_teacher_info':
                teacher = self.db.get_teacher_by_user_id(data.get('user_id'))
                if teacher:
                    return {
                        'success': True,
                        'data': {'teacher': teacher}
                    }
                else:
                    return {
                        'success': False,
                        'message': '未找到教师信息'
                    }
            
            # 获取课程列表
            elif action == 'get_courses':
                courses = self.db.get_all_courses()
                return {
                    'success': True,
                    'data': {'courses': courses}
                }
            
            # 获取学生选课
            elif action == 'get_student_courses':
                courses = self.db.get_student_courses(data.get('student_id'))
                return {
                    'success': True,
                    'data': {'courses': courses}
                }
            
            # 选课
            elif action == 'enroll_course':
                success, message = self.db.enroll_course(
                    data.get('student_id'),
                    data.get('course_id')
                )
                return {
                    'success': success,
                    'message': message
                }
            
            # 退课
            elif action == 'drop_course':
                success = self.db.drop_course(
                    data.get('student_id'),
                    data.get('course_id')
                )
                return {
                    'success': success,
                    'message': '退课成功' if success else '退课失败'
                }
            
            # 获取成绩
            elif action == 'get_student_grades':
                grades = self.db.get_student_grades(data.get('student_id'))
                return {
                    'success': True,
                    'data': {'grades': grades}
                }
            
            # 获取教师课程
            elif action == 'get_teacher_courses':
                courses = self.db.get_courses_by_teacher(data.get('teacher_id'))
                return {
                    'success': True,
                    'data': {'courses': courses}
                }
            
            # 获取课程学生
            elif action == 'get_course_students':
                students = self.db.get_course_students(data.get('course_id'))
                return {
                    'success': True,
                    'data': {'students': students}
                }
            
            # 获取课程成绩
            elif action == 'get_course_grades':
                grades = self.db.get_course_grades(data.get('course_id'))
                return {
                    'success': True,
                    'data': {'grades': grades}
                }
            
            # 录入成绩
            elif action == 'add_or_update_grade':
                success = self.db.add_or_update_grade(data.get('grade_data'))
                return {
                    'success': success,
                    'message': '成绩录入成功' if success else '成绩录入失败'
                }
            
            # 其他操作...
            else:
                return {
                    'success': False,
                    'message': f'未知操作: {action}'
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }


if __name__ == '__main__':
    server = Server(host='0.0.0.0', port=8888)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n收到中断信号")
        server.stop()

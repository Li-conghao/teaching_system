"""
用户模型
"""


class User:
    """用户类"""
    
    def __init__(self, user_id=None, username=None, password_hash=None,
                 role=None, status='active', created_at=None, updated_at=None):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role  # admin, teacher, student
        self.status = status  # active, inactive
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """转换为字典"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password_hash': self.password_hash,
            'role': self.role,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username'),
            password_hash=data.get('password_hash'),
            role=data.get('role'),
            status=data.get('status', 'active'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def is_active(self):
        """是否激活"""
        return self.status == 'active'
    
    def is_admin(self):
        """是否管理员"""
        return self.role == 'admin'
    
    def is_teacher(self):
        """是否教师"""
        return self.role == 'teacher'
    
    def is_student(self):
        """是否学生"""
        return self.role == 'student'
    
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

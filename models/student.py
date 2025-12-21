"""
学生模型
"""


class Student:
    """学生类"""
    
    def __init__(self, student_id=None, user_id=None, name=None,
                 gender=None, birth_date=None, major=None,
                 grade=None, class_name=None, phone=None,
                 email=None, address=None, created_at=None, updated_at=None):
        self.student_id = student_id
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.major = major
        self.grade = grade
        self.class_name = class_name
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """转换为字典"""
        return {
            'student_id': self.student_id,
            'user_id': self.user_id,
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'major': self.major,
            'grade': self.grade,
            'class_name': self.class_name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        return cls(
            student_id=data.get('student_id'),
            user_id=data.get('user_id'),
            name=data.get('name'),
            gender=data.get('gender'),
            birth_date=data.get('birth_date'),
            major=data.get('major'),
            grade=data.get('grade'),
            class_name=data.get('class_name'),
            phone=data.get('phone'),
            email=data.get('email'),
            address=data.get('address'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def get_info(self):
        """获取学生信息（格式化）"""
        return f"{self.name} ({self.student_id}) - {self.major} {self.grade}级"
    
    def __repr__(self):
        return f"<Student {self.student_id} {self.name}>"

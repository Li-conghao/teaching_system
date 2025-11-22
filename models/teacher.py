"""
教师模型
"""


class Teacher:
    """教师类"""
    
    def __init__(self, teacher_id=None, user_id=None, name=None,
                 gender=None, birth_date=None, department=None,
                 title=None, phone=None, email=None, office=None,
                 hire_date=None, created_at=None, updated_at=None):
        self.teacher_id = teacher_id
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.department = department
        self.title = title
        self.phone = phone
        self.email = email
        self.office = office
        self.hire_date = hire_date
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """转换为字典"""
        return {
            'teacher_id': self.teacher_id,
            'user_id': self.user_id,
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'department': self.department,
            'title': self.title,
            'phone': self.phone,
            'email': self.email,
            'office': self.office,
            'hire_date': self.hire_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        return cls(
            teacher_id=data.get('teacher_id'),
            user_id=data.get('user_id'),
            name=data.get('name'),
            gender=data.get('gender'),
            birth_date=data.get('birth_date'),
            department=data.get('department'),
            title=data.get('title'),
            phone=data.get('phone'),
            email=data.get('email'),
            office=data.get('office'),
            hire_date=data.get('hire_date'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def get_info(self):
        """获取教师信息（格式化）"""
        return f"{self.name} ({self.teacher_id}) - {self.title} {self.department}"
    
    def __repr__(self):
        return f"<Teacher {self.teacher_id} {self.name}>"

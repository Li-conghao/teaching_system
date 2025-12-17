"""
课程模型
"""


class Course:
    """课程类"""
    
    def __init__(self, course_id=None, course_name=None, teacher_id=None,
                 credits=None, hours=None, semester=None,
                 class_time=None, classroom=None, capacity=50, status='open',
                 created_at=None, updated_at=None):
        self.course_id = course_id
        self.course_name = course_name
        self.teacher_id = teacher_id
        self.credits = credits
        self.hours = hours
        self.semester = semester
        self.class_time = class_time
        self.classroom = classroom
        self.capacity = capacity
        self.status = status  # open, closed
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """转换为字典"""
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'teacher_id': self.teacher_id,
            'credits': self.credits,
            'hours': self.hours,
            'semester': self.semester,
            'class_time': self.class_time,
            'classroom': self.classroom,
            'capacity': self.capacity,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        return cls(
            course_id=data.get('course_id'),
            course_name=data.get('course_name'),
            teacher_id=data.get('teacher_id'),
            credits=data.get('credits'),
            hours=data.get('hours'),
            semester=data.get('semester'),
            class_time=data.get('class_time'),
            classroom=data.get('classroom'),
            capacity=data.get('capacity', 50),
            status=data.get('status', 'open'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def is_open(self):
        """是否开放选课"""
        return self.status == 'open'
    
    def is_full(self, enrolled_count):
        """是否已满"""
        return enrolled_count >= self.capacity
    
    def get_info(self):
        """获取课程信息（格式化）"""
        return f"{self.course_name} ({self.course_id}) - {self.credits}学分 {self.hours}学时"
    
    def __repr__(self):
        return f"<Course {self.course_id} {self.course_name}>"
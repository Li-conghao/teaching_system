"""
数据验证工具模块
"""
import re


class Validator:
    """数据验证类"""
    
    @staticmethod
    def validate_username(username):
        """验证用户名"""
        if not username:
            return False, "用户名不能为空"
        
        if len(username) < 3:
            return False, "用户名长度至少3个字符"
        
        if len(username) > 20:
            return False, "用户名长度不能超过20个字符"
        
        # 只允许字母、数字、下划线
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "用户名只能包含字母、数字和下划线"
        
        return True, ""
    
    @staticmethod
    def validate_password(password):
        """验证密码"""
        if not password:
            return False, "密码不能为空"
        
        if len(password) < 6:
            return False, "密码长度至少6个字符"
        
        if len(password) > 20:
            return False, "密码长度不能超过20个字符"
        
        return True, ""
    
    @staticmethod
    def validate_student_id(student_id):
        """验证学号"""
        if not student_id:
            return False, "学号不能为空"
        
        # 学号格式：10位数字
        if not re.match(r'^\d{10}$', student_id):
            return False, "学号必须是10位数字"
        
        return True, ""
    
    @staticmethod
    def validate_teacher_id(teacher_id):
        """验证教师ID"""
        if not teacher_id:
            return False, "教师ID不能为空"
        
        # 教师ID格式：teacher + 3位数字
        if not re.match(r'^teacher\d{3}$', teacher_id):
            return False, "教师ID格式错误（如: teacher001）"
        
        return True, ""
    
    @staticmethod
    def validate_course_id(course_id):
        """验证课程ID"""
        if not course_id:
            return False, "课程ID不能为空"
        
        # 课程ID格式：2-4个大写字母 + 3位数字
        if not re.match(r'^[A-Z]{2,4}\d{3}$', course_id):
            return False, "课程ID格式错误（如: CS101）"
        
        return True, ""
    
    @staticmethod
    def validate_email(email):
        """验证邮箱"""
        if not email:
            return True, ""  # 邮箱可以为空
        
        # 简单的邮箱格式验证
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return False, "邮箱格式不正确"
        
        return True, ""
    
    @staticmethod
    def validate_phone(phone):
        """验证手机号"""
        if not phone:
            return True, ""  # 手机号可以为空
        
        # 中国手机号格式：11位数字，以1开头
        if not re.match(r'^1\d{10}$', phone):
            return False, "手机号格式不正确"
        
        return True, ""
    
    @staticmethod
    def validate_score(score):
        """验证分数"""
        if score is None:
            return True, ""  # 分数可以为空
        
        try:
            score = float(score)
            if score < 0 or score > 100:
                return False, "分数必须在0-100之间"
            return True, ""
        except ValueError:
            return False, "分数必须是数字"
    
    @staticmethod
    def validate_credits(credits):
        """验证学分"""
        if not credits:
            return False, "学分不能为空"
        
        try:
            credits = float(credits)
            if credits <= 0 or credits > 10:
                return False, "学分必须在0-10之间"
            return True, ""
        except ValueError:
            return False, "学分必须是数字"
    
    @staticmethod
    def validate_hours(hours):
        """验证学时"""
        if not hours:
            return False, "学时不能为空"
        
        try:
            hours = int(hours)
            if hours <= 0 or hours > 200:
                return False, "学时必须在0-200之间"
            return True, ""
        except ValueError:
            return False, "学时必须是整数"
    
    @staticmethod
    def validate_capacity(capacity):
        """验证课程容量"""
        if not capacity:
            return False, "容量不能为空"
        
        try:
            capacity = int(capacity)
            if capacity <= 0 or capacity > 500:
                return False, "容量必须在0-500之间"
            return True, ""
        except ValueError:
            return False, "容量必须是整数"
    
    @staticmethod
    def validate_name(name):
        """验证姓名"""
        if not name:
            return False, "姓名不能为空"
        
        if len(name) < 2:
            return False, "姓名长度至少2个字符"
        
        if len(name) > 20:
            return False, "姓名长度不能超过20个字符"
        
        return True, ""


if __name__ == '__main__':
    # 测试验证功能
    validator = Validator()
    
    print(validator.validate_username("admin"))
    print(validator.validate_password("123456"))
    print(validator.validate_student_id("2021001001"))
    print(validator.validate_email("test@example.com"))
    print(validator.validate_phone("13800138000"))
    print(validator.validate_score(85.5))

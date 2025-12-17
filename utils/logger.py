"""
日志工具模块
"""
import logging
from datetime import datetime
import os


class Logger:
    """日志记录器"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.log_dir = 'logs'
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            
            # 配置日志
            log_file = os.path.join(
                self.log_dir,
                f'system_{datetime.now().strftime("%Y%m%d")}.log'
            )
            
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )
            
            self.logger = logging.getLogger('TeachingSystem')
            self.initialized = True
    
    def info(self, message):
        """记录信息日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """记录警告日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """记录错误日志"""
        self.logger.error(message)
    
    def debug(self, message):
        """记录调试日志"""
        self.logger.debug(message)
    
    def log_user_action(self, username, action, details=''):
        """记录用户操作"""
        message = f"用户: {username} | 操作: {action}"
        if details:
            message += f" | 详情: {details}"
        self.info(message)


# 创建全局日志对象
system_logger = Logger()


if __name__ == '__main__':
    # 测试日志功能
    logger = Logger()
    logger.info("系统启动")
    logger.log_user_action("admin", "登录", "管理员登录系统")
    logger.warning("这是一个警告")
    logger.error("这是一个错误")

"""
数据可视化工具模块
"""
try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('TkAgg')  # 使用TkAgg后端
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("警告: matplotlib未安装，数据可视化功能不可用")


class Visualizer:
    """数据可视化类"""
    
    @staticmethod
    def is_available():
        """检查可视化功能是否可用"""
        return MATPLOTLIB_AVAILABLE
    
    @staticmethod
    def plot_grade_distribution(data, title="成绩分布", save_path=None):
        """绘制成绩分布图"""
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib未安装，无法绘制图表")
            return False
        
        try:
            # 数据格式: [{'grade_level': '优秀', 'count': 10}, ...]
            labels = [item['grade_level'] for item in data]
            counts = [item['count'] for item in data]
            
            # 创建图表
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # 柱状图
            colors = ['#4CAF50', '#2196F3', '#FFC107', '#FF9800', '#F44336']
            ax1.bar(labels, counts, color=colors[:len(labels)])
            ax1.set_xlabel('成绩等级', fontsize=12)
            ax1.set_ylabel('人数', fontsize=12)
            ax1.set_title(f'{title} - 柱状图', fontsize=14, fontweight='bold')
            ax1.grid(axis='y', alpha=0.3)
            
            # 在柱状图上显示数值
            for i, count in enumerate(counts):
                ax1.text(i, count, str(count), ha='center', va='bottom')
            
            # 饼图
            ax2.pie(counts, labels=labels, autopct='%1.1f%%',
                   colors=colors[:len(labels)], startangle=90)
            ax2.set_title(f'{title} - 饼图', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"图表已保存到: {save_path}")
            else:
                plt.show()
            
            plt.close()
            return True
        
        except Exception as e:
            print(f"绘制图表失败: {e}")
            return False
    
    @staticmethod
    def plot_score_trend(data, title="成绩趋势", save_path=None):
        """绘制成绩趋势图"""
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib未安装，无法绘制图表")
            return False
        
        try:
            # 数据格式: [{'course_name': '课程名', 'score': 85}, ...]
            courses = [item['course_name'] for item in data]
            scores = [item['score'] for item in data]
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # 绘制折线图
            ax.plot(courses, scores, marker='o', linewidth=2, markersize=8,
                   color='#2196F3', markerfacecolor='#FFC107')
            
            ax.set_xlabel('课程', fontsize=12)
            ax.set_ylabel('成绩', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 100)
            
            # 在数据点上显示分数
            for i, score in enumerate(scores):
                ax.text(i, score + 2, f'{score:.1f}', ha='center')
            
            # 旋转x轴标签
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"图表已保存到: {save_path}")
            else:
                plt.show()
            
            plt.close()
            return True
        
        except Exception as e:
            print(f"绘制图表失败: {e}")
            return False
    
    @staticmethod
    def plot_course_statistics(data, title="课程统计", save_path=None):
        """绘制课程统计图"""
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib未安装，无法绘制图表")
            return False
        
        try:
            # 数据格式: [{'course_name': '课程名', 'enrolled': 45, 'capacity': 50}, ...]
            courses = [item['course_name'] for item in data]
            enrolled = [item['enrolled'] for item in data]
            capacity = [item['capacity'] for item in data]
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(12, 6))
            
            x = range(len(courses))
            width = 0.35
            
            # 绘制分组柱状图
            ax.bar([i - width/2 for i in x], enrolled, width, 
                  label='已选人数', color='#4CAF50')
            ax.bar([i + width/2 for i in x], capacity, width,
                  label='课程容量', color='#2196F3')
            
            ax.set_xlabel('课程', fontsize=12)
            ax.set_ylabel('人数', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(courses, rotation=45, ha='right')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"图表已保存到: {save_path}")
            else:
                plt.show()
            
            plt.close()
            return True
        
        except Exception as e:
            print(f"绘制图表失败: {e}")
            return False
    
    @staticmethod
    def plot_student_performance(student_name, data, title=None, save_path=None):
        """绘制学生个人成绩雷达图"""
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib未安装，无法绘制图表")
            return False
        
        try:
            import numpy as np
            
            # 数据格式: [{'course_name': '课程名', 'score': 85}, ...]
            if not data:
                print("没有数据可绘制")
                return False
            
            courses = [item['course_name'] for item in data]
            scores = [item['score'] for item in data]
            
            # 计算角度
            angles = np.linspace(0, 2 * np.pi, len(courses), endpoint=False).tolist()
            scores = scores + scores[:1]  # 闭合图形
            angles = angles + angles[:1]
            
            # 创建雷达图
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            
            ax.plot(angles, scores, 'o-', linewidth=2, color='#2196F3')
            ax.fill(angles, scores, alpha=0.25, color='#2196F3')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(courses)
            ax.set_ylim(0, 100)
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.grid(True)
            
            if title is None:
                title = f'{student_name} - 各科成绩雷达图'
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"图表已保存到: {save_path}")
            else:
                plt.show()
            
            plt.close()
            return True
        
        except Exception as e:
            print(f"绘制图表失败: {e}")
            return False


if __name__ == '__main__':
    # 测试可视化功能
    if Visualizer.is_available():
        print("可视化功能可用")
        
        # 测试成绩分布图
        grade_data = [
            {'grade_level': '优秀', 'count': 15},
            {'grade_level': '良好', 'count': 25},
            {'grade_level': '中等', 'count': 20},
            {'grade_level': '及格', 'count': 10},
            {'grade_level': '不及格', 'count': 5}
        ]
        Visualizer.plot_grade_distribution(grade_data)
    else:
        print("可视化功能不可用，请安装 matplotlib")

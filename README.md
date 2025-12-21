# 本科教学管理系统

一个基于Python和Tkinter开发的完整教学管理系统，支持本地和网络两种运行模式。

## 🚀 快速开始

### 1. 安装依赖（可选）

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
# Windows
python database\init_db.py

# Linux/macOS
python database/init_db.py
```

### 3. 启动系统

**本地模式**（推荐）：
```bash
python main.py
```

**网络模式**：
```bash
# 启动服务器
python server_main.py

# 启动客户端（另一个终端）
python client_main.py
```

### 4. 默认账户

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 教师 | teacher001~005 | teacher123 |
| 学生 | 2021001001等 | student123 |

## 📖 详细文档

完整使用说明请查看 **[用户手册.md](./用户手册.md)**

## 🎯 功能清单

### 管理员功能
- ✅ 数据总览与统计
- ✅ 学生信息管理（增删改查）
- ✅ 教师信息管理
- ✅ 课程管理
- ✅ 成绩统计与可视化
- ✅ 用户管理（激活/禁用/重置密码）
- ✅ 系统日志查看
- ✅ 数据导出（CSV格式）

### 教师功能
- ✅ 个人信息查看
- ✅ 课程管理（查看任教课程）
- ✅ 成绩录入与管理
- ✅ 学生管理（查看选课学生）
- ✅ 选课学生列表

### 学生功能
- ✅ 个人信息查看
- ✅ 我的课程查看
- ✅ 选课管理（选课/退课）
- ✅ 成绩查询

## 📁 项目结构

```
teaching_system/
├── database/              # 数据库模块
│   ├── db_manager.py      # 数据库管理器
│   └── init_db.py         # 数据库初始化
├── gui/                   # 图形界面模块
│   ├── login_window.py    # 登录窗口
│   ├── admin_window.py    # 管理员界面
│   ├── teacher_window.py  # 教师界面
│   └── student_window.py  # 学生界面
├── network/               # 网络通信模块
│   ├── server.py          # 服务器
│   └── client.py          # 客户端
├── main.py                # 本地模式启动
├── server_main.py         # 服务器启动
├── client_main.py         # 客户端启动
├── requirements.txt       # 依赖列表
├── README.md              # 项目说明
└── 用户手册.md            # 详细手册
```

## 🛠️ 技术栈

- **语言**：Python 3.7+
- **GUI**：Tkinter
- **数据库**：SQLite 3
- **网络**：Socket (TCP)
- **可视化**：Matplotlib (可选)
- **数据处理**：Pandas (可选)

## 💡 核心功能说明

### 初始化数据

运行初始化脚本后，系统自动创建：
- 1个管理员账号
- 5个教师账号
- 10个学生账号
- 10门课程
- 28条选课记录
- 15条成绩记录

### 成绩计算规则

- **总评成绩** = 平时成绩 × 40% + 考试成绩 × 60%
- **等级划分**：
  - 优秀：≥90分
  - 良好：80-89分
  - 中等：70-79分
  - 及格：60-69分
  - 不及格：<60分

### 用户管理功能

管理员可以：
- 激活/禁用用户账号
- 重置密码（教师→teacher123，学生→student123）
- 查看系统日志
- 导出数据

### 教师-学生关联

- 教师只能查看选了自己课程的学生
- 教师只能为自己课程的学生录入成绩
- 学生管理界面显示学生选的该教师所有课程

## 📊 示例数据

### 教师-课程对应

| 教师 | 课程编号 | 课程名称 |
|------|----------|----------|
| teacher001 | CS101, CS102 | Python程序设计, 数据结构与算法 |
| teacher002 | CS201, CS202 | 操作系统原理, 计算机网络 |
| teacher003 | SE101, SE201 | 软件工程, 数据库系统 |
| teacher004 | DS101, DS201 | 数据分析基础, 机器学习 |
| teacher005 | AI101, AI201 | 人工智能导论, 深度学习 |

### 学生选课示例

- 学生2021001001: CS101, CS102, CS201, SE101 (4门课)
- 学生2021001002: CS101, CS102, CS202, SE201 (4门课)
- 学生2021001003: CS101, CS201, SE101 (3门课)

## 🔧 常见问题

### 无法启动

```bash
# 检查Python版本
python --version

# 查看错误信息
python main.py
```

### 数据库问题

```bash
# 重新初始化
del teaching_system.db       # Windows
rm teaching_system.db        # Linux/macOS
python database\init_db.py
```

### 网络连接问题

1. 确认服务器已启动
2. 检查IP地址和端口
3. 检查防火墙设置

## 📝 命令速查

```bash
# 初始化数据库
python database/init_db.py

# 本地模式
python main.py

# 网络模式 - 服务器
python server_main.py

# 网络模式 - 客户端
python client_main.py

# 安装依赖
pip install -r requirements.txt
```

## 🔒 安全特性

- ✅ SHA-256密码加密
- ✅ 角色权限控制
- ✅ 操作日志记录
- ✅ 管理员保护（不可删除/禁用）

## 📦 数据备份

备份数据库文件：
```bash
# 复制数据库文件
copy teaching_system.db teaching_system_backup.db    # Windows
cp teaching_system.db teaching_system_backup.db      # Linux/macOS
```

恢复数据：
```bash
# 用备份文件替换当前数据库
copy teaching_system_backup.db teaching_system.db    # Windows
cp teaching_system_backup.db teaching_system.db      # Linux/macOS
```

## 📞 技术支持

遇到问题请查看 [用户手册.md](./用户手册.md) 获取详细帮助。

## 📄 许可证

本项目仅用于教学和学习目的。

---

**版本**：v1.0  
**更新日期**：2024-11-22

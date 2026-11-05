# 企业审批系统

《BS 体系软件设计》2026 课程项目。原始要求见 [assignment(2026).pdf](assignment%282026%29.pdf)，需求分析和中期设计见 [设计文档](docs/midterm-design.md)。

当前为**初始化骨架**：含首页、数据库健康检查、用户/部门模型、迁移、基础部门与角色初始化、Docker 配置；尚未实现注册业务、采购、差旅、报销、审批、通知和附件授权。Django Admin 仅用于当前基础数据维护，不能代表最终系统管理员权限实现。

## 技术栈

Python 3.11、Django 5.2 LTS、Django Templates、原生 CSS/JavaScript；PostgreSQL 16 为部署及验收数据库，SQLite 仅用于本地快速启动；Waitress + WhiteNoise + Docker Compose。精确依赖见 `requirements.txt`。

## 本地启动（PowerShell）

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
$env:DJANGO_DEBUG = '1'
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py seed_base
.\.venv\Scripts\python manage.py createsuperuser
.\.venv\Scripts\python manage.py runserver
```

访问 http://127.0.0.1:8000/ 和 `/health/`。本地命令不会自动读取 `.env`，未设置 `DB_HOST` 时使用 SQLite。初始化不会创建默认账号或分配权限，`seed_base` 可重复执行。

## Docker 启动

先启动 Docker Desktop 的 Linux 引擎。复制 `.env.example` 为 `.env`，将密钥和数据库密码改为随机值；Compose 会加载该文件。

```powershell
Copy-Item .env.example .env
# 编辑 .env 后运行
docker compose up --build -d
docker compose exec web python manage.py createsuperuser
docker compose ps
docker compose logs web
```

Web 启动时执行迁移、幂等初始化和静态资源收集。数据库和附件使用独立命名卷；`docker compose down` 保留数据，勿对需保留的数据使用 `down -v`。当前配置绑定本机回环地址用于课程演示；公开部署另需 HTTPS、可信域名、Secure Cookie、备份与 `check --deploy` 审查。

## 验证

```powershell
$env:DJANGO_DEBUG = '1'
.\.venv\Scripts\python manage.py check
.\.venv\Scripts\python manage.py makemigrations --check --dry-run
.\.venv\Scripts\python manage.py test
```

验证结果和待验收项见 [验证记录](docs/verification.md)。版本管理使用小步提交；最终提交包含 `.git` 或可核对的 Git 日志。未配置远程仓库；按需执行 `git remote add origin <仓库地址>`，再推送。

## 人工实现边界

作业第 3 页第 6 节规定自定义审批流程模块不得使用 AI 辅助编程。该模块无生成代码，学生须独立完成。详见 [人工任务清单](docs/manual-module.md) 和 [AGENTS.md](AGENTS.md)。中期文档为设计稿，提交前由本人审阅并补齐个人信息；不得将计划功能描述为已实现。

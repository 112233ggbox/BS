# 初始化验证记录

验证日期：2026-11-05。环境：Windows、Python 3.11、Django 5.2.19；本地 SQLite。以下为实际执行结果，不代表最终业务验收。

|检查|结果|
|---|---|
|安装依赖并导出精确 requirements.txt|通过|
|生成 accounts 初始迁移、执行全部 migrate|通过|
|seed_base 连续执行两次|通过，3部门、5角色，不创建用户和授权|
|manage.py check|通过，0问题|
|makemigrations --check --dry-run|通过，无待生成变更|
|manage.py test|5项通过，约1.18秒|
|collectstatic|通过，127项静态文件|
|Django测试客户端首页、admin登录页|均HTTP 200|
|docker compose config --quiet|通过；本地.env已随机生成且被Git忽略|
|Docker引擎与容器运行|未通过环境前置检查：Docker Desktop Linux引擎未运行，未执行构建/容器启动|

测试涵盖：初始化幂等及不授予权限、邮箱大小写不敏感唯一、默认低权限与密码哈希、数据库健康检查成功及故障脱敏。首次测试时静态资源尚未收集，出现目录不存在提示，随后 collectstatic 成功。Git初始化时出现目录所有者与沙箱用户不一致，后续命令使用仅该次生效的 `-c safe.directory=D:/BS`，不修改全局信任设置。

尚未验证：PostgreSQL迁移与行锁并发、镜像构建及Linux容器启动、跨机器部署、CI远程运行、任何正式审批/附件/通知业务、移动端提分功能。GitHub Actions仅添加配置，未声称远程通过。

Docker引擎启动后按README运行Compose；需再次检查静态资源、迁移、健康检查和重启数据持久性。最终验收使用PostgreSQL，不以SQLite通过替代。

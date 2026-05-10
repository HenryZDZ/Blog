# Blog Project — 屏息之间

Flask 博客应用，部署在 PythonAnywhere，Obsidian 写作同步。

## 项目结构

| 路径 | 用途 |
|------|------|
| `app.py` | Flask 工厂 `create_app()` |
| `config.py` | 配置，支持 `DATABASE_URL` 环境变量（Turso/libsql） |
| `models.py` | Comment 模型，SQLAlchemy ORM |
| `routes.py` | 路由：首页、文章、搜索、标签、评论、关于 |
| `posts/` | Markdown 文章，含 YAML frontmatter（title, date, tags, summary） |
| `templates/` | Jinja2 模板，Bauhaus 风格 |
| `static/` | CSS/JS，Pink Floyd 匿名昵称、几何头像 |
| `blog.db` | SQLite 数据库（评论），已 gitignore |

## 发布文章

用户写道：`~/Documents/Obsidian Vault/Blog-Posts/xxx.md`

**一键发布：**

```bash
bash ~/Project/Posts/publish.sh
```

**手动发布：** 直接上传文件到 PythonAnywhere 并 reload

```
curl -F "content=@文件路径" -H "Authorization: Token <token>" \
  https://www.pythonanywhere.com/api/v0/user/HenryAQA/files/path/home/HenryAQA/Blog/posts/文件名
curl -X POST -H "Authorization: Token <token>" \
  https://www.pythonanywhere.com/api/v0/user/HenryAQA/webapps/HenryAQA.pythonanywhere.com/reload/
```

## 部署信息

- **博客 URL**: https://HenryAQA.pythonanywhere.com
- **平台**: PythonAnywhere（免费账号 HenryAQA）
- **GitHub**: https://github.com/HenryZDZ/Blog
- **API Token**: 已在 `publish.sh` 中配置

## 本地运行

```bash
uv run python run.py     # 开发模式 localhost:5000
uv run pytest tests/ -v  # 跑测试
```

## Git 代理

仓库已配置代理：`http.proxy = http://127.0.0.1:7897`（Clash Verge）

# 个人技术博客 — 设计说明

## 概述

一个后端驱动的个人技术博客网站。内容以中文技术文章为主，Markdown 文件管理文章，Flask 渲染页面。

## 技术栈

- **Web 框架：** Flask
- **数据库：** SQLite（评论、访问量）
- **模板：** Jinja2
- **Markdown 渲染：** Python-Markdown + Pygments（代码高亮）+ 自定义扩展（KaTeX 数学公式）
- **部署：** Gunicorn + Nginx

## 项目结构

```
博客/
├── app.py                # Flask 入口，创建应用
├── config.py             # 配置（数据库路径、站点名、每页文章数等）
├── models.py             # 数据表（评论、访问量）
├── routes.py             # 所有路由
├── markdown_utils.py     # Markdown 解析、代码高亮、LaTeX
├── templates/            # Jinja2 模板
│   ├── base.html         # 公共布局（导航、页脚）
│   ├── index.html        # 首页文章列表（分页）
│   ├── post.html         # 文章详情页
│   ├── tag.html          # 标签筛选页
│   ├── search.html       # 搜索结果页
│   └── 404.html          # 404 页面
├── static/
│   ├── css/style.css     # 全局样式
│   └── js/               # 前端交互（可选）
├── posts/                # Markdown 文章文件
│   └── hello-world.md
├── requirements.txt
├── Makefile              # 常用命令封装
└── run.py                # 开发启动入口
```

## 文章格式

每篇文章是 `posts/` 下一个 `.md` 文件，文件名作为 slug（如 `python-decorators.md` → `/post/python-decorators`）。

文件头使用 YAML frontmatter：

```yaml
---
title: Python 装饰器详解
date: 2026-05-09
tags: [Python, 基础]
summary: 阅读一个带 @ 参数的装饰器实现
---
```

## 功能清单

### 首页
- 按日期倒序显示文章列表
- 每页 10 篇，底部分页导航
- 每项显示：标题、日期、标签、摘要

### 文章详情
- Markdown 渲染为 HTML
- 代码块语法高亮（Pygments）
- 数学公式渲染（KaTeX，CDN 加载）
- 显示标签，点击可跳转标签筛选页
- 底部评论区

### 标签筛选
- `/tag/Python` 显示带有该标签的所有文章
- 列表格式同首页

### 搜索
- 导航栏搜索框，关键词搜索标题和标签
- 搜索结果页列出匹配文章

### 评论
- 文章底部评论区
- 提交表单：昵称（必填，2-20 字）、内容（必填，1-1000 字）
- 支持嵌套回复（两级）
- 提交内容做 HTML 转义防 XSS
- SQLite 存储，按文章 slug 关联

### RSS
- `/rss.xml` 提供 RSS 2.0 订阅

### 关于页
- `/about` 展示个人信息，内容从 `posts/about.md` 或配置读取

## 数据流

1. Flask 启动时扫描 `posts/` 目录，解析所有 `.md` 文件的 frontmatter，缓存到内存列表
2. 首页路由从缓存取文章列表，分页渲染
3. 文章请求 `/post/<slug>` → 读对应 `.md` 文件 → Markdown 渲染 → 查询评论 → 渲染模板
4. 搜索 / 标签筛选 → 在缓存列表里过滤匹配项 → 渲染

## 缓存策略

- 启动时加载所有文章元数据到内存（标题、日期、标签、摘要、slug、文件路径）
- 文章正文按需读取和渲染
- 文件修改后需重启服务刷新缓存（暂不做热重载，后续可加）

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 文章 slug 不存在 | 404 页面，列出最近 10 篇文章链接 |
| Markdown 解析失败 | 记录日志，跳过该文章，首页标记"渲染失败" |
| 搜索无结果 | 显示"未找到相关文章"，建议其他关键词 |
| posts/ 目录为空 | 首页显示"还没有文章"提示 |
| 数据库操作失败 | 捕获异常，返回友好提示 |

## 安全措施

- 评论输入 HTML 转义，防 XSS
- 昵称和内容做长度校验
- 静态文件走 Nginx，Flask 不直接暴露

## 不做

- 后台编辑器（文章直接手写 .md 文件）
- 用户登录 / 权限系统
- 邮件订阅 / 推送
- 文章热重载（后续可加）
- RSS 全文输出（只输出摘要）

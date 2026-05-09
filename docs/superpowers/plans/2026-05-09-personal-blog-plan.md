# 个人技术博客 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个基于 Flask + Markdown + SQLite 的个人技术博客，支持文章列表、详情、标签筛选、搜索、评论和关于页。

**Architecture:** Flask 应用读取 posts/ 目录下的 Markdown 文件，解析 YAML frontmatter 获取元数据，缓存到内存。请求时按需渲染 Markdown 为 HTML（含代码高亮和数学公式）。评论存储在 SQLite 中。

**Tech Stack:** Flask, Python-Markdown, Pygments, PyYAML, SQLAlchemy, Jinja2, pytest

---

### Task 1: 项目骨架搭建

**Files:**
- Create: `requirements.txt`
- Create: `config.py`
- Create: `run.py`
- Create: `posts/hello-world.md`

- [ ] **Step 1: 写 requirements.txt**

```txt
flask==3.1.0
flask-sqlalchemy==3.1.1
markdown==3.7
pygments==2.18.0
pyyaml==6.0.2
gunicorn==23.0.0
pytest==8.3.4
```

- [ ] **Step 2: 写 config.py**

```python
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SITE_NAME = os.environ.get("SITE_NAME", "技术小站")
SITE_DESCRIPTION = os.environ.get("SITE_DESCRIPTION", "写代码，记笔记")
ABOUT_TEXT = os.environ.get("ABOUT_TEXT", "一名开发者，热爱技术，喜欢分享。")
POSTS_PER_PAGE = 10
DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'blog.db')}"
POSTS_DIR = os.path.join(BASE_DIR, 'posts')
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
```

- [ ] **Step 3: 写 run.py**

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

- [ ] **Step 4: 创建示例文章**

创建 `posts/hello-world.md`：

```markdown
---
title: Hello World
date: 2026-05-09
tags: [随笔]
summary: 博客的第一篇文章
---

## 欢迎

这是我的个人技术博客，这里会记录我学习技术的过程和心得。
```

- [ ] **Step 5: 安装依赖并验证**

```bash
pip install -r requirements.txt
python -c "from config import *; print('config OK')"
```

- [ ] **Step 6: 提交**

```bash
git add requirements.txt config.py run.py posts/hello-world.md
git commit -m "feat: project skeleton with config and sample post"
```

---

### Task 2: Markdown 解析工具

**Files:**
- Create: `markdown_utils.py`
- Create: `tests/test_markdown_utils.py`

- [ ] **Step 1: 写 markdown_utils.py**

```python
import os
import re
import logging
import yaml
import markdown

logger = logging.getLogger(__name__)


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file. Returns (metadata_dict, body_text)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}, content

    fm = yaml.safe_load(match.group(1)) or {}
    body = content[match.end():]
    return fm, body


def render_markdown(text):
    """Convert markdown text to HTML with code highlighting and table support."""
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'codehilite',
        'tables',
    ], extension_configs={
        'codehilite': {
            'css_class': 'highlight',
            'guess_lang': True,
        },
    })
    return md.convert(text)


def load_posts(posts_dir):
    """Scan posts directory, parse frontmatter from all .md files, return list sorted by date desc."""
    posts = []
    if not os.path.isdir(posts_dir):
        return posts

    for filename in sorted(os.listdir(posts_dir)):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(posts_dir, filename)
        try:
            fm, _ = parse_frontmatter(filepath)
            slug = filename[:-3]
            posts.append({
                'slug': slug,
                'title': fm.get('title', slug),
                'date': str(fm.get('date', '')),
                'tags': fm.get('tags', []),
                'summary': fm.get('summary', ''),
                'filepath': filepath,
            })
        except Exception:
            logger.warning("Failed to parse %s", filename, exc_info=True)

    posts.sort(key=lambda p: p['date'], reverse=True)
    return posts


def get_post(posts, slug):
    """Find a post by slug in the cached post list."""
    for p in posts:
        if p['slug'] == slug:
            return p
    return None
```

- [ ] **Step 2: 写测试文件 tests/test_markdown_utils.py**

```python
import os
import tempfile
import pytest
from markdown_utils import parse_frontmatter, render_markdown, load_posts, get_post


class TestParseFrontmatter:
    def test_parses_valid_frontmatter(self):
        content = "---\ntitle: Test\ndate: 2026-01-01\ntags: [a, b]\n---\n\n# Body"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(content)
            path = f.name
        try:
            fm, body = parse_frontmatter(path)
            assert fm['title'] == 'Test'
            assert fm['date'] == '2026-01-01'
            assert fm['tags'] == ['a', 'b']
            assert '# Body' in body
        finally:
            os.unlink(path)

    def test_no_frontmatter_returns_empty_dict(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# Just a heading")
            path = f.name
        try:
            fm, body = parse_frontmatter(path)
            assert fm == {}
            assert '# Just a heading' in body
        finally:
            os.unlink(path)


class TestRenderMarkdown:
    def test_renders_heading(self):
        html = render_markdown('# Hello')
        assert '<h1>Hello</h1>' in html

    def test_renders_code_block(self):
        html = render_markdown('```python\nprint(1)\n```')
        assert 'highlight' in html
        assert 'print' in html


class TestLoadPosts:
    def test_loads_and_sorts_posts(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, 'b.md'), 'w', encoding='utf-8') as f:
                f.write("---\ntitle: B\ndate: 2026-01-01\ntags: []\nsummary: b\n---\nbody")
            with open(os.path.join(d, 'a.md'), 'w', encoding='utf-8') as f:
                f.write("---\ntitle: A\ndate: 2026-06-01\ntags: [x]\nsummary: a\n---\nbody")
            with open(os.path.join(d, 'not.md~'), 'w') as f:
                f.write('backup')
            posts = load_posts(d)
            assert len(posts) == 2
            assert posts[0]['title'] == 'A'  # newer first
            assert posts[1]['title'] == 'B'

    def test_empty_dir_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as d:
            assert load_posts(d) == []

    def test_nonexistent_dir_returns_empty_list(self):
        assert load_posts('/nonexistent/path') == []


class TestGetPost:
    def test_finds_post_by_slug(self):
        posts = [{'slug': 'hello', 'title': 'Hello'}, {'slug': 'world', 'title': 'World'}]
        assert get_post(posts, 'hello')['title'] == 'Hello'

    def test_returns_none_for_missing_slug(self):
        assert get_post([], 'missing') is None
```

- [ ] **Step 3: 运行测试确认失败（代码还没装依赖）**

```bash
pip install pytest pyyaml markdown pygments && python -m pytest tests/test_markdown_utils.py -v
```

Expected: 全部 PASS。

- [ ] **Step 4: 提交**

```bash
git add markdown_utils.py tests/test_markdown_utils.py
git commit -m "feat: markdown parsing and rendering utilities"
```

---

### Task 3: 数据库模型

**Files:**
- Create: `models.py`

- [ ] **Step 1: 写 models.py**

```python
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_slug = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    parent = db.relationship('Comment', remote_side=[id], backref='replies')
```

- [ ] **Step 2: 验证模型可创建**

```bash
python -c "
from flask import Flask
from models import db, Comment
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db.init_app(app)
with app.app_context():
    db.create_all()
    c = Comment(post_slug='test', author='me', content='hi')
    db.session.add(c)
    db.session.commit()
    print('model OK, comment id:', c.id)
"
```

- [ ] **Step 3: 提交**

```bash
git add models.py
git commit -m "feat: comment database model"
```

---

### Task 4: Flask 应用工厂与路由骨架

**Files:**
- Create: `app.py`
- Create: `routes.py`
- Create: `templates/base.html`
- Create: `templates/index.html`

- [ ] **Step 1: 写 app.py**

```python
from flask import Flask
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes import register_routes
    register_routes(app)

    return app
```

- [ ] **Step 2: 写 routes.py**

```python
from flask import render_template, request, redirect, url_for, abort
import markdown_utils
from models import db, Comment

_posts_cache = None


def _cache(app):
    global _posts_cache
    if _posts_cache is None:
        _posts_cache = markdown_utils.load_posts(app.config['POSTS_DIR'])
    return _posts_cache


def register_routes(app):
    @app.route('/')
    def index():
        posts = _cache(app)
        page = request.args.get('page', 1, type=int)
        per_page = app.config['POSTS_PER_PAGE']
        total_pages = max((len(posts) + per_page - 1) // per_page, 1)
        if page < 1:
            page = 1
        if page > total_pages:
            page = total_pages
        start = (page - 1) * per_page
        posts_page = posts[start:start + per_page]
        return render_template('index.html', posts=posts_page, page=page, total_pages=total_pages)
```

- [ ] **Step 3: 写 templates/base.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ config.SITE_NAME }}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/pygments.css') }}">
    {% block head %}{% endblock %}
</head>
<body>
    <nav class="nav">
        <div class="nav-inner">
            <a href="{{ url_for('index') }}" class="nav-brand">{{ config.SITE_NAME }}</a>
            <form action="{{ url_for('search') }}" method="get" class="nav-search">
                <input type="text" name="q" placeholder="搜索文章..." value="{{ request.args.get('q', '') }}">
            </form>
        </div>
    </nav>

    <main class="main">
        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        <p>&copy; {{ config.SITE_NAME }} · powered by Flask</p>
    </footer>
</body>
</html>
```

- [ ] **Step 4: 写 templates/index.html**

```html
{% extends "base.html" %}
{% block title %}{{ config.SITE_NAME }}{% endblock %}

{% block content %}
{% if not posts %}
<div class="empty-state">
    <h2>还没有文章</h2>
    <p>在 posts/ 目录下添加 .md 文件来发布文章。</p>
</div>
{% else %}
<div class="post-list">
    {% for post in posts %}
    <article class="post-card">
        <h2><a href="{{ url_for('post', slug=post.slug) }}">{{ post.title }}</a></h2>
        <div class="post-meta">
            <time>{{ post.date }}</time>
            {% if post.tags %}
            <span class="post-tags">
                {% for tag in post.tags %}
                <a href="{{ url_for('tag', tag=tag) }}" class="tag">{{ tag }}</a>
                {% endfor %}
            </span>
            {% endif %}
        </div>
        {% if post.summary %}
        <p class="post-summary">{{ post.summary }}</p>
        {% endif %}
    </article>
    {% endfor %}
</div>

{% if total_pages > 1 %}
<div class="pagination">
    {% if page > 1 %}
    <a href="{{ url_for('index', page=page-1) }}">← 上一页</a>
    {% endif %}
    <span>第 {{ page }}/{{ total_pages }} 页</span>
    {% if page < total_pages %}
    <a href="{{ url_for('index', page=page+1) }}">下一页 →</a>
    {% endif %}
</div>
{% endif %}
{% endif %}
{% endblock %}
```

- [ ] **Step 5: 验证应用可启动**

```bash
pip install flask flask-sqlalchemy && python -c "
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.get('/')
    print('status:', r.status_code)
"
```

Expected: `status: 200`

- [ ] **Step 6: 提交**

```bash
git add app.py routes.py templates/base.html templates/index.html
git commit -m "feat: flask app with home page route"
```

---

### Task 5: 文章详情页

**Files:**
- Create: `templates/post.html`
- Modify: `routes.py`

- [ ] **Step 1: 在 routes.py 中添加文章详情路由**

在 `register_routes` 函数中，`index` 路由之后添加：

```python
    @app.route('/post/<slug>')
    def post(slug):
        posts = _cache(app)
        post_data = markdown_utils.get_post(posts, slug)
        if not post_data:
            recent = posts[:10]
            return render_template('404.html', recent_posts=recent), 404

        with open(post_data['filepath'], 'r', encoding='utf-8') as f:
            content = f.read()

        _, body = markdown_utils.parse_frontmatter(post_data['filepath'])
        html_body = markdown_utils.render_markdown(body)

        comments = (Comment.query
                    .filter_by(post_slug=slug, parent_id=None)
                    .order_by(Comment.created_at.desc())
                    .all())

        return render_template('post.html', post=post_data, content=html_body, comments=comments)
```

- [ ] **Step 2: 写 templates/post.html**

```html
{% extends "base.html" %}
{% block title %}{{ post.title }} - {{ config.SITE_NAME }}{% endblock %}

{% block head %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}]})"></script>
{% endblock %}

{% block content %}
<article class="post-full">
    <header class="post-header">
        <h1>{{ post.title }}</h1>
        <div class="post-meta">
            <time>{{ post.date }}</time>
            {% if post.tags %}
            <span class="post-tags">
                {% for tag in post.tags %}
                <a href="{{ url_for('tag', tag=tag) }}" class="tag">{{ tag }}</a>
                {% endfor %}
            </span>
            {% endif %}
        </div>
    </header>

    <div class="post-body">
        {{ content | safe }}
    </div>
</article>

<section class="comments">
    <h2>评论 ({{ comments | length }})</h2>

    <form method="post" action="{{ url_for('add_comment', slug=post.slug) }}" class="comment-form">
        <input type="text" name="author" placeholder="昵称（必填，2-20字）" maxlength="20" minlength="2" required>
        <textarea name="content" placeholder="评论内容（必填，1-1000字）" maxlength="1000" minlength="1" required></textarea>
        <button type="submit">提交评论</button>
    </form>

    {% for comment in comments %}
    <div class="comment">
        <div class="comment-author">{{ comment.author }}</div>
        <div class="comment-time">{{ comment.created_at.strftime('%Y-%m-%d %H:%M') }}</div>
        <div class="comment-content">{{ comment.content }}</div>
        <button class="reply-btn" onclick="toggleReply({{ comment.id }})">回复</button>

        <form method="post" action="{{ url_for('add_comment', slug=post.slug) }}" class="comment-form reply-form" id="reply-form-{{ comment.id }}" style="display:none">
            <input type="hidden" name="parent_id" value="{{ comment.id }}">
            <input type="text" name="author" placeholder="昵称（必填，2-20字）" maxlength="20" minlength="2" required>
            <textarea name="content" placeholder="回复内容" maxlength="1000" required></textarea>
            <button type="submit">提交回复</button>
        </form>

        {% for reply in comment.replies %}
        <div class="comment comment-reply">
            <div class="comment-author">{{ reply.author }}</div>
            <div class="comment-time">{{ reply.created_at.strftime('%Y-%m-%d %H:%M') }}</div>
            <div class="comment-content">{{ reply.content }}</div>
        </div>
        {% endfor %}
    </div>
    {% endfor %}
</section>

<script>
function toggleReply(id) {
    var el = document.getElementById('reply-form-' + id);
    el.style.display = el.style.display === 'none' ? 'block' : 'none';
}
</script>
{% endblock %}
```

- [ ] **Step 3: 验证文章页可访问**

```bash
python -c "
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.get('/post/hello-world')
    print('status:', r.status_code)
    assert 'Hello World' in r.data.decode()
    print('post page OK')
"
```

- [ ] **Step 4: 提交**

```bash
git add templates/post.html routes.py
git commit -m "feat: post detail page with markdown rendering"
```

---

### Task 6: 标签筛选页

**Files:**
- Create: `templates/tag.html`
- Modify: `routes.py`

- [ ] **Step 1: 在 routes.py 中添加标签路由**

```python
    @app.route('/tag/<tag>')
    def tag(tag):
        posts = _cache(app)
        filtered = [p for p in posts if tag in p['tags']]
        return render_template('tag.html', posts=filtered, tag=tag)
```

- [ ] **Step 2: 写 templates/tag.html**

```html
{% extends "base.html" %}
{% block title %}标签: {{ tag }} - {{ config.SITE_NAME }}{% endblock %}

{% block content %}
<h2 class="page-title">标签: {{ tag }}</h2>
{% if not posts %}
<p>没有找到带有此标签的文章。</p>
{% else %}
<div class="post-list">
    {% for post in posts %}
    <article class="post-card">
        <h2><a href="{{ url_for('post', slug=post.slug) }}">{{ post.title }}</a></h2>
        <div class="post-meta">
            <time>{{ post.date }}</time>
            <span class="post-tags">
                {% for t in post.tags %}
                <a href="{{ url_for('tag', tag=t) }}" class="tag">{{ t }}</a>
                {% endfor %}
            </span>
        </div>
        {% if post.summary %}
        <p class="post-summary">{{ post.summary }}</p>
        {% endif %}
    </article>
    {% endfor %}
</div>
{% endif %}
{% endblock %}
```

- [ ] **Step 3: 验证**

```bash
python -c "
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.get('/tag/随笔')
    print('status:', r.status_code)
    html = r.data.decode()
    assert 'Hello World' in html
    print('tag page OK')
"
```

- [ ] **Step 4: 提交**

```bash
git add templates/tag.html routes.py
git commit -m "feat: tag filtering page"
```

---

### Task 7: 搜索功能

**Files:**
- Create: `templates/search.html`
- Modify: `routes.py`

- [ ] **Step 1: 在 routes.py 中添加搜索路由**

```python
    @app.route('/search')
    def search():
        q = request.args.get('q', '').strip()
        posts = _cache(app)
        if not q:
            return render_template('search.html', posts=[], query='')
        results = [p for p in posts if q.lower() in p['title'].lower() or any(q.lower() in t.lower() for t in p['tags'])]
        return render_template('search.html', posts=results, query=q)
```

- [ ] **Step 2: 写 templates/search.html**

```html
{% extends "base.html" %}
{% block title %}搜索: {{ query }} - {{ config.SITE_NAME }}{% endblock %}

{% block content %}
<h2 class="page-title">搜索: {{ query }}</h2>
{% if not posts %}
<p>未找到相关文章，试试其他关键词。</p>
{% else %}
<div class="post-list">
    {% for post in posts %}
    <article class="post-card">
        <h2><a href="{{ url_for('post', slug=post.slug) }}">{{ post.title }}</a></h2>
        <div class="post-meta">
            <time>{{ post.date }}</time>
            <span class="post-tags">
                {% for tag in post.tags %}
                <a href="{{ url_for('tag', tag=tag) }}" class="tag">{{ tag }}</a>
                {% endfor %}
            </span>
        </div>
        {% if post.summary %}
        <p class="post-summary">{{ post.summary }}</p>
        {% endif %}
    </article>
    {% endfor %}
</div>
{% endif %}
{% endblock %}
```

- [ ] **Step 3: 验证**

```bash
python -c "
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.get('/search?q=Hello')
    assert 'Hello World' in r.data.decode()
    r2 = c.get('/search?q=nothing')
    assert '未找到' in r2.data.decode()
    print('search OK')
"
```

- [ ] **Step 4: 提交**

```bash
git add templates/search.html routes.py
git commit -m "feat: article search"
```

---

### Task 8: 评论提交

**Files:**
- Modify: `routes.py`

- [ ] **Step 1: 在 routes.py 中添加评论路由**

```python
    @app.route('/post/<slug>/comment', methods=['POST'])
    def add_comment(slug):
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()
        parent_id = request.form.get('parent_id', type=int)

        if len(author) < 2 or len(author) > 20:
            abort(400)
        if len(content) < 1 or len(content) > 1000:
            abort(400)

        comment = Comment(
            post_slug=slug,
            author=author,
            content=content,
            parent_id=parent_id,
        )
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('post', slug=slug) + '#comments')
```

- [ ] **Step 2: 验证评论功能**

```bash
python -c "
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.post('/post/hello-world/comment', data={
        'author': 'test', 'content': 'great post'
    }, follow_redirects=True)
    assert 'great post' in r.data.decode()
    # test XSS protection
    c.post('/post/hello-world/comment', data={
        'author': 'tester', 'content': '<script>alert(1)</script>'
    }, follow_redirects=True)
    r2 = c.get('/post/hello-world')
    html = r2.data.decode()
    assert '&lt;script&gt;' in html
    print('comment with XSS protection OK')
"
```

- [ ] **Step 3: 提交**

```bash
git add routes.py
git commit -m "feat: comment submission with validation and XSS protection"
```

---

### Task 9: 关于页与错误处理

**Files:**
- Create: `templates/about.html`
- Create: `templates/404.html`
- Modify: `routes.py`

- [ ] **Step 1: 在 routes.py 中添加关于页和 404 处理器**

```python
    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.errorhandler(404)
    def not_found(e):
        posts = _cache(app)
        recent = posts[:10]
        return render_template('404.html', recent_posts=recent), 404
```

- [ ] **Step 2: 写 templates/about.html**

```html
{% extends "base.html" %}
{% block title %}关于 - {{ config.SITE_NAME }}{% endblock %}

{% block content %}
<article class="about">
    <h1>关于</h1>
    <div class="about-content">
        <p>{{ config.ABOUT_TEXT }}</p>
    </div>
</article>
{% endblock %}
```

- [ ] **Step 3: 写 templates/404.html**

```html
{% extends "base.html" %}
{% block title %}页面不存在 - {{ config.SITE_NAME }}{% endblock %}

{% block content %}
<div class="error-page">
    <h1>404 · 页面不存在</h1>
    <p>你找的文章可能已经被移动或删除。</p>
    {% if recent_posts %}
    <h3>最近文章</h3>
    <ul class="recent-posts">
        {% for p in recent_posts %}
        <li><a href="{{ url_for('post', slug=p.slug) }}">{{ p.title }}</a></li>
        {% endfor %}
    </ul>
    {% endif %}
</div>
{% endblock %}
```

- [ ] **Step 4: 验证 404**

```bash
python -c "
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.get('/post/nonexistent')
    assert r.status_code == 404
    html = r.data.decode()
    assert 'Hello World' in html  # recent posts link
    r2 = c.get('/about')
    assert 'ABOUT_TEXT' not in r2.data.decode()
    print('404 and about OK')
"
```

- [ ] **Step 5: 提交**

```bash
git add templates/about.html templates/404.html routes.py
git commit -m "feat: about page and 404 error handler"
```

---

### Task 10: CSS 样式

**Files:**
- Create: `static/css/style.css`
- Create: `static/css/pygments.css`

- [ ] **Step 1: 写 static/css/style.css**

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg: #fffef9;
    --text: #333;
    --text-light: #666;
    --accent: #2563eb;
    --accent-hover: #1d4ed8;
    --border: #e5e7eb;
    --code-bg: #f5f5f5;
    --max-width: 720px;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.8;
    font-size: 16px;
}

a { color: var(--accent); text-decoration: none; }
a:hover { color: var(--accent-hover); }

/* Navigation */
.nav {
    border-bottom: 1px solid var(--border);
    padding: 16px 20px;
    position: sticky;
    top: 0;
    background: var(--bg);
    z-index: 100;
}
.nav-inner {
    max-width: var(--max-width);
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}
.nav-brand {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    white-space: nowrap;
}
.nav-brand:hover { color: var(--accent); }
.nav-search input {
    padding: 6px 12px;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 0.9rem;
    width: 200px;
    font-family: inherit;
}
.nav-search input:focus { outline: none; border-color: var(--accent); }

/* Main */
.main {
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 40px 20px 60px;
}

/* Post cards */
.post-list { display: flex; flex-direction: column; gap: 32px; }
.post-card h2 { font-size: 1.4rem; margin-bottom: 4px; }
.post-card h2 a { color: var(--text); }
.post-card h2 a:hover { color: var(--accent); }
.post-meta {
    font-size: 0.875rem;
    color: var(--text-light);
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.post-summary { margin-top: 8px; color: var(--text-light); }

/* Tags */
.tag {
    display: inline-block;
    font-size: 0.8rem;
    padding: 1px 8px;
    border-radius: 4px;
    background: #eff6ff;
    color: var(--accent);
}
.tag:hover { background: var(--accent); color: #fff; }

/* Pagination */
.pagination {
    margin-top: 40px;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
}

/* Full post */
.post-full { margin-bottom: 48px; }
.post-header { margin-bottom: 24px; }
.post-header h1 { font-size: 2rem; line-height: 1.3; margin-bottom: 8px; }
.post-body { font-size: 1rem; }

.post-body h1, .post-body h2, .post-body h3 { margin-top: 1.5em; margin-bottom: 0.5em; }
.post-body h2 { font-size: 1.4rem; }
.post-body h3 { font-size: 1.15rem; }
.post-body p { margin-bottom: 1em; }
.post-body ul, .post-body ol { margin-bottom: 1em; padding-left: 1.5em; }
.post-body li { margin-bottom: 0.25em; }
.post-body blockquote {
    border-left: 3px solid var(--accent);
    padding-left: 16px;
    margin: 1em 0;
    color: var(--text-light);
}
.post-body code {
    font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace;
    font-size: 0.9em;
    background: var(--code-bg);
    padding: 2px 6px;
    border-radius: 4px;
}
.post-body pre {
    background: var(--code-bg);
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin-bottom: 1em;
    font-size: 0.85rem;
    line-height: 1.6;
}
.post-body pre code {
    background: none;
    padding: 0;
    border-radius: 0;
}
.post-body table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 1em;
}
.post-body th, .post-body td {
    border: 1px solid var(--border);
    padding: 8px 12px;
    text-align: left;
}
.post-body th { background: var(--code-bg); }
.post-body img { max-width: 100%; border-radius: 8px; }

/* Comments */
.comments { border-top: 1px solid var(--border); padding-top: 32px; }
.comments h2 { margin-bottom: 20px; }
.comment-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 24px;
}
.comment-form input, .comment-form textarea {
    padding: 10px 12px;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 0.9rem;
    font-family: inherit;
}
.comment-form textarea { min-height: 80px; resize: vertical; }
.comment-form button {
    align-self: flex-start;
    padding: 8px 20px;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 0.9rem;
    cursor: pointer;
}
.comment-form button:hover { background: var(--accent-hover); }

.comment {
    padding: 16px 0;
    border-bottom: 1px solid var(--border);
}
.comment:last-child { border-bottom: none; }
.comment-reply { margin-left: 32px; border-bottom: 1px dashed var(--border); }
.comment-author { font-weight: 600; margin-bottom: 2px; }
.comment-time { font-size: 0.8rem; color: var(--text-light); margin-bottom: 6px; }
.comment-content { line-height: 1.6; }
.reply-btn {
    background: none;
    border: none;
    color: var(--text-light);
    font-size: 0.8rem;
    cursor: pointer;
    margin-top: 4px;
    padding: 0;
}
.reply-btn:hover { color: var(--accent); }
.reply-form { margin-top: 12px; }

/* Empty state */
.empty-state { text-align: center; padding: 60px 0; color: var(--text-light); }
.empty-state h2 { margin-bottom: 8px; }

/* Error page */
.error-page { text-align: center; padding: 60px 0; }
.error-page h1 { margin-bottom: 12px; }
.recent-posts { list-style: none; margin-top: 16px; }
.recent-posts li { margin-bottom: 4px; }

/* About */
.about h1 { margin-bottom: 16px; }
.about-content { line-height: 1.8; }

/* Page title */
.page-title { margin-bottom: 24px; }

/* Footer */
.footer {
    text-align: center;
    padding: 24px 20px;
    border-top: 1px solid var(--border);
    color: var(--text-light);
    font-size: 0.85rem;
}
```

- [ ] **Step 2: 生成 Pygments CSS**

```bash
python -c "
from pygments.formatters import HtmlFormatter
css = HtmlFormatter(style='github-dark').get_style_defs('.highlight')
with open('static/css/pygments.css', 'w') as f:
    f.write(css)
print('pygments.css generated')
"
```

- [ ] **Step 3: 提交**

```bash
git add static/css/style.css static/css/pygments.css
git commit -m "feat: stylesheet and code highlighting theme"
```

---

### Task 11: 部署配置

**Files:**
- Create: `Makefile`

- [ ] **Step 1: 写 Makefile**

```makefile
.PHONY: run test clean deploy

run:
	python run.py

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -f blog.db

deploy:
	gunicorn app:create_app\(\) -w 2 -b 127.0.0.1:8000
```

- [ ] **Step 2: 运行测试**

```bash
python -m pytest tests/ -v
```

Expected: 全部 PASS。

- [ ] **Step 3: 提交**

```bash
git add Makefile
git commit -m "feat: makefile for run, test, and deploy"
```

---

### Task 12: 端到端验证

- [ ] **Step 1: 启动应用并手动验证所有页面**

```bash
python run.py
```

然后在浏览器中验证：
1. 首页 `http://localhost:5000/` — 显示文章列表
2. 文章页 `http://localhost:5000/post/hello-world` — 显示渲染后的文章
3. 标签页 `http://localhost:5000/tag/随笔`
4. 搜索 `http://localhost:5000/search?q=Hello`
5. 关于页 `http://localhost:5000/about`
6. 404 页 `http://localhost:5000/post/nonexistent`
7. 评论提交
8. 嵌套评论回复

- [ ] **Step 2: 运行测试套件确认全部通过**

```bash
python -m pytest tests/ -v
```

# Bauhaus Blog Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace all frontend CSS and templates with a Bauhaus modernism design featuring geometric elements, dual light/dark mode, and anonymous Pink Floyd-themed comments.

**Architecture:** Single-column 720px reading flow. CSS custom properties drive light/dark mode switching via a `.dark` class on `<html>`. All JS is self-contained in one small file handling dark mode toggle, anonymous identity persistence, and geometric element rendering. No external CSS framework or font loading.

**Tech Stack:** Flask (Jinja2 templates), vanilla CSS, vanilla JS, SQLAlchemy (unchanged backend)

---

### Task 1: Update site config

**Files:**
- Modify: `config.py:5-7`

- [ ] **Step 1: Update SITE_NAME, SITE_DESCRIPTION, and ABOUT_TEXT**

```python
SITE_NAME = os.environ.get("SITE_NAME", "屏息之间")
SITE_DESCRIPTION = os.environ.get("SITE_DESCRIPTION", "Breathe, breathe in the air")
ABOUT_TEXT = os.environ.get("ABOUT_TEXT", "写代码，记笔记。")
```

- [ ] **Step 2: Restart Flask and verify**

Navigate to http://localhost:5000, confirm the browser tab shows "屏息之间".

- [ ] **Step 3: Commit**

```bash
git add config.py
git commit -m "feat: update site name to 屏息之间 with PF-inspired subtitle
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 2: Rewrite CSS with Bauhaus design system

**Files:**
- Modify: `static/css/style.css`

- [ ] **Step 1: Replace style.css with the complete Bauhaus design system**

Write `static/css/style.css`:

```css
/* === Reset === */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* === Light mode tokens === */
:root {
    --paper: #f8f6f0;
    --ink: #1a1a2e;
    --red: #e63946;
    --blue: #2563eb;
    --yellow: #f4d03f;
    --green: #10b981;
    --border: #e5e5e5;
    --muted: #555;
    --surface: #fff;
    --code-bg: #e8e8e8;
    --max-width: 720px;
    --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif;
    --mono: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace;
}

/* === Dark mode tokens === */
html.dark {
    --paper: #1a1a2e;
    --ink: #f0ebe3;
    --red: #ff6b6b;
    --blue: #60a5fa;
    --yellow: #facc15;
    --green: #34d399;
    --border: #3a3a5c;
    --muted: #94a3b8;
    --surface: #2d2d44;
    --code-bg: #252540;
}

body {
    font-family: var(--font);
    background: var(--paper);
    color: var(--ink);
    line-height: 1.8;
    font-size: 16px;
}

a { color: var(--blue); text-decoration: none; border-bottom: 2px solid transparent; }
a:hover { border-bottom-color: var(--blue); }

/* === Navigation === */
.nav {
    border-bottom: 2px solid var(--ink);
    padding: 16px 28px;
    background: var(--paper);
}
.nav-inner {
    max-width: var(--max-width);
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.nav-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    color: var(--ink);
    border-bottom: none;
}
.nav-logo:hover { border-bottom: none; }
.nav-logo .geo { display: flex; align-items: center; gap: 5px; }
.nav-logo .geo > * { width: 14px; height: 14px; display: flex; align-items: center; justify-content: center; }
.geo-circle { width: 12px; height: 12px; background: var(--red); border-radius: 50%; }
.geo-square { width: 12px; height: 12px; background: var(--blue); }
.geo-triangle { width: 0; height: 0; border-left: 7px solid transparent; border-right: 7px solid transparent; border-bottom: 13px solid var(--yellow); }
.geo-cross { position: relative; width: 12px; height: 12px; }
.geo-cross::before, .geo-cross::after {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 13px; height: 2px;
    background: var(--ink);
}
.geo-cross::before { transform: translate(-50%, -50%) rotate(45deg); }
.geo-cross::after { transform: translate(-50%, -50%) rotate(-45deg); }
.nav-brand { font-weight: 900; font-size: 18px; letter-spacing: -0.5px; }
.theme-toggle {
    width: 32px; height: 32px;
    border: 2px solid var(--ink);
    background: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: var(--ink);
}

/* === Main layout === */
.main { max-width: var(--max-width); margin: 0 auto; padding: 40px 28px 60px; }

/* === Intro line === */
.intro { padding: 0 0 28px; font-size: 14px; color: var(--muted); }

/* === Post cards === */
.post-list { display: flex; flex-direction: column; gap: 18px; }
.post-card {
    border-left: 4px solid var(--red);
    padding: 16px 20px;
    background: var(--surface);
}
.post-card:nth-child(5n+1) { border-left-color: var(--red); }
.post-card:nth-child(5n+2) { border-left-color: var(--blue); }
.post-card:nth-child(5n+3) { border-left-color: var(--yellow); }
.post-card:nth-child(5n+4) { border-left-color: var(--ink); }
.post-card:nth-child(5n+5) { border-left-color: var(--green); }
.post-card h2 { font-size: 18px; font-weight: 800; line-height: 1.3; margin: 4px 0; }
.post-card h2 a { color: var(--ink); border-bottom: none; }
.post-card h2 a:hover { color: var(--blue); border-bottom: none; }
.post-meta {
    font-size: 12px;
    color: var(--muted);
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.post-summary { margin-top: 4px; font-size: 14px; color: var(--muted); line-height: 1.6; }

/* === Tags: solid fill, 5-color cycle === */
.tag {
    display: inline-block;
    padding: 2px 8px;
    font-size: 10px;
    font-weight: 700;
    color: #fff;
    background: var(--ink);
    text-decoration: none;
    border-bottom: none;
}
.tag:hover { opacity: 0.85; border-bottom: none; }
.tag:nth-of-type(5n+1) { background: var(--red); }
.tag:nth-of-type(5n+2) { background: var(--blue); }
.tag:nth-of-type(5n+3) { background: var(--yellow); color: var(--ink); }
.tag:nth-of-type(5n+4) { background: var(--ink); }
.tag:nth-of-type(5n+5) { background: var(--green); }

/* === Pagination === */
.pagination {
    margin-top: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
}
.page-btn {
    width: 32px; height: 32px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700;
    color: var(--ink);
    text-decoration: none;
    border: 2px solid var(--ink);
    border-bottom: 2px solid var(--ink);
}
.page-btn:hover { background: var(--ink); color: var(--paper); border-bottom: 2px solid var(--ink); }
.page-btn.active { background: var(--ink); color: var(--paper); }
.page-btn.disabled { border-color: #ccc; color: #ccc; cursor: default; pointer-events: none; }
.pagination .geo-dot { width: 6px; height: 6px; flex-shrink: 0; }
.pagination .geo-dot.circle { background: var(--red); border-radius: 50%; }
.pagination .geo-dot.square { background: var(--blue); }

/* === Full post === */
.post-full { margin-bottom: 48px; }
.post-header { margin-bottom: 28px; }
.post-header h1 { font-size: 28px; font-weight: 900; line-height: 1.25; letter-spacing: -0.5px; margin-bottom: 10px; }
.post-header .post-meta { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.post-header .meta-dot { width: 4px; height: 4px; background: var(--red); border-radius: 50%; display: inline-block; }

.post-body { font-size: 16px; line-height: 1.85; }
.post-body h2 { font-size: 20px; font-weight: 800; margin: 1.8em 0 0.5em; }
.post-body h3 { font-size: 16px; font-weight: 700; margin: 1.5em 0 0.5em; }
.post-body p { margin-bottom: 1em; }
.post-body ul, .post-body ol { margin-bottom: 1em; padding-left: 1.2em; }
.post-body li { margin-bottom: 0.3em; }
.post-body blockquote {
    border-left: 4px solid var(--blue);
    padding: 10px 16px;
    margin: 1.2em 0;
    background: var(--surface);
    color: var(--muted);
}
.post-body code {
    font-family: var(--mono);
    font-size: 0.9em;
    background: var(--code-bg);
    padding: 2px 6px;
}
.post-body pre {
    background: #1a1a2e;
    padding: 18px;
    margin-bottom: 1em;
    overflow-x: auto;
    font-size: 13px;
    line-height: 1.6;
}
.post-body pre code {
    background: none;
    padding: 0;
    font-size: inherit;
    color: #e0e0e0;
}
.post-body table { border-collapse: collapse; width: 100%; margin-bottom: 1em; }
.post-body th, .post-body td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
.post-body th { background: var(--code-bg); }
.post-body img { max-width: 100%; }

/* === Tags at article bottom === */
.post-tags { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 24px; }

/* === Comments === */
.comments { border-top: 2px solid var(--ink); padding-top: 28px; margin-top: 32px; }
.comments h3 { font-size: 16px; font-weight: 800; margin-bottom: 16px; }
.comment-form {
    display: flex; flex-direction: column; gap: 8px;
    margin-bottom: 20px;
}
.comment-form textarea {
    width: 100%;
    padding: 10px 12px;
    border: 2px solid var(--ink);
    font-size: 14px;
    font-family: inherit;
    resize: vertical;
    background: var(--surface);
    color: var(--ink);
}
.comment-form textarea:focus { outline: none; }
.comment-form button {
    align-self: flex-start;
    padding: 8px 18px;
    background: var(--ink);
    color: var(--paper);
    border: none;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
}
.comment-form button:hover { opacity: 0.9; }

.comment { margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-start; }
.comment-avatar {
    width: 32px; height: 32px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.comment-avatar.circle-avatar > div { width: 18px; height: 18px; border-radius: 50%; }
.comment-avatar.square-avatar > div { width: 18px; height: 18px; }
.comment-avatar.triangle-avatar > div { width: 0; height: 0; border-left: 9px solid transparent; border-right: 9px solid transparent; border-bottom: 18px solid; }
.comment-avatar.cross-avatar { position: relative; }
.comment-avatar.cross-avatar::before, .comment-avatar.cross-avatar::after {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 15px; height: 2px;
}
.comment-avatar.cross-avatar::before { transform: translate(-50%, -50%) rotate(45deg); }
.comment-avatar.cross-avatar::after { transform: translate(-50%, -50%) rotate(-45deg); }
.comment-body { flex: 1; }
.comment-author { font-weight: 700; font-size: 13px; }
.comment-time { font-size: 11px; color: var(--muted); margin-bottom: 4px; }
.comment-content { font-size: 14px; line-height: 1.6; }

.reply-btn {
    background: none; border: none;
    color: var(--muted); font-size: 12px;
    cursor: pointer; padding: 0; margin-top: 4px;
}
.reply-btn:hover { color: var(--blue); }

.comment-reply {
    margin-left: 24px;
    padding-left: 12px;
    border-left: 2px solid var(--blue);
}

.reply-form { margin-top: 12px; display: none; }

/* === Empty state === */
.empty-state { text-align: center; padding: 60px 0; color: var(--muted); }
.empty-state h2 { margin-bottom: 8px; color: var(--ink); }

/* === Error page === */
.error-page { text-align: center; padding: 60px 0; }
.error-page h1 { margin-bottom: 12px; }
.recent-posts { list-style: none; margin-top: 16px; }
.recent-posts li { margin-bottom: 4px; }

/* === About === */
.about h1 { margin-bottom: 16px; }
.about-content { line-height: 1.8; }

/* === Page title === */
.page-title { margin-bottom: 24px; font-size: 20px; font-weight: 800; }

/* === Footer === */
.footer {
    border-top: 2px solid var(--ink);
    padding: 18px 28px;
    text-align: center;
}
.footer .geo { display: flex; align-items: center; justify-content: center; gap: 6px; }
.footer .geo-circle { width: 8px; height: 8px; background: var(--red); border-radius: 50%; }
.footer .geo-square { width: 8px; height: 8px; background: var(--blue); }
.footer .geo-triangle { width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 9px solid var(--yellow); }
.footer .geo-cross { position: relative; width: 9px; height: 9px; }
.footer .geo-cross::before, .footer .geo-cross::after {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 9px; height: 1.8px;
    background: var(--ink);
}
.footer .geo-cross::before { transform: translate(-50%, -50%) rotate(45deg); }
.footer .geo-cross::after { transform: translate(-50%, -50%) rotate(-45deg); }
```

- [ ] **Step 2: Commit**

```bash
git add static/css/style.css
git commit -m "feat: rewrite CSS with Bauhaus design system and dual light/dark mode
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 3: Update syntax highlighting theme

**Files:**
- Modify: `static/css/pygments.css`

- [ ] **Step 1: Replace pygments.css with a Bauhaus-coordinated dark theme**

Write `static/css/pygments.css`:

```css
/* Dark code block syntax highlighting coordinated with Bauhaus palette */
/* Light mode: code blocks use dark background, so highlight colors are fixed */
pre { background: #1a1a2e; }
.highlight .hll { background-color: #2d2d44; }
.highlight .c { color: #888; font-style: italic; }
.highlight .cm { color: #888; font-style: italic; }
.highlight .cp { color: #888; font-style: italic; }
.highlight .c1 { color: #888; font-style: italic; }
.highlight .cs { color: #888; font-style: italic; }
.highlight .k { color: #ff6b6b; font-weight: bold; }
.highlight .kc { color: #ff6b6b; font-weight: bold; }
.highlight .kd { color: #ff6b6b; font-weight: bold; }
.highlight .kn { color: #ff6b6b; font-weight: bold; }
.highlight .kp { color: #ff6b6b; }
.highlight .kr { color: #ff6b6b; font-weight: bold; }
.highlight .kt { color: #ff6b6b; font-weight: bold; }
.highlight .n { color: #e0e0e0; }
.highlight .na { color: #e0e0e0; }
.highlight .nb { color: #60a5fa; }
.highlight .nc { color: #60a5fa; font-weight: bold; }
.highlight .no { color: #facc15; }
.highlight .nd { color: #60a5fa; }
.highlight .ni { color: #e0e0e0; }
.highlight .ne { color: #ff6b6b; font-weight: bold; }
.highlight .nf { color: #60a5fa; }
.highlight .nl { color: #e0e0e0; }
.highlight .nn { color: #e0e0e0; }
.highlight .nt { color: #ff6b6b; font-weight: bold; }
.highlight .nv { color: #e0e0e0; }
.highlight .o { color: #facc15; }
.highlight .ow { color: #facc15; font-weight: bold; }
.highlight .p { color: #e0e0e0; }
.highlight .s { color: #a5d6a5; }
.highlight .sa { color: #a5d6a5; }
.highlight .sb { color: #a5d6a5; }
.highlight .sc { color: #a5d6a5; }
.highlight .dl { color: #a5d6a5; }
.highlight .sd { color: #a5d6a5; }
.highlight .s2 { color: #a5d6a5; }
.highlight .se { color: #a5d6a5; }
.highlight .sh { color: #a5d6a5; }
.highlight .si { color: #a5d6a5; }
.highlight .sx { color: #a5d6a5; }
.highlight .sr { color: #a5d6a5; }
.highlight .s1 { color: #a5d6a5; }
.highlight .ss { color: #a5d6a5; }
.highlight .m { color: #facc15; }
.highlight .mb { color: #facc15; }
.highlight .mf { color: #facc15; }
.highlight .mh { color: #facc15; }
.highlight .mi { color: #facc15; }
.highlight .mo { color: #facc15; }
.highlight .il { color: #facc15; }
.highlight .gd { color: #ff6b6b; }
.highlight .gi { color: #34d399; }
```

- [ ] **Step 2: Commit**

```bash
git add static/css/pygments.css
git commit -m "feat: update code highlighting theme to Bauhaus primary color palette
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 4: Create JavaScript module for dark mode and anonymous identity

**Files:**
- Create: `static/js/app.js`

- [ ] **Step 1: Write app.js**

```javascript
(function () {
    /* === Dark mode toggle === */
    const html = document.documentElement;
    const saved = localStorage.getItem('theme');
    if (saved === 'dark') html.classList.add('dark');
    if (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches) html.classList.add('dark');

    function toggleTheme() {
        html.classList.toggle('dark');
        localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
    }

    document.addEventListener('DOMContentLoaded', function () {
        var btn = document.getElementById('theme-toggle');
        if (btn) btn.addEventListener('click', toggleTheme);
    });

    /* === Anonymous identity === */
    var NICKNAMES = [
        'Echoes', 'Time', 'Money', 'Shine On', 'Comfortably Numb',
        'Wish You Were Here', 'Brain Damage', 'Breathe', 'Us and Them',
        'Hey You', 'Dogs', 'Sheep', 'Pigs', 'One Slip',
        'Marooned', 'Astronomy Domine', 'Lucifer Sam', 'See-Saw',
        'Julia Dream', 'Remember a Day'
    ];

    var AVATAR_TYPES = ['circle', 'square', 'triangle', 'cross'];
    var AVATAR_COLORS = ['#e63946', '#2563eb', '#f4d03f', '#1a1a2e', '#10b981'];

    function rand(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

    function getIdentity() {
        try {
            var stored = localStorage.getItem('anon-identity');
            if (stored) return JSON.parse(stored);
        } catch (_) {}
        var identity = {
            name: rand(NICKNAMES),
            avatar: rand(AVATAR_TYPES),
            color: rand(AVATAR_COLORS)
        };
        localStorage.setItem('anon-identity', JSON.stringify(identity));
        return identity;
    }

    /* Wire up comment forms: inject hidden author field */
    document.addEventListener('DOMContentLoaded', function () {
        var identity = getIdentity();
        var forms = document.querySelectorAll('.comment-form');
        for (var i = 0; i < forms.length; i++) {
            var hidden = document.createElement('input');
            hidden.type = 'hidden';
            hidden.name = 'author';
            hidden.value = identity.name;
            forms[i].appendChild(hidden);
        }
    });

    /* Expose for template use */
    window.getAnonIdentity = getIdentity;
})();
```

- [ ] **Step 2: Commit**

```bash
mkdir -p static/js
git add static/js/app.js
git commit -m "feat: add dark mode toggle and anonymous identity JS module
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 5: Rewrite base template

**Files:**
- Modify: `templates/base.html`

- [ ] **Step 1: Replace base.html with Bauhaus nav and footer**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ config.SITE_NAME }}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/pygments.css') }}">
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    {% block head %}{% endblock %}
</head>
<body>
    <nav class="nav">
        <div class="nav-inner">
            <a href="{{ url_for('index') }}" class="nav-logo">
                <span class="geo">
                    <span class="geo-circle"></span>
                    <span class="geo-square"></span>
                    <span class="geo-triangle"></span>
                    <span class="geo-cross"></span>
                </span>
                <span class="nav-brand">{{ config.SITE_NAME }}</span>
            </a>
            <button id="theme-toggle" class="theme-toggle" title="切换亮色/暗色模式">&#9728;</button>
        </div>
    </nav>

    <main class="main">
        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        <div class="geo">
            <div class="geo-circle"></div>
            <div class="geo-square"></div>
            <div class="geo-triangle"></div>
            <div class="geo-cross"></div>
        </div>
    </footer>
</body>
</html>
```

- [ ] **Step 2: Restart Flask and verify nav/footer appear correctly on any page**

- [ ] **Step 3: Commit**

```bash
git add templates/base.html
git commit -m "feat: rewrite base template with Bauhaus nav logo and geometric footer
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 6: Rewrite index template

**Files:**
- Modify: `templates/index.html`

- [ ] **Step 1: Replace index.html**

```html
{% extends "base.html" %}
{% block title %}{{ config.SITE_NAME }}{% endblock %}

{% block content %}
<p class="intro">{{ config.SITE_DESCRIPTION }}</p>

{% if not posts %}
<div class="empty-state">
    <h2>还没有文章</h2>
    <p>在 posts/ 目录下添加 .md 文件来发布文章。</p>
</div>
{% else %}
<div class="post-list">
    {% for post in posts %}
    <article class="post-card">
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
        <h2><a href="{{ url_for('post', slug=post.slug) }}">{{ post.title }}</a></h2>
        {% if post.summary %}
        <p class="post-summary">{{ post.summary }}</p>
        {% endif %}
    </article>
    {% endfor %}
</div>

{% if total_pages > 1 %}
<div class="pagination">
    {% if page > 1 %}
    <a href="{{ url_for('index', page=page-1) }}" class="page-btn">←</a>
    {% else %}
    <span class="page-btn disabled">←</span>
    {% endif %}

    {% for p in range(1, total_pages + 1) %}
    {% if p == page %}
    <span class="page-btn active">{{ p }}</span>
    {% else %}
    <a href="{{ url_for('index', page=p) }}" class="page-btn">{{ p }}</a>
    {% endif %}
    {% if p < total_pages %}
    {% if p % 2 == 1 %}
    <span class="geo-dot circle"></span>
    {% else %}
    <span class="geo-dot square"></span>
    {% endif %}
    {% endif %}
    {% endfor %}

    {% if page < total_pages %}
    <a href="{{ url_for('index', page=page+1) }}" class="page-btn">→</a>
    {% else %}
    <span class="page-btn disabled">→</span>
    {% endif %}
</div>
{% endif %}
{% endif %}
{% endblock %}
```

- [ ] **Step 2: Commit**

```bash
git add templates/index.html
git commit -m "feat: rewrite index with Bauhaus post cards, color-cycling borders, geometric pagination
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 7: Rewrite post template with anonymous comments

**Files:**
- Modify: `templates/post.html`

- [ ] **Step 1: Replace post.html**

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
            <span class="meta-dot"></span>
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

    {% if post.tags %}
    <div class="post-tags">
        {% for tag in post.tags %}
        <a href="{{ url_for('tag', tag=tag) }}" class="tag">{{ tag }}</a>
        {% endfor %}
    </div>
    {% endif %}
</article>

<section class="comments" id="comments">
    <h3>评论 ({{ comments | length }})</h3>

    <form method="post" action="{{ url_for('add_comment', slug=post.slug) }}" class="comment-form">
        <textarea name="content" placeholder="说点什么..." maxlength="1000" required></textarea>
        <button type="submit">提交评论</button>
    </form>

    {% for comment in comments %}
    <div class="comment">
        <div class="comment-avatar" id="avatar-{{ comment.id }}"></div>
        <div class="comment-body">
            <div class="comment-author">{{ comment.author }}</div>
            <div class="comment-time">{{ comment.created_at.strftime('%Y-%m-%d %H:%M') }}</div>
            <div class="comment-content">{{ comment.content }}</div>
            <button class="reply-btn" onclick="toggleReply({{ comment.id }})">回复</button>

            <form method="post" action="{{ url_for('add_comment', slug=post.slug) }}" class="comment-form reply-form" id="reply-form-{{ comment.id }}">
                <input type="hidden" name="parent_id" value="{{ comment.id }}">
                <textarea name="content" placeholder="回复内容" maxlength="1000" required></textarea>
                <button type="submit">提交回复</button>
            </form>

            {% for reply in comment.replies %}
            <div class="comment comment-reply">
                <div class="comment-avatar" id="avatar-{{ reply.id }}"></div>
                <div class="comment-body">
                    <div class="comment-author">{{ reply.author }}</div>
                    <div class="comment-time">{{ reply.created_at.strftime('%Y-%m-%d %H:%M') }}</div>
                    <div class="comment-content">{{ reply.content }}</div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endfor %}
</section>

<script>
function toggleReply(id) {
    var el = document.getElementById('reply-form-' + id);
    el.style.display = el.style.display === 'block' ? 'none' : 'block';
}
</script>
{% endblock %}
```

- [ ] **Step 2: Commit**

```bash
git add templates/post.html
git commit -m "feat: rewrite post template with Bauhaus article layout and anonymous comment form
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 8: Update tag, search, about, and 404 templates

**Files:**
- Modify: `templates/tag.html`
- Modify: `templates/search.html`
- Modify: `templates/about.html`
- Modify: `templates/404.html`

- [ ] **Step 1: Update tag.html**

```html
{% extends "base.html" %}
{% block title %}标签: {{ tag }} - {{ config.SITE_NAME }}{% endblock %}

{% block content %}
<h2 class="page-title">标签: {{ tag }}</h2>
{% if not posts %}
<div class="empty-state"><p>没有找到带有此标签的文章。</p></div>
{% else %}
<div class="post-list">
    {% for post in posts %}
    <article class="post-card">
        <div class="post-meta">
            <time>{{ post.date }}</time>
            <span class="post-tags">
                {% for t in post.tags %}
                <a href="{{ url_for('tag', tag=t) }}" class="tag">{{ t }}</a>
                {% endfor %}
            </span>
        </div>
        <h2><a href="{{ url_for('post', slug=post.slug) }}">{{ post.title }}</a></h2>
        {% if post.summary %}
        <p class="post-summary">{{ post.summary }}</p>
        {% endif %}
    </article>
    {% endfor %}
</div>
{% endif %}
{% endblock %}
```

- [ ] **Step 2: Update search.html**

```html
{% extends "base.html" %}
{% block title %}搜索: {{ query }} - {{ config.SITE_NAME }}{% endblock %}

{% block content %}
<h2 class="page-title">搜索: {{ query }}</h2>
{% if not posts %}
<div class="empty-state"><p>未找到相关文章，试试其他关键词。</p></div>
{% else %}
<div class="post-list">
    {% for post in posts %}
    <article class="post-card">
        <div class="post-meta">
            <time>{{ post.date }}</time>
            <span class="post-tags">
                {% for tag in post.tags %}
                <a href="{{ url_for('tag', tag=tag) }}" class="tag">{{ tag }}</a>
                {% endfor %}
            </span>
        </div>
        <h2><a href="{{ url_for('post', slug=post.slug) }}">{{ post.title }}</a></h2>
        {% if post.summary %}
        <p class="post-summary">{{ post.summary }}</p>
        {% endif %}
    </article>
    {% endfor %}
</div>
{% endif %}
{% endblock %}
```

- [ ] **Step 3: Update about.html**

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

- [ ] **Step 4: Update 404.html**

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

- [ ] **Step 5: Commit all**

```bash
git add templates/tag.html templates/search.html templates/about.html templates/404.html
git commit -m "feat: update tag, search, about, and 404 templates for Bauhaus style
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 9: Update routes for anonymous comments

**Files:**
- Modify: `routes.py:67-74`

- [ ] **Step 1: Allow author to be empty (auto-filled by JS hidden field)**

Replace the comment route validation:

```python
@app.route('/post/<slug>/comment', methods=['POST'])
def add_comment(slug):
    author = request.form.get('author', '').strip()
    content = request.form.get('content', '').strip()
    parent_id = request.form.get('parent_id', type=int)

    if not author:
        author = '屏息者'
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

- [ ] **Step 2: Commit**

```bash
git add routes.py
git commit -m "feat: support anonymous comments with auto-generated author name
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 10: Verification — end-to-end test

- [ ] **Step 1: Start the Flask server**

```bash
cd /Users/zhanghengrui/Project/Posts && python run.py &
```

Wait for the server to start.

- [ ] **Step 2: Verify homepage**

Open http://localhost:5000 and check:
- Nav bar shows four geometric shapes + "屏息之间" on the left, dark toggle on the right
- Intro line shows "Breathe, breathe in the air"
- Post cards have left colored borders and colored tags
- Footer shows four geometric shapes, no text

- [ ] **Step 3: Verify dark mode**

Click the dark mode toggle. Confirm:
- Background changes from paper to ink
- Text changes to light
- Colors remain distinguishable
- Refresh the page: preference persists

- [ ] **Step 4: Verify post page**

Open a post and check:
- Article title and body render correctly
- Code blocks have dark background with colored syntax
- Tags at bottom are solid-colored
- Comment form has only a textarea (no name field)
- Submit a comment, verify it appears with a Pink Floyd song name

- [ ] **Step 5: Verify other pages**

- Navigate to /search?q=test — check layout
- Navigate to /tag/rust — check layout
- Navigate to /about — check layout
- Navigate to /post/nonexistent — check 404 page

- [ ] **Step 6: Run existing tests**

```bash
cd /Users/zhanghengrui/Project/Posts && python -m pytest tests/ -v
```

Ensure all existing tests pass.

- [ ] **Step 7: Kill the server**

```bash
pkill -f "python run.py"
```

- [ ] **Step 8: Final commit if any fixes were made**

```bash
git status
# If changes: git add ... && git commit -m "fix: verification fixes"
```

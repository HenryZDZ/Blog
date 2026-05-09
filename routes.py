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

    @app.route('/search')
    def search():
        q = request.args.get('q', '').strip()
        posts = _cache(app)
        if not q:
            return render_template('search.html', posts=[], query='')
        results = [p for p in posts if q.lower() in p['title'].lower() or any(q.lower() in t.lower() for t in p['tags'])]
        return render_template('search.html', posts=results, query=q)

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

    @app.route('/tag/<tag>')
    def tag(tag):
        posts = _cache(app)
        filtered = [p for p in posts if tag in p['tags']]
        return render_template('tag.html', posts=filtered, tag=tag)

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

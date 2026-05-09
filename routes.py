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
        return redirect(url_for('index'))

    @app.route('/post/<slug>')
    def post(slug):
        return redirect(url_for('index'))

    @app.route('/tag/<tag>')
    def tag(tag):
        return redirect(url_for('index'))

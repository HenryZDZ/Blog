import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SITE_NAME = os.environ.get("SITE_NAME", "技术小站")
SITE_DESCRIPTION = os.environ.get("SITE_DESCRIPTION", "写代码，记笔记")
ABOUT_TEXT = os.environ.get("ABOUT_TEXT", "一名开发者，热爱技术，喜欢分享。")
POSTS_PER_PAGE = 10
DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'blog.db')}"
POSTS_DIR = os.path.join(BASE_DIR, 'posts')
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

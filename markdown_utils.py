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
    # Convert any date objects to strings (PyYAML auto-parses YAML dates)
    for key, value in fm.items():
        if hasattr(value, 'isoformat'):
            fm[key] = value.isoformat()
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

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

#!/usr/bin/env python3
"""Sync posts from Obsidian to blog repo, matching by frontmatter title.

Usage:
    python3 sync_posts.py <obsidian_dir> <repo_posts_dir>
    python3 sync_posts.py <obsidian_dir> <repo_posts_dir> --dry-run

Output: JSON on stdout with keys "added", "updated", "removed", "renamed".
"""

import hashlib
import json
import os
import sys
import yaml


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file. Returns (frontmatter_dict, body)."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}, content

    return fm, parts[2].strip()


def content_hash(filepath):
    """SHA256 of the file body (everything after frontmatter)."""
    _, body = parse_frontmatter(filepath)
    return hashlib.sha256(body.encode()).hexdigest()


def scan_posts(directory):
    """Scan a directory for .md files with frontmatter titles.

    Returns list of {"title": str, "filename": str, "filepath": str, "hash": str}.
    """
    posts = []
    try:
        files = [f for f in os.listdir(directory) if f.endswith(".md")]
    except FileNotFoundError:
        print(f"目录不存在: {directory}", file=sys.stderr)
        sys.exit(1)

    for filename in files:
        filepath = os.path.join(directory, filename)
        fm, _ = parse_frontmatter(filepath)
        title = fm.get("title", "").strip()

        if not title:
            print(f"  警告: {filename} 缺少 title，跳过", file=sys.stderr)
            continue

        posts.append({
            "title": title,
            "filename": filename,
            "filepath": filepath,
            "hash": content_hash(filepath),
        })

    return posts


def index_by_title(posts):
    """Index posts by title. Returns {title: [entries]}, preserving all entries for
    duplicate detection."""
    index = {}
    for p in posts:
        index.setdefault(p["title"], []).append(p)
    return index


def main():
    dry_run = "--dry-run" in sys.argv

    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    obsidian_dir = sys.argv[1]
    repo_dir = sys.argv[2]

    obsidian_posts = scan_posts(obsidian_dir)
    repo_posts = scan_posts(repo_dir)

    obsidian_index = index_by_title(obsidian_posts)
    repo_index = index_by_title(repo_posts)

    actions = {"added": [], "updated": [], "removed": [], "renamed": [], "unchanged": []}
    repo_handled = set()  # track (title, filepath) that we've processed

    for title, obs_entries in obsidian_index.items():
        obs = obs_entries[0]  # Obsidian has unique filenames per title

        if title not in repo_index:
            # New article
            dest = os.path.join(repo_dir, obs["filename"])
            if not dry_run:
                with open(obs["filepath"], "r", encoding="utf-8") as src_f:
                    with open(dest, "w", encoding="utf-8") as dst_f:
                        dst_f.write(src_f.read())
            actions["added"].append(obs["filename"])
            print(f"  新增: {obs['filename']}", file=sys.stderr)

        else:
            repo_entries = repo_index[title]

            # Pick best match: prefer same filename, otherwise use first
            match = repo_entries[0]
            for r in repo_entries:
                if r["filename"] == obs["filename"]:
                    match = r
                    break

            # Remove any other repo files with same title (duplicates from old sync)
            for r in repo_entries:
                if r["filepath"] != match["filepath"]:
                    if not dry_run:
                        os.remove(r["filepath"])
                    actions["removed"].append(r["filename"])
                    print(f"  清理重复: {r['filename']}", file=sys.stderr)

            repo_handled.add(match["filepath"])

            same_content = obs["hash"] == match["hash"]
            same_name = obs["filename"] == match["filename"]

            if same_content and same_name:
                actions["unchanged"].append(obs["filename"])
                continue

            if not same_name:
                old_path = match["filepath"]
                if not dry_run:
                    os.remove(old_path)
                actions["renamed"].append(
                    {"from": match["filename"], "to": obs["filename"]}
                )
                print(f"  重命名: {match['filename']} -> {obs['filename']}", file=sys.stderr)

            if not same_content:
                dest = os.path.join(repo_dir, obs["filename"])
                if not dry_run:
                    with open(obs["filepath"], "r", encoding="utf-8") as src_f:
                        with open(dest, "w", encoding="utf-8") as dst_f:
                            dst_f.write(src_f.read())
                if same_name:
                    actions["updated"].append(obs["filename"])
                    print(f"  已同步: {obs['filename']}", file=sys.stderr)

    # Removed (in repo but not in Obsidian)
    for title, repo_entries in repo_index.items():
        if title in obsidian_index:
            continue
        for r in repo_entries:
            if not dry_run:
                os.remove(r["filepath"])
            actions["removed"].append(r["filename"])
            print(f"  已删除: {r['filename']}", file=sys.stderr)

    print(json.dumps(actions, ensure_ascii=False))
    return actions


if __name__ == "__main__":
    main()

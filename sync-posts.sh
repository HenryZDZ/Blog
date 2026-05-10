#!/bin/bash
set -e

BLOG_REPO="$HOME/Project/Posts"
OBSIDIAN_POSTS="$HOME/Documents/Obsidian Vault/Blog-Posts"

# Copy new/updated .md files from Obsidian to blog posts dir
changed=0
for src in "$OBSIDIAN_POSTS"/*.md; do
    [ -f "$src" ] || continue
    filename=$(basename "$src")
    dest="$BLOG_REPO/posts/$filename"

    if [ ! -f "$dest" ] || ! cmp -s "$src" "$dest"; then
        cp "$src" "$dest"
        echo "Synced: $filename"
        changed=1
    fi
done

# Commit and push if changes
if [ $changed -eq 1 ]; then
    cd "$BLOG_REPO"
    git add posts/
    git commit -m "sync: update posts from Obsidian" || true
    git push origin main
    echo "Pushed to GitHub"
fi

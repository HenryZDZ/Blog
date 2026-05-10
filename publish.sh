#!/bin/bash
# 一键发布：从 Obsidian 同步文章到博客并上线
set -e

OBSIDIAN_POSTS="$HOME/Documents/Obsidian Vault/Blog-Posts"
BLOG_REPO="$HOME/Project/Posts"
PA_API_TOKEN="9841545a07af5fc398bc96f780a14eb81d19d999"
PA_USER="HenryAQA"
PA_DOMAIN="HenryAQA.pythonanywhere.com"
PA_API="https://www.pythonanywhere.com/api/v0/user/$PA_USER"

echo "同步 Obsidian 文章..."

for src in "$OBSIDIAN_POSTS"/*.md; do
    [ -f "$src" ] || continue
    filename=$(basename "$src")
    dest="$BLOG_REPO/posts/$filename"
    if [ ! -f "$dest" ] || ! cmp -s "$src" "$dest"; then
        cp "$src" "$dest"
        echo "  已同步: $filename"

        encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$filename'))")
        curl -s -X POST \
            -H "Authorization: Token $PA_API_TOKEN" \
            -F "content=@$src" \
            "$PA_API/files/path/home/$PA_USER/Blog/posts/$encoded" > /dev/null
        echo "  已上传: $filename"
    fi
done

echo "重载网站..."
curl -s -X POST -H "Authorization: Token $PA_API_TOKEN" \
    "$PA_API/webapps/$PA_DOMAIN/reload/" > /dev/null

echo "推送到 GitHub..."
cd "$BLOG_REPO"
git add posts/
git commit -m "publish: sync posts from Obsidian" || true
git push origin main 2>/dev/null || true

echo "完成。访问 https://$PA_DOMAIN"

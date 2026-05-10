#!/bin/bash
# 一键发布：从 Obsidian 同步文章到博客并上线
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/.env"

OBSIDIAN_POSTS="$HOME/Documents/Obsidian Vault/Blog-Posts"
BLOG_REPO="$HOME/Project/Posts"
PA_USER="HenryAQA"
PA_DOMAIN="HenryAQA.pythonanywhere.com"
PA_API="https://www.pythonanywhere.com/api/v0/user/$PA_USER"

echo "同步 Obsidian 文章..."

# Run sync script, capture JSON from the last line
sync_json=$(python3 "$BLOG_REPO/sync_posts.py" "$OBSIDIAN_POSTS" "$BLOG_REPO/posts")

echo "上传变更到 PythonAnywhere..."

upload_file() {
    local filepath="$1"
    local filename="$2"
    local encoded
    encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$filename'))")
    curl -s -X POST \
        -H "Authorization: Token $PA_API_TOKEN" \
        -F "content=@$filepath" \
        "$PA_API/files/path/home/$PA_USER/Blog/posts/$encoded" > /dev/null
    echo "  已上传: $filename"
}

delete_file() {
    local filename="$1"
    local encoded
    encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$filename'))")
    curl -s -X DELETE \
        -H "Authorization: Token $PA_API_TOKEN" \
        "$PA_API/files/path/home/$PA_USER/Blog/posts/$encoded" > /dev/null
    echo "  已删除: $filename"
}

# Process added and updated files
python3 -c "
import json, sys
data = json.loads(sys.argv[1])
files = data.get('added', []) + data.get('updated', []) + [r['to'] for r in data.get('renamed', [])]
for f in files:
    print(f)
" "$sync_json" | while read -r filename; do
    [ -z "$filename" ] && continue
    upload_file "$BLOG_REPO/posts/$filename" "$filename"
done

# Process removed files
python3 -c "
import json, sys
data = json.loads(sys.argv[1])
for f in data.get('removed', []):
    print(f)
" "$sync_json" | while read -r filename; do
    [ -z "$filename" ] && continue
    delete_file "$filename"
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

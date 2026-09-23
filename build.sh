#!/usr/bin/env bash
# 從 src/content.py 產生 index.html，並重編 Tailwind CSS。
#
# 改內容 → 改 src/content.py
# 改版面／樣式／JS → 改 src/template.html（或 src/render.py 的輸出格式）
# 改完一律跑這支腳本，index.html 不要手改。
set -euo pipefail
cd "$(dirname "$0")"

python3 src/render.py
bash build-tailwind.sh

echo
echo "完成。要部署："
echo "  git add -A && git commit -m 'update: ...' && git push"

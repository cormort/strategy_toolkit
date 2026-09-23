#!/usr/bin/env bash
# 重新產生 assets/tailwind.css
#
# 為什麼需要這一步：
# index.html 原本用 Tailwind Play CDN（執行時產生樣式，但會在 console 警告不適合正式環境）。
# 現在改成預先編譯成靜態 CSS。副作用是：新增或修改 HTML 裡的 Tailwind class 之後，
# 若沒有重跑這支腳本，新 class 不會出現在 assets/tailwind.css，樣式會「靜默失效」——
# 畫面不會報錯，只是那個 class 完全沒有效果。
#
# 因此：任何新增 class 的改動，都要跟著重跑這支腳本，並把 assets/tailwind.css 一起提交。
#
# 用法：bash build-tailwind.sh
set -euo pipefail
cd "$(dirname "$0")"

TMP="$(mktemp -t tw_in).css"
printf '@tailwind base;\n@tailwind components;\n@tailwind utilities;\n' > "$TMP"

npx --yes tailwindcss@3.4.17 \
  -i "$TMP" \
  -o assets/tailwind.css \
  --content ./index.html \
  --minify

rm -f "$TMP"
echo "已產生 assets/tailwind.css（$(wc -c < assets/tailwind.css | tr -d ' ') bytes）"

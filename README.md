# 商業生命週期策略工具箱

單頁 HTML 工具：依企業生命週期（創業／成長／成熟／衰退轉型）分頁，提供對應的策略框架工作單，
可存檔、匯出 Word、列印，並整合「🎮 認知作弊器」模組。

線上：https://cormort.github.io/strategy_toolkit/

## 檔案結構

```
src/content.py        內容資料 —— 唯一真實來源（框架、階段、欄位、說明、總結）
src/template.html     版面外殼（CSS / JS / 分頁按鈕，不含各階段內容）
src/render.py         產生器：content.py + template.html → index.html
build.sh              產生 index.html 並重編 Tailwind CSS（改完一律跑這個）
build-tailwind.sh     只重編 Tailwind CSS
index.html            ⚠️ 產生出來的檔案，不要直接編輯
assets/tailwind.css   產生出來的 Tailwind 靜態 CSS
```

## 改東西要改哪裡

| 想改什麼 | 改哪裡 |
|---|---|
| 問題文字、提示、階段重點、工具說明、總結 | `src/content.py` |
| 新增一個策略框架 | `src/content.py` 的 `FRAMEWORKS` 加一筆，再到 `STAGE_ORDER` 對應階段加進去 |
| 版面、CSS、JS 行為 | `src/template.html` |
| 產生的 HTML 長相（縮排、class 組合） | `src/render.py` |

改完一律：

```bash
bash build.sh
```

**不要直接編 `index.html`** —— 每次建置都會整個覆蓋。

## ⚠️ 三個會靜默出錯的地方

**1. 欄位 id 由 `f"{item_key}-{stage}"` 自動產生，不要手寫。**
手寫會漂移，而使用者的舊存檔以 id 為 key 存在 localStorage 裡，一漂移就載不回來。
真的不能改名的舊欄位放在 `content.py` 的 `ID_OVERRIDES`（目前只有 `ws-ec` → `ws-growth-ec` 一個）。

**2. 新增 Tailwind class 之後一定要重跑 Tailwind 編譯。**
`build.sh` 已包含這一步；若只跑 `render.py`，新 class 不會出現在 `assets/tailwind.css`，
該 class 會**完全沒有效果，而且不會有任何錯誤訊息**。

**3. 樣式表順序。**
`assets/tailwind.css` 必須排在 `index.html` 自訂 `<style>` **之後**。兩者特異度相同，
順序決定誰勝出（原本的 CDN 版是執行時注入，天生在後面）。

## 功能

- **階段判定**：4 題判定目前所處階段並跳轉對應工作表（同分取較早階段，並列出各階段票數）
- **跨階段沿用**：把上一階段已填寫的同框架欄位帶入（附加不覆蓋）
- **自動儲存**：停止輸入 1.5 秒後自動寫入 localStorage；未存就關頁面會攔一次
- **手動儲存／載入**：`Cmd/Ctrl + S` 也可儲存
- **備份／還原**：JSON 匯出匯入，可跨裝置搬移
- **匯出 Word**：HTML 形式的 `.doc`（Word／Google Docs／LibreOffice／Pages 都能開）
- **列印**：長內容的 textarea 會完整展開，不會被裁掉
- **🎮 認知作弊器**：5 個 MOD 卡、分類篩選、關鍵字搜尋、30/120/600 秒計時器

## 開發備註

- 只有 `textarea.worksheet-input` 的內容會進存檔；搜尋框刻意用 `type="search"` 以免被存進 localStorage
- 下載檔名用本地日期（`localDateStr()`），不用 `toISOString()`（那是 UTC，在台北會差一天）
- 互動輔助元件（階段判定卡、沿用按鈕）標記 `no-print`，列印與匯出只輸出工作表內容
- 單欄欄位的 class 依位置決定：排在矩陣**前面**用 `mb-4`，排在**後面**用 `mt-4`（由 `render.py` 推導）
- 改動後請驗證：`python3 src/render.py` 的欄位數應為 91 且無重複 id

## 現況備註（下一階段可處理）

- 7 個框架散布在 91 個欄位；其中約 70 欄是**同一批問題在不同階段重填**（VRIO 24 欄、五力 18 欄、
  BCG 15 欄、安索夫 15 欄、SWOT 14 欄）。原因是「分析」與「階段判讀」目前綁在同一個分頁裡 ——
  而同框架的核心問題在各階段其實一字不差，只有最後一題綜合判斷與提示文字不同。
  `content.py` 已把框架集中成一份資料，要拆成「分析填一次 ＋ 各階段只填判讀」比之前容易很多。
- 18 條工具說明合計只有 217 字（平均 12 字），沒有判讀準則、範例或評分。
- `經驗曲線` 只有 1 個欄位，且未列入「策略分析」分頁的總覽。
- 「分析」與「階段判讀」若拆開，`STAGE_ORDER` 之外還要加一層「分析框架清單」的資料結構。

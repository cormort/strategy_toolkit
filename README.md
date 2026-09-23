# 商業生命週期策略工具箱 v2

單頁 HTML 工具：把「與階段無關的策略分析」集中在一個分頁做一次，各階段分頁只留下該階段
特有的判讀問題；每個框架都附判讀準則與實例，VRIO 與 BCG 會自動算出結論。

線上：https://cormort.github.io/strategy_toolkit/

## 檔案結構

```
src/content.py        內容資料 —— 唯一真實來源（框架、階段、欄位、準則、實例、舊存檔對應表）
src/template.html     版面外殼（CSS / JS / 分頁按鈕，不含各階段內容）
src/render.py         產生器：content.py + template.html → index.html
build.sh              產生 index.html 並重編 Tailwind CSS（改完一律跑這個）
build-tailwind.sh     只重編 Tailwind CSS
index.html            ⚠️ 產生出來的檔案，不要直接編輯
assets/tailwind.css   產生出來的 Tailwind 靜態 CSS
```

## 分頁結構

- **📋 現況與分析**：① 對象與現況 ② SWOT ③ 五力 ④ VRIO ⑤ BCG ⑥ 安索夫 ⑦ 波特基本策略
  ⑧ 經驗曲線 ⑨ 綜合判斷 —— **與階段無關，只填一次**
- **🌱🚀🌳🍂 四個階段**：每階段 3 題判讀（核心矛盾／該先做的一件事／訊號）
- **🎯 行動計畫**：4 項 ×（要做什麼／負責人／期限／成功指標）
- **🎮 認知作弊器**：隨身作弊代碼，獨立、不存檔、不匯出

## 改東西要改哪裡

| 想改什麼 | 改哪裡 |
|---|---|
| 問題文字、提示、準則、實例、階段判讀 | `src/content.py` |
| 新增一個框架 | `src/content.py` 的 `ANALYSIS` 加一個 dict（`layout` 決定版面形狀） |
| 版面、CSS、JS 行為 | `src/template.html` |
| 產生的 HTML 長相（縮排、class 組合） | `src/render.py` |

改完一律 `bash build.sh`。**不要直接編 `index.html`** —— 每次建置都會整個覆蓋。

### layout 的形狀

`ANALYSIS` 每個區塊的 `layout` 是一串 tuple，決定該框架用什麼形狀呈現：

```python
("grid", 2, [keys])                      # 兩欄並排（對象與現況）
("matrix", 2, [s, w, o, t])              # 2×2 矩陣（SWOT、安索夫）
("list", [keys])                         # 單欄直排（五力、經驗曲線）
("radio", key, opts, note_key)           # 是/否選項 + 說明欄（VRIO）
("radio", key, opts, None, "題目文字")   # 沒有說明欄的選項（BCG、波特基本策略）
("verdict", key)                         # 自動判定框（JS 依選項即時計算）
```

## ⚠️ 三個會靜默出錯的地方

**1. 欄位 id 就是存檔的 key，不要手寫、不要改。**
分析欄位用 `obj-name`、`swot-s` 這類固定字串；判讀欄位 `read-<階段>-<n>`；行動 `act-<列>-<欄>`。
改 id 等於使用者的存檔找不到欄位。舊版（v1）id → v2 id 的對應表是 `content.py` 的
`ID_MIGRATION`，這是「舊存檔能不能搬過來」的唯一依據；新增或改動欄位時要一起維護。

**2. 新增 Tailwind class 之後一定要重跑 Tailwind 編譯。**
`build.sh` 已包含這一步；只跑 `render.py` 的話，新 class 不會出現在 `assets/tailwind.css`，
該 class 會**完全沒有效果，而且不會有任何錯誤訊息**。

**3. 樣式表順序。**
`assets/tailwind.css` 必須排在 `index.html` 自訂 `<style>` **之後**。兩者特異度相同，
順序決定誰勝出（原本的 CDN 版是執行時注入，天生在後面）。

## 存檔、遷移與備份

- 存檔只存在瀏覽器 localStorage（key `businessLifecycleData`），格式
  `{ _schema: 2, <欄位 id>: 值, ... }`，是/否選項也一併存。
- **開頁會自動還原**上次內容。偵測到沒有 `_schema` 的舊版存檔時會自動轉換（同一批問題在舊版
  四個階段各一份，只保留有內容的，完全相同者只留一份），並立刻寫回新格式。
- 匯出 Word 依「區塊 → 欄位」順序輸出**已填寫**的內容（含自動判定結果與選項選擇）；
  列印輸出畫面上整份表格，長 textarea 會完整展開不裁切。
- 分頁列、階段判定卡、展開準則按鈕都標記 `no-print`，列印與匯出只留內容。

## 功能

- **階段判定**：4 題判定目前所處階段並跳轉對應分頁（同分取較早階段，並列出各階段票數）
- **自動判定**：VRIO 四道關卡 → 競爭劣勢／競爭均勢／暫時優勢／未利用的潛力／持續優勢；
  BCG 成長率 × 相對市佔 → 明星／問號／金牛／狗
- **判讀準則與實例**：7 個框架各一段，預設收合，可單鍵展開全部
- **自動儲存**：停止輸入 1.5 秒後自動寫入；未存就關頁面會攔一次；`Cmd/Ctrl + S` 也可儲存
- **備份／還原 JSON**：可跨裝置搬移；舊版備份檔也能還原（自動轉換）
- **列印／匯出 Word**：見上
- **🎮 認知作弊器**：5 個 MOD 卡、分類篩選、關鍵字搜尋、30/120/600 秒計時器

## 開發備註

- 只有 `textarea.worksheet-input` 與 `input[type=radio][data-save]` 會進存檔；
  作弊器的搜尋框刻意用 `type="search"` 以免被存進 localStorage
- 下載檔名用本地日期（`localDateStr()`），不用 `toISOString()`（那是 UTC，在台北會差一天）
- 單欄欄位的 class 依位置決定：排在矩陣**前面**用 `mb-4`，排在**後面**用 `mt-4`（由 `render.py` 推導）
- 改動後請驗證：`python3 src/render.py` 應產出 **60 個文字欄位、15 個是/否選項**，且無重複 id
- `build.sh` 的產出必須可重現（連跑兩次 sha256 相同）

# 商業生命週期策略工具箱 v3

單頁 HTML 工具：把「與階段無關的策略分析」集中在一個分頁做一次，各階段分頁只留下該階段
特有的判讀問題；每個框架都附判讀準則與實例，VRIO 與 BCG 會自動算出結論，BCG 支援多個
事業單位並自動畫出組合矩陣，行動計畫可追蹤狀態與逾期。

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

- **現況與分析**：① 對象與現況 ② SWOT ③ 五力 ④ VRIO ⑤ BCG ⑥ 安索夫 ⑦ 波特基本策略
  ⑧ 經驗曲線 ⑨ 綜合判斷 —— **與階段無關，只填一次**
- **四個階段**（創業／成長／成熟／衰退轉型）：每階段 3 題判讀（核心矛盾／該先做的一件事／訊號）
- **行動計畫**：4 項 ×（要做什麼／負責人／期限／成功指標／狀態）
- **認知作弊器**：隨身作弊代碼，獨立、不存檔、不匯出

## 改東西要改哪裡

| 想改什麼 | 改哪裡 |
|---|---|
| 問題文字、提示、準則、實例、階段判讀 | `src/content.py` |
| 新增一個框架 | `src/content.py` 的 `ANALYSIS` 加一個 dict（`layout` 決定版面形狀） |
| 版面、CSS、JS 行為 | `src/template.html` |
| 產生的 HTML 長相（縮排、class 組合） | `src/render.py` |
| 事業單位數量上限、行動列數、狀態選項 | `src/content.py` 的 `BCG_MAX_UNITS`／`ACTION_ROWS`／`ACTION_STATUS` |

改完一律 `bash build.sh`。**不要直接編 `index.html`** —— 每次建置都會整個覆蓋。
`render.py` 走的是 `.replace()` 精準置換，所以 `template.html` 裡的錨點文字（含佔位標記）
不能改字。

### layout 的形狀

`ANALYSIS` 每個區塊的 `layout` 是一串 tuple，決定該框架用什麼形狀呈現：

```python
("grid", 2, [keys])                      # 兩欄並排（對象與現況）
("matrix", 2, [s, w, o, t])              # 2×2 矩陣（SWOT、安索夫）
("list", [keys])                         # 單欄直排（五力、經驗曲線）
("radio", key, opts, note_key)           # 是/否選項 + 說明欄（VRIO）
("radio", key, opts, None, "題目文字")   # 沒有說明欄的選項（波特基本策略）
("verdict", key)                         # 自動判定框（JS 依選項即時計算）
("bcgmatrix", None)                      # BCG：多事業單位列表 + 自動繪製 2×2 + 組合摘要
```

`bcgmatrix` 的欄位不是寫在 `content.py` 的 `items`，而是由 `BCG_UNIT_FIELDS` 乘上
`BCG_MAX_UNITS` 產生，id 規則 `bcg-<n>-<欄>`；後 3 列預設 `hidden`，由「＋ 新增事業單位」
逐列打開（`bcgSyncHidden()`）。

## ⚠️ 四個會靜默出錯的地方

**1. 欄位 id 就是存檔的 key，不要手寫、不要改。**
分析欄位用 `obj-name`、`swot-s` 這類固定字串；判讀欄位 `read-<階段>-<n>`；行動 `act-<列>-<欄>`；
BCG `bcg-<n>-<欄>`。改 id 等於使用者的存檔找不到欄位。舊版（v1／v2）id → 現行 id 的對應表是
`content.py` 的 `ID_MIGRATION`（v1→v3）與 `ID_MIGRATION_V2`（v2→v3），這是「舊存檔能不能搬過來」
的唯一依據；新增或改動欄位時要一起維護。

**2. JS 不能直接寫 Python 端的常數名。**
`SCHEMA_VERSION`、`ACTION_ROWS`、`BCG_MAX_UNITS`、`BCG_DEFAULT_UNITS` 都由 `render.py` 注入成頁面上的
`const`。直接寫在 `template.html` 的 JS 裡會**通過語法檢查、建置也成功**，但開頁時丟
`ReferenceError`，而且如果那句在 `try{}` 裡就會被 catch 吞掉 —— 症狀是某段初始化「什麼都沒發生」。
`render.py` 已加入建置期檢查：JS 用到但頁面沒有對應 `const` 宣告就中止建置。

**3. 新增 Tailwind class 之後一定要重跑 Tailwind 編譯。**
`build.sh` 已包含這一步；只跑 `render.py` 的話，新 class 不會出現在 `assets/tailwind.css`，
該 class 會**完全沒有效果，而且不會有任何錯誤訊息**。

**4. 樣式表順序。**
`assets/tailwind.css` 必須排在 `index.html` 自訂 `<style>` **之後**。兩者特異度相同，
順序決定誰勝出（原本的 CDN 版是執行時注入，天生在後面）。

## 存檔、遷移與備份

- 存檔只存在瀏覽器 localStorage（key `businessLifecycleData`），格式
  `{ _schema: 3, <欄位 id>: 值, ... }`，是/否選項與下拉都在內，另存 `_savedAt`、`_reviewedAt`。
- **開頁會自動還原**上次內容。舊版存檔自動升級：`_schema` 缺漏或 < 2 先跑 `migrateV1`，
  再一律跑 `migrateV2to3`；轉換後立刻寫回現行格式（否則每次開頁都要重轉）。
  同一批分析問題在舊版四個階段各一份時，只保留有內容的，完全相同者只留一份；
  不同問題的內容以「── 舊版『某某』內容 ──」分段保留，不丟資料。
- **只進存檔的元素**：`textarea.worksheet-input`、`input[type=radio][data-save]`、
  `select[data-save]`。作弊器的搜尋框刻意用 `type="search"` 以免被存進去。
- 匯出 Word 依「區塊 → 欄位」順序輸出**已填寫**的內容（含自動判定結果與選項選擇）；
  **匯出空白表格**則輸出全部欄位（含 placeholder 當填寫提示、準則與實例一併附上），可印出來手寫。
- 列印輸出畫面上整份表格，長 textarea 會完整展開不裁切；分頁列、階段判定卡、展開準則按鈕、
  工具列都標記 `no-print`。

## 功能

- **階段判定**：4 題判定目前所處階段並跳轉對應分頁（同分取較早階段，並列出各階段票數）
- **自動判定**：
  - VRIO 四道關卡 → 競爭劣勢／競爭均勢／暫時優勢／未利用的潛力／持續優勢
  - BCG 成長率 × 相對市佔 → 明星／問號／金牛／狗（每個事業單位各自算）
  - BCG 組合圖：依象限自動把事業單位畫進 2×2（同名象限多個單位會自動錯位不重疊）
  - 組合摘要：各象限計數 + 依組合給的現金流建議（有狗先排退出順序、有問號別吊著…）
- **多事業單位**：預設 3 個，可加到 6 個，每列可單獨移除（至少留一列）
- **行動追蹤**：每項可設狀態（未開始／進行中／已完成／已取消）；期限格式 `YYYY-MM-DD` 且
  逾期未完成者自動標紅；摘要顯示已填／已完成／進行中／逾期數；「記錄本次檢視」記下檢視時間
- **判讀準則與實例**：7 個框架各一段，預設收合，可單鍵展開全部
- **自動儲存**：停止輸入 1.5 秒後自動寫入；未存就關頁面會攔一次；`Cmd/Ctrl + S` 也可儲存
- **備份／還原 JSON**：可跨裝置搬移；舊版備份檔也能還原（自動轉換）
- **認知作弊器**：5 個 MOD 卡、分類篩選、關鍵字搜尋、30/120/600 秒計時器

## 開發備註

- 下載檔名用本地日期（`localDateStr()`），不用 `toISOString()`（那是 UTC，在台北會差一天）
- 單欄欄位的 class 依位置決定：排在矩陣**前面**用 `mb-4`，排在**後面**用 `mt-4`（由 `render.py` 推導）
- **分頁列用 `flex-wrap` 換行，不要改回 `overflow-x: auto` 的橫向捲動。** 7 個分頁在 1100px 容器
  約 797px 寬；改成橫向捲動後，375px 手機只看得到 3 個分頁、其餘要靠滑動且畫面上沒有任何提示。
  換行後 320/375px 為 3 行、768px 為 2 行、≥1024px 仍是一行（桌面外觀逐像素不變）。
- **視覺樣式改「商務風格覆寫層」**（`template.html` 自訂樣式最後一段，IBM Carbon 語彙：單一藍色
  accent、灰階、扁平、字重 300/400/600、介面不用 emoji）。它靠「同特異度、後者勝」覆寫上面的舊規則，
  要改樣式改這一層。字重若有增減，要同步改 `<head>` 的 Google Fonts `wght@` 參數，否則該字重不會載入。
- 通知（`.notification`）是 `position: fixed`，列印時會被重複印在每一頁，已在 `@media print` 隱藏。
- 改動後請驗證：`python3 src/render.py` 應產出 **70 個文字欄位、37 個是/否選項、4 個下拉**，
  且無重複 id（`render.py` 會自己檢查欄位數加總與重複 id）
- `build.sh` 的產出必須可重現（連跑兩次 sha256 相同）
- 遷移邏輯若改動，兩種舊存檔都要實測：v1（無 `_schema`）與 v2（`_schema: 2`），
  確認欄位落在正確的新 id、舊 key 已清掉、且寫回的 `_schema` 是 3

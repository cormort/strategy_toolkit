# 商業生命週期策略工具箱

單頁 HTML 工具：依企業生命週期（創業／成長／成熟／衰退轉型）分頁，提供對應的策略框架工作單，
可存檔、匯出 Word、列印，並整合「🎮 認知作弊器」模組。

線上：https://cormort.github.io/strategy_toolkit/

## 檔案結構

```
index.html            整個應用程式（HTML + CSS + JS 單檔）
assets/tailwind.css   Tailwind 工具類別編譯後的靜態 CSS（由 build-tailwind.sh 產生）
build-tailwind.sh     重新編譯 assets/tailwind.css
```

## ⚠️ 修改 index.html 的 class 之後，一定要重跑 CSS 編譯

原本使用 Tailwind Play CDN（執行時產生樣式），但 CDN 會在瀏覽器 console 警告不適合正式環境。
現在改為預先編譯：

```bash
bash build-tailwind.sh
```

**沒重跑的後果**：新增的 Tailwind class 不會出現在 `assets/tailwind.css`，
該 class 會**完全沒有效果，而且不會有任何錯誤訊息**。改完請把 `assets/tailwind.css` 一起提交。

> 樣式表順序也很重要：`assets/tailwind.css` 必須排在 `index.html` 的自訂 `<style>` **之後**。
> 兩者特異度相同，順序決定誰勝出（CDN 版是執行時注入，天生在後面）。

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

- 只填寫 `textarea.worksheet-input` 的內容會進存檔；搜尋框刻意用 `type="search"` 以免被存進 localStorage
- 下載檔名用本地日期（`localDateStr()`），不用 `toISOString()`（那是 UTC，在台北會差一天）
- 互動輔助元件（階段判定卡、沿用按鈕）標記 `no-print`，列印與匯出只輸出工作表內容

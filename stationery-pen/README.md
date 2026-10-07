# 世上最強鋼筆百科（100 頁鋼筆最強網站）

> 以「三層 Dropdown 導航結構對 SEO/AEO/GEO 的好處與擴充建議」規格書為依據，將鋼筆百科擴充為百頁級多頁靜態知識網站。
> 多頁靜態架構：每篇文章都是真實的 `.html` 檔案，形成 `/category/subcategory/article` 乾淨 URL，滿足 SEO / AEO / GEO 與爬蟲可達性要求。

## 版本紀錄

| 版本 | 日期 | 說明 |
| --- | --- | --- |
| v1.0.0 | 2026-10-06 | 首版：16 大章、49 個子分類、103 篇文章、全部功能層實作完成 |
| v1.1.0 | 2026-10-06 | 下拉導覽合併為兩層（章節 → 文章）；移除全站章節編號前綴；修復深層頁選單／側欄／搜尋／收藏連結錯位；並將桌面 Mega Menu 下拉改為獨立圖層渲染，修復被捲動容器裁切的問題 |

- 每篇文章標頭均顯示「最後更新」日期與版本號。
- 網站地圖 `sitemap.xml` 自動產生，無孤兒頁。

## 功能清單

### 必備層
- [x] 兩層 Dropdown 主導航（章節 → 文章，下拉直接列出該章全部文章；16 大章超過 15 項，桌面版以 **Mega Menu** 呈現；底層仍保留「分類 → 子分類 → 文章」三層乾淨 URL）
- [x] 麵包屑 Breadcrumb（每頁顯示，含 BreadcrumbList JSON-LD）
- [x] 側邊欄樹狀導覽（文章頁左側同章節目錄，可展開收合）
- [x] 文章目錄 TOC（長文右側浮動目錄，點擊跳轉章節，含滾動偵測 active 狀態）
- [x] 日夜主題切換（亮 / 暗 / 跟隨系統三選一，localStorage 記憶 `pen-theme`）

### 推薦層
- [x] Mega Menu（分類 >15 項時啟用，本網站 16 章）
- [x] 多面向篩選 Faceted Search（首頁與章節頁依分類瀏覽；標籤頁依標籤彙整；難度與更新日期顯示於卡片）
- [x] 標籤系統（每篇 3–6 個標籤 + 標籤彙整頁 `tags/`）
- [x] 全站搜尋＋自動完成（即時建議文章 / 章節 / 標籤，含獨立 `search.html` 結果頁）
- [x] 相關文章（文末 3–6 篇，同子分類優先、跨章節補充）

### 加值層
- [x] A–Z 字母索引（`az-index.html` 全站字母索引 + `glossary/index.html` 詞彙術語 A–Z）
- [x] 版本紀錄／最後更新時間（每頁顯示）
- [x] 閱讀進度條與收藏清單（localStorage `pen-favs`，收藏抽屜可管理）
- [x] 列印／匯出 PDF（文章頁「列印」按鈕，瀏覽器列印即存 PDF，含列印樣式）
- [ ] 知識圖譜檢視（暫未實作，見 Roadmap）
- [ ] 文末留言區（需後端，未實作）

### 其他
- [x] 響應式設計 RWD（手機版漢堡抽屜選單、單欄版面）
- [x] 防複製保護（contextmenu / copy 阻擋 + Toast 提示）
- [x] Breathe Clamp 可重用響應式元件（`assets/js/breathe-clamp.js`：過長內容自動夾取＋「展開全部」，已用於首頁最新文章區塊）
- [x] 語意化 HTML（header / nav / main / article / aside / footer）
- [x] 每頁唯一 meta title / description；首頁 ItemList + WebSite（SearchAction）schema；章節/子分類/標籤頁 CollectionPage + ItemList；文章頁 BreadcrumbList + Article + FAQPage JSON-LD

## 資料來源

- 分類骨架：`D:\_WWW_325\鋼筆百科多層導覽.html`（既有原型，含 16 大章 NAV 結構與 tylee.tw i文具控商品分類映射；**原檔未動**）
- 文章內容：由 AI 依通用鋼筆知識撰寫（繁體中文 zh-Hant），涵蓋原理、結構、材質、筆尖、上墨、墨水、分類、品牌、選購、保養、歷史、收藏、DIY、詞彙、附錄與i文具控章節
- 事實性說明：品牌年份、規格範圍等以「約略／常見」說法呈現；未編造精確成交價或未公開數據
- 圖影素材：本版無外部位圖；如需補圖，提示詞建議見下節

## 圖影素材提示詞（供後續補圖）

- 首頁 Hero：`極簡文具攝影，深色木桌上斜放一支金夾深藍樹脂鋼筆，筆尖朝右下，側逆光，暖色紙感背景，留白充足，高級雜誌質感`
- 章節題圖（16 張，3:2）：`(章節關鍵物) 特寫，微距，柔和窗光，牛皮紙背景，鋼筆工具攝影`
  - 例：材質章 → 賽璐珞筆桿紋理特寫；筆尖章 → 金尖銥粒微距；上墨章 → 活塞吸墨器分解；墨水章 → 試墨色卡暈染
- 品牌章配圖：`鋼筆品牌徽章/經典筆款平視圖，白底商品攝影`
- 示意圖（筆尖尺寸比較、供墨路徑、上墨系統結構）：`細線工程插畫風，單色墨線，等距透視`

## 目錄結構

```
100頁鋼筆最強百科/
├── index.html                 # 首頁（ItemList + WebSite schema）
├── search.html                # 全站搜尋結果頁
├── az-index.html              # A–Z 字母索引
├── sitemap.xml                # 自動產生（爬蟲專用）
├── robots.txt
├── CONTENT-SPEC.md            # 內容撰寫規範（格式標準）
├── build.py                   # 建置腳本（產生全部頁面）
├── assets/
│   ├── css/style.css          # 共用樣式（主題變數、RWD、列印）
│   └── js/                    # 共用 JS（config 由建置產生）
│       ├── config.js          # [自動產生] 導覽/搜尋資料
│       ├── theme.js           # 日夜主題（亮/暗/系統）
│       ├── nav.js             # Mega Menu、側欄樹、手機抽屜
│       ├── search.js          # 全站搜尋＋自動完成
│       ├── reading.js         # 閱讀進度、收藏、列印
│       ├── breathe-clamp.js   # Breathe Clamp 響應式元件
│       └── main.js            # FAQ 手風琴、TOC 滾動偵測、防複製
├── data/
│   ├── site.json              # 章節/子分類/文章規劃（單一來源）
│   ├── articles.json          # [自動產生] 文章資料索引
│   └── articles/              # 內容原始檔（frontmatter + markdown）
│       ├── overview/ … tylee/ # 16 章，每章下依子分類分目錄
├── <chapter>/index.html        # 章節頁（建置產生，如 overview/index.html）
├── <chapter>/<sub>/index.html  # 子分類頁（建置產生）
├── <chapter>/<sub>/<slug>.html # 文章頁（建置產生，103 篇）
├── tags/                       # 標籤彙整頁（建置產生，每標籤一頁）
├── glossary/                   # 詞彙 A–Z 頁（建置產生）
└── _shots/                     # 自檢截圖（非交付物）
```

> 說明：章節、子分類與文章頁產出於網站根目錄下的 `<chapter>/` 與 `<chapter>/<sub>/` 目錄（與 `data/articles` 同名對應），形成 `/category/subcategory/article` 乾淨 URL；此處省略逐章列出。

## 啟動方式

- 直接以瀏覽器開啟 `index.html` 即可（`file://` 即可運作；搜尋資料內建於 config.js，不需伺服器）。
- 建議架站：將整個目錄上傳至任何靜態空間（GitHub Pages / Netlify / Vercel / 自有伺服器），`sitemap.xml` 與 `robots.txt` 已就緒。
- 上線前請在 `data/site.json` 的 `site.rootUrl` 填入正式網域（目前為範例網址），再執行 `python build.py` 重新產生 canonical 與 sitemap。

## 重新建置

```bash
cd 100頁鋼筆最強百科
python build.py --list        # 列出每章文章數
python build.py --check       # 檢查內容檔完整性
python build.py               # 完整建置（產生全部 HTML / sitemap / config.js / articles.json）
```

## Roadmap

- 知識圖譜／心智圖檢視（以同章互鏈與標籤為邊，前端視覺化）
- 文末留言區（靜態方案：Webmention / 第三方評論嵌入）
- 全站圖片素材補齊（提示詞見上節）
- 文章版本歷史（git-based changelog 頁）

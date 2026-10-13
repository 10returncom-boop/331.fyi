# 營養與生活 — CONTENT-SPEC.md（內容規格書）

**版本**：Static-FINAL-20261012
**最後更新**：2026-10-13
**技術棧**：純 HTML5 + CSS3 + Vanilla JavaScript（無框架、無 Python 執行期）
**編碼**：UTF-8 繁體中文
**實體路徑**：`D:\WWW\325_pub\自建主題目錄`

---

## 一、網站定位

| 項目 | 說明 |
|---|---|
| 網站名稱 | 營養與生活（Nutrition & Life） |
| 目標受眾 | 一般大眾、慢性病患、外食族、銀髮族家屬 |
| 語氣 | 權威、專業、大白話、去 AI 化 |
| 差異化 | 每頁附真實案例（非虛構情境）、不業配、不賣保健品 |
| 內容原則 | 非 AI 樣板文、痛點開頭、補充非虛構案例 |

---

## 二、網站變數（部署時替換）

| 變數 | 目前值 | 部署時 |
|---|---|---|
| `SITE_URL` | `https://nutrition.example.com` | 改為正式網域 |
| `CANONICAL` | 同 SITE_URL | 每頁 `<link rel="canonical">` 必須與 loc 一致 |
| `OG_IMAGE` | `/assets/images/hero-*.webp` | OG=9 等級設定 |
| `FAVICON` | `/assets/images/favicon.svg` | 不變 |

---

## 三、檔案與資料夾架構

```
自建主題目錄/
├── index.html                    首頁（Hub）
├── about.html                    關於我們
├── 404.html                      404 頁（noindex）
├── robots.txt                    標註 sitemap
├── sitemap.xml                   只放可收錄頁
├── manifest.json                 Web App Manifest
├── assets/
│   ├── css/style.css             共享設計系統
│   ├── js/main.js                共享 JS（MegaMenu/搜尋/折疊/收藏）
│   ├── js/search-data.js         全站搜尋索引
│   └── images/                   WebP 圖片 + favicon.svg
├── nutrition-basics/index.html   主題 1：營養基礎
├── diet-disease/index.html       主題 2：飲食與疾病
├── life-stage/index.html         主題 3：各族群營養
├── food-guide/index.html         主題 4：食材與標示
├── lifestyle/index.html          主題 5：生活型態
├── docs/
│   ├── CONTENT-SPEC.md           本檔
│   ├── 網站地圖.xlsx
│   ├── 網站變數與導覽表.xlsx
│   ├── convert_webp.py          圖片轉換工具（一次性）
│   └── gen_excel.py              Excel 產生工具
├── check-site.ps1                批次檢查腳本
└── README.md                      部署說明
```

---

## 四、UI 元件清單（全部已實裝）

| 元件 | 實裝位置 |
|---|---|
| Breadcrumb 麵包屑 + BreadcrumbList Schema | 每頁 |
| Accordion 折疊卡片 | 內頁內容 |
| Sidebar + Treemap 樹狀地圖 + TOC 文章目錄 | 內頁側邊欄 |
| MegaMenu 巨型導覽（2 層以內） | 頂端列 |
| Tag System 標籤系統 | 側邊欄 + 卡片 |
| 全站搜尋 autocomplete | 頂端列 |
| Faceted Search 多面向篩選 | Tag 點選篩選 |
| 相關文章推薦模組 | 每頁底部 |
| 知識圖譜（SVG 節點連結） | 首頁 |
| 收藏清單（localStorage） | 每頁收藏按鈕 |
| 右下角浮動固定導航（回首頁/回頂端） | 每頁 |
| OG 標籤、Favicon | 每頁 head |
| 白天模式 | 預設 |

---

## 五、SEO 規格

### 5.1 結構化資料（每頁至少 3 種 JSON-LD）

| 頁面 | JSON-LD |
|---|---|
| 首頁 | WebSite + Organization + FAQPage |
| 主題內頁 | BreadcrumbList + Article + FAQPage |
| 關於頁 | —（簡約） |
| 404 | `noindex, follow` |

### 5.2 Sitemap 規則

- 只放可收錄頁（排除 404、noindex）
- `lastmod` 填真實檔案修改日期（由 `check-site.ps1` 自動產生）
- URL 與 canonical 一致
- **不要重複提交**，GSC 只提交一次 `sitemap.xml`

### 5.3 robots.txt

```
User-agent: *
Allow: /
Sitemap: https://正式網域/sitemap.xml
```

### 5.4 GSC 提交清單

1. 將 `SITE_URL` 改為正式網域
2. GSC 設定偏好網域（www/non-www、http/https 二選一）
3. 提交 `sitemap.xml`（只提交一次）
4. 用「網址檢查工具」逐頁驗證抓取與 Schema
5. 重點頁才申請索引（首頁 + 5 個主題頁）
6. 定期用「索引覆蓋報告」修錯
7. 搭配 IndexNow 推送更新（部署後呼叫一次）

---

## 六、內容寫作規範

1. **痛點開頭**：每段第一句直接講使用者痛點，不繞遠路
2. **大白話**：避免學術黑話，每個觀念附生活例子
3. **真實案例**：每個主題至少 1 個非虛構情境案例
4. **重點加粗**：關鍵數字與結論用 `<strong>`
5. **H1/H2/H3 層級**：一頁一個 H1，H2 為主章節，H3 為子節
6. **圖文並茂**：每頁至少 1 張 WebP 圖，含 alt text
7. **醫療免責**：疾病相關頁面加「不能取代醫師診斷」

---

## 七、效能優化目標

| 指標 | 目標 |
|---|---|
| 首屏載入 | < 2 秒（桌面） |
| 圖片格式 | 全 WebP（62–161KB/張） |
| 無外部框架 | 0（純 Vanilla JS） |
| AEO/RAG | 語義化 HTML、明確 H 標題、FAQPage Schema |
| Topic Cluster | 5 大主題互相連結，首頁為 Hub |

---

## 八、批次檢查腳本

執行 `powershell -ExecutionPolicy Bypass -File check-site.ps1`，會跑 3 項檢核：

1. **SEO 元素掃描**：每頁 title/meta description/OG/JSON-LD 是否存在
2. **連結與圖片路徑檢查**：內部連結、圖片 `src` 是否存在
3. **404 斷鏈偵測**：比對本機檔案存在與否，列出壞掉的連結

---

## 九、資料驅動生成器架構（build.py + data/）

**原則：改資料不動模板。** 新增/修改課程 = 編輯 `data/*.json`，執行 `python build.py`，HTML 自動重生成。

```
data/
├── site.json          # 網站變數：名稱、網域、導覽結構
├── courses.json       # 所有課程資料（標題/講師/價格/大綱）
└── articles.json      # 文章中繼資料（未來擴充）

build.py               # 讀 data/ → 產生 courses/*.html
check-site.ps1         # 產生後跑 3 項檢核
```

**新增一堂課的流程：**
1. 在 `data/courses.json` 的 `courses` 陣列加一筆物件
2. 執行 `python build.py`
3. 執行 `powershell -ExecutionPolicy Bypass -File check-site.ps1`
4. 執行 `python docs/gen_sitemaps.py` 更新 sitemap

**未來升級路徑**：可遷移至 Astro Content Collections，語義與目前 JSON 結構對應，模板可複用。

---

## 十、UI 元件清單（已實裝）

| 元件 | 狀態 |
|---|---|
| Breadcrumb + BreadcrumbList Schema | ✅ |
| Accordion 折疊卡片（FAQ） | ✅ |
| Sidebar + Treemap 樹狀圖 | ✅ |
| TOC 文章目錄 | ✅ |
| 預設白天模式 + 深色切換 | ✅ |
| 三層 MegaMenu 下拉 | ✅ |
| Tag System 標籤 | ✅ |
| 全站搜尋 + 自動完成 | ✅ |
| Faceted Search 多面向篩選（分類/價格/時數） | ✅ |
| 相關文章推薦 | ✅ |
| 知識圖譜 SVG + 收藏清單 | ✅ |
| 右下角浮動導覽（回首頁/回頂端） | ✅ |
| 分頁 Pagination | ✅ |
| OG 標籤（level 9）+ Favicon | ✅ |
| 閱讀進度條 / 字級切換 / 分享 / 列印 | ✅ |
| sitemap-index + article/gallery sitemap | ✅ |
| robots.txt / 404.html / manifest.json | ✅ |

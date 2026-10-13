# 營養與生活 — README

Static-FINAL-20261012｜純 HTML5 + CSS3 + Vanilla JS 多頁式網站

## 快速開始

```bash
# 1. 直接用瀏覽器打開
start index.html

# 2. 或本機預覽（任一靜態伺服器）
python -m http.server 8080
# 打開 http://localhost:8080
```

## 目錄結構

每個資料夾是一個獨立主題，都有自己的 `index.html`。整個資料夾搬移到任何位置都能獨立運作（相對路徑）。

## 部署到 GitHub Pages

1. 在 GitHub 建立 repo
2. 將整個 `自建主題目錄/` 內容上傳
3. Settings → Pages → 選擇 branch
4. 將所有 HTML 中的 `https://nutrition.example.com` 改為正式網域

## 提交 sitemap 到 GSC

1. 部署後打開 `robots.txt`，確認 `Sitemap:` 網址正確
2. Google Search Console → Sitemaps → 提交 `sitemap.xml`
3. **只提交一次**，不要重複
4. 重點頁用「網址檢查工具」驗證 Schema

## 批次檢查（斷鏈/SEO）

```powershell
powershell -ExecutionPolicy Bypass -File check-site.ps1
```

## 圖片更新

所有圖片都是 WebP。若要新增圖片：

1. 放原圖到 `assets/images/`
2. 執行 `python docs/convert_webp.py` 轉 WebP
3. HTML 中引用 `.webp` 檔並加 `alt`

## Git 工作流程

- 本機修改後請**手動** `git add`、`commit`、`push`
- **不會自動 commit**，所有 push 必須經過同意
- 本機 folder 必須與 GitHub 維持一致

## 技術棧

- 純 HTML5（semantic）
- CSS3（CSS variables、Grid、Flexbox、RWD）
- Vanilla JavaScript（無 jQuery、無 React、無 Vue）
- 無後端、無資料庫

## 授權

內容僅供教育用途，不能取代專業醫療建議。

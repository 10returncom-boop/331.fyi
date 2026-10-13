"""Regenerate courses/index.html in NailPut gallery style."""
import json, os, html
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

with open(os.path.join(DATA, "site.json"), encoding="utf-8") as f:
    site = json.load(f)
with open(os.path.join(DATA, "courses.json"), encoding="utf-8") as f:
    cdata = json.load(f)

courses = cdata["courses"]

# NailPut-style gallery cards: image-first, clean tags
cards_html = ""
for i, c in enumerate(courses):
    price_label = f"NT${c['price_sale']:,}" if c['price_sale'] > 0 else "免費"
    cards_html += f'''    <a class="gallery-item" href="{c['slug']}.html">
      <div class="gallery-img">
        <img src="../{c['img']}" alt="{html.escape(c['title'])}" loading="lazy">
        <span class="gallery-tag">#{c['category']}</span>
      </div>
      <div class="gallery-info">
        <h3>{html.escape(c['title'])}</h3>
        <p>{html.escape(c['desc'])}</p>
        <div class="gallery-meta">
          <span>{c['teacher']} 營養師</span>
          <span class="gallery-price">{price_label}</span>
        </div>
      </div>
    </a>
'''

html_out = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>營養圖庫｜{len(courses)}堂精選線上課程 - {site['site_name']}</title>
  <meta name="description" content="大眾化營養知識圖庫：糖尿病、減重、銀髮族、備孕。由資深營養師設計，大白話解說。">
  <link rel="canonical" href="{site['domain']}/courses/">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{site['site_name']}">
  <meta property="og:title" content="營養圖庫｜{len(courses)}堂精選課程">
  <meta property="og:description" content="大白話營養課程圖庫">
  <meta property="og:url" content="{site['domain']}/courses/">
  <meta property="og:image" content="{site['domain']}/assets/images/hero-home.webp">
  <meta property="og:locale" content="zh_TW">
  <link rel="icon" type="image/svg+xml" href="../assets/images/favicon.svg">
  <link rel="stylesheet" href="../assets/css/style.css">
  <style>
    /* NailPut 風格客製 */
    :root {{ --np-pink: #b86b7d; --np-pink-light: #f5e8ec; }}
    .np-header {{ background:#fff; border-bottom:3px solid #3a3a3a; padding:20px 0; }}
    .np-logo {{ display:flex; align-items:center; gap:12px; }}
    .np-logo-icon {{ width:40px; height:56px; background:var(--np-pink); border-radius:20px 20px 8px 8px; position:relative; }}
    .np-logo-icon::after {{ content:""; position:absolute; bottom:-10px; left:50%; transform:translateX(-50%); width:6px; height:12px; background:var(--np-pink); border-radius:0 0 3px 3px; }}
    .np-logo-text {{ font-size:1.6rem; font-weight:900; color:var(--np-pink); letter-spacing:2px; }}
    .np-hero {{ text-align:center; padding:40px 20px; background:var(--np-pink-light); }}
    .np-hero h1 {{ font-size:1.8rem; margin:0 0 8px; }}
    .np-hero p {{ color:#666; margin:0; }}
    .np-tabs {{ display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin:24px 0; }}
    .np-tab {{ padding:8px 18px; border-radius:999px; border:1px solid #ddd; background:#fff; cursor:pointer; font-size:.88rem; }}
    .np-tab.active {{ background:var(--np-pink); color:#fff; border-color:var(--np-pink); }}
    .gallery-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }}
    .gallery-item {{ display:block; text-decoration:none; color:inherit; }}
    .gallery-img {{ position:relative; aspect-ratio:1; border-radius:12px; overflow:hidden; background:#f0f0f0; }}
    .gallery-img img {{ width:100%; height:100%; object-fit:cover; transition:transform .3s; }}
    .gallery-item:hover .gallery-img img {{ transform:scale(1.05); }}
    .gallery-tag {{ position:absolute; top:8px; left:8px; background:rgba(255,255,255,.9); padding:3px 10px; border-radius:999px; font-size:.72rem; color:var(--np-pink); font-weight:700; }}
    .gallery-info {{ padding:10px 4px; }}
    .gallery-info h3 {{ font-size:.92rem; margin:0 0 4px; line-height:1.3; }}
    .gallery-info p {{ font-size:.78rem; color:#888; margin:0 0 8px; line-height:1.4; }}
    .gallery-meta {{ display:flex; justify-content:space-between; font-size:.76rem; color:#999; }}
    .gallery-price {{ color:var(--np-pink); font-weight:700; }}
    @media (max-width:1024px) {{ .gallery-grid {{ grid-template-columns:repeat(3,1fr); }} }}
    @media (max-width:640px) {{ .gallery-grid {{ grid-template-columns:repeat(2,1fr); }} }}
  </style>
</head>
<body>

<!-- NailPut 風格標頭 -->
<div class="np-header">
  <div class="container" style="display:flex; justify-content:space-between; align-items:center;">
    <a href="../index.html" class="np-logo">
      <span class="np-logo-icon"></span>
      <span class="np-logo-text">營養圖庫</span>
    </a>
    <nav style="display:flex; gap:16px; font-size:.88rem;">
      <a href="../index.html" style="color:#333; text-decoration:none;">首頁</a>
      <a href="index.html" style="color:var(--np-pink); font-weight:700;">圖庫</a>
      <a href="../about.html" style="color:#333; text-decoration:none;">關於</a>
    </nav>
  </div>
</div>

<section class="np-hero">
  <h1>營養圖庫</h1>
  <p>大白話營養知識，{len(courses)}堂精選課程，一次搞懂</p>
</section>

<div class="container" style="padding:24px 20px 60px;">

  <!-- 分類 Tab -->
  <div class="np-tabs">
    <button class="np-tab active">全部（{len(courses)}）</button>
    <button class="np-tab">疾病飲食</button>
    <button class="np-tab">體重管理</button>
    <button class="np-tab">族群營養</button>
    <button class="np-tab">食材應用</button>
    <button class="np-tab">生活型態</button>
  </div>

  <!-- 圖庫網格 24 張 -->
  <div class="gallery-grid">
{cards_html}  </div>

  <!-- 分頁 -->
  <nav class="pagination" style="margin-top:40px;">
    <span class="current">1</span>
    <a href="#">2</a>
    <a href="#">下一頁 ›</a>
  </nav>
</div>

<div class="floating-nav">
  <button class="fab secondary" onclick="location.href='../index.html'">⌂</button>
  <button class="fab" id="fabTop">↑</button>
</div>

<footer class="site-footer">
  <div class="container">
    <div class="footer-bottom" style="border:0;margin:0;">
      © {datetime.now().year} {site['site_name']}｜營養圖庫
    </div>
  </div>
</footer>

<script src="../assets/js/search-data.js"></script>
<script src="../assets/js/main.js"></script>
</body>
</html>
'''

out_path = os.path.join(ROOT, "courses", "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_out)
print(f"courses/index.html: NailPut gallery style, {len(courses)} items")

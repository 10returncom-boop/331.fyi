"""
build.py - 資料驅動網站生成器
用法：python build.py
讀取 data/*.json → 產生 courses/*.html
新增課程 = 在 data/courses.json 加一筆，跑 python build.py，不用動 HTML 模板。
"""
import json, os, html
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
COURSES_DIR = os.path.join(ROOT, "courses")

def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)

def esc(s):
    return html.escape(str(s), quote=True)

def head(title, desc, url, img):
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{esc(url)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:type" content="product">
  <meta property="og:site_name" content="營養與生活">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{esc(url)}">
  <meta property="og:image" content="{esc(img)}">
  <meta property="og:locale" content="zh_TW">
  <link rel="icon" type="image/svg+xml" href="../assets/images/favicon.svg">
  <link rel="stylesheet" href="../assets/css/style.css">"""

def build_course_detail(c, site):
    url = f"{site['domain']}/courses/{c['slug']}.html"
    img = f"{site['domain']}/{c['img']}"
    head_html = head(
        f"{c['title']}｜營養與生活", c['desc'], url, img
    )
    cur_html = ""
    for num, title, dur in c["curriculum"]:
        cur_html += f'''      <details class="curriculum-item" style="cursor:pointer;">
        <summary style="display:flex;justify-content:space-between;align-items:center;list-style:none;">
          <div><span class="lesson-num">{esc(num)}</span>{esc(title)}</div>
          <span class="lesson-duration">{esc(dur)} ▸</span>
        </summary>
        <p style="padding:10px 16px;color:var(--c-ink-2);font-size:.88rem;margin:0;">本章節帶你認識{esc(title)}的重點，包含觀念解說、實務操作與常見迷思破解。</p>
      </details>\n'''

    price_display = f"NT${c['price_sale']:,}" if c['price_sale'] > 0 else "免費"
    orig_display = f"NT${c['price_orig']:,}" if c['price_orig'] > 0 else ""

    return f"""{head_html}
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Course","name":"{esc(c['title'])}","description":"{esc(c['desc'])}","provider":{{"@type":"Organization","name":"營養與生活"}},"offers":{{"@type":"Offer","price":"{c['price_sale']}","priceCurrency":"TWD"}},"hasCourseInstance":{{"@type":"CourseInstance","courseMode":"online"}}}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"首頁","item":"{site['domain']}/"}},
    {{"@type":"ListItem","position":2,"name":"線上課程","item":"{site['domain']}/courses/"}},
    {{"@type":"ListItem","position":3,"name":"{esc(c['title'])}","item":"{url}"}}
  ]}}
  </script>
</head>
<body>
<a class="skip-link" href="#main">跳至主內容</a>
<header class="site-header">
  <div class="header-bar">
    <a class="brand" href="../index.html">
      <svg class="brand-mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#1f7a4d"/><path d="M32 14 C22 24 18 34 22 44 C26 54 38 56 44 48 C50 40 46 28 32 14 Z" fill="#fff"/></svg>
      <span>營養與生活<small>NUTRITION & LIFE</small></span>
    </a>
    <button class="nav-toggle" aria-label="開啟選單">☰</button>
    <nav class="main-nav" id="mainNav" aria-label="主導覽">
      <div class="nav-item"><a class="nav-link" href="../index.html">首頁</a></div>
      <div class="nav-item active"><a class="nav-link" href="index.html">線上課程</a></div>
    </nav>
  </div>
</header>

<section class="course-detail-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="麵包屑" style="padding:10px 0;">
      <ol>
        <li><a href="../index.html">首頁</a></li>
        <li><a href="index.html">線上課程</a></li>
        <li><a href="{c['slug']}.html" aria-current="page">{esc(c['title'])}</a></li>
      </ol>
    </nav>
    <div class="course-detail-grid">
      <div>
        <h1>{esc(c['title'])}</h1>
        <p class="lead">{esc(c['desc'])}</p>
        <img src="../{esc(c['img'])}" alt="{esc(c['title'])}課程封面" width="1280" height="720" style="border-radius:12px; margin-top:20px;">
      </div>
      <div class="course-price-box">
        <div style="display:flex; gap:10px; align-items:baseline; margin-bottom:16px;">
          <span style="font-size:2rem; font-weight:800; color:var(--c-danger);">{price_display}</span>
          {"<span style='font-size:1.1rem; color:var(--c-ink-3); text-decoration:line-through;'>"+orig_display+"</span>" if orig_display else ""}
        </div>
        <button class="btn" style="width:100%; padding:14px; font-size:1rem; margin-bottom:10px;">立即報名</button>
        <button class="btn ghost" style="width:100%;">免費試看第一課</button>
        <hr style="border:0; border-top:1px solid var(--c-line); margin:16px 0;">
        <p class="meta" style="margin:4px 0;">⏱ 總長 {c['duration_hours']} 小時｜{c['lessons']} 堂課</p>
        <p class="meta" style="margin:4px 0;">♾ 購買後終身觀看</p>
        <p class="meta" style="margin:4px 0;">🎓 講師：專業營養師</p>
      </div>
    </div>
  </div>
</section>

<div class="container" id="main" style="padding:30px 20px 60px;">
  <main class="content-main article-body">
    <h2>課程大綱</h2>
{cur_html}    <h2>適合對象</h2>
    <ul>
      <li>想有系統學習營養知識的一般大眾</li>
      <li>需要照顧長輩或家人飲食的照顧者</li>
    </ul>
    <div class="share-bar">
      <strong>分享課程：</strong>
      <button class="share-btn" data-share="fb">Facebook</button>
      <button class="share-btn" data-share="line">Line</button>
      <button class="share-btn" data-copy-link>🔗 複製連結</button>
    </div>
  </main>
</div>

<div class="floating-nav">
  <button class="fab secondary" onclick="location.href='index.html'" title="課程列表">⌂</button>
  <button class="fab" id="fabTop" title="回到頂端">↑</button>
</div>

<footer class="site-footer">
  <div class="container">
    <div class="footer-bottom" style="border:0;margin:0;">
      © {datetime.now().year} 營養與生活｜<a href="index.html" style="display:inline">課程列表</a>
    </div>
  </div>
</footer>

<script src="../assets/js/search-data.js"></script>
<script src="../assets/js/main.js"></script>
</body>
</html>
"""

def main():
    site = load("site.json")
    data = load("courses.json")
    count = 0
    for c in data["courses"]:
        html_path = os.path.join(COURSES_DIR, f"{c['slug']}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(build_course_detail(c, site))
        count += 1
        print(f"  [OK] {c['slug']}.html")
    print(f"\nGenerated {count} course detail pages from data/courses.json")
    print("To add a course: edit data/courses.json, then run python build.py")

if __name__ == "__main__":
    main()

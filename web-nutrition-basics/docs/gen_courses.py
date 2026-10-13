"""Generate 2 more course detail pages."""
import os

BASE = r"D:\WWW\325_pub\自建主題目錄\courses"

COURSES = [
    {
        "file": "style-course-weight.html",
        "h1": "減重不挨餓：熱量赤字實作班",
        "teacher": "李淑貞 營養師（10年執業）",
        "price_sale": "1,980", "price_orig": "3,200",
        "duration": "4.5 小時", "lessons": 6, "students": "2,356",
        "img": "../assets/images/hero-lifestyle.webp",
        "img_alt": "減重課程：藜麥沙拉與綠拿鐵",
        "desc": "不用斷食、不用運到死，21天建立可長期執行的飲食習慣。",
        "curriculum": [
            ("01", "減重唯一真理：熱量赤字", "35 分鐘"),
            ("02", "高飽足感食物清單", "40 分鐘"),
            ("03", "外食族 211 餐盤公式", "45 分鐘"),
            ("04", "吃飯順序：先吃菜再吃肉", "30 分鐘"),
            ("05", "手搖飲代換策略", "25 分鐘"),
            ("06", "真實案例：三個月瘦6公斤", "40 分鐘"),
        ],
    },
    {
        "file": "style-course-basics.html",
        "h1": "21天飲食健檢：營養基礎全攻略",
        "teacher": "林宜慧 營養師（11年執業）",
        "price_sale": "1,680", "price_orig": "2,800",
        "duration": "5 小時", "lessons": 7, "students": "1,534",
        "img": "../assets/images/hero-basics.webp",
        "img_alt": "營養基礎課程：三大營養素食物",
        "desc": "蛋白質、碳水、脂肪、維生素、礦物質，21天一次搞懂。",
        "curriculum": [
            ("01", "三大營養素：身體的建材", "40 分鐘"),
            ("02", "蛋白質要吃多少、怎麼吃", "45 分鐘"),
            ("03", "好澱粉 vs 壞澱粉", "40 分鐘"),
            ("04", "好脂肪：橄欖油、堅果、鮭魚", "35 分鐘"),
            ("05", "維生素：脂溶性 vs 水溶性", "40 分鐘"),
            ("06", "礦物質：鈣鐵鎂鋅", "35 分鐘"),
            ("07", "膳食纖維怎麼吃才夠", "30 分鐘"),
        ],
    },
]

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{h1}｜營養與生活線上課程</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://nutrition.example.com/courses/{file}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:type" content="product">
  <meta property="og:site_name" content="營養與生活">
  <meta property="og:title" content="{h1}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="https://nutrition.example.com/courses/{file}">
  <meta property="og:image" content="https://nutrition.example.com{img}">
  <meta property="og:locale" content="zh_TW">
  <link rel="icon" type="image/svg+xml" href="../assets/images/favicon.svg">
  <link rel="stylesheet" href="../assets/css/style.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Course","name":"{h1}","description":"{desc}","provider":{{"@type":"Organization","name":"營養與生活"}},"offers":{{"@type":"Offer","price":"{price_sale}","priceCurrency":"TWD"}},"hasCourseInstance":{{"@type":"CourseInstance","courseMode":"online"}}}}
  </script>
</head>
<body>
<a class="skip-link" href="#main">跳至主內容</a>
<header class="site-header">
  <div class="header-bar">
    <a class="brand" href="../index.html">
      <svg class="brand-mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#1f7a4d"/><path d="M32 14 C22 24 18 34 22 44 C26 54 38 56 44 48 C50 40 46 28 32 14 Z" fill="#fff"/></svg>
      <span>營養與生活<small>NUTRITION &amp; LIFE</small></span>
    </a>
    <div class="search-wrap">
      <div class="search-box">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6b7c72" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
        <input type="search" id="siteSearch" placeholder="搜尋營養知識…" aria-label="全站搜尋">
      </div>
      <div class="autocomplete" id="acBox"></div>
    </div>
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
        <li><a href="{file}" aria-current="page">{h1}</a></li>
      </ol>
    </nav>
    <div class="course-detail-grid">
      <div>
        <h1>{h1}</h1>
        <p class="lead">{desc}</p>
        <img src="{img}" alt="{img_alt}" width="1280" height="720" style="border-radius:12px; margin-top:20px;">
      </div>
      <div class="course-price-box">
        <div style="display:flex; gap:10px; align-items:baseline; margin-bottom:16px;">
          <span style="font-size:2rem; font-weight:800; color:var(--c-danger);">NT${price_sale}</span>
          <span style="font-size:1.1rem; color:var(--c-ink-3); text-decoration:line-through;">NT${price_orig}</span>
        </div>
        <button class="btn" style="width:100%; padding:14px; font-size:1rem; margin-bottom:10px;">立即報名</button>
        <button class="btn ghost" style="width:100%;">免費試看第一課</button>
        <hr style="border:0; border-top:1px solid var(--c-line); margin:16px 0;">
        <p class="meta" style="margin:4px 0;">👥 已有 <strong>{students}</strong> 人報名</p>
        <p class="meta" style="margin:4px 0;">⏱ 總長 {duration}｜{lessons} 堂課</p>
        <p class="meta" style="margin:4px 0;">♾ 購買後終身觀看</p>
        <p class="meta" style="margin:4px 0;">🎓 講師：{teacher}</p>
      </div>
    </div>
  </div>
</section>

<div class="container" id="main" style="padding:30px 20px 60px;">
  <main class="content-main article-body">
    <h2>課程大綱</h2>
{curriculum_html}
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
      © <span id="yr">2026</span> 營養與生活｜<a href="index.html" style="display:inline">課程列表</a>
    </div>
  </div>
</footer>

<script src="../assets/js/search-data.js"></script>
<script src="../assets/js/main.js"></script>
</body>
</html>
"""

for c in COURSES:
    cur = ""
    for num, title, dur in c["curriculum"]:
        cur += f'      <div class="curriculum-item">\n        <div><span class="lesson-num">{num}</span>{title}</div>\n        <span class="lesson-duration">{dur}</span>\n      </div>\n'
    html = TEMPLATE.format(
        h1=c["h1"], desc=c["desc"], file=c["file"], img=c["img"],
        img_alt=c["img_alt"], price_sale=c["price_sale"], price_orig=c["price_orig"],
        duration=c["duration"], lessons=c["lessons"], students=c["students"],
        teacher=c["teacher"], curriculum_html=cur,
    )
    with open(os.path.join(BASE, c["file"]), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created: {c['file']}")

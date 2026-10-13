"""Generate 10 style-xxx.html article pages from a shared template."""
import os

BASE = r"D:\WWW\325_pub\自建主題目錄"

# 每篇文章的資料
articles = [
    {
        "folder": "nutrition-basics", "file": "style-protein.html",
        "h1": "蛋白質完整指南：一天要吃多少、怎麼吃才吸收好",
        "topic": "營養基礎", "topic_url": "../index.html", "topic_folder": "index.html",
        "img": "../assets/images/hero-basics.webp",
        "img_alt": "蛋白質食物來源：雞胸、鮭魚、豆腐",
        "tags": "蛋白質, 肌肉, 胺基酸",
        "desc": "蛋白質每日需求、完全蛋白與不完全蛋白、植物性蛋白選擇、運動後補充時機。",
        "sections": [
            ("s1", "一、蛋白質是什麼？為什麼不能少", "蛋白質由 20 種胺基酸組成，其中 9 種是必需胺基酸，人體無法自製，必須從食物取得。長期蛋白質不足會導致肌肉流失、免疫力下降、傷口癒合慢、掉髮。"),
            ("s2", "二、一天到底要吃多少？", "一般成人每公斤體重 0.8–1.0 g。60 kg 的人一天 48–60 g。銀髮族提高到 1.2–1.6 g/kg。運動員 1.4–2.0 g/kg。懷孕後期每天多 15–25 g。"),
            ("s3", "三、動物性 vs 植物性蛋白", "動物性（肉、魚、蛋、奶）是完全蛋白，胺基酸模式完整。植物性（黃豆、黑豆、毛豆、豆腐）也屬完全蛋白；大多數穀類與豆類互補可提高品質。"),
            ("s4", "四、真實案例", "70 歲王阿公長期吃素，每天只吃一碗飯配豆腐。體檢發現白蛋白過低、小腿無力。營養師建議每天加 1 個蛋＋1 杯無糖豆漿，三個月後體力明顯改善。"),
        ],
    },
    {
        "folder": "nutrition-basics", "file": "style-vitamin.html",
        "h1": "維生素全攻略：脂溶性 vs 水溶性，哪些要補哪些不用",
        "topic": "營養基礎", "topic_url": "../index.html", "topic_folder": "index.html",
        "img": "../assets/images/hero-basics.webp",
        "img_alt": "新鮮蔬菜與水果提供維生素",
        "tags": "維生素, 抗氧化, 補充劑",
        "desc": "脂溶性維生素 A/D/E/K 會累積，水溶性 B/C 過量隨尿排出。哪些人需要額外補充？",
        "sections": [
            ("s1", "一、兩大類維生素的差異", "脂溶性（A、D、E、K）溶於油脂，可儲存在肝臟與脂肪組織，過量有毒性。水溶性（B 群、C）溶於水，過量隨尿液排出，較安全但仍不應濫補。"),
            ("s2", "二、維生素 D：現代人最常缺", "維生素 D 協助鈣吸收、免疫調節。日曬 15 分鐘是人體合成來源。室內工作者、老年人、黑皮膚者容易不足。冬天可考慮補充 800–2000 IU。"),
            ("s3", "三、維生素 B 群：能量代謝", "B1、B2、B6、B12 參與能量代謝。壓力大、喝酒多、吃素者容易缺 B12。食物來源：全穀、瘦肉、深綠菜、蛋、奶。"),
            ("s4", "四、真實案例", "35 歲工程師長期熬夜、手搖飲每天一杯。自覺疲倦、口角炎。抽血發現 B12 偏低。改成早餐吃蛋＋全麥土司、少喝手搖飲，兩個月後症狀改善。"),
        ],
    },
    {
        "folder": "diet-disease", "file": "style-diabetes.html",
        "h1": "糖尿病飲食完整指南：低GI、低醣、外食怎麼點",
        "topic": "飲食與疾病", "topic_url": "../index.html", "topic_folder": "index.html",
        "img": "../assets/images/hero-disease.webp",
        "img_alt": "均衡餐盤：蔬菜、全穀、蛋白質",
        "tags": "糖尿病, 低GI, 血糖",
        "desc": "糖尿病患的飲食原則、低GI食物清單、外食組合、水果選擇。",
        "sections": [
            ("s1", "一、糖尿病飲食不是不能吃飯", "重點是讓血糖不要像溜滑梯。低 GI（GI<55）食物升糖慢、有飽足感。白飯改成糙米、白土司改成全麥，血糖波動立刻減半。"),
            ("s2", "二、低GI食物清單", "主食：糙米、燕麥、地瓜、藜麥。水果：芭樂、小番茄、蘋果、莓果。避免：西瓜、荔枝、芒果、果汁、蛋糕。"),
            ("s3", "三、外食怎麼點", "211 餐盤：2 份蔬菜、1 份蛋白質、1 份澱粉。選擇滷、烤、蒸，避開炸、勾芡。不喝湯底、不喝果汁。"),
            ("s4", "四、真實案例", "52 歲林先生飯後血糖常達 200 mg/dL。營養師建議把早餐珍珠奶茶換成無糖茶＋蛋三明治，午餐便當白飯減半加燙青菜。一個月後飯後血糖降到 140。"),
        ],
    },
    {
        "folder": "diet-disease", "file": "style-hypertension.html",
        "h1": "高血壓減鈉實戰：隱形鈉地雷與高鉀食物",
        "topic": "飲食與疾病", "topic_url": "../index.html", "topic_folder": "index.html",
        "img": "../assets/images/hero-disease.webp",
        "img_alt": "低鈉餐盤與被劃掉的鹽罐",
        "tags": "高血壓, 減鈉, 高鉀",
        "desc": "高血壓飲食的減鈉策略、隱形鈉食物表、高鉀食物幫助排鈉。",
        "sections": [
            ("s1", "一、減鈉不是炒菜少放鹽", "台灣人一天鈉攝取平均 4000–5000 mg，建議 2400 mg 以下。外食族一餐泡麵湯就超過 1500 mg。重點是避開隱形鈉。"),
            ("s2", "二、隱形鈉地雷", "醬油 1 大匙 900 mg、加工肉品 500–800 mg、沙茶醬 1 大匙 500 mg、運動飲料一瓶 300 mg、泡麵湯底 1500 mg。"),
            ("s3", "三、高鉀食物幫助排鈉", "鉀可以促進鈉排出。來源：香蕉、菠菜、蕃茄、馬鈴薯、地瓜、鱷梨。腎功能不佳者需醫師評估。"),
            ("s4", "四、真實案例", "60 歲陳阿姨血壓 160/95，每天洗腎習慣喝湯。改成不喝湯、沾醬分開裝、每天一根香蕉。兩個月後血壓降到 140/85。"),
        ],
    },
    {
        "folder": "life-stage", "file": "style-senior.html",
        "h1": "銀髮族營養：預防肌少症的蛋白質與運動搭配",
        "topic": "各族群營養", "topic_url": "../index.html", "topic_folder": "index.html",
        "img": "../assets/images/hero-lifestage.webp",
        "img_alt": "銀髮長者在家用餐",
        "tags": "銀髮族, 肌少症, 蛋白質",
        "desc": "銀髮族肌肉流失速度、蛋白質需求、牙口不好的替代方案、阻力運動搭配。",
        "sections": [
            ("s1", "一、為什麼銀髮族要多吃蛋白質", "30 歲後肌肉每十年流失 3–8%，70 歲後更快。蛋白質合成效率下降，需要比年輕人更多蛋白質才能維持肌肉。"),
            ("s2", "二、每餐 25–30g 蛋白質", "研究顯示每餐攝取 25–30 g 蛋白質最能刺激肌肉合成。早餐吃蛋＋牛奶＋黃豆，不要只有稀飯配醬菜。"),
            ("s3", "三、牙口不好怎麼辦", "蒸蛋、豆花、魚鬆、豆腐、泥狀堅果醬、切成小塊的肉。必要時使用營養補充品（如均衡配方奶）。"),
            ("s4", "四、真實案例", "75 歲趙伯伯體重 50 kg、握力變差。改成每天 2 杯牛奶＋1 個蛋＋豆腐，加上每週 2 次舉寶特瓶。半年後握力提升、上下樓梯不喘。"),
        ],
    },
    {
        "folder": "life-stage", "file": "style-pregnant.html",
        "h1": "孕婦營養：葉酸、鐵、DHA 什麼時候補",
        "topic": "各族群營養", "topic_url": "../index.html", "topic_folder": "index.html",
        "img": "../assets/images/hero-lifestage.webp",
        "img_alt": "孕婦喝牛奶補充營養",
        "tags": "孕婦, 葉酸, 鐵, DHA",
        "desc": "懷孕三期的營養重點、葉酸補充時機、鐵劑與鈣劑如何配、DHA 食物來源。",
        "sections": [
            ("s1", "一、前期（0–12 週）：葉酸最重要", "懷孕前期每天 400 μg 葉酸，預防胎兒神經管缺陷。來源：深綠色蔬菜、豆類、營養強化穀物。戒酒精、生食。"),
            ("s2", "二、中期（13–27 週）：熱量與鐵", "熱量 +350 kcal、鐵 15 mg、鈣 1000 mg。體重開始成長。鐵劑配維生素 C 吸收更好。"),
            ("s3", "三、後期（28 週後）：DHA", "熱量 +450 kcal、DHA 200 mg。每週吃 2 次深海魚（鮭魚、鯖魚）。避免大型魚（鮪魚、鯊魚）以防汞污染。"),
            ("s4", "四、真實案例", "28 歲孕婦初期嚴重孕吐，只吃白吐司。營養師建議少量多餐、補充 B6、電解質水。第二個月食慾恢復後開始補充葉酸與鐵劑。"),
        ],
    },
    {
        "folder": "food-guide", "file": "style-label.html",
        "h1": "營養標示解讀：60 秒看懂每日參考值",
        "topic": "食材與標示", "topic_url": "../index.html", "topic_folder": "index.html",
        "img": "../assets/images/hero-food.webp",
        "img_alt": "手拿優格看營養標示",
        "tags": "營養標示, 每日參考值, 食品標示",
        "desc": "營養標示的份量、熱量、%每日參考值怎麼看。超市購物實用技巧。",
        "sections": [
            ("s1", "一、第一步：看份量", "標示是「每份」還是「每100g」。一包洋芋片可能是 3 份，熱量要乘 3。"),
            ("s2", "二、第二步：看熱量", "一份超過 300 kcal 就是高熱量。飲料類 100 ml 超過 60 kcal 就是甜飲。"),
            ("s3", "三、第三步：看%每日參考值", "<5% 低、5–20% 中、>20% 高。鈉超過 20% 代表一份吃掉一天 1/5 的鹽。"),
            ("s4", "四、真實案例", "30 歲小華以為優格健康，每天喝一杯。看標示發現每杯糖 18 g（佔每日 36%）。改成無糖優格加新鮮水果，糖攝取立刻減半。"),
        ],
    },
    {
        "folder": "food-guide", "file": "style-superfood.html",
        "h1": "超級食物真實 CP 值：哪些值得買、哪些是行銷",
        "topic": "食材與標示", "topic_url": "../index.html", "topic_folder": "index.html",
        "img": "../assets/images/hero-food.webp",
        "img_alt": "藜麥、杏仁、奇亞籽",
        "tags": "超級食物, 藜麥, 藍莓, CP值",
        "desc": "藜麥、藍莓、酪梨、奇亞籽、燕麥的真實營養價格與性價比。",
        "sections": [
            ("s1", "一、超級食物不是萬靈丹", "營養價值高，但不是神藥。均衡飲食比單吃一種超級食物重要。"),
            ("s2", "二、CP 值排行榜", "燕麥（β-聚葡萄糖降膽固醇，最便宜）★★★★★；奇亞籽（Omega-3、纖維）★★★★；藜麥（完全蛋白）★★★★；冷凍藍莓（抗氧化物）★★★；酪梨（好脂肪）★★。"),
            ("s3", "三、哪些是行銷話術", "機能飲料、排毒果汁、酵素飲——價格高但營養不如原型食物。"),
            ("s4", "四、真實案例", "40 歲王先生花 2000 元買各種超級食物粉。營養師建議改成每天一碗燕麥＋一把堅果＋一份藍莓，一個月省 1500 元，膽固醇還降了。"),
        ],
    },
    {
        "folder": "lifestyle", "file": "style-weight.html",
        "h1": "減重不挨餓：熱量赤字與飽足感食物",
        "topic": "生活型態", "topic_url": "../index.html", "topic_folder": "index.html",
        "img": "../assets/images/hero-lifestyle.webp",
        "img_alt": "藜麥沙拉與綠拿鐵",
        "tags": "減重, 熱量赤字, 飽足感",
        "desc": "減重的熱量赤字原理、高飽足感食物清單、外食策略、常見錯誤。",
        "sections": [
            ("s1", "一、減重唯一真理：熱量赤字", "消耗 > 攝取。一天少 300–500 kcal，一週減 0.5 kg 是健康速度。不要節食到基礎代謝以下。"),
            ("s2", "二、高飽足感食物", "蛋白質（肌肉合成、食物熱效應高）、膳食纖維（延長胃排空）、水（餐前喝水減少食量）。"),
            ("s3", "三、吃飯順序", "喝湯 → 蔬菜 → 蛋白質 → 澱粉。研究顯示自然少吃 20% 熱量。"),
            ("s4", "四、真實案例", "35 歲工程師 88 kg，不節食不運動，只改「不喝手搖飲＋先吃菜再吃肉最後吃飯」。三個月瘦 6 kg，體脂降 3%。"),
        ],
    },
    {
        "folder": "lifestyle", "file": "style-fasting.html",
        "h1": "168 斷食完整指南：適合誰、不適合誰、怎麼開始",
        "topic": "生活型態", "topic_url": "../index.html", "topic_folder": "index.html",
        "img": "../assets/images/hero-lifestyle.webp",
        "img_alt": "計時器與健康食物",
        "tags": "斷食, 168, 減重",
        "desc": "168 斷食的原理、執行方法、適合族群、不適合族群、常見問題。",
        "sections": [
            ("s1", "一、168 是什麼", "一天 24 小時中，8 小時進食（如 12:00–20:00）、16 小時禁食。自然縮小進食視窗，降低熱量。"),
            ("s2", "二、為什麼會紅", "研究顯示 168 可改善胰島素敏感性、血壓、發炎指標。但只要熱量赤字相同，減重效果和傳統節食差不多。"),
            ("s3", "三、不適合誰", "孕婦、哺乳、青少年、糖尿病用藥者、胃潰瘍、有進食疾患傾向、營養不良者。"),
            ("s4", "四、真實案例", "45 歲王小姐體重 70 kg，採 12:00–20:00 進食，一天 1500 kcal。三個月減重 8 kg，空腹血糖從 110 降到 95。"),
        ],
    },
]

# HTML 範本
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{h1}｜營養與生活</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://nutrition.example.com/{folder}/{file}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="營養與生活">
  <meta property="og:title" content="{h1}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="https://nutrition.example.com/{folder}/{file}">
  <meta property="og:image" content="https://nutrition.example.com{img}">
  <meta property="og:locale" content="zh_TW">
  <link rel="icon" type="image/svg+xml" href="../assets/images/favicon.svg">
  <link rel="stylesheet" href="../assets/css/style.css">

  <!-- ItemList Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": [
{{itemlist_items}}
    ]
  }}
  </script>
  <!-- ImageObject Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ImageObject",
    "url": "https://nutrition.example.com{img}",
    "contentUrl": "https://nutrition.example.com{img}",
    "caption": "{img_alt}"
  }}
  </script>
  <!-- BreadcrumbList -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type":"ListItem","position":1,"name":"首頁","item":"https://nutrition.example.com/"}},
      {{"@type":"ListItem","position":2,"name":"{topic}","item":"https://nutrition.example.com/{folder}/"}},
      {{"@type":"ListItem","position":3,"name":"{h1}","item":"https://nutrition.example.com/{folder}/{file}"}}
    ]
  }}
  </script>
</head>
<body>
<a class="skip-link" href="#main">跳至主內容</a>

<!-- 公告列 -->
<div class="announce-bar">
  2026 全新改版｜營養知識庫全面升級
  <button class="announce-close" aria-label="關閉公告">×</button>
</div>

<header class="site-header">
  <div class="header-bar">
    <a class="brand" href="../index.html">
      <svg class="brand-mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#1f7a4d"/><path d="M32 14 C22 24 18 34 22 44 C26 54 38 56 44 48 C50 40 46 28 32 14 Z" fill="#fff"/></svg>
      <span>營養與生活<small>NUTRITION & LIFE</small></span>
    </a>
    <div class="search-wrap">
      <div class="search-box">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6b7c72" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
        <input type="search" id="siteSearch" placeholder="搜尋營養知識…" aria-label="全站搜尋">
      </div>
      <div class="autocomplete" id="acBox"></div>
    </div>
    <button class="theme-toggle" id="themeToggle" title="深色模式" aria-label="切換深色模式">☾</button>
    <div class="font-controls">
      <button class="font-btn" data-font="sm" title="小字級">A-</button>
      <button class="font-btn" data-font="md" title="預設字級">A</button>
      <button class="font-btn" data-font="lg" title="大字級">A+</button>
    </div>
    <button class="nav-toggle" aria-label="開啟選單">☰</button>
    <nav class="main-nav" id="mainNav" aria-label="主導覽">
      <div class="nav-item"><a class="nav-link" href="../index.html">首頁</a></div>
      <div class="nav-item"><a class="nav-link" href="../nutrition-basics/index.html">營養基礎</a></div>
      <div class="nav-item"><a class="nav-link" href="../diet-disease/index.html">飲食與疾病</a></div>
      <div class="nav-item"><a class="nav-link" href="../life-stage/index.html">各族群營養</a></div>
      <div class="nav-item"><a class="nav-link" href="../food-guide/index.html">食材與標示</a></div>
      <div class="nav-item"><a class="nav-link" href="../lifestyle/index.html">生活型態</a></div>
    </nav>
  </div>
</header>

<div class="container" id="main" style="padding-top:20px;">
  <nav class="breadcrumb" aria-label="麵包屑">
    <ol>
      <li><a href="../index.html">首頁</a></li>
      <li><a href="{topic_folder}">{topic}</a></li>
      <li><a href="{file}" aria-current="page">本文</a></li>
    </ol>
  </nav>

  <div class="layout">
    <main class="content-main article-body">
      <h1>{h1}</h1>
      <div class="article-meta">
        <span>📖 <span id="readTime">約 3 分鐘</span></span>
        <span>📝 <span id="wordCount">0 字</span></span>
        <span>🏷️ {tags}</span>
      </div>

      <img src="{img}" alt="{img_alt}" width="1280" height="720" loading="lazy" class="article-img">

{sections_html}

      <!-- 社交分享 -->
      <div class="share-bar">
        <strong>分享本文：</strong>
        <button class="share-btn" data-share="fb">Facebook</button>
        <button class="share-btn" data-share="line">Line</button>
        <button class="share-btn" data-share="twitter">X / Twitter</button>
        <button class="share-btn" data-share="email">Email</button>
        <button class="share-btn" data-copy-link>🔗 複製連結</button>
        <button class="share-btn" data-print>🖨️ 列印</button>
      </div>

      <div class="bookmark-bar">
        <div><strong>收藏本文</strong>：隨時回來看</div>
        <button class="btn ghost" data-bookmark="{folder}/{file}">☆ 收藏</button>
      </div>

      <h2>相關文章</h2>
      <div class="related-list">
        <a class="related-item" href="../nutrition-basics/index.html"><h4>營養基礎總覽</h4><p>回到主題首頁</p></a>
        <a class="related-item" href="../diet-disease/index.html"><h4>飲食與疾病</h4><p>相關主題</p></a>
        <a class="related-item" href="../life-stage/index.html"><h4>各族群營養</h4><p>相關主題</p></a>
      </div>
    </main>

    <aside class="sidebar">
      <div class="side-box">
        <h3>本文目錄</h3>
        <ul class="toc-list">
{toc_items}
        </ul>
      </div>
      <div class="side-box">
        <h3>最近瀏覽</h3>
        <ul class="recent-list" id="recentList"><li class="meta">載入中…</li></ul>
      </div>
      <div class="side-box">
        <h3>標籤</h3>
        <div class="tag-cloud">
{tag_items}
        </div>
      </div>
    </aside>
  </div>
</div>

<div class="floating-nav">
  <button class="fab secondary" onclick="location.href='../index.html'" title="回首頁">⌂</button>
  <button class="fab" id="fabTop" title="回到頂端">↑</button>
</div>

<footer class="site-footer">
  <div class="container">
    <div class="footer-bottom" style="border:0;margin:0;">
      © <span id="yr">2026</span> 營養與生活｜<a href="../index.html" style="display:inline">回首頁</a>｜本文為 {topic} 主題文章
    </div>
  </div>
</footer>

<script src="../assets/js/search-data.js"></script>
<script src="../assets/js/main.js"></script>
</body>
</html>
"""

for a in articles:
    sections_html = ""
    toc_items = ""
    itemlist_items = ""
    for i, (sid, title, body) in enumerate(a["sections"]):
        sections_html += f'      <h2 id="{sid}">{title}</h2>\n      <p>{body}</p>\n'
        toc_items += f'          <li><a href="#{sid}">{title[:20]}</a></li>\n'
        itemlist_items += f'        {{"@type":"ListItem","position":{i+1},"name":"{title}","url":"https://nutrition.example.com/{a["folder"]}/{a["file"]}#{sid}"}}'
        if i < len(a["sections"]) - 1:
            itemlist_items += ",\n"

    tag_items = ""
    for tag in a["tags"].split(", "):
        tag_items += f'          <a class="tag" href="#">{tag}</a>\n'

    html = TEMPLATE.format(
        h1=a["h1"], desc=a["desc"], folder=a["folder"], file=a["file"],
        topic=a["topic"], topic_folder=a["topic_folder"],
        img=a["img"], img_alt=a["img_alt"], tags=a["tags"],
        sections_html=sections_html, toc_items=toc_items,
        itemlist_items=itemlist_items, tag_items=tag_items,
    )

    outpath = os.path.join(BASE, a["folder"], a["file"])
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Created: {a['folder']}/{a['file']} ({len(html)//1024}KB)")

print(f"\nDone. {len(articles)} article pages generated.")

"""Expand courses.json to 24 courses and regenerate all pages."""
import json, os, random

ROOT = r"D:\WWW\325_pub\自建主題目錄"
DATA = os.path.join(ROOT, "data")

TEACHERS = [
    ("張建國", 12), ("李淑貞", 10), ("林宜慧", 11), ("王美玲", 15),
    ("陳建宏", 8), ("趙雅芬", 9), ("黃郁婷", 7), ("吳柏翰", 13),
]

CATEGORIES = ["disease", "weight", "stage", "food", "lifestyle"]

COURSE_TITLES = [
    "糖尿病低GI飲食實戰班", "減重不挨餓：熱量赤字", "21天飲食健檢",
    "銀髮族防肌少飲食", "超市購物攻略", "備孕孕期營養",
    "高血壓減鈉實戰", "腸道保健與益生菌", "痛風低普林飲食",
    "高血脂飲食管理", "兒童成長營養", "更年期飲食調理",
    "運動員增肌飲食", "外食族211餐盤", "手搖飲代換指南",
    "素食蛋白質攻略", "低鐵貧血飲食", "過敏兒營養調理",
    "脂肪肝逆轉飲食", "半夜偷吃剋星", "減醣168斷食",
    "胃食道逆流飲食", "骨質疏鬆補鈣", "便秘膳食纖維實戰",
]

IMAGES = [
    "assets/images/hero-disease.webp", "assets/images/hero-lifestyle.webp",
    "assets/images/hero-basics.webp", "assets/images/hero-lifestage.webp",
    "assets/images/hero-food.webp", "assets/images/hero-home.webp",
]

DESCRIPTIONS = [
    "8堂課教你觀念落地，外食族也能執行。",
    "不用斷食不用運到死，建立可長期的飲食習慣。",
    "三大營養素一次搞懂，看完就知道三餐怎麼配。",
    "為長輩打造：蛋白質、鈣質、牙口問題全解答。",
    "60秒看懂營養標示，買對不買貴。",
    "從備孕到哺乳，關鍵營養素什麼時候補。",
    "隱形鈉地雷、高鉀食物、外食點餐公式。",
    "益生菌怎麼挑、什麼時候吃、什麼時候不用吃。",
    "認識普林、哪些食物要節制、真實案例。",
    "壞膽固醇怎麼降、好油脂怎麼選。",
    "成長期蛋白質、鈣、DHA的關鍵角色。",
    "熱潮紅、失眠、骨質疏鬆的飲食對策。",
    "增肌期蛋白質攝取、訓練前後飲食。",
    "便當、超商、火鍋、壽司實戰點餐。",
    "手搖飲熱量地圖、低卡代換清單。",
    "素食者蛋白質來源、胺基酸互補。",
    "鐵質吸收、維生素C助攻、正餐安排。",
    "食物過敏、異位性皮膚炎的飲食調理。",
    "脂肪肝怎麼吃、多少运动才夠。",
    "半夜想吃東西的心理與生理對策。",
    "168斷食的正確做法、常見錯誤。",
    "戒夜食、胃排空、低刺激食物清單。",
    "鈣質吸收率、維生素D、日常補鈣食物。",
    "膳食纖維怎麼吃、喝水量、益生菌搭配。",
]

random.seed(42)
courses = []
for i in range(24):
    teacher, years = TEACHERS[i % len(TEACHERS)]
    category = CATEGORIES[i % len(CATEGORIES)]
    price_orig = random.choice([2000, 2800, 3200, 3800, 4500])
    price_sale = int(price_orig * random.choice([0.55, 0.6, 0.65, 0.7]))
    duration = random.choice([2, 3, 4, 4.5, 5, 6])
    lessons = int(duration * 1.5)
    students = random.randint(120, 3500)
    progress = round(students / 10, -1)
    img = IMAGES[i % len(IMAGES)]
    slug = f"style-course-{i+1:02d}" if i >= 4 else [
        "style-course-diabetes", "style-course-weight", "style-course-basics",
        "style-course-senior"
    ][i]
    badge = random.choice(["熱賣", "限時優惠", "新人優惠", "熱門"])
    if i == 3:
        badge = "免費試聽"
        price_sale = 0

    curriculum = []
    for j in range(1, lessons+1):
        cur_titles = [
            "觀念建立與常見迷思", "實戰食物清單", "外食點餐公式",
            "真實案例解析", "常見問題 Q&A", "進階應用",
        ]
        curriculum.append([f"{j:02d}", cur_titles[j % len(cur_titles)], f"{random.randint(25,50)} 分鐘"])

    courses.append({
        "slug": slug,
        "title": COURSE_TITLES[i],
        "teacher": teacher,
        "teacher_years": years,
        "category": category,
        "price_sale": price_sale,
        "price_orig": price_orig,
        "duration_hours": duration,
        "lessons": lessons,
        "students": students,
        "progress_pct": int(progress),
        "badge": badge,
        "img": img,
        "desc": DESCRIPTIONS[i],
        "curriculum": curriculum,
    })

data = {
    "categories": [
        {"id": "all", "label": "全部課程"},
        {"id": "disease", "label": "疾病飲食"},
        {"id": "weight", "label": "體重管理"},
        {"id": "stage", "label": "族群營養"},
        {"id": "food", "label": "食材應用"},
        {"id": "lifestyle", "label": "生活型態"},
    ],
    "courses": courses,
}

with open(os.path.join(DATA, "courses.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"courses.json: {len(courses)} courses written")

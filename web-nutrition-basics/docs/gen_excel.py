"""Generate two Excel deliverables for the 營養與生活 site."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = r"D:\WWW\325_pub\自建主題目錄\docs"

HEADER_FILL = PatternFill("solid", fgColor="1F7A4D")
HEADER_FONT = Font(name="Microsoft JhengHei", bold=True, color="FFFFFF", size=11)
BODY_FONT = Font(name="Microsoft JhengHei", size=10)
THIN = Side(style="thin", color="D8E2DC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

def style_sheet(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = BODY_FONT
            cell.alignment = WRAP
            cell.border = BORDER
    ws.row_dimensions[1].height = 28

# ============================================================
# 1. 網站地圖.xlsx
# ============================================================
wb1 = openpyxl.Workbook()
ws1 = wb1.active
ws1.title = "網站地圖"
headers1 = ["序號", "頁面 URL", "頁面標題 (Title)", "Meta Description", "主題叢集",
            "JSON-LD 類型", "標籤", "Lastmod", "優先權", "收錄狀態"]
ws1.append(headers1)

rows1 = [
    [1, "/index.html", "營養與生活｜2026 大白話營養知識庫",
     "權威級繁體中文營養知識庫：三大營養素到疾病飲食一次看懂。", "首頁",
     "WebSite, Organization, FAQPage", "首頁, 總覽", "2026-10-13", "1.0", "index"],
    [2, "/nutrition-basics/index.html", "營養基礎｜蛋白質碳水脂肪維生素礦物質",
     "三大營養素每日需求；水溶性與脂溶性維生素差異；鈣鐵鎂鋅不足症狀。", "營養基礎",
     "BreadcrumbList, Article, FAQPage", "營養素, 維生素, 礦物質, 纖維", "2026-10-13", "0.9", "index"],
    [3, "/diet-disease/index.html", "飲食與疾病｜糖尿病高血壓高血脂痛風",
     "低GI食物、減鈉作法、好油壞油、高普林食物避開表。", "飲食與疾病",
     "BreadcrumbList, Article, FAQPage", "糖尿病, 高血壓, 高血脂, 痛風", "2026-10-13", "0.9", "index"],
    [4, "/life-stage/index.html", "各族群營養｜兒童孕婦銀髮族運動員",
     "兒童鈣與蛋白質、孕婦葉酸鐵、銀髮族防肌少、運動員補給時機。", "各族群營養",
     "BreadcrumbList, Article, FAQPage", "兒童, 孕婦, 銀髮族, 運動員", "2026-10-13", "0.9", "index"],
    [5, "/food-guide/index.html", "食材與標示｜營養標示超級食物加工食品",
     "每日參考值%、超級食物CP值、加工食品避雷、食物搭配。", "食材與標示",
     "BreadcrumbList, Article, FAQPage", "營養標示, 超級食物, 加工食品", "2026-10-13", "0.9", "index"],
    [6, "/lifestyle/index.html", "生活型態飲食｜減重斷食外食睡眠腸道",
     "熱量赤字、168斷食、外食211公式、睡眠與食慾、益生菌。", "生活型態",
     "BreadcrumbList, Article, FAQPage", "減重, 斷食, 外食, 睡眠, 腸道", "2026-10-13", "0.9", "index"],
    [7, "/about.html", "關於我們｜編輯方針", "網站定位、內容審查機制、聯絡方式。", "關於",
     "—", "關於", "2026-10-13", "0.5", "index"],
    [8, "/404.html", "404 找不到頁面", "—", "工具頁", "—", "—", "2026-10-13", "0.0", "noindex"],
]
for r in rows1:
    ws1.append(r)
style_sheet(ws1, [6, 32, 36, 40, 14, 30, 24, 12, 8, 10])
wb1.save(OUT + r"\網站地圖.xlsx")
print("Saved 網站地圖.xlsx")

# ============================================================
# 2. 網站變數與網站導覽表.xlsx
# ============================================================
wb2 = openpyxl.Workbook()

# Sheet A: 網站變數
ws2 = wb2.active
ws2.title = "網站變數"
ws2.append(["變數名稱", "值", "說明"])
vars_rows = [
    ["SITE_NAME", "營養與生活", "網站名稱"],
    ["SITE_URL", "https://nutrition.example.com", "正式網域（部署時替換）"],
    ["LOCALE", "zh_TW", "語系"],
    ["ENCODING", "UTF-8", "編碼"],
    ["OG_IMAGE_DEFAULT", "/assets/images/hero-home.webp", "預設 OG 圖"],
    ["FAVICON", "/assets/images/favicon.svg", "Favicon"],
    ["THEME_COLOR", "#1f7a4d", "主色"],
    ["TECH_STACK", "HTML5 + CSS3 + Vanilla JS", "技術棧（無框架）"],
    ["SEARCH_INDEX", "/assets/js/search-data.js", "全站搜尋索引"],
    ["MAIN_JS", "/assets/js/main.js", "共享 JS"],
    ["STYLE_CSS", "/assets/css/style.css", "共享 CSS"],
    ["SITEMAP", "/sitemap.xml", "Sitemap 位置"],
    ["ROBOTS", "/robots.txt", "robots.txt"],
    ["MANIFEST", "/manifest.json", "Web App Manifest"],
    ["CONTACT_EMAIL", "（部署時填入）", "聯絡信箱"],
]
for r in vars_rows:
    ws2.append(r)
style_sheet(ws2, [22, 38, 40])

# Sheet B: 網站導覽 (MegaMenu)
ws3 = wb2.create_sheet("網站導覽")
ws3.append(["主選單", "連結", "第二層選單", "第二層連結", "錨點"])
nav_rows = [
    ["首頁", "/index.html", "—", "—", "—"],
    ["營養基礎", "/nutrition-basics/index.html", "巨量營養素", "/nutrition-basics/index.html", "#protein / #carbs / #fat"],
    ["營養基礎", "/nutrition-basics/index.html", "微量營養素", "/nutrition-basics/index.html", "#vitamin / #mineral / #fiber"],
    ["飲食與疾病", "/diet-disease/index.html", "代謝疾病", "/diet-disease/index.html", "#diabetes / #hypertension / #lipid"],
    ["飲食與疾病", "/diet-disease/index.html", "發炎與代謝", "/diet-disease/index.html", "#gout / #allergy"],
    ["各族群營養", "/life-stage/index.html", "成長與生命期", "/life-stage/index.html", "#child / #pregnant"],
    ["各族群營養", "/life-stage/index.html", "熟齡與運動", "/life-stage/index.html", "#senior / #athlete"],
    ["食材與標示", "/food-guide/index.html", "標示解讀", "/food-guide/index.html", "#label / #superfood"],
    ["食材與標示", "/food-guide/index.html", "食材避雷", "/food-guide/index.html", "#processed / #pairing"],
    ["生活型態", "/lifestyle/index.html", "—", "—", "#weight / #fasting / #eatingout / #sleep / #gut"],
    ["關於我們", "/about.html", "—", "—", "—"],
]
for r in nav_rows:
    ws3.append(r)
style_sheet(ws3, [14, 32, 16, 32, 30])

# Sheet C: Tag 標籤清單
ws4 = wb2.create_sheet("標籤清單")
ws4.append(["標籤", "出現頁面", "用途"])
tag_rows = [
    ["蛋白質", "營養基礎, 銀髮族, 運動員", "主題分類"],
    ["碳水", "營養基礎, 糖尿病", "主題分類"],
    ["維生素", "營養基礎", "主題分類"],
    ["糖尿病", "飲食與疾病, 生活型態", "疾病標籤"],
    ["高血壓", "飲食與疾病, 食材標示", "疾病標籤"],
    ["痛風", "飲食與疾病", "疾病標籤"],
    ["孕婦", "各族群營養", "族群標籤"],
    ["銀髮族", "各族群營養, 生活型態", "族群標籤"],
    ["減重", "生活型態", "生活型態標籤"],
    ["斷食", "生活型態, 糖尿病", "生活型態標籤"],
    ["營養標示", "食材與標示", "實用標籤"],
    ["超級食物", "食材與標示", "實用標籤"],
]
for r in tag_rows:
    ws4.append(r)
style_sheet(ws4, [14, 36, 16])

wb2.save(OUT + r"\網站變數與導覽表.xlsx")
print("Saved 網站變數與導覽表.xlsx")

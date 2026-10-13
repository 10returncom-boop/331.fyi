"""Generate article-sitemap.xml, gallery-sitemap.xml, sitemap-index.xml"""
import os, glob
from datetime import datetime

ROOT = r"D:\WWW\325_pub\自建主題目錄"
SITE_URL = "https://nutrition.example.com"

# 收集所有 HTML
html_files = []
for root, dirs, files in os.walk(ROOT):
    # 跳過 docs, _backup, _shots, node_modules
    dirs[:] = [d for d in dirs if d not in ("docs", "_backup", "_shots", "node_modules", ".git")]
    for f in files:
        if f.endswith(".html"):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            # 檢查 noindex
            with open(full, encoding="utf-8") as fh:
                content = fh.read(5000)
            if 'name="robots" content="noindex' in content:
                continue
            html_files.append((rel, full))

# 分類
hub_pages = []
gallery_pages = []
for rel, full in html_files:
    if rel == "404.html":
        continue
    if os.path.basename(rel).startswith("style-"):
        gallery_pages.append((rel, full))
    else:
        hub_pages.append((rel, full))

def url_entry(rel, full, priority):
    mod = datetime.fromtimestamp(os.path.getmtime(full)).strftime("%Y-%m-%d")
    return f'  <url>\n    <loc>{SITE_URL}/{rel}</loc>\n    <lastmod>{mod}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{priority}</priority>\n  </url>'

# article-sitemap.xml
hub_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for rel, full in sorted(hub_pages):
    pri = "1.0" if rel == "index.html" else "0.9"
    hub_xml += url_entry(rel, full, pri) + "\n"
hub_xml += "</urlset>\n"
with open(os.path.join(ROOT, "article-sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(hub_xml)
print(f"article-sitemap.xml: {len(hub_pages)} pages")

# gallery-sitemap.xml
gal_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for rel, full in sorted(gallery_pages):
    gal_xml += url_entry(rel, full, "0.8") + "\n"
gal_xml += "</urlset>\n"
with open(os.path.join(ROOT, "gallery-sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(gal_xml)
print(f"gallery-sitemap.xml: {len(gallery_pages)} pages")

# sitemap-index.xml
today = datetime.now().strftime("%Y-%m-%d")
idx_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{SITE_URL}/article-sitemap.xml</loc>
    <lastmod>{today}</lastmod>
  </sitemap>
  <sitemap>
    <loc>{SITE_URL}/gallery-sitemap.xml</loc>
    <lastmod>{today}</lastmod>
  </sitemap>
</sitemapindex>
'''
with open(os.path.join(ROOT, "sitemap-index.xml"), "w", encoding="utf-8") as f:
    f.write(idx_xml)
print("sitemap-index.xml: generated")

# 刪除舊的單一 sitemap.xml（由 sitemap-index 取代）
old = os.path.join(ROOT, "sitemap.xml")
if os.path.exists(old):
    os.remove(old)
    print("Removed old sitemap.xml (replaced by sitemap-index.xml)")

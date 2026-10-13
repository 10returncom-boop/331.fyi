"""Rename brand to 營養綠手指 across all HTML files."""
import os

ROOT = r"D:\_WWW_325_pub\web-nutrition-basics"
count = 0
for dirpath, dirs, files in os.walk(ROOT):
    if "assets" in dirpath or "docs" in dirpath or "data" in dirpath:
        continue
    for fn in files:
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(dirpath, fn)
        with open(fp, encoding="utf-8") as f:
            html = f.read()
        if "營養與生活" not in html:
            continue
        html = html.replace("營養與生活", "營養綠手指")
        with open(fp, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
print(f"Updated brand in {count} files")

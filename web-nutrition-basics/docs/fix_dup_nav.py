"""Remove duplicate 線上課程 nav items - keep only one, prefer the flyout version."""
import os, re

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

        # Count how many times courses/index.html appears in nav context
        # Find all nav-item blocks containing courses
        # If there are 2+ "線上課程" nav-items, remove the simpler one (without flyout)
        nav_items = re.findall(r'<div class="nav-item[^"]*">.*?線上課程.*?</div>\s*(?=<div class="nav-item|</nav>)', html, re.DOTALL)

        if len(nav_items) <= 1:
            continue

        # Keep the one with flyout, remove the simple one
        for item in nav_items:
            if "flyout" not in item:
                html = html.replace(item, "", 1)
                count += 1
                print(f"  [OK] Removed duplicate in {os.path.relpath(fp, ROOT)}")
                break

        with open(fp, "w", encoding="utf-8") as f:
            f.write(html)

print(f"\nFixed {count} duplicates")

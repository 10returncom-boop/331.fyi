"""Fix hero background image path - relative to CSS file (assets/css/)."""
import os, re

ROOT = r"D:\_WWW_325_pub\web-nutrition-basics"

FOLDER_IMG = {
    "": "../images/hero-home.webp",
    "nutrition-basics": "../images/hero-basics.webp",
    "diet-disease": "../images/hero-disease.webp",
    "life-stage": "../images/hero-lifestage.webp",
    "food-guide": "../images/hero-food.webp",
    "lifestyle": "../images/hero-lifestyle.webp",
    "courses": "../images/hero-home.webp",
}

count = 0
for dirpath, dirs, files in os.walk(ROOT):
    if "assets" in dirpath or "docs" in dirpath or "data" in dirpath:
        continue
    for fn in files:
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(dirpath, fn)
        rel = os.path.relpath(fp, ROOT)
        folder = rel.split(os.sep)[0] if os.sep in rel else ""
        img = FOLDER_IMG.get(folder, FOLDER_IMG[""])

        with open(fp, encoding="utf-8") as f:
            html = f.read()

        new_hero = f'<section class="hero" style="--hero-bg: url(\'{img}\')">'
        html_new = re.sub(r'<section class="hero"[^>]*>', new_hero, html, count=1)

        if html_new != html:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(html_new)
            count += 1
            print(f"  [OK] {rel} -> {img}")

print(f"\nFixed {count} pages")

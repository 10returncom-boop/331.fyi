"""Set hero background image per page folder."""
import os, re

ROOT = r"D:\_WWW_325_pub\web-nutrition-basics"

FOLDER_IMG = {
    "": "assets/images/hero-home.webp",
    "nutrition-basics": "assets/images/hero-basics.webp",
    "diet-disease": "assets/images/hero-disease.webp",
    "life-stage": "assets/images/hero-lifestage.webp",
    "food-guide": "assets/images/hero-food.webp",
    "lifestyle": "assets/images/hero-lifestyle.webp",
    "courses": "assets/images/hero-home.webp",
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

        # Calculate relative path depth
        depth = rel.count(os.sep)
        prefix = "../" * depth
        img_url = prefix + img

        with open(fp, encoding="utf-8") as f:
            html = f.read()

        # Replace hero section opening tag to add style with --hero-bg
        # Match <section class="hero"> or <section class="hero" style="...">
        new_hero = f'<section class="hero" style="--hero-bg: url(\'{img_url}\')">'
        html_new = re.sub(r'<section class="hero"[^>]*>', new_hero, html, count=1)

        if html_new != html:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(html_new)
            count += 1
            print(f"  [OK] {rel} -> {img}")

print(f"\nUpdated {count} pages with full-bleed hero")

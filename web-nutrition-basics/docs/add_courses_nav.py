"""Add 線上課程 nav item to all HTML pages that don't have it yet."""
import os, re

ROOT = r"D:\_WWW_325_pub\web-nutrition-basics"

# Determine relative path prefix based on folder depth
def get_prefix(filepath):
    rel = os.path.relpath(filepath, ROOT)
    depth = rel.count(os.sep)
    return "../" * depth

COURSES_NAV = '''      <div class="nav-item flyout">
        <a class="nav-link" href="{p}courses/index.html" aria-haspopup="true">線上課程 ▾</a>
        <div class="flyout-menu">
          <a href="{p}courses/style-course-diabetes.html">糖尿病實戰班</a>
          <a href="{p}courses/style-course-weight.html">減重不挨餓</a>
          <a href="{p}courses/style-course-basics.html">21天飲食健檢</a>
          <a href="{p}courses/style-course-senior.html">銀髮族防肌少</a>
          <a href="{p}courses/index.html">全部24堂課 →</a>
        </div>
      </div>
'''

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
        if "線上課程" in html and "courses/index.html" in html:
            continue  # already has it
        prefix = get_prefix(fp)
        courses_html = COURSES_NAV.format(p=prefix)

        # Find </nav> and insert before it
        if "</nav>" in html and "mainNav" in html:
            html = html.replace("</nav>", courses_html + "    </nav>", 1)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(html)
            count += 1
            print(f"  [OK] {os.path.relpath(fp, ROOT)}")

print(f"\nUpdated {count} pages")

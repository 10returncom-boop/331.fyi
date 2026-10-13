"""Clean up courses/index.html: unify teacher, remove student counts."""
import re

fp = r"D:\_WWW_325_pub\web-nutrition-basics\courses\index.html"
with open(fp, encoding="utf-8") as f:
    html = f.read()

# Replace all teacher lines
html = re.sub(
    r'<div class="course-teacher">[^<]*</div>',
    '<div class="course-teacher">講師：專業營養師</div>',
    html
)

# Remove course-progress and course-students lines
html = re.sub(r'\s*<div class="course-progress">.*?</div>\n', '\n', html)
html = re.sub(r'\s*<div class="course-students">.*?</div>\n', '\n', html)

# Remove meta line with students count (👥)
html = re.sub(r'\s*<span>👥.*?</span>\n', '\n', html)

with open(fp, "w", encoding="utf-8") as f:
    f.write(html)
print("Done: teacher unified, student counts removed")

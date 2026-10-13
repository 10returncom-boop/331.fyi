"""Convert downloaded JPEG .img files to optimized WebP. One-time build tool."""
import os
from PIL import Image

img_dir = r"D:\WWW\325_pub\自建主題目錄\assets\images"
MAX_W = 1280
QUALITY = 82

for f in os.listdir(img_dir):
    if not f.endswith(".img"):
        continue
    src = os.path.join(img_dir, f)
    name = os.path.splitext(f)[0]
    dst = os.path.join(img_dir, name + ".webp")
    im = Image.open(src).convert("RGB")
    if im.width > MAX_W:
        ratio = MAX_W / im.width
        im = im.resize((MAX_W, int(im.height * ratio)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=QUALITY, method=6)
    old_kb = os.path.getsize(src) // 1024
    new_kb = os.path.getsize(dst) // 1024
    print(f"{name}: {im.width}x{im.height}  {old_kb}KB -> {new_kb}KB")
    os.remove(src)

# remove test file
test = os.path.join(img_dir, "test.webp")
if os.path.exists(test):
    os.remove(test)

print("Done. Files:")
for f in sorted(os.listdir(img_dir)):
    print(" ", f, os.path.getsize(os.path.join(img_dir, f)) // 1024, "KB")

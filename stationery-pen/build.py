# -*- coding: utf-8 -*-
"""
100頁鋼筆最強百科 — 建置腳本 build.py
====================================================
用法：
  python build.py            完整建置（產生全部 HTML、sitemap.xml、assets/js/config.js、data/articles.json）
  python build.py --check    只驗證內容檔（frontmatter / 章節歸屬 / 篇數完整性 / 正文長度），不輸出頁面
  python build.py --check <路徑>   只驗證指定內容檔或目錄
  python build.py --list     列出每章文章數與遺漏清單

資料流：
  data/site.json（章節/子分類/文章規劃）
  data/articles/**/*.md（frontmatter + 輕量 markdown 正文）→ 產生頁面
"""
import json
import os
import re
import sys
import html as htmlmod
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_JSON = os.path.join(ROOT, 'data', 'site.json')
ART_DIR = os.path.join(ROOT, 'data', 'articles')
OUT = ROOT

FAVICON = ('data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\'%3E'
           '%3Cpath fill=\'%239a7b3c\' d=\'M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 0 0 0-1.41'
           'l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z\'/%3E%3C/svg%3E')

# 每個章節對應的 WebP 配圖（assets/images/<key>.webp）
CHAPTER_IMG = {
    'overview': 'overview', 'structure': 'structure', 'material': 'material',
    'nib': 'nib', 'filling': 'filling', 'ink': 'ink', 'category': 'category',
    'brand': 'brand', 'buy': 'buy', 'care': 'care', 'history': 'history',
    'collect': 'collect', 'diy': 'diy', 'glossary': 'glossary',
    'appendix': 'appendix', 'tylee': 'tylee',
}

def _top_tags(site, n=20):
    from collections import Counter
    c = Counter()
    for a in site['articles']:
        for t in str(a.get('tags', '')).split(','):
            t = t.strip()
            if t:
                c[t] += 1
    return [t for t, _ in c.most_common(n)]

ICON_SEARCH = ('<svg class="s-ico" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
               '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>')
ICON_MENU = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
             '<path d="M3 6h18M3 12h18M3 18h18"/></svg>')
ICON_SUN = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
            '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>')
ICON_MOON = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
             '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>')
ICON_AUTO = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
             '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>'
             '<path d="M9 12h6"/></svg>')
ICON_BOOKMARK = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
                 '<path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>')
ICON_PRINT = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
              '<path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>')
ICON_BACKTOP = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
                '<path d="M12 19V5M5 12l7-7 7 7"/></svg>')
ICON_HOME = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
             '<path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-7h-6v7H4a1 1 0 0 1-1-1z"/></svg>')
CHEV = '<svg class="chev" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4.5L6 7.5 9 4.5"/></svg>'
ICON_SITEMAP = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
                '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="8.5" y="14" width="7" height="7" rx="1"/><path d="M6.5 10v4h11v-4"/></svg>')


# ============================================================
# 載入規劃
# ============================================================
def load_site():
    with open(SITE_JSON, encoding='utf-8') as f:
        return json.load(f)


def chapter_map(site):
    m = {}
    for c in site['chapters']:
        m[c['id']] = c
        for s in c['subs']:
            key = (c['id'], s['id'])
    return m


def sub_map(site):
    m = {}
    for c in site['chapters']:
        for s in c['subs']:
            m[(c['id'], s['id'])] = s
    return m


def plan_articles(site):
    return {a['slug']: a for a in site['articles']}


# ============================================================
# 內容檔解析
# ============================================================
def parse_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    meta, body = parse_frontmatter(text)
    return meta, body


def parse_frontmatter(text):
    lines = text.split('\n')
    if not lines or lines[0].strip() != '---':
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end = i
            break
    if end is None:
        return {}, text
    meta = {}
    for ln in lines[1:end]:
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        if ':' in ln:
            k, v = ln.split(':', 1)
            meta[k.strip().lower()] = v.strip()
    return meta, '\n'.join(lines[end + 1:])


def split_list(v):
    if not v:
        return []
    return [x.strip() for x in v.split(',') if x.strip()]


def validate_article(meta, body, path, site, plan):
    errors, warns = [], []
    required = ['title', 'chapter', 'sub', 'slug', 'summary', 'tags', 'difficulty', 'updated']
    for k in required:
        if k not in meta or not meta[k]:
            errors.append('缺少欄位: %s' % k)
    chid = meta.get('chapter', '')
    subid = meta.get('sub', '')
    if chid not in chapter_map(site):
        errors.append('章節 id 不存在: %s' % chid)
    if subid and (chid, subid) not in sub_map(site):
        errors.append('子分類 (%s,%s) 不存在於規劃' % (chid, subid))
    slug = meta.get('slug', '')
    if slug and slug not in plan:
        warns.append('slug 不在規劃清單（可能是新增未規劃文章）: %s' % slug)
    rel = split_list(meta.get('related', ''))
    for r in rel:
        if r not in plan:
            warns.append('related 指向不存在的文章: %s' % r)
    tags = split_list(meta.get('tags', ''))
    if not tags:
        warns.append('tags 為空')
    # 正文長度
    body_stripped = re.sub(r'\s', '', body)
    if len(body_stripped) < 400:
        errors.append('正文過短（%d 字，需 ≥400）' % len(body_stripped))
    elif len(body_stripped) < 600:
        warns.append('正文偏短（%d 字，建議 ≥1000 字）' % len(body_stripped))
    n_h2 = len(re.findall(r'(?m)^##\s', body))
    if n_h2 < 3:
        errors.append('小節（##）少於 3 個（目前 %d 個）' % n_h2)
    if '常見問題' not in body and 'FAQ' not in body:
        warns.append('缺少「常見問題」段落（建議每篇附 2–4 組 Q/A）')
    return errors, warns


# ============================================================
# 輕量 markdown → HTML
# ============================================================
_CODE_RE = re.compile(r'`([^`]+)`')
_BOLD_RE = re.compile(r'\*\*(.+?)\*\*')
_ITALIC_RE = re.compile(r'(?<!\*)\*([^*\n]+)\*(?!\*)')
_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)\s]+)\)')
_OL_RE = re.compile(r'^\d+\.\s')


def inline(text):
    text = htmlmod.escape(text, quote=False)
    codes = []
    def _c(m):
        codes.append(m.group(1))
        return '\x00%d\x00' % (len(codes) - 1)
    text = _CODE_RE.sub(_c, text)
    text = _BOLD_RE.sub(r'<strong>\1</strong>', text)
    text = _ITALIC_RE.sub(r'<em>\1</em>', text)
    text = _LINK_RE.sub(lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), text)
    def _r(m):
        return '<code>%s</code>' % codes[int(m.group(1))]
    return re.sub(r'\x00(\d+)\x00', _r, text)


def render_table(rows):
    cells = []
    for r in rows:
        r = r.strip()
        if r.startswith('|'):
            r = r[1:]
        if r.endswith('|'):
            r = r[:-1]
        cells.append([c.strip() for c in r.split('|')])
    header = None
    body_rows = cells
    if len(cells) >= 2 and all(re.fullmatch(r':?-{2,}:?', c) for c in cells[1] if c != ''):
        header = cells[0]
        body_rows = cells[2:]
    ncols = max(len(r) for r in cells)
    out = ['<div class="tbl-wrap"><table class="tbl"><colgroup>']
    for _ in range(ncols):
        out.append('<col style="width:%s%%">' % round(100 / ncols, 1))
    out.append('</colgroup>')
    if header:
        out.append('<thead><tr>' + ''.join('<th>%s</th>' % inline(c) for c in header) + '</tr></thead>')
    out.append('<tbody>')
    for r in body_rows:
        while len(r) < ncols:
            r.append('')
        out.append('<tr>' + ''.join('<td>%s</td>' % inline(c) for c in r) + '</tr>')
    out.append('</tbody></table></div>')
    return ''.join(out)


def is_block_start(s):
    if not s:
        return False
    if s.startswith(('#', '|', '>', '- ', '---')):
        return True
    if _OL_RE.match(s):
        return True
    return False


def render_body(body):
    lines = body.split('\n')
    i, n = 0, len(lines)
    out = []
    toc = []
    faq_items = []
    h2_count = 0
    h3_count = 0
    in_faq = False
    cur_faq = None

    def flush_faq():
        nonlocal cur_faq
        if cur_faq is not None:
            faq_items.append(cur_faq)
            cur_faq = None

    while i < n:
        ln = lines[i]
        s = ln.strip()
        if not s:
            i += 1
            continue
        if s.startswith('|'):
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(lines[i].strip())
                i += 1
            out.append(render_table(rows))
            continue
        if s.startswith('>'):
            parts = []
            while i < n and lines[i].strip().startswith('>'):
                parts.append(lines[i].strip()[1:].strip())
                i += 1
            text = ' '.join(parts)
            kind = 'info'
            if text.startswith('注意') or text.startswith('警告'):
                kind = 'warn'
            elif text.startswith(('提示', '小知識', '秘訣', '小提醒')):
                kind = 'tip'
            out.append('<div class="callout %s">%s</div>' % (kind, inline(text)))
            continue
        if s.startswith('####'):
            text = s[4:].strip()
            out.append('<h4>%s</h4>' % inline(text))
            i += 1
            continue
        if s.startswith('###'):
            text = s[3:].strip()
            h3_count += 1
            hid = 'sec-%d-%d' % (h2_count, h3_count)
            out.append('<h3 id="%s">%s</h3>' % (hid, inline(text)))
            toc.append((3, hid, text))
            i += 1
            continue
        if s.startswith('##'):
            flush_faq()
            text = s[2:].strip()
            h2_count += 1
            h3_count = 0
            hid = 'sec-%d' % h2_count
            out.append('<h2 id="%s">%s</h2>' % (hid, inline(text)))
            toc.append((2, hid, text))
            in_faq = text.startswith('常見問題') or text.startswith('FAQ')
            i += 1
            continue
        if s.startswith('#'):
            i += 1
            continue
        if s == '---':
            out.append('<hr>')
            i += 1
            continue
        if s.startswith('- '):
            items = []
            while i < n and lines[i].strip().startswith('- '):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append('<ul>' + ''.join('<li>%s</li>' % inline(x) for x in items) + '</ul>')
            continue
        if _OL_RE.match(s):
            items = []
            while i < n and _OL_RE.match(lines[i].strip()):
                items.append(_OL_RE.sub('', lines[i].strip()))
                i += 1
            out.append('<ol>' + ''.join('<li>%s</li>' % inline(x) for x in items) + '</ol>')
            continue
        # FAQ 問答行
        if in_faq:
            s2 = s.replace('**', '')
            if s2.startswith(('Q：', 'Q:')):
                flush_faq()
                cur_faq = {'q': inline(s2[2:].strip()), 'a': []}
                i += 1
                continue
            if s2.startswith(('A：', 'A:')):
                if cur_faq is not None:
                    cur_faq['a'].append(inline(s2[2:].strip()))
                i += 1
                continue
            if cur_faq is not None:
                cur_faq['a'].append(inline(s))
                i += 1
                continue
        # 段落
        para = [s]
        i += 1
        while i < n and lines[i].strip() and not is_block_start(lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append('<p>%s</p>' % ' '.join(inline(x) for x in para))
    flush_faq()

    if faq_items:
        faq_html = ['<div class="faq-wrap">']
        for fq in faq_items:
            faq_html.append('<div class="faq-item"><button class="faq-q" type="button">'
                            '<span class="fq-ico">?</span><span>%s</span>'
                            '<svg class="chev" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2">'
                            '<path d="M3 4.5L6 7.5 9 4.5"/></svg></button>'
                            '<div class="faq-a"><p>%s</p></div></div>'
                            % (fq['q'], '<br>'.join(fq['a'])))
        faq_html.append('</div>')
        out.append(''.join(faq_html))
    return '\n'.join(out), toc, faq_items


# ============================================================
# 頁面骨架
# ============================================================
def rel_prefix(out_rel):
    parts = out_rel.split('/')
    return '../' * (len(parts) - 1)


def jsonld_script(data):
    return '<script type="application/ld+json">%s</script>' % json.dumps(data, ensure_ascii=False)


def page_html(site, rel, title, desc, path, breadcrumb, body_html, jsonlds, current):
    r = rel
    root_url = site['site']['rootUrl']
    # 決定本頁 WebP 配圖（用於 og:image 與文章頁 hero）
    ch = current.get('chapter') if current else None
    if path == 'index.html':
        img_key = 'home-hero'
    elif ch in CHAPTER_IMG:
        img_key = CHAPTER_IMG[ch]
    else:
        img_key = 'home-hero'
    img_rel = r + 'assets/images/' + img_key + '.webp'
    img_abs = root_url + 'assets/images/' + img_key + '.webp'
    og_image_tag = ('<meta property="og:image" content="' + img_abs + '">\n'
                    '<meta name="twitter:card" content="summary_large_image">\n'
                    '<meta name="twitter:image" content="' + img_abs + '">\n')
    header = (
        '<header class="topbar"><div class="topbar-inner">'
        '<button class="icon-btn menu-toggle" id="menuToggle" aria-label="開啟選單">' + ICON_MENU + '</button>'
        '<a class="brand" href="' + r + 'index.html"><span class="brand-mark">筆</span>'
        '<span class="brand-titles"><span class="brand-title">從文具控到鋼筆控～這些那些鋼筆知識百科</span></span></a>'
        '<div class="topbar-spacer"></div>'
        '<div class="searchbox">' + ICON_SEARCH + '<input type="text" placeholder="搜尋文章、章節、標籤…" aria-label="全站搜尋" autocomplete="off">'
        '<button class="s-clear" aria-label="清除搜尋">✕</button><div class="search-results"></div></div>'
        '<button class="icon-btn" id="favOpen" aria-label="收藏清單" title="收藏清單">' + ICON_BOOKMARK + '<span class="badge" id="favBadge"></span></button>'
        '<div class="theme-seg" id="themeSeg" role="group" aria-label="主題切換">'
        '<button data-theme="light" aria-label="亮色主題">' + ICON_SUN + '</button>'
        '<button data-theme="dark" aria-label="暗色主題">' + ICON_MOON + '</button>'
        '<button data-theme="system" aria-label="跟隨系統">' + ICON_AUTO + '</button>'
        '</div></div></header>'
    )
    nav = ('<nav class="mainnav" aria-label="主導覽"><div class="mainnav-inner" id="mainNav"></div>'
           '<div class="mega-layer" id="megaLayer"></div></nav>')
    crumb = '<div class="crumbbar"><div class="crumb-inner">' + breadcrumb + '</div></div>'
    footer = (
        '<footer class="footer"><div class="footer-inner">'
        '<div><h4>快速導覽</h4><div class="footer-links">'
        + ''.join('<a href="' + r + c['id'] + '/index.html">' + c['zh'] + '</a>' for c in site['chapters'][:8])
        + '<a href="' + r + 'index.html">全部 16 大章 →</a></div></div>'
        '<div><h4>資源</h4><div class="footer-links">'
        '<a href="' + r + 'tags/index.html">標籤彙整</a>'
        '<a href="' + r + 'az-index.html">A–Z 字母索引</a>'
        '<a href="' + r + 'search.html">全站搜尋</a>'
        '<a href="' + r + 'sitemap.xml">Sitemap</a>'
        '<a href="' + r + 'glossary/index.html">詞彙辭典（A–Z）</a></div></div>'
        '<div><h4>熱門標籤</h4><div class="footer-links">'
        + ''.join('<a href="' + r + 'tags/' + tg + '.html">#' + tg + '</a>' for tg in _top_tags(site, 20))
        + '</div></div>'
        '</div><div class="footer-bottom">© 2026 從文具控到鋼筆控～這些那些鋼筆知識百科 · 內容僅供學習與參考 · 建置於 '
        + site['site']['updated'] + '</div></footer>'
    )
    mobile = (
        '<div class="mobile-panel" id="mobilePanel" aria-hidden="true">'
        '<div class="mob-head"><h3>全站導覽</h3><button class="mob-close" id="mobClose" aria-label="關閉選單">✕</button></div>'
        '<div id="mobNav"></div></div>'
    )
    drawer = (
        '<div class="drawer-mask" id="favMask"></div>'
        '<aside class="fav-drawer" id="favDrawer" aria-label="收藏清單">'
        '<div class="fav-drawer-head"><h3>我的收藏</h3><button class="icon-btn" aria-label="關閉">✕</button></div>'
        '<div class="fav-list" id="favList"></div></aside>'
    )
    toast = '<div class="toast" id="toast" role="status"></div>'
    dock = ('<div class="float-dock">'
            '<a class="float-btn" href="' + r + 'index.html" title="回首頁" aria-label="回首頁">' + ICON_HOME + '</a>'
            '<a class="float-btn" href="' + r + 'az-index.html" title="站內導覽：全站文章 A–Z" aria-label="站內導覽">' + ICON_SITEMAP + '</a>'
            '<button class="float-btn backtop" id="backTop" aria-label="回到頂端">' + ICON_BACKTOP + '</button>'
            '</div>')
    scripts = ''.join(
        '<script src="%sassets/js/%s"></script>' % (r, f)
        for f in ['config.js', 'theme.js', 'nav.js', 'search.js', 'reading.js', 'breathe-clamp.js', 'main.js']
    )
    jsonld = ''.join(jsonld_script(j) for j in jsonlds)
    og_url = root_url + path
    return (
        '<!DOCTYPE html>\n<html lang="zh-Hant">\n<head>\n'
        '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>' + htmlmod.escape(title) + '</title>\n'
        '<meta name="description" content="' + htmlmod.escape(desc) + '">\n'
        '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">\n'
        '<meta name="author" content="從文具控到鋼筆控編輯部">\n'
        '<meta name="theme-color" content="#9a7b3c">\n'
        '<meta property="og:locale" content="zh_TW">\n'
        '<link rel="canonical" href="' + og_url + '">\n'
        '<meta property="og:type" content="website">\n<meta property="og:title" content="' + htmlmod.escape(title) + '">\n'
        '<meta property="og:description" content="' + htmlmod.escape(desc) + '">\n'
        '<meta property="og:url" content="' + og_url + '">\n'
        + og_image_tag +
        '<meta name="twitter:title" content="' + htmlmod.escape(title) + '">\n'
        '<meta name="twitter:description" content="' + htmlmod.escape(desc) + '">\n'
        '<meta name="generator" content="100頁鋼筆最強百科 build.py">\n'
        '<link rel="icon" href="' + FAVICON + '">\n'
        '<link rel="stylesheet" href="https://miaoda.feishu.cn/fonts/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Noto+Serif+TC:wght@600;700&display=swap">\n'
        '<link rel="stylesheet" href="' + r + 'assets/css/style.css">\n'
        '<script>(function(){try{var t=localStorage.getItem(\'pen-theme\')||\'light\';'
        'var d=t===\'dark\'?\'dark\':\'light\';document.documentElement.setAttribute(\'data-theme\',d);}catch(e){}})();</script>\n'
        '<script>window.PEN_DEPTH=' + str(path.count('/')) + ';</script>\n'
        + jsonld + '\n</head>\n<body>\n'
        '<div class="progress-bar" id="progressBar"></div>\n'
        + header + '\n' + nav + '\n' + crumb + '\n'
        + body_html + '\n'
        + footer + '\n' + mobile + '\n' + drawer + '\n' + toast + '\n' + dock + '\n'
        + scripts + '\n</body>\n</html>\n'
    )


# ============================================================
# 麵包屑與 JSON-LD
# ============================================================
def crumb_home(rel):
    return '<a href="' + rel + 'index.html">首頁</a><span class="crumb-sep">/</span>'


def breadcrumb_list(site, items):
    root = site['site']['rootUrl']
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1,
                                 'name': it[0], 'item': root + it[1]} for i, it in enumerate(items)]}


# ============================================================
# 頁面產生
# ============================================================
def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)


def build(site, force=False):
    chapters = chapter_map(site)
    subs = sub_map(site)
    plan = plan_articles(site)
    root_url = site['site']['rootUrl']
    problems = []

    # 掃描內容檔
    files = {}
    for dirpath, _dirs, fnames in os.walk(ART_DIR):
        for fn in fnames:
            if fn.endswith('.md'):
                files[os.path.join(dirpath, fn)] = fn[:-3]

    # 解析全部文章
    articles = {}      # slug -> dict
    order = []         # slug 依規劃順序
    for p in site['articles']:
        order.append(p['slug'])
    missing = [p['slug'] for p in site['articles']]
    extra = []

    for path, slug in files.items():
        meta, body = parse_file(path)
        meta.setdefault('slug', slug)
        s = meta.get('slug', slug)
        if s not in plan:
            extra.append(s)
            continue
        errs, warns = validate_article(meta, body, path, site, plan)
        for e in errs:
            problems.append('  ✗ [%s] %s' % (s, e))
        for w in warns:
            print('  ⚠ [%s] %s' % (s, w))
        body_html, toc, faq = render_body(body)
        articles[s] = {
            'meta': meta, 'body': body_html, 'toc': toc, 'faq': faq,
            'chars': len(re.sub(r'\s', '', body)), 'path': path,
        }
        if s in missing:
            missing.remove(s)

    if missing and not force:
        problems.append('  遺漏內容檔（%d 篇）：%s' % (len(missing), ', '.join(missing)))
    if extra:
        print('  ⚠ 未規劃的內容檔：%s' % ', '.join(extra))

    if problems:
        print('內容檔檢查失敗，共 %d 項問題：' % len(problems))
        for p in problems:
            print(p)
        return False, articles, order, missing

    # 建立章節資料
    chapters_out = []
    flat = []
    for c in site['chapters']:
        subs_out = []
        n_arts = 0
        for s in c['subs']:
            arts = []
            for slug in order:
                a = plan.get(slug)
                if a and a['chapter'] == c['id'] and a['sub'] == s['id']:
                    if slug not in articles:
                        continue  # 缺稿時（--force 預覽）跳過
                    art = articles[slug]
                    m = art['meta']
                    arts.append({
                        'slug': slug,
                        'title': m.get('title', slug),
                        'url': '%s/%s/%s.html' % (c['id'], s['id'], slug),
                        'summary': m.get('summary', ''),
                        'tags': split_list(m.get('tags', '')),
                        'difficulty': m.get('difficulty', '一般'),
                        'updated': m.get('updated', site['site']['updated']),
                        'chars': art['chars'],
                    })
                    n_arts += 1
            subs_out.append({
                'id': s['id'], 'zh': s['zh'], 'en': s['en'], 'desc': s['desc'],
                'url': '%s/%s/index.html' % (c['id'], s['id']),
                'articles': arts,
            })
        chapters_out.append({
            'id': c['id'], 'zh': c['zh'], 'en': c['en'], 'desc': c['desc'],
            'url': '%s/index.html' % c['id'],
            'nArts': n_arts,
            'subs': subs_out,
        })
        for s in c['subs']:
            for a in subs_out:
                if a['id'] == s['id']:
                    for art in a['articles']:
                        flat.append(dict(art, chapter=c['id'], sub=s['id'],
                                         cat='%s › %s' % (c['zh'], s['zh'])))
    flat_map = {a['slug']: a for a in flat}

    # ============ 產生文章頁 ============
    for c in site['chapters']:
        for s in c['subs']:
            sub_arts = [a for a in flat if a['chapter'] == c['id'] and a['sub'] == s['id']]
            for i, a in enumerate(sub_arts):
                art = articles[a['slug']]
                m = art['meta']
                title = m.get('title', a['slug'])
                desc = m.get('summary', '')
                out_rel = '%s/%s/%s.html' % (c['id'], s['id'], a['slug'])
                rel = rel_prefix(out_rel)
                # 麵包屑
                crumb = (crumb_home(rel)
                         + '<a href="' + rel + c['id'] + '/index.html">' + c['zh'] + '</a><span class="crumb-sep">/</span>'
                         + '<a href="' + rel + c['id'] + '/' + s['id'] + '/index.html">' + s['zh'] + '</a><span class="crumb-sep">/</span>'
                         + '<span class="crumb-current">' + title + '</span>')
                # JSON-LD
                root = site['site']['rootUrl']
                img_key = CHAPTER_IMG.get(c['id'], 'home-hero')
                jld = [
                    breadcrumb_list(site, [('首頁', 'index.html'), (c['zh'], c['id'] + '/index.html'),
                                           (s['zh'], c['id'] + '/' + s['id'] + '/index.html'), (title, out_rel)]),
                    {'@context': 'https://schema.org', '@type': 'Article',
                     'headline': title, 'description': desc,
                     'datePublished': m.get('updated', site['site']['updated']),
                     'dateModified': m.get('updated', site['site']['updated']),
                     'inLanguage': 'zh-Hant',
                     'image': root + 'assets/images/' + img_key + '.webp',
                     'mainEntityOfPage': root + out_rel,
                     'author': {'@type': 'Organization', 'name': site['site']['name']},
                     'publisher': {'@type': 'Organization', 'name': site['site']['name'],
                                   'logo': {'@type': 'ImageObject', 'url': root + 'assets/images/home-hero.webp'}}},
                ]
                if art['faq']:
                    jld.append({'@context': 'https://schema.org', '@type': 'FAQPage',
                                'mainEntity': [{'@type': 'Question', 'name': fq['q'],
                                                'acceptedAnswer': {'@type': 'Answer', 'text': ' '.join(fq['a'])}}
                                               for fq in art['faq']]})
                # 相關文章
                rels = []
                seen = {a['slug']}
                for r in split_list(m.get('related', '')):
                    if r in flat_map and r not in seen:
                        ra = flat_map[r]
                        rels.append(ra)
                        seen.add(r)
                for ra in sub_arts:
                    if len(rels) >= 6:
                        break
                    if ra['slug'] not in seen:
                        rels.append(ra)
                        seen.add(ra['slug'])
                for fa in flat:
                    if len(rels) >= 6:
                        break
                    if fa['slug'] not in seen and fa['chapter'] == c['id']:
                        rels.append(fa)
                        seen.add(fa['slug'])
                rel_html = ''
                if rels:
                    rel_html = ('<section class="related"><h3>相關文章</h3><div class="related-grid">'
                                + ''.join('<a class="rel-card" href="' + rel + ra['url'] + '">'
                                          '<div class="rc-cat">' + c['zh'] + '</div><div class="rc-t">' + ra['title'] + '</div>'
                                          '<div class="rc-d">' + ra['difficulty'] + ' · 更新 ' + ra['updated'] + '</div></a>'
                                          for ra in rels[:6])
                                + '</div></section>')
                # 上一頁/下一頁
                prev_a = sub_arts[i - 1] if i > 0 else None
                next_a = sub_arts[i + 1] if i < len(sub_arts) - 1 else None
                pager = ('<nav class="pager" aria-label="文章導覽">'
                         + ('<a href="' + rel + (prev_a['url'] if prev_a else c['id'] + '/index.html') + '">'
                            '<div class="p-label">' + ('上一篇' if prev_a else '返回章節') + '</div>'
                            '<div class="p-title">' + (prev_a['title'] if prev_a else c['zh'] + ' 總覽') + '</div></a>'
                            if (prev_a or True) else '<div class="p-void"></div>')
                         + ('<a href="' + rel + (next_a['url'] if next_a else c['id'] + '/index.html') + '">'
                            '<div class="p-label">' + ('下一篇' if next_a else '返回章節') + '</div>'
                            '<div class="p-title">' + (next_a['title'] if next_a else c['zh'] + ' 總覽') + '</div></a>'
                            if (next_a or True) else '<div class="p-void"></div>')
                         + '</nav>')
                # TOC 右欄
                toc_html = ''
                if len(art['toc']) >= 3:
                    toc_html = ('<aside class="toc-rail"><h4>本頁目錄</h4><nav class="rail-toc">'
                                + ''.join(('<a href="#' + tid + '"' + (' class="lv3"' if lv == 3 else '') + '>' + t + '</a>')
                                          for lv, tid, t in art['toc'])
                                + '</nav></aside>')
                # 正文佈局
                read_min = max(1, round(art['chars'] / 400))
                body_html = (
                    '<div class="layout with-toc">'
                    '<aside class="sidebar" id="sidebar"></aside>'
                    '<main class="main"><article class="article">'
                    '<header class="article-head">'
                    '<div class="eyebrow">' + c['en'] + ' ／ ' + s['zh'] + '</div>'
                    '<h1 class="article-title">【鋼筆控】' + title + '</h1>'
                    '<p class="article-summary">' + htmlmod.escape(desc) + '</p>'
                    '<div class="tags-row">'
                    + ''.join('<a class="tag" href="' + rel + 'tags/' + tg + '.html">#' + tg + '</a>'
                              for tg in split_list(m.get('tags', '')))
                    + '</div></header>'
                    '<figure class="article-hero-img"><img src="' + rel + 'assets/images/' + (a['slug'] if os.path.exists(os.path.join('assets','images',a['slug']+'.webp')) else CHAPTER_IMG.get(c['id'], 'home-hero')) + '.webp" alt="' + htmlmod.escape(title) + '" width="1280" height="720" loading="lazy"></figure>'
                    '<div class="article-body">' + art['body'] + '</div>'
                    + rel_html + pager
                    + '</article></main>'
                    + toc_html + '</div>'
                )
                write(out_rel, page_html(site, rel, '【鋼筆控】' + title + '｜' + site['site']['name'], desc, out_rel,
                                         crumb, body_html, jld,
                                         {'slug': a['slug'], 'chapter': c['id']}))
                print('  ✓ %s' % out_rel)

    # ============ 產生章節頁 / 子分類頁 ============
    for c in site['chapters']:
        ch = next(x for x in chapters_out if x['id'] == c['id'])
        # 章節頁
        out_rel = '%s/index.html' % c['id']
        rel = rel_prefix(out_rel)
        crumb = (crumb_home(rel) + '<span class="crumb-current">' + c['zh'] + '</span>')
        sub_html = []
        for s in ch['subs']:
            arts = s['articles']
            cards = ''.join('<a class="card" href="' + rel + a['url'] + '">'
                            '<div class="card-title">' + a['title'] + '</div>'
                            '<div class="card-meta">' + a['difficulty'] + ' · 更新 ' + a['updated'] + ' · 約 ' + str(max(1, round(a['chars'] / 400))) + ' 分鐘</div>'
                            '<div class="card-tags">' + ''.join('<span>#' + t + '</span>' for t in a['tags'][:3]) + '</div></a>'
                            for a in arts)
            sub_html.append(
                '<a class="sub-row" href="' + rel + s['url'] + '">'
                '<div><div class="t">' + s['zh'] + '</div><div class="d">' + s['desc'] + '</div>'
                '<div class="count">' + str(len(arts)) + ' 篇文章</div></div></a>'
                '<div class="grid" style="margin-bottom:22px">' + cards + '</div>'
            )
        body_html = ('<div class="layout cols-2"><aside class="sidebar" id="sidebar"></aside><main class="main">'
                     '<div class="page-head"><div class="eyebrow">' + c['en'] + '</div>'
                     '<h1 class="page-title">' + c['zh'] + '</h1><p class="page-desc">' + c['desc'] + '</p>'
                     '<div class="page-stats"><span><b>' + str(ch['nArts']) + '</b> 篇文章</span>'
                     '<span><b>' + str(len(ch['subs'])) + '</b> 個子分類</span></div>'
                     '<figure class="page-hero-img"><img src="' + rel + 'assets/images/' + CHAPTER_IMG.get(c['id'], 'home-hero') + '.webp" alt="' + c['zh'] + '" width="1280" height="720" loading="lazy"></figure></div>'
                     + ''.join(sub_html)
                     + '</main></div>')
        jld = [breadcrumb_list(site, [('首頁', 'index.html'), (c['zh'], out_rel)]),
               {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': c['zh'],
                'description': c['desc'],
                'mainEntity': {'@type': 'ItemList',
                               'itemListElement': [{'@type': 'ListItem', 'position': i + 1,
                                                    'name': a['title'], 'url': root_url + a['url']}
                                                   for i, a in enumerate([x for x in flat if x['chapter'] == c['id']])]}}]
        write(out_rel, page_html(site, rel, c['zh'] + '｜' + site['site']['name'], c['desc'], out_rel,
                                 crumb, body_html, jld, {'slug': None, 'chapter': c['id']}))
        print('  ✓ %s' % out_rel)
        # 子分類頁
        for s in ch['subs']:
            out_rel2 = '%s/%s/index.html' % (c['id'], s['id'])
            rel2 = rel_prefix(out_rel2)
            arts = next(x for x in ch['subs'] if x['id'] == s['id'])['articles']
            crumb2 = (crumb_home(rel2)
                      + '<a href="' + rel2 + c['id'] + '/index.html">' + c['zh'] + '</a><span class="crumb-sep">/</span>'
                      + '<span class="crumb-current">' + s['zh'] + '</span>')
            cards = ''.join('<a class="card" href="' + rel2 + a['url'] + '">'
                            '<div class="card-num">' + s['zh'] + '</div>'
                            '<div class="card-title">' + a['title'] + '</div>'
                            '<div class="card-en">' + a['slug'] + '</div>'
                            '<div class="card-meta">' + a['difficulty'] + ' · 更新 ' + a['updated'] + '</div>'
                            '<div class="card-tags">' + ''.join('<span>#' + t + '</span>' for t in a['tags'][:3]) + '</div></a>'
                            for a in arts)
            body_html2 = ('<div class="layout cols-2"><aside class="sidebar" id="sidebar"></aside><main class="main">'
                          '<div class="page-head"><div class="eyebrow">' + c['zh'] + ' ／ ' + s['zh'] + '</div>'
                          '<h1 class="page-title">' + s['zh'] + '</h1><p class="page-desc">' + s['desc'] + '</p>'
                          '<div class="page-stats"><span><b>' + str(len(arts)) + '</b> 篇文章</span></div></div>'
                          '<div class="grid">' + cards + '</div></main></div>')
            jld2 = [breadcrumb_list(site, [('首頁', 'index.html'), (c['zh'], c['id'] + '/index.html'),
                                           (s['zh'], out_rel2)]),
                    {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': s['zh'],
                     'mainEntity': {'@type': 'ItemList',
                                    'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': a['title'],
                                                         'url': root_url + a['url']} for i, a in enumerate(arts)]}}]
            write(out_rel2, page_html(site, rel2, s['zh'] + '｜' + site['site']['name'], s['desc'], out_rel2,
                                      crumb2, body_html2, jld2, {'slug': None, 'chapter': c['id']}))
            print('  ✓ %s' % out_rel2)

    # ============ 標籤彙整頁 ============
    tag_map = {}
    for a in flat:
        for t in a['tags']:
            tag_map.setdefault(t, []).append(a)
    for tg, arts in sorted(tag_map.items()):
        out_rel = 'tags/%s.html' % tg
        rel = rel_prefix(out_rel)
        crumb = (crumb_home(rel) + '<a href="' + rel + 'tags/index.html">標籤</a><span class="crumb-sep">/</span>'
                 + '<span class="crumb-current">#' + tg + '</span>')
        cards = ''.join('<a class="card" href="' + rel + a['url'] + '">'
                        '<div class="card-num">' + a['cat'] + '</div>'
                        '<div class="card-title">' + a['title'] + '</div>'
                        '<div class="card-meta">' + a['difficulty'] + ' · 更新 ' + a['updated'] + '</div>'
                        '<div class="card-tags">' + ''.join('<span>#' + t + '</span>' for t in a['tags'][:4]) + '</div></a>'
                        for a in arts)
        body_html = ('<div class="layout"><main class="main" style="grid-column:1/-1">'
                     '<div class="page-head"><div class="eyebrow">TAG</div>'
                     '<h1 class="page-title">#' + tg + '</h1>'
                     '<p class="page-desc">共 ' + str(len(arts)) + ' 篇文章帶有此標籤。</p></div>'
                     '<div class="grid">' + cards + '</div></main></div>')
        jld = [breadcrumb_list(site, [('首頁', 'index.html'), ('標籤', 'tags/index.html'), ('#' + tg, out_rel)]),
               {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': '#' + tg,
                'mainEntity': {'@type': 'ItemList',
                               'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': a['title'],
                                                    'url': root_url + a['url']} for i, a in enumerate(arts)]}}]
        write(out_rel, page_html(site, rel, '#' + tg + '｜標籤彙整｜' + site['site']['name'],
                                 '收錄 %d 篇關於「%s」的鋼筆知識文章。' % (len(arts), tg), out_rel,
                                 crumb, body_html, jld, {'slug': None, 'chapter': None}))
        print('  ✓ %s' % out_rel)

    # 標籤索引頁
    out_rel = 'tags/index.html'
    rel = rel_prefix(out_rel)
    crumb = crumb_home(rel) + '<span class="crumb-current">標籤彙整</span>'
    cloud = '<div class="tag-cloud">' + ''.join(
        '<a href="' + rel + 'tags/' + tg + '.html">#' + tg + '<span style="opacity:.7">（' + str(len(arts)) + '）</span></a>'
        for tg, arts in sorted(tag_map.items(), key=lambda x: -len(x[1]))) + '</div>'
    body_html = ('<div class="layout"><main class="main" style="grid-column:1/-1">'
                 '<div class="page-head"><div class="eyebrow">TAGS</div>'
                 '<h1 class="page-title">標籤彙整</h1>'
                 '<p class="page-desc">共 ' + str(len(tag_map)) + ' 個標籤，點擊任一標籤瀏覽跨章節的相關文章。</p></div>'
                 + cloud + '</main></div>')
    jld = [breadcrumb_list(site, [('首頁', 'index.html'), ('標籤彙整', out_rel)])]
    write(out_rel, page_html(site, rel, '標籤彙整｜' + site['site']['name'], '全站標籤雲，依標籤跨章節彙整文章。', out_rel,
                             crumb, body_html, jld, {'slug': None, 'chapter': None}))
    print('  ✓ %s' % out_rel)

    # ============ 首頁 ============
    out_rel = 'index.html'
    rel = ''
    crumb = '<span class="crumb-current">世界總覽</span>'
    hero_stats = ('<div class="hero-stats">'
                  '<div class="hero-stat"><b>' + str(len(flat)) + '</b><span>篇文章</span></div>'
                  '<div class="hero-stat"><b>' + str(len(site['chapters'])) + '</b><span>大章節</span></div>'
                  '<div class="hero-stat"><b>' + str(len(tag_map)) + '</b><span>標籤</span></div>'
                  '<div class="hero-stat"><b>' + site['site']['version'] + '</b><span>版本</span></div></div>')
    hero = ('<section class="hero"><div class="hero-eyebrow">ULTIMATE FOUNTAIN PEN ENCYCLOPEDIA</div>'
            '<h1>從文具控到鋼筆控～這些那些鋼筆知識百科</h1>'
            '<p class="hero-sub">從萬寶龍到你手上的那張紙，就是我的天地</p>'
            + '<figure class="hero-img"><img src="assets/images/home-hero.webp" alt="從文具控到鋼筆控～這些那些鋼筆知識百科" width="1280" height="720"></figure>'
            + '<div class="hero-search">' + ICON_SEARCH + '<input type="text" placeholder="搜尋文章、章節、標籤…" aria-label="全站搜尋" autocomplete="off">'
            '<div class="search-results"></div></div></section>')
    # 章節群組標籤
    CH_GROUP = {
        'overview': '鋼筆知識', 'structure': '鋼筆知識', 'material': '鋼筆知識',
        'nib': '鋼筆知識', 'filling': '鋼筆知識', 'ink': '鋼筆知識', 'category': '鋼筆知識',
        'glossary': '索引工具', 'appendix': '索引工具',
    }
    _ch_parts = []
    for c in chapters_out:
        img_key = CHAPTER_IMG.get(c['id'], 'home-hero')
        grp = CH_GROUP.get(c['id'], '')
        tag_list = []
        for s in c['subs']:
            tag_list.append('<span class="cc-tag">' + s['zh'] + '</span>')
        subs_html = ''.join(tag_list)
        if grp:
            grp_pill = '<span class="cc-group-pill">' + grp + '</span>'
        else:
            grp_pill = ''
        img_tag = '<figure class="cc-img"><img src="assets/images/' + img_key + '.webp" alt="' + c['zh'] + '" width="1280" height="720" loading="lazy"></figure>'
        head_tag = '<button class="acc-head" type="button"><span class="cc-zh">' + c['zh'] + '</span><span class="cc-en">' + c['en'] + '</span>' + CHEV + '</button>'
        body_tag = '<div class="acc-body">' + grp_pill + '<div class="cc-desc">' + c['desc'] + '</div><div class="cc-tags">' + subs_html + '</div><a class="acc-link" href="' + c['url'] + '">進入「' + c['zh'] + '」→</a></div>'
        card = '<div class="acc-card">' + img_tag + head_tag + body_tag + '</div>'
        _ch_parts.append(card)
    ch_cards = ''.join(_ch_parts)
    recent = flat[-8:]
    recent_items = ''.join('<a href="' + rel + a['url'] + '"><span class="cm-cat">' + a['cat'].split(' › ')[0] + '</span>'
                           '<span class="cm-t">' + a['title'] + '</span>'
                           '<span class="cm-d">' + a['updated'] + '</span></a>' for a in recent)
    latest = ('<section><div class="section-title"><h2>最新文章</h2><span class="st-sub">依建置順序排列，每篇皆為完整內容</span></div>'
              '<div class="clamp-box" data-clamp data-clamp-memo="home-latest">'
              '<div class="clamp-content"><div class="clamp-more-list">' + recent_items + '</div></div>'
              '</div></section>')
    cloud_small = '<div class="tag-cloud">' + ''.join(
        '<a href="tags/' + tg + '.html">#' + tg + '</a>' for tg, arts in sorted(tag_map.items(), key=lambda x: -len(x[1]))[:24]) + '</div>'
    body_html = ('<div class="wrap" style="padding-top:26px">' + hero +
                 latest +
                 '<section><div class="section-title"><h2>從文具控到鋼筆控～這些那些鋼筆知識百科</h2><span class="st-sub">點擊卡片展開章節說明</span></div>'
                 '<div class="grid">' + ch_cards + '</div></section>' +
                 '<section><div class="section-title"><h2>檢索工具</h2></div><div class="sub-list">'
                 '<a class="sub-row" href="az-index.html"><div class="n">A–Z</div><div><div class="t">字母索引</div><div class="d">依英文字母瀏覽全站 103 篇文章</div></div></a>'
                 '<a class="sub-row" href="glossary/index.html"><div class="n">詞彙</div><div><div class="t">詞彙辭典</div><div class="d">鋼筆術語 A–Z 中英對照</div></div></a>'
                 '<a class="sub-row" href="search.html"><div class="n">搜尋</div><div><div class="t">全站搜尋</div><div class="d">關鍵字檢索文章、章節與標籤</div></div></a>'
                 '<a class="sub-row" href="sitemap.xml"><div class="n">站點</div><div><div class="t">Sitemap</div><div class="d">網站地圖（爬蟲專用）</div></div></a>'
                 '</div></section></div>')
    jld = [
        {'@context': 'https://schema.org', '@type': 'WebSite', 'name': site['site']['name'],
         'url': root_url, 'inLanguage': 'zh-Hant',
         'potentialAction': {'@type': 'SearchAction', 'target': root_url + 'search.html?q={search_term_string}',
                             'query-input': 'required name=search_term_string'}},
        {'@context': 'https://schema.org', '@type': 'ItemList', 'name': '章節索引',
         'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': c['zh'],
                              'url': root_url + c['url']} for i, c in enumerate(chapters_out)]},
    ]
    write(out_rel, page_html(site, rel, site['site']['name'], site['site']['desc'], out_rel,
                             crumb, body_html, jld, {'slug': None, 'chapter': None}))
    print('  ✓ index.html')

    # ============ A–Z 字母索引 ============
    def az_key(a):
        en = a.get('en', '') or ''
        m = re.match(r'^[A-Za-z]', en)
        if m:
            return m.group(0).upper()
        m2 = re.match(r'^[A-Za-z]', a.get('title', ''))
        if m2:
            return m2.group(0).upper()
        return '中'
    az_groups = {}
    for a in flat:
        k = az_key(a)
        az_groups.setdefault(k, []).append(a)
    letters = sorted(az_groups.keys(), key=lambda x: (x != '中', x))
    az_nav = '<nav class="az-nav">' + ''.join('<a href="#az-%s">%s</a>' % (l, l) for l in letters) + '</nav>'
    az_body = ''.join('<div class="az-group" id="az-%s"><h3>%s</h3><div class="az-items">%s</div></div>' % (
        l, l,
        ''.join('<a class="az-item" href="' + a['url'] + '"><span class="az-t">' + a['title'] + '</span>'
                '<span class="az-m">' + a['cat'] + '</span></a>' for a in sorted(az_groups[l], key=lambda x: x['title']))
    ) for l in letters)
    out_rel = 'az-index.html'
    rel = ''
    crumb = crumb_home(rel) + '<span class="crumb-current">A–Z 字母索引</span>'
    body_html = ('<div class="wrap" style="padding-top:26px">'
                 '<div class="page-head"><div class="eyebrow">ALPHABETICAL INDEX</div>'
                 '<h1 class="page-title">A–Z 字母索引</h1>'
                 '<p class="page-desc">依英文名稱首字母，將全站文章分組排列；詞彙章節另有專屬術語索引。</p></div>'
                 + az_nav + az_body + '</div>')
    jld = [breadcrumb_list(site, [('首頁', 'index.html'), ('A–Z 字母索引', out_rel)])]
    write(out_rel, page_html(site, rel, 'A–Z 字母索引｜' + site['site']['name'], '全站文章英文字母索引。', out_rel,
                             crumb, body_html, jld, {'slug': None, 'chapter': None}))
    print('  ✓ %s' % out_rel)

    # ============ 詞彙章節頁（A–Z 術語索引） ============
    out_rel = 'glossary/index.html'
    rel = '../'
    gl = next(c for c in chapters_out if c['id'] == 'glossary')
    gl_flat = [a for a in flat if a['chapter'] == 'glossary']
    gz_groups = {}
    for a in gl_flat:
        k = az_key(a)
        gz_groups.setdefault(k, []).append(a)
    gz_body = '<div class="az-nav">' + ''.join('<a href="#gaz-%s">%s</a>' % (l, l) for l in sorted(gz_groups)) + '</div>'
    gz_body += ''.join('<div class="az-group" id="gaz-%s"><h3>%s</h3><div class="az-items">%s</div></div>' % (
        l, l,
        ''.join('<a class="az-item" href="' + rel + a['url'] + '"><span class="az-t">' + a['title'] + '</span>'
                '<span class="az-m">' + a['difficulty'] + '</span></a>' for a in sorted(gz_groups[l], key=lambda x: x['title']))
    ) for l in sorted(gz_groups))
    crumb = (crumb_home(rel) + '<a href="' + rel + 'glossary/index.html">詞彙</a><span class="crumb-sep">/</span>'
             + '<span class="crumb-current">術語 A–Z 索引</span>')
    body_html = ('<div class="layout cols-2"><aside class="sidebar" id="sidebar"></aside><main class="main">'
                 '<div class="page-head"><div class="eyebrow">GLOSSARY</div>'
                 '<h1 class="page-title">詞彙辭典（A–Z）</h1>'
                 '<p class="page-desc">鋼筆圈術語的中英對照與深度解析，按英文首字母索引。</p>'
                 '<div class="page-stats"><span><b>' + str(len(gl_flat)) + '</b> 篇術語文章</span></div></div>'
                 + gz_body + '</main></div>')
    jld = [breadcrumb_list(site, [('首頁', 'index.html'), ('詞彙', out_rel)]),
           {'@context': 'https://schema.org', '@type': 'ItemList', 'name': '詞彙 A–Z',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': a['title'],
                                 'url': root_url + a['url']} for i, a in enumerate(gl_flat)]}]
    write(out_rel, page_html(site, rel, '詞彙辭典 A–Z｜' + site['site']['name'], '鋼筆術語中英對照與深度解析。', out_rel,
                             crumb, body_html, jld, {'slug': None, 'chapter': 'glossary'}))
    print('  ✓ %s' % out_rel)

    # ============ 搜尋頁 ============
    out_rel = 'search.html'
    rel = ''
    crumb = crumb_home(rel) + '<span class="crumb-current">全站搜尋</span>'
    body_html = (
        '<div class="wrap" style="padding-top:26px">'
        '<div class="page-head"><div class="eyebrow">SEARCH</div><h1 class="page-title">全站搜尋</h1>'
        '<p class="page-desc">輸入關鍵字，即時檢索文章標題、章節、標籤與摘要。</p></div>'
        '<div class="searchbox" style="width:100%;max-width:560px">' + ICON_SEARCH +
        '<input type="text" id="qInput" placeholder="例如：筆尖、墨水、清洗、萬寶龍…" aria-label="搜尋" autocomplete="off">'
        '<div class="search-results"></div></div>'
        '<main id="qResults" style="margin-top:22px"></main></div>'
        '<script>(function(){var i=document.getElementById(\'qInput\');var res=document.getElementById(\'qResults\');'
        'function esc(s){return s.replace(/[&<>"]/g,function(c){return{\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'\"\':\'&quot;\'}[c];});}'
        'function run(q){if(!q){res.innerHTML=\'\';return;}q=q.trim().toLowerCase();var h=[];'
        'PEN.articles.forEach(function(a){var hay=(a.title+\' \'+a.tags.join(\' \')+\' \'+a.summary+\' \'+a.cat).toLowerCase();'
        'if(hay.indexOf(q)>=0)h.push(a);});'
        'res.innerHTML=h.length?\'<div class="grid">\'+h.map(function(a){return\'<a class="card" href="\'+a.url+\'">'
        '<div class="card-num">\'+esc(a.cat)+\'</div><div class="card-title">\'+esc(a.title)+\'</div>'
        '<div class="card-meta">\'+esc(a.difficulty)+\' · 更新 \'+esc(a.updated)+\'</div></a>\';}).join(\'\')+\'</div>\''
        ':\'<p style="color:var(--fg-mute)">沒有符合「\'+esc(i.value)+\'」的結果。</p>\';}'
        'i.addEventListener(\'input\',function(){run(i.value);});'
        'var q=new URLSearchParams(location.search).get(\'q\');if(q){i.value=q;run(q);}'
        '})();</script></div>'
    )
    jld = [breadcrumb_list(site, [('首頁', 'index.html'), ('全站搜尋', out_rel)])]
    write(out_rel, page_html(site, rel, '全站搜尋｜' + site['site']['name'], '全站關鍵字搜尋。', out_rel,
                             crumb, body_html, jld, {'slug': None, 'chapter': None}))
    print('  ✓ %s' % out_rel)

    # ============ config.js（前端導覽/搜尋資料） ============
    tag_cfg = {t: {'url': 'tags/%s.html' % t, 'count': len(v)} for t, v in tag_map.items()}
    cfg = {
        'site': {'name': site['site']['name'], 'version': site['site']['version'], 'updated': site['site']['updated']},
        'current': {'slug': None, 'chapter': None},
        'chapters': chapters_out,
        'articles': flat,
        'tags': tag_cfg,
    }
    js = '/* 由 build.py 自動產生 — 請勿手動編輯 */\nwindow.PEN = ' + json.dumps(cfg, ensure_ascii=False) + ';\n'
    write('assets/js/config.js', js)
    print('  ✓ assets/js/config.js')

    # ============ data/articles.json（資料檔） ============
    write('data/articles.json', json.dumps(
        {'site': site['site'], 'updated': site['site']['updated'],
         'articles': [{k: a[k] for k in ('slug', 'title', 'url', 'cat', 'tags', 'difficulty', 'updated', 'summary', 'chapter', 'sub')} for a in flat]},
        ensure_ascii=False, indent=1))
    print('  ✓ data/articles.json')

    # ============ sitemap.xml ============
    urls = [('index.html', site['site']['updated']), ('search.html', site['site']['updated']),
            ('az-index.html', site['site']['updated']), ('tags/index.html', site['site']['updated'])]
    for c in site['chapters']:
        urls.append(('%s/index.html' % c['id'], site['site']['updated']))
        for s in c['subs']:
            urls.append(('%s/%s/index.html' % (c['id'], s['id']), site['site']['updated']))
    for a in flat:
        urls.append((a['url'], a['updated']))
    for tg in tag_map:
        urls.append(('tags/%s.html' % tg, site['site']['updated']))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, last in urls:
        sitemap.append('  <url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq></url>'
                       % (root_url, u, last))
    sitemap.append('</urlset>')
    write('sitemap.xml', '\n'.join(sitemap) + '\n')
    print('  ✓ sitemap.xml（%d 條 URL）' % len(urls))

    # ============ robots.txt ============
    write('robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % root_url)
    print('  ✓ robots.txt')

    return True, articles, order, []


# ============================================================
# 主流程
# ============================================================
def main():
    args = sys.argv[1:]
    site = load_site()
    # i文具控章節只保留「關於i文具控」一篇
    site['articles'] = [a for a in site['articles'] if not (a.get('chapter')=='tylee' and a.get('sub')!='about')]
    plan = plan_articles(site)

    if '--list' in args:
        chs = {}
        for a in site['articles']:
            chs.setdefault(a['chapter'], 0)
            chs[a['chapter']] += 1
        print('規劃文章總數：%d' % len(site['articles']))
        for c in site['chapters']:
            print('  %s：%d 篇' % (c['zh'], chs.get(c['id'], 0)))
        return

    if '--check' in args:
        idx = args.index('--check')
        target = args[idx + 1] if idx + 1 < len(args) else None
        problems = []
        if target:
            if os.path.isdir(target):
                files = [os.path.join(dp, fn) for dp, _d, fns in os.walk(target) for fn in fns if fn.endswith('.md')]
            else:
                files = [target]
            for p in files:
                meta, body = parse_file(p)
                errs, warns = validate_article(meta, body, p, site, plan)
                slug = meta.get('slug', os.path.basename(p)[:-3])
                for e in errs:
                    problems.append('  ✗ [%s] %s' % (slug, e))
                for w in warns:
                    print('  ⚠ [%s] %s' % (slug, w))
        else:
            # 全量檢查
            for dp, _d, fns in os.walk(ART_DIR):
                for fn in fns:
                    if fn.endswith('.md'):
                        p = os.path.join(dp, fn)
                        meta, body = parse_file(p)
                        errs, warns = validate_article(meta, body, p, site, plan)
                        slug = meta.get('slug', fn[:-3])
                        for e in errs:
                            problems.append('  ✗ [%s] %s' % (slug, e))
                        for w in warns:
                            print('  ⚠ [%s] %s' % (slug, w))
        # 完整性
        have = set()
        for dp, _d, fns in os.walk(ART_DIR):
            for fn in fns:
                if fn.endswith('.md'):
                    meta, _b = parse_file(os.path.join(dp, fn))
                    if meta.get('slug'):
                        have.add(meta['slug'])
        miss = [a['slug'] for a in site['articles'] if a['slug'] not in have]
        if miss:
            problems.append('  遺漏內容檔（%d 篇）：%s' % (len(miss), ', '.join(miss)))
        if problems:
            print('檢查未通過，共 %d 項問題：' % len(problems))
            for p in problems:
                print(p)
            print('總計：已撰寫 %d / %d 篇' % (len(have), len(site['articles'])))
            sys.exit(1)
        print('檢查通過：%d / %d 篇內容就緒，無錯誤。' % (len(have), len(site['articles'])))
        return

    print('開始建置「%s」…' % site['site']['name'])
    ok, _arts, _order, miss = build(site, force='--force' in args)
    if not ok:
        sys.exit(1)
    print('建置完成。' if not miss else ('建置完成，但有 %d 篇遺漏：%s' % (len(miss), ', '.join(miss))))


if __name__ == '__main__':
    main()

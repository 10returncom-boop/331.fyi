/**
 * build-sitemap.js — 自動產生 sitemap
 * 用法：node build-sitemap.js
 * 功能：
 *   1. 掃描所有 HTML 檔
 *   2. 產生 article-sitemap.xml（主題 hub 頁）
 *   3. 產生 gallery-sitemap.xml（style-*.html 深讀文章頁）
 *   4. 產生 sitemap-index.xml（總索引）
 *   5. 排除 noindex / 404 頁面
 */
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const SITE_URL = "https://nutrition.example.com";

/** 遞迴掃描所有 .html 檔 */
function scanHtml(dir) {
  let results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".") || entry.name === "node_modules") continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results = results.concat(scanHtml(full));
    } else if (entry.name.endsWith(".html")) {
      results.push(full);
    }
  }
  return results;
}

/** 讀取 HTML 內容，判斷是否 noindex */
function isNoindex(file) {
  const html = fs.readFileSync(file, "utf8");
  return /name="robots"\s+content="noindex/.test(html);
}

/** 取得 lastmod（檔案修改日期 YYYY-MM-DD） */
function lastmod(file) {
  const stat = fs.statSync(file);
  return stat.mtime.toISOString().slice(0, 10);
}

/** 產生單一 url entry */
function urlEntry(relPath, priority) {
  const full = path.join(ROOT, relPath);
  return `  <url>
    <loc>${SITE_URL}/${relPath.replace(/\\/g, "/")}</loc>
    <lastmod>${lastmod(full)}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>${priority}</priority>
  </url>`;
}

/** 主流程 */
function main() {
  const files = scanHtml(ROOT).filter((f) => !isNoindex(f));

  // 分類：hub 頁 vs gallery 頁
  const hubPages = [];
  const galleryPages = [];

  for (const file of files) {
    const rel = path.relative(ROOT, file).replace(/\\/g, "/");
    if (rel === "404.html") continue;
    if (/style-.*\.html$/.test(rel)) {
      galleryPages.push(rel);
    } else {
      hubPages.push(rel);
    }
  }

  // 產生 article-sitemap.xml
  const hubXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${hubPages.map((p) => urlEntry(p, p === "index.html" ? "1.0" : "0.9")).join("\n")}
</urlset>`;
  fs.writeFileSync(path.join(ROOT, "article-sitemap.xml"), hubXml, "utf8");
  console.log(`article-sitemap.xml: ${hubPages.length} pages`);

  // 產生 gallery-sitemap.xml
  const galleryXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${galleryPages.map((p) => urlEntry(p, "0.8")).join("\n")}
</urlset>`;
  fs.writeFileSync(path.join(ROOT, "gallery-sitemap.xml"), galleryXml, "utf8");
  console.log(`gallery-sitemap.xml: ${galleryPages.length} pages`);

  // 產生 sitemap-index.xml
  const today = new Date().toISOString().slice(0, 10);
  const indexXml = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>${SITE_URL}/article-sitemap.xml</loc>
    <lastmod>${today}</lastmod>
  </sitemap>
  <sitemap>
    <loc>${SITE_URL}/gallery-sitemap.xml</loc>
    <lastmod>${today}</lastmod>
  </sitemap>
</sitemapindex>`;
  fs.writeFileSync(path.join(ROOT, "sitemap-index.xml"), indexXml, "utf8");
  console.log("sitemap-index.xml: generated");
}

main();

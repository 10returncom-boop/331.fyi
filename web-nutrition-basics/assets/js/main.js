/* =========================================================
   營養與生活 — 共享 JS (main.js)
   純 Vanilla JS，無框架、無 jQuery
   功能：MegaMenu、搜尋 autocomplete、Accordion、TOC、
        收藏清單(localStorage)、浮動導覽、Tag 篩選
   ========================================================= */
(function () {
  "use strict";

  /* ---------- 1. 漢堡選單（行動版） ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("mainNav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
    });
    // 手機版 MegaMenu 展開
    document.querySelectorAll(".nav-item > .nav-link").forEach(function (link) {
      link.addEventListener("click", function (e) {
        var item = link.parentElement;
        if (window.innerWidth < 900 && item.querySelector(".mega")) {
          e.preventDefault();
          item.classList.toggle("open");
        }
      });
    });
  }

  /* ---------- 2. Accordion 折疊卡片 ---------- */
  document.querySelectorAll(".acc-head").forEach(function (head) {
    head.addEventListener("click", function () {
      var item = head.parentElement;
      var isOpen = item.classList.contains("open");
      // 同群組只開一個（若有 data-single）
      var singleGroup = item.closest("[data-single]");
      if (singleGroup) {
        singleGroup.querySelectorAll(".acc-item.open").forEach(function (o) {
          o.classList.remove("open");
          o.querySelector(".acc-head").setAttribute("aria-expanded", "false");
        });
      }
      item.classList.toggle("open", !isOpen);
      head.setAttribute("aria-expanded", String(!isOpen));
    });
  });

  /* ---------- 3. 全站搜尋 + Autocomplete ---------- */
  var searchInput = document.getElementById("siteSearch");
  var acBox = document.getElementById("acBox");
  if (searchInput && acBox && window.SEARCH_INDEX) {
    var debounce;
    searchInput.addEventListener("input", function () {
      clearTimeout(debounce);
      debounce = setTimeout(function () {
        var q = searchInput.value.trim().toLowerCase();
        if (q.length < 2) { acBox.classList.remove("open"); acBox.innerHTML = ""; return; }
        var hits = window.SEARCH_INDEX.filter(function (p) {
          return p.title.toLowerCase().indexOf(q) > -1 ||
                 p.tags.some(function (t) { return t.toLowerCase().indexOf(q) > -1; }) ||
                 p.desc.toLowerCase().indexOf(q) > -1;
        }).slice(0, 8);
        if (hits.length === 0) {
          acBox.innerHTML = '<div class="ac-empty">找不到「' + escapeHtml(q) + '」相關內容，試試其他關鍵字</div>';
        } else {
          acBox.innerHTML = hits.map(function (p) {
            return '<a class="ac-item" href="' + p.url + '">' +
                   '<div class="ac-title">' + escapeHtml(p.title) + '</div>' +
                   '<div class="ac-path">' + escapeHtml(p.breadcrumb || p.url) + '</div></a>';
          }).join("");
        }
        acBox.classList.add("open");
      }, 120);
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".search-wrap")) acBox.classList.remove("open");
    });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------- 4. TOC 捲動偵測（scroll-spy） ---------- */
  var tocLinks = document.querySelectorAll(".toc-list a[href^='#']");
  if (tocLinks.length) {
    var sections = Array.prototype.map.call(tocLinks, function (a) {
      var el = document.querySelector(a.getAttribute("href"));
      return el ? { link: a, el: el } : null;
    }).filter(Boolean);
    window.addEventListener("scroll", function () {
      var pos = window.scrollY + 120;
      var current = null;
      sections.forEach(function (s) { if (s.el.offsetTop <= pos) current = s; });
      tocLinks.forEach(function (a) { a.classList.remove("active"); });
      if (current) current.link.classList.add("active");
    }, { passive: true });
  }

  /* ---------- 5. 收藏清單（localStorage） ---------- */
  var BM_KEY = "nl_bookmarks";
  function getBM() { try { return JSON.parse(localStorage.getItem(BM_KEY)) || []; } catch (e) { return []; } }
  function setBM(list) { localStorage.setItem(BM_KEY, JSON.stringify(list)); renderBM(); }

  document.querySelectorAll("[data-bookmark]").forEach(function (btn) {
    var url = btn.getAttribute("data-bookmark");
    var list = getBM();
    if (list.indexOf(url) > -1) btn.classList.add("bookmarked");
    btn.addEventListener("click", function () {
      var cur = getBM();
      var idx = cur.indexOf(url);
      if (idx > -1) { cur.splice(idx, 1); btn.classList.remove("bookmarked"); }
      else { cur.push(url); btn.classList.add("bookmarked"); }
      setBM(cur);
    });
  });

  function renderBM() {
    var box = document.getElementById("bookmarkList");
    if (!box) return;
    var list = getBM();
    if (list.length === 0) { box.innerHTML = '<p class="meta">尚無收藏。點擊文章旁的「收藏」即可儲存到瀏覽器。</p>'; return; }
    box.innerHTML = '<ul>' + list.map(function (u) {
      return '<li><a href="' + u + '">' + u + '</a></li>';
    }).join("") + '</ul>';
  }
  renderBM();

  /* ---------- 6. 浮動導覽 ---------- */
  var fabTop = document.getElementById("fabTop");
  if (fabTop) {
    window.addEventListener("scroll", function () {
      fabTop.style.opacity = window.scrollY > 400 ? "1" : "0";
    }, { passive: true });
    fabTop.style.transition = "opacity .2s";
    fabTop.style.opacity = "0";
    fabTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }

  /* ---------- 7. Tag 篩選 ---------- */
  var tagFilters = document.querySelectorAll("[data-tag-filter]");
  if (tagFilters.length) {
    tagFilters.forEach(function (tag) {
      tag.addEventListener("click", function (e) {
        e.preventDefault();
        var t = tag.getAttribute("data-tag-filter");
        document.querySelectorAll("[data-tag-filter]").forEach(function (x) { x.classList.remove("active"); });
        tag.classList.add("active");
        document.querySelectorAll("[data-tags]").forEach(function (card) {
          var tags = (card.getAttribute("data-tags") || "").split(/\s+/);
          card.style.display = (t === "all" || tags.indexOf(t) > -1) ? "" : "none";
        });
      });
    });
  }

  /* ---------- 8. 年份自動帶入 ---------- */
  var yr = document.getElementById("yr");
  if (yr) yr.textContent = new Date().getFullYear();

  /* ============================================================
     新增 30 項功能擴充
     ============================================================ */

  /* F1. 閱讀進度條 */
  var progressBar = document.createElement("div");
  progressBar.className = "read-progress";
  document.body.appendChild(progressBar);
  window.addEventListener("scroll", function () {
    var h = document.documentElement;
    var pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
    progressBar.style.width = pct + "%";
  }, { passive: true });

  /* F2. 深色模式切換 */
  var savedTheme = localStorage.getItem("nl_theme");
  if (savedTheme === "dark") document.documentElement.setAttribute("data-theme", "dark");
  var themeBtn = document.getElementById("themeToggle");
  if (themeBtn) {
    themeBtn.textContent = savedTheme === "dark" ? "☀" : "☾";
    themeBtn.addEventListener("click", function () {
      var cur = document.documentElement.getAttribute("data-theme");
      if (cur === "dark") {
        document.documentElement.removeAttribute("data-theme");
        localStorage.setItem("nl_theme", "light");
        themeBtn.textContent = "☾";
      } else {
        document.documentElement.setAttribute("data-theme", "dark");
        localStorage.setItem("nl_theme", "dark");
        themeBtn.textContent = "☀";
      }
    });
  }

  /* F3. 字級切換 */
  var savedFont = localStorage.getItem("nl_fontsize");
  if (savedFont) document.body.classList.add("font-" + savedFont);
  document.querySelectorAll("[data-font]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var f = btn.getAttribute("data-font");
      document.body.classList.remove("font-sm", "font-lg");
      if (f !== "md") document.body.classList.add("font-" + f);
      localStorage.setItem("nl_fontsize", f === "md" ? "" : f);
    });
  });

  /* F4. 社交分享 */
  document.querySelectorAll("[data-share]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var type = btn.getAttribute("data-share");
      var url = encodeURIComponent(location.href);
      var title = encodeURIComponent(document.title);
      var shareUrl = "";
      if (type === "fb") shareUrl = "https://www.facebook.com/sharer/sharer.php?u=" + url;
      else if (type === "line") shareUrl = "https://social-plugins.line.me/lineit/share?url=" + url;
      else if (type === "twitter") shareUrl = "https://twitter.com/intent/tweet?url=" + url + "&text=" + title;
      else if (type === "email") shareUrl = "mailto:?subject=" + title + "&body=" + url;
      if (shareUrl) window.open(shareUrl, "_blank", "width=600,height=500");
    });
  });

  /* F5. 列印文章 */
  document.querySelectorAll("[data-print]").forEach(function (btn) {
    btn.addEventListener("click", function () { window.print(); });
  });

  /* F6. 複製連結 */
  document.querySelectorAll("[data-copy-link]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(location.href).then(function () {
        var orig = btn.textContent;
        btn.textContent = "✓ 已複製";
        setTimeout(function () { btn.textContent = orig; }, 1500);
      });
    });
  });

  /* F7. 閱讀時間估計 */
  var articleBody = document.querySelector(".article-body, .content-main");
  if (articleBody) {
    var text = articleBody.innerText || "";
    var words = text.length;
    var minutes = Math.max(1, Math.round(words / 400));
    var rt = document.getElementById("readTime");
    if (rt) rt.textContent = "約 " + minutes + " 分鐘";
    var wc = document.getElementById("wordCount");
    if (wc) wc.textContent = words.toLocaleString() + " 字";
  }

  /* F8. 最近瀏覽（localStorage） */
  (function () {
    var KEY = "nl_recent";
    var recent = [];
    try { recent = JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) {}
    var entry = { url: location.pathname, title: document.title };
    recent = recent.filter(function (r) { return r.url !== entry.url; });
    recent.unshift(entry);
    recent = recent.slice(0, 5);
    try { localStorage.setItem(KEY, JSON.stringify(recent)); } catch (e) {}
    var box = document.getElementById("recentList");
    if (box) {
      box.innerHTML = recent.map(function (r) {
        return '<li><a href="' + r.url + '">' + escapeHtml(r.title) + '</a></li>';
      }).join("");
    }
  })();

  /* F9. 搜尋歷史 */
  if (searchInput) {
    searchInput.addEventListener("focus", function () {
      var history = [];
      try { history = JSON.parse(localStorage.getItem("nl_search_history")) || []; } catch (e) {}
      if (history.length > 0 && searchInput.value === "") {
        acBox.innerHTML = '<div class="search-history">最近搜尋：' +
          history.map(function (h) {
            return '<span class="sh-item" data-q="' + escapeHtml(h) + '">' + escapeHtml(h) + '</span>';
          }).join("") + '</div>';
        acBox.classList.add("open");
        acBox.querySelectorAll(".sh-item").forEach(function (el) {
          el.addEventListener("click", function () {
            searchInput.value = el.getAttribute("data-q");
            acBox.classList.remove("open");
            searchInput.dispatchEvent(new Event("input"));
          });
        });
      }
    });
    // 儲存搜尋歷史
    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && searchInput.value.trim().length >= 2) {
        var history = [];
        try { history = JSON.parse(localStorage.getItem("nl_search_history")) || []; } catch (e2) {}
        history = history.filter(function (h) { return h !== searchInput.value.trim(); });
        history.unshift(searchInput.value.trim());
        history = history.slice(0, 8);
        try { localStorage.setItem("nl_search_history", JSON.stringify(history)); } catch (e3) {}
      }
    });
  }

  /* F10. Cookie 同意 */
  if (!localStorage.getItem("nl_cookie_ok")) {
    var cookie = document.createElement("div");
    cookie.className = "cookie-banner";
    cookie.innerHTML = '<p>本網站使用 localStorage 儲存你的收藏與閱讀偏好（無追蹤、無第三方 Cookie）。繼續瀏覽即表示同意。</p>' +
      '<button class="btn" id="cookieAccept">我知道了</button>';
    document.body.appendChild(cookie);
    document.getElementById("cookieAccept").addEventListener("click", function () {
      localStorage.setItem("nl_cookie_ok", "1");
      cookie.remove();
    });
  }

  /* F11. 公告列（可關閉） */
  document.querySelectorAll(".announce-close").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.parentElement.remove();
    });
  });

  /* F12. 右側邊垂直中間 Line 按鈕 */
  if (!document.querySelector(".line-side-btn")) {
    var inSubfolder = /\/(courses|nutrition-basics|diet-disease|life-stage|food-guide|lifestyle)\//.test(location.pathname);
    var prefix = inSubfolder ? "../" : "";
    var lineBtn = document.createElement("a");
    lineBtn.className = "line-side-btn";
    lineBtn.href = "https://line.me/ti/p/g-FTLSqJAR";
    lineBtn.target = "_blank";
    lineBtn.rel = "noopener";
    lineBtn.title = "加入Line好友";
    lineBtn.innerHTML = '<img src="' + prefix + 'assets/images/line-icon.png" alt="LINE" width="42" height="42">';
    document.body.appendChild(lineBtn);
  }

})();

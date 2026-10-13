/* =========================================================
   有AI了還有學甚麼? — 全站互動 (main.js)
   ========================================================= */
(function () {
  'use strict';

  /* 閱讀進度條 */
  var bar = document.querySelector('.read-progress');
  if (bar) {
    function onScroll() {
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      bar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* 行動裝置選單 */
  var navToggle = document.querySelector('.nav-toggle');
  var mainNav = document.querySelector('.main-nav');
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function () {
      mainNav.classList.toggle('open');
    });
  }

  /* Accordion 摺疊 */
  document.querySelectorAll('.accordion').forEach(function (acc) {
    var single = acc.hasAttribute('data-single');
    acc.querySelectorAll('.acc-item').forEach(function (item) {
      var head = item.querySelector('.acc-head');
      if (!head) return;
      head.addEventListener('click', function () {
        var open = item.classList.contains('open');
        if (single) {
          acc.querySelectorAll('.acc-item.open').forEach(function (o) {
            o.classList.remove('open');
            var h = o.querySelector('.acc-head'); if (h) h.setAttribute('aria-expanded', 'false');
          });
        }
        if (!open) {
          item.classList.add('open');
          head.setAttribute('aria-expanded', 'true');
        }
      });
    });
  });

  /* 側欄 TOC 捲動高亮 */
  var toc = document.querySelector('.toc-list');
  if (toc) {
    var links = toc.querySelectorAll('a[href^="#"]');
    var map = [];
    links.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var el = document.getElementById(id);
      if (el) map.push({ a: a, el: el });
    });
    function highlight() {
      var pos = window.scrollY + 120;
      var cur = null;
      map.forEach(function (m) { if (m.el.offsetTop <= pos) cur = m; });
      links.forEach(function (a) { a.classList.remove('active'); });
      if (cur) cur.a.classList.add('active');
    }
    window.addEventListener('scroll', highlight, { passive: true });
    highlight();
  }

  /* 回到頂端 */
  var fabTop = document.getElementById('fabTop');
  if (fabTop) {
    fabTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }

  /* 深色模式切換（localStorage 記住） */
  var themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    function apply(t) {
      document.documentElement.setAttribute('data-theme', t);
      try { localStorage.setItem('ai-course-theme', t); } catch (e) {}
    }
    themeBtn.addEventListener('click', function () {
      var cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      apply(cur);
      themeBtn.textContent = cur === 'dark' ? '☾' : '☀';
    });
    var saved = null;
    try { saved = localStorage.getItem('ai-course-theme'); } catch (e) {}
    if (saved === 'dark') apply('dark');
    if (document.documentElement.getAttribute('data-theme') === 'dark') themeBtn.textContent = '☀';
  }
})();

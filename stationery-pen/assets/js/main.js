/* ============================================================
   main.js — 啟動各模組、防複製保護、FAQ 摺疊、回到頂端
   ============================================================ */
(function () {
  function initFaq() {
    var items = document.querySelectorAll('.faq-item');
    for (var i = 0; i < items.length; i++) {
      var q = items[i].querySelector('.faq-q');
      if (q) q.addEventListener('click', function () {
        var item = this.parentNode;
        var open = item.classList.contains('open');
        // 手風琴：同頁其他項目收合
        var siblings = item.parentNode.querySelectorAll('.faq-item.open');
        for (var s = 0; s < siblings.length; s++) siblings[s].classList.remove('open');
        item.classList.toggle('open', !open);
      });
    }
  }

  /* 首頁章節 accordion 開合 */
  function initAccordion() {
    var cards = document.querySelectorAll('.acc-card');
    cards.forEach(function (card) {
      var head = card.querySelector('.acc-head');
      if (!head) return;
      head.addEventListener('click', function () {
        var isOpen = card.classList.contains('open');
        cards.forEach(function (c) { c.classList.remove('open'); });
        if (!isOpen) card.classList.add('open');
      });
    });
  }

  function initBackTop() {
    var btn = document.getElementById('backTop');
    if (!btn) return;
    function upd() { btn.classList.toggle('show', document.documentElement.scrollTop > 600); }
    btn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    document.addEventListener('scroll', upd, { passive: true });
    upd();
  }

  /* 防複製保護（依 _WWW_325 規格） */
  function initCopyProtect() {
    document.addEventListener('contextmenu', function (e) { e.preventDefault(); });
    var blocked = false;
    document.addEventListener('copy', function (e) {
      e.preventDefault();
      if (!blocked) {
        blocked = true;
        if (window.showToast) window.showToast('本站內容已開啟防複製保護，如需引用請聯絡站方。');
        setTimeout(function () { blocked = false; }, 1600);
      }
    });
  }

  /* 回到頂端按鈕樣式由 CSS 控制，此處僅綁定行為 */
  /* TOC 滾動偵測（文章右欄目錄 active 狀態） */
  function initTocSpy() {
    var links = document.querySelectorAll('.rail-toc a');
    if (!links.length) return;
    var heads = [];
    for (var i = 0; i < links.length; i++) {
      var id = links[i].getAttribute('href').slice(1);
      var h = document.getElementById(id);
      if (h) heads.push({ el: h, link: links[i] });
    }
    if (!heads.length) return;
    function upd() {
      var pos = document.documentElement.scrollTop + 140;
      var cur = null;
      for (var j = 0; j < heads.length; j++) {
        if (heads[j].el.offsetTop <= pos) cur = heads[j].link;
      }
      for (var k = 0; k < links.length; k++) links[k].classList.toggle('active', links[k] === cur);
    }
    document.addEventListener('scroll', upd, { passive: true });
    upd();
  }

  function init() {
    initFaq();
    initAccordion();
    initBackTop();
    initTocSpy();
    initCopyProtect();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

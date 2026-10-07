/* ============================================================
   reading.js — 閱讀進度條、收藏清單（localStorage）、列印匯出
   ============================================================ */
(function () {
  var FAV_KEY = 'pen-favs';

  function penUrl(u) {
    if (!u) return u;
    if (/^(?:[a-z]+:|#|\/)/i.test(u)) return u;
    var d = window.PEN_DEPTH || 0, p = '';
    while (d-- > 0) p += '../';
    return p + u;
  }

  function toast(msg) {
    var t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._timer);
    t._timer = setTimeout(function () { t.classList.remove('show'); }, 1800);
  }
  window.showToast = toast;

  /* 閱讀進度條 */
  function initProgress() {
    var bar = document.getElementById('progressBar');
    if (!bar) return;
    function upd() {
      var doc = document.documentElement;
      var total = doc.scrollHeight - doc.clientHeight;
      var p = total > 0 ? (doc.scrollTop / total) * 100 : 0;
      bar.style.width = p.toFixed(2) + '%';
    }
    document.addEventListener('scroll', upd, { passive: true });
    upd();
  }

  /* 收藏清單 */
  function getFavs() {
    try { return JSON.parse(localStorage.getItem(FAV_KEY)) || []; } catch (e) { return []; }
  }
  function setFavs(list) {
    try { localStorage.setItem(FAV_KEY, JSON.stringify(list)); } catch (e) {}
    renderFavDrawer();
    updateFavBadge();
  }
  function updateFavBadge() {
    var b = document.getElementById('favBadge');
    if (b) b.classList.toggle('show', getFavs().length > 0);
  }
  function renderFavDrawer() {
    var list = document.getElementById('favList');
    if (!list) return;
    var favs = getFavs();
    if (!favs.length) {
      list.innerHTML = '<div class="fav-empty">收藏清單是空的。<br>在文章頁點擊右上角「收藏」，即可在此建立你的閱讀清單。</div>';
      return;
    }
    var bySlug = {};
    (PEN ? PEN.articles : []).forEach(function (a) { bySlug[a.slug] = a; });
    list.innerHTML = favs.map(function (slug) {
      var a = bySlug[slug];
      if (!a) return '';
      return '<div class="fav-item"><span class="fi-c">收藏</span>' +
        '<a class="fi-t" href="' + penUrl(a.url) + '">' + a.title + '</a>' +
        '<button class="fi-x" data-rm="' + slug + '" title="移除收藏" aria-label="移除收藏">✕</button></div>';
    }).join('');
    list.querySelectorAll('[data-rm]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        setFavs(getFavs().filter(function (s) { return s !== btn.getAttribute('data-rm'); }));
        toast('已從收藏移除');
      });
    });
  }
  function initFav() {
    var btn = document.getElementById('favBtn');
    var drawer = document.getElementById('favDrawer');
    var mask = document.getElementById('favMask');
    var openBtn = document.getElementById('favOpen');
    if (btn && window.PEN && window.PEN.current) {
      var slug = window.PEN.current.slug;
      function syncBtn() {
        var faved = getFavs().indexOf(slug) >= 0;
        btn.classList.toggle('faved', faved);
        btn.innerHTML = faved
          ? '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21s-7-4.6-9.3-8.8C.6 8.6 2.4 5 5.8 5c2 0 3.4 1.1 4.2 2.4h4C14.8 6.1 16.2 5 18.2 5c3.4 0 5.2 3.6 3.1 7.2C19 16.4 12 21 12 21z"/></svg>已收藏'
          : '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-4.6-9.3-8.8C.6 8.6 2.4 5 5.8 5c2 0 3.4 1.1 4.2 2.4h4C14.8 6.1 16.2 5 18.2 5c3.4 0 5.2 3.6 3.1 7.2C19 16.4 12 21 12 21z"/></svg>收藏';
      }
      btn.addEventListener('click', function () {
        var favs = getFavs();
        var i = favs.indexOf(slug);
        if (i >= 0) { favs.splice(i, 1); toast('已取消收藏'); }
        else { favs.push(slug); toast('已加入收藏清單'); }
        setFavs(favs); syncBtn();
      });
      syncBtn();
    }
    if (openBtn) openBtn.addEventListener('click', function () {
      renderFavDrawer();
      if (drawer) drawer.classList.add('open');
      if (mask) mask.classList.add('show');
    });
    if (mask) mask.addEventListener('click', closeFav);
    function closeFav() {
      if (drawer) drawer.classList.remove('open');
      if (mask) mask.classList.remove('show');
    }
    var closeBtn = drawer ? drawer.querySelector('.fav-drawer-head .icon-btn') : null;
    if (closeBtn) closeBtn.addEventListener('click', closeFav);
    updateFavBadge();
  }

  /* 列印 / 匯出 PDF */
  function initPrint() {
    var btn = document.getElementById('printBtn');
    if (btn) btn.addEventListener('click', function () { window.print(); });
  }

  function init() {
    initProgress();
    initFav();
    initPrint();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

/* ============================================================
   search.js — 全站搜尋＋自動完成（即時建議文章 / 章節 / 標籤）
   資料來源：window.PEN（config.js）
   ============================================================ */
(function () {
  function penUrl(u) {
    if (!u) return u;
    if (/^(?:[a-z]+:|#|\/)/i.test(u)) return u;
    var d = window.PEN_DEPTH || 0, p = '';
    while (d-- > 0) p += '../';
    return p + u;
  }

  function initSearch(box) {
    if (!box || !window.PEN) return;
    var input = box.querySelector('input[type="text"],input:not([type])');
    if (!input) input = box.querySelector('input');
    var res = box.querySelector('.search-results');
    var clear = box.querySelector('.s-clear');
    if (!input || !res) return;

    function normalize(s) { return (s || '').toLowerCase(); }
    function show(q) {
      q = normalize(q.trim());
      if (!q) { res.classList.remove('open'); res.innerHTML = ''; return; }
      var qs = q.split(/\s+/);
      var hitArts = [], hitChs = [], hitTags = [];
      PEN.articles.forEach(function (a) {
        var hay = normalize(a.title + ' ' + a.tags.join(' ') + ' ' + a.summary + ' ' + a.cat);
        var all = qs.every(function (w) { return hay.indexOf(w) >= 0; });
        if (all) hitArts.push(a);
      });
      PEN.chapters.forEach(function (ch) {
        if (qs.every(function (w) { return normalize(ch.zh + ch.en).indexOf(w) >= 0; })) hitChs.push(ch);
      });
      Object.keys(PEN.tags).forEach(function (tg) {
        if (qs.every(function (w) { return normalize(tg).indexOf(w) >= 0; })) hitTags.push(tg);
      });
      var html = '';
      if (!hitArts.length && !hitChs.length && !hitTags.length) {
        html = '<div class="sr-empty">沒有符合「' + input.value.trim() + '」的結果，試試其他關鍵字（如：筆尖、墨水、清洗）。</div>';
      }
      if (hitChs.length) {
        html += '<div class="sr-group">章節</div>' + hitChs.slice(0, 5).map(function (ch) {
          return '<a class="sr-item" href="' + penUrl(ch.url) + '">' + ch.zh + '<span class="sr-k">' + ch.en + ' · ' + ch.nArts + ' 篇</span></a>';
        }).join('');
      }
      if (hitTags.length) {
        html += '<div class="sr-group">標籤</div>' + hitTags.slice(0, 5).map(function (tg) {
          return '<a class="sr-item" href="' + penUrl(PEN.tags[tg].url) + '">#' + tg + '<span class="sr-tag">' + PEN.tags[tg].count + ' 篇</span></a>';
        }).join('');
      }
      if (hitArts.length) {
        html += '<div class="sr-group">文章</div>' + hitArts.slice(0, 10).map(function (a) {
          return '<a class="sr-item" href="' + penUrl(a.url) + '">' + a.title + '<span class="sr-k">' + a.cat + '</span><span class="sr-tag">' + a.difficulty + '</span></a>';
        }).join('');
      }
      res.innerHTML = html;
      res.classList.add('open');
    }
    input.addEventListener('input', function () { show(input.value); if (clear) clear.style.display = input.value ? 'grid' : 'none'; });
    if (clear) clear.addEventListener('click', function () { input.value = ''; show(''); clear.style.display = 'none'; input.focus(); });
    document.addEventListener('click', function (e) {
      if (!box.contains(e.target)) res.classList.remove('open');
    });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { res.classList.remove('open'); input.blur(); }
    });
  }

  function init() {
    var boxes = document.querySelectorAll('.searchbox,.hero-search');
    for (var i = 0; i < boxes.length; i++) initSearch(boxes[i]);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

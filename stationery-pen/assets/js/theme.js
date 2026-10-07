/* ============================================================
   theme.js — 日夜主題切換（亮 / 暗 / 跟隨系統），localStorage 記憶
   ============================================================ */
(function () {
  var KEY = 'pen-theme';

  function systemDark() {
    try { return window.matchMedia('(prefers-color-scheme: dark)').matches; } catch (e) { return false; }
  }
  function resolve(t) {
    return (t === 'dark' || (t === 'system' && systemDark())) ? 'dark' : 'light';
  }
  function apply(t) {
    document.documentElement.setAttribute('data-theme', resolve(t));
    try { localStorage.setItem(KEY, t); } catch (e) {}
  }
  function init() {
    var t = 'system';
    try { t = localStorage.getItem(KEY) || 'system'; } catch (e) {}
    if (['light', 'dark', 'system'].indexOf(t) < 0) t = 'system';
    apply(t);
    var seg = document.getElementById('themeSeg');
    if (seg) {
      var btns = seg.querySelectorAll('button');
      function sync() {
        for (var i = 0; i < btns.length; i++) {
          btns[i].classList.toggle('active', btns[i].getAttribute('data-theme') === t);
        }
      }
      seg.addEventListener('click', function (e) {
        var b = e.target.closest('button');
        if (!b) return;
        t = b.getAttribute('data-theme');
        apply(t); sync();
      });
      sync();
    }
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    var onChange = function () { if (t === 'system') document.documentElement.setAttribute('data-theme', resolve(t)); };
    if (mq.addEventListener) mq.addEventListener('change', onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

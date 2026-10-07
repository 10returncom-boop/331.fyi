/* ============================================================
   breathe-clamp.js — BreatheClamp 可重用響應式元件
   用途：將過長內容「夾取」為可展開的折疊區塊，隨視窗寬度響應調整折疊高度。

   用法（HTML）：
     <div class="clamp-box" data-clamp>
       <div class="clamp-content">…很長的內容…</div>
     </div>

   行為：
     - 內容高度超過折疊上限（預設 7.2em ≈ 4 行）時，自動顯示「展開全部」按鈕；
     - 點擊後展開，按鈕變為「收合」；
     - 展開狀態以 sessionStorage 記憶（可選，data-clamp-memo）；
     - 視窗縮放時重新計算折疊高度，寬螢幕看更多、窄螢幕看更少。
   ============================================================ */
(function () {
  var DEFAULT_HEIGHT = 7.2; /* em */

  function realHeight(el) {
    var clone = el.cloneNode(true);
    clone.style.position = 'absolute';
    clone.style.visibility = 'hidden';
    clone.style.height = 'auto';
    clone.style.overflow = 'visible';
    el.parentNode.appendChild(clone);
    var h = clone.getBoundingClientRect().height;
    clone.parentNode.removeChild(clone);
    return h;
  }

  function cssEmHeight() {
    var body = document.body;
    var fs = parseFloat(getComputedStyle(body).fontSize) || 16;
    return fs * DEFAULT_HEIGHT;
  }

  function setup(root) {
    var content = root.querySelector('.clamp-content');
    if (!content) return;
    var btn = root.querySelector('.clamp-btn');
    var memoKey = root.getAttribute('data-clamp-memo') || null;

    function measure() {
      if (root.getAttribute('data-open') === 'true') return;
      var limit = cssEmHeight();
      var h = realHeight(content);
      if (h > limit) {
        root.classList.add('clamped');
        content.style.maxHeight = limit + 'px';
        if (!btn) {
          btn = document.createElement('button');
          btn.className = 'clamp-btn';
          btn.type = 'button';
          btn.textContent = '展開全部';
          root.appendChild(btn);
          btn.addEventListener('click', function () {
            var open = root.getAttribute('data-open') === 'true';
            root.setAttribute('data-open', open ? 'false' : 'true');
            content.style.maxHeight = open ? limit + 'px' : '';
            btn.textContent = open ? '展開全部' : '收合';
            if (memoKey) { try { sessionStorage.setItem('clamp-' + memoKey, open ? '0' : '1'); } catch (e) {} }
          });
        }
      } else {
        root.classList.remove('clamped');
        if (btn) { btn.remove(); btn = null; }
        content.style.maxHeight = '';
      }
    }
    root._breatheMeasure = measure;
    measure();
  }

  function init() {
    var boxes = document.querySelectorAll('[data-clamp]');
    for (var i = 0; i < boxes.length; i++) {
      var memo = boxes[i].getAttribute('data-clamp-memo');
      if (memo) {
        try {
          if (sessionStorage.getItem('clamp-' + memo) === '1') {
            boxes[i].setAttribute('data-open', 'true');
          }
        } catch (e) {}
      }
      setup(boxes[i]);
    }
    var resizeT;
    window.addEventListener('resize', function () {
      clearTimeout(resizeT);
      resizeT = setTimeout(function () {
        var bs = document.querySelectorAll('[data-clamp]');
        for (var i = 0; i < bs.length; i++) { if (bs[i]._breatheMeasure) bs[i]._breatheMeasure(); }
      }, 160);
    });
  }
  window.BreatheClamp = { init: init, setup: setup };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

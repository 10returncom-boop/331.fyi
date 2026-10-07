/* ============================================================
   anticopy.js — 全站防複製保護
   封鎖：右鍵選單、複製、剪下、文字選取、圖片拖曳、Ctrl/Cmd+C/X
   例外：輸入框/文字區/下拉選單（搜尋、評論等）仍可正常輸入與選取
   ============================================================ */
(function () {
  var INPUT = /^(INPUT|TEXTAREA|SELECT)$/i;

  function block(e) { e.preventDefault(); }

  document.addEventListener('contextmenu', block);

  document.addEventListener('copy', function (e) {
    var t = e.target;
    if (t && INPUT.test(t.tagName)) return;   // 輸入框內允許複製
    e.preventDefault();
  });

  document.addEventListener('cut', block);

  document.addEventListener('selectstart', function (e) {
    var t = e.target;
    if (t && INPUT.test(t.tagName)) return;
    e.preventDefault();
  });

  document.addEventListener('dragstart', function (e) {
    var t = e.target;
    if (t && INPUT.test(t.tagName)) return;
    e.preventDefault();
  });

  document.addEventListener('keydown', function (e) {
    if (!(e.ctrlKey || e.metaKey)) return;
    if (e.key === 'c' || e.key === 'C' || e.key === 'x' || e.key === 'X') {
      var t = e.target;
      if (t && INPUT.test(t.tagName)) return;
      e.preventDefault();
    }
  });
})();

/* Minimal progressive enhancement: collapsible navigation on narrow screens. No tracking, no requests. */
(function () {
  var doc = document.documentElement;
  doc.classList.add("js");
  var btn = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.textContent = open ? "Close" : "Menu";
  });
})();

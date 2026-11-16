(function () {
  var t = (location.pathname + location.search).slice(0, 96) || '/';
  Array.prototype.forEach.call(document.querySelectorAll('[data-nfp]'), function (e) { e.textContent = t; });
})();

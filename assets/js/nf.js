(function () {
  var c = document.getElementById('nfp');
  if (c) c.textContent = (location.pathname + location.search).slice(0, 96) || '/';
})();

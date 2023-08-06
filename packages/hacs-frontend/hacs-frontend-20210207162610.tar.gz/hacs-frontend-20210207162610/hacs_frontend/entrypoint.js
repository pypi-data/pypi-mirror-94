
try {
  new Function("import('/hacsfiles/frontend/e.0123aca4.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/e.0123aca4.js';
  document.body.appendChild(el);
}
  
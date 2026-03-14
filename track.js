// Fallback: если inline-скрипт страницы не определил сноски
if (typeof referencesPl === 'undefined') var referencesPl = {};
if (typeof referencesRu  === 'undefined') var referencesRu  = {};

// ─── Найти ближайшего предка с нужным классом (включая сам элемент) ───────────
function up(el, cls) {
  while (el && el.tagName) {
    if (el.classList && el.classList.contains(cls)) return el;
    el = el.parentElement;
  }
  return null;
}

// ─── Открыть/показать панель ──────────────────────────────────────────────────
function showRef(key, lang) {
  var panel   = document.getElementById('referencePanel');
  var content = document.getElementById('referenceContent');
  var title   = document.getElementById('referenceTitle');
  if (!panel || !content) return;

  var refs = (lang === 'ru') ? referencesRu : referencesPl;
  var ref  = refs[String(key)];

  if (!ref || (!ref.title && !ref.text)) {
    if (title) title.textContent = 'Справка';
    content.innerHTML = '<p class="reference-placeholder">Нет данных для этой сноски.</p>';
    panel.classList.add('open');
    return;
  }

  if (title) {
    title.textContent = (ref.title || '').trim() || 'Справка';
    title.classList.add('reference-phrase');
  }

  var html = '';
  if (ref.text) {
    html += '<div class="ref-text">' + ref.text + '</div>';
  }
  if (ref.videoId) {
    html += '<div class="reference-video-wrap">'
          + '<div class="reference-video"><iframe src="https://www.youtube-nocookie.com/embed/'
          + ref.videoId + '?rel=0" frameborder="0" allowfullscreen></iframe></div>'
          + '<a class="reference-video-link" href="https://www.youtube.com/watch?v='
          + ref.videoId + '" target="_blank" rel="noopener">Смотреть на YouTube</a>'
          + '</div>';
  }
  if (ref.image) {
    html += '<div class="reference-image-wrap"><img class="reference-image" src="'
          + ref.image.replace(/"/g, '') + '" alt=""></div>';
  }
  if (ref.url) {
    html += '<a class="reference-video-link" href="' + ref.url.replace(/"/g, '')
          + '" target="_blank" rel="noopener">Источник</a>';
  }

  content.innerHTML = html;
  panel.classList.add('open');
  positionPanel(panel);
}

// ─── Закрыть панель ───────────────────────────────────────────────────────────
function hideRef() {
  var panel   = document.getElementById('referencePanel');
  var content = document.getElementById('referenceContent');
  var title   = document.getElementById('referenceTitle');
  if (panel)   panel.classList.remove('open');
  if (title)   { title.textContent = 'Справка'; title.classList.remove('reference-phrase'); }
  if (content) content.innerHTML = '<p class="reference-placeholder">Кликни на выделенное слово в тексте, чтобы увидеть справку.</p>';
}

// ─── Позиционирование панели под хедером ─────────────────────────────────────
function positionPanel(panel) {
  panel = panel || document.getElementById('referencePanel');
  if (!panel) return;
  var header = document.querySelector('.track-top-bar');
  var top = header ? Math.round(header.getBoundingClientRect().bottom) + 10 : 80;
  panel.style.top       = top + 'px';
  panel.style.maxHeight = (window.innerHeight - top - 8) + 'px';
}

window.addEventListener('resize', function () {
  var panel = document.getElementById('referencePanel');
  if (panel && panel.classList.contains('open')) positionPanel(panel);
});

// ─── Единый обработчик кликов (event delegation) ─────────────────────────────
document.addEventListener('click', function (e) {
  var t = e.target;

  // Кнопка «закрыть»
  if (up(t, 'close-reference') || t.id === 'closeReference') {
    hideRef();
    return;
  }

  // Выделенное слово
  var kw = up(t, 'keyword');
  if (kw) {
    var key  = kw.getAttribute('data-key');
    var lang = up(kw, 'lyrics-line-ru') ? 'ru' : 'pl';
    showRef(key, lang);
    return;
  }

  // Переключатель вида
  var tog = up(t, 'view-toggle');
  if (tog) {
    var view = tog.getAttribute('data-view');
    document.body.classList.remove('view-pol', 'view-ru', 'view-both');
    document.body.classList.add(view === 'pol' ? 'view-pol' : view === 'ru' ? 'view-ru' : 'view-both');
    document.querySelectorAll('.view-toggle').forEach(function (b) {
      var active = b === tog;
      b.classList.toggle('active', active);
      b.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    return;
  }

  // Клик вне панели — закрыть
  var panel = document.getElementById('referencePanel');
  if (panel && panel.classList.contains('open') && !panel.contains(t)) {
    hideRef();
  }
});

// Задать top при загрузке (до первого клика)
document.addEventListener('DOMContentLoaded', function () { positionPanel(); });

// Сноски к первому треку: отдельно польские (только к польскому тексту) и русские (только к русскому)
var referencesPl = {
  0: {
    title: 'Szlugi',
    text: 'Słowo „szlugi” w języku polskim to potoczna nazwa na papierosy lub pety. Od razu przywołuje zapach klatki schodowej, ulicy. Dla papierosów jest neutralne słowo „papierosy”.'
  },
  1: {
    title: 'Fragment dokumentu o prostytucji w PRL',
    text: 'Fragment ten pochodzi z dokumentu o prostytucji w PRL.',
    videoId: 'XQ1ksdUO9P0'
  },
  2: {
    title: 'Sample: żona Śliwy — Czesław Śliwa',
    text: 'O wykorzystanym tu samplu Taco wypowiedział się w wywiadzie z Metro Warszawa. Cytat: Sampel w pierwszym utworze „Szlugi i kalafiory” to wypowiedź żony Śliwy, która opowiada o nim bez złości – była nim zauroczona, nawet po tym, jak okazało się, że jest oszustem. Chodzi tu o Czesława Śliwę, oszusta żyjącego w PRL-u, którym Taco był zafascynowany. Wers ten zwraca uwagę na kontrast między tym, jak podrywało się dziewczyny wtedy (na przykładzie Cz. Śliwy), a jak robi się to teraz (na przykładzie Piotra). Kiedyś można było traktować kobiety z klasą, dziś prawdopodobnie nie będzie to już docenione.',
    videoId: 'iw5TCHlcoVE'
  },
  3: {
    title: 'Kalafiory i szlugi — zapach klatki',
    text: 'W wywiadzie z Taco przeprowadzonym przez Mateusza Osiaka zapytano go o motyw szlugów i kalafiorów: „O co chodzi z tymi kalafiorami, poza tym, że wyglądają jak mózgi?” Cytat: „Smród kalafiora i papierosów to taki trochę zapach polskiej klatki schodowej. I sam kalafior jest giga smutnym bytem.”'
  },
  4: {
    title: 'Taco w wywiadzie dla Vogue',
    text: 'Taco w wywiadzie dla Vogue powiedział: Cytat: „Ten zapach bardzo mi się kojarzy z takim blokiem, w którym mieszkałem, stary budynek. To jest zapach klatki schodowej polskiej. Jest to też taka stęchlizna i zależało mi na tym, żeby całe miasto tak pachniało dla głównego bohatera, bo tak też się czuje człowiek ze złamanym sercem. Jakby miasto jego tak pachniało… Te szlugi i kalafiory to myślę, że to są silne emocje wywołujące skupisko zapachowe.”'
  },
  5: {
    title: '„Panie władzo”',
    text: 'Dosłownie: «panie władzo». Tak po polsku można zwrócić się do osoby przy władzy: policjantowi, urzędnikowi, biurokracie. Blisko rosyjskiemu «gospodin naczalnik», ale z wymuszoną, złośliwą uprzejmością.'
  },
  6: {
    title: 'Kraina mlekiem i miodem płynąca',
    text: 'Jest to nawiązanie do biblijnego cytatu „Kraina mlekiem i miodem płynąca”, która określała Ziemię Obiecaną w Starym Testamencie.'
  },
  7: {
    title: 'Wygadam się Tobie',
    text: 'W pewnym sensie burzy czwartą ścianę, zwracając się wprost do słuchacza.'
  },
  8: {
    title: 'Kim jest Piotr?',
    text: 'W wywiadzie z Metro Warszawa Taco wyjaśnił również kim jest Piotr: Cytat: „Piotr nie jest moim nemesis. Ktoś mnie już pytał, kto mi tyle przykrości zrobił, kto to jest ten Piotr. Piotr jest zlepkiem wyobrażeń o kimś, w kim zakochała się nasza niespełniona miłość. Ktoś jednocześnie lepszy i gorszy od nas. Nic o nim nie wiesz, ale wyobrażasz sobie, że może ma więcej kasy i lepiej wygląda, ale za to jest głupszy i upośledzony emocjonalnie. Jak bym miał kiedyś zrobić teledysk do tej płyty, to Piotra grałoby wielu różnych aktorów, ubranych i zachowujących się tak samo. Bo on jest tylko symbolem, figurą. A ponieważ główny bohater jest ciągle pijany, to może widzieć wielu innych mężczyzn ze swoją ukochaną kobietą, ale wyobrażać sobie, że to ciągle jest ten sam Piotr.”'
  }
};

var referencesRu = {
  0: {
    title: 'Szlugi / окурки',
    text: 'Слово szlugi в польском можно перевести как сиги или окурки. Оно сразу ассоциируется пожухлым, уличным, подъездным запахом. Для сигарет в польском есть нейтральное слово papierosy.'
  },
  1: {
    title: 'Фрагмент документального фильма о проституции в ПНР',
    text: 'Фрагмент взят из документального фильма о проституции в Польской Народной Республике.',
    videoId: 'XQ1ksdUO9P0'
  },
  2: {
    title: 'Сэмпл: жена Сливы — Чеслав Слива',
    text: 'О использованном здесь сэмпле Taco рассказывал в интервью для Metro Warszawa. Цитата: Сэмпл в треке «Szlugi i kalafiory» — это высказывание жены Сливы, которая говорит о нём без злости, она была им очарована, даже после того, как выяснилось, что он мошенник. Речь идёт о Чеславе Сливе, аферисте времен ПНР, которым Taco был увлечён. Эта строчка подчёркивает контраст между тем, как подкатывали к девушкам тогда (на примере Ч. Сливы), и тем, как это делается сейчас (на примере Петра). Раньше можно было ухаживать «с классом», а сегодня это, вероятно, уже не будет оценено.',
    videoId: 'iw5TCHlcoVE'
  },
  3: {
    title: 'Окурки и цветная капуста — запах подъезда',
    text: 'В интервью Taco, которое проводил Матеуш Осяк, его спросили о мотиве окурков и цветной капусты: «Почему капуста, кроме того, что она похожа на мозги?» Цитата: «Вонь цветной капусты и сигарет — это такой, знаешь, запах польского подъезда. И сама цветная капуста — это ужасно грустная штука».'
  },
  4: {
    title: 'Taco в интервью для Vogue',
    text: 'В интервью для Vogue Taco сказал: Цитата: «Этот запах очень ассоциируется у меня с домом, где я жил. Это было старое здание. Это запах польского подъезда. Там есть и затхлость, и мне было важно, чтобы для главного героя так пах весь город, потому что так чувствует себя человек с разбитым сердцем. Как будто его город вот так пахнет… Эти „окурки и цветная капуста“, мне кажется, это такой мощный, эмоциональный „сгусток запаха“».'
  },
  5: {
    title: '«Господин власть»',
    text: 'Буквально: «господин власть». По-польски так могут обратиться к любому человеку «при власти»: полицейскому, чиновнику, бюрократу и т.п. По смыслу это близко к русскому «господин начальник», но с нарочитой, чуть язвительной вежливостью.'
  },
  6: {
    title: 'Земля, где течёт молоко и мёд',
    text: 'Это отсылка к библейскому выражению «земля, где течёт молоко и мёд». Образ Земли Обетованной в Ветхом Завете.'
  },
  7: {
    title: 'Выговорюсь тебе',
    text: 'В некотором смысле герой ломает четвёртую стену, потому что обращается напрямую к слушателю.'
  },
  8: {
    title: 'Кто такой Пётр?',
    text: 'В интервью для Metro Warszawa Taco также объяснил, кто такой Пётр: Цитата: «Пётр не мой немезис. Меня уже спрашивали, кто мне сделал столько боли, кто этот Пётр. Пётр — это слепок наших представлений о том, в кого влюбилась наша несбывшаяся любовь. Кто-то одновременно лучше и хуже нас. Ты ничего о нём не знаешь, но представляешь, что, может, у него больше денег и он лучше выглядит, зато он глупее и эмоционально ущербнее. Если бы я когда-нибудь делал клип к этой пластинке, Петра играли бы многие разные актёры, одетые и ведущие себя одинаково. Потому что он всего лишь символ, фигура. А поскольку главный герой постоянно пьян, он может видеть рядом со своей любимой женщиной разных мужчин, но воображать, что это всё время один и тот же Пётр».'
  }
};

var referencePanel = document.getElementById('referencePanel');
var referenceContent = document.getElementById('referenceContent');
var referenceTitle = document.getElementById('referenceTitle');
var closeRef = document.getElementById('closeReference');

function escapeHtml(s) {
  var div = document.createElement('div');
  div.textContent = s;
  return div.innerHTML;
}

function openReference(key, lang, phraseText) {
  var ref = lang === 'pl' ? referencesPl[key] : referencesRu[key];
  if (!ref) return;
  var phrase = (phraseText || '').trim();
  var words = phrase.split(/\s+/).filter(Boolean);
  var phraseWords = words.length <= 6 ? phrase : words.slice(0, 6).join(' ');
  if (referenceTitle) {
    referenceTitle.textContent = phraseWords || 'Справка';
    referenceTitle.classList.add('reference-phrase');
  }

  var text = ref.text || '';
  var quoteRe = /\s*(?:Cytat|Цитата):\s*/i;
  var quoteIdx = text.search(quoteRe);
  var intro = quoteIdx >= 0 ? text.slice(0, quoteIdx).trim() : text;
  var quote = quoteIdx >= 0 ? text.slice(quoteIdx).replace(quoteRe, '').trim() : '';

  var html = '';
  if (intro) html += '<p>' + escapeHtml(intro) + '</p>';
  if (quote) html += '<div class="reference-quote">' + escapeHtml(quote) + '</div>';
  if (ref.videoId) {
    var embedUrl = 'https://www.youtube.com/embed/' + ref.videoId + '?rel=0';
    html += '<div class="reference-video">';
    html += '<iframe src="' + embedUrl + '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen title="YouTube"></iframe>';
    html += '<a class="reference-video-link" href="https://www.youtube.com/watch?v=' + ref.videoId + '" target="_blank" rel="noopener">Смотреть на YouTube</a>';
    html += '</div>';
  }
  referenceContent.innerHTML = html;
  referencePanel.classList.add('open');
}

document.querySelectorAll('.view-toggle').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var view = this.getAttribute('data-view');
    document.body.classList.remove('view-pol', 'view-ru', 'view-both');
    if (view === 'pol') document.body.classList.add('view-pol');
    else if (view === 'ru') document.body.classList.add('view-ru');
    else document.body.classList.add('view-both');
    document.querySelectorAll('.view-toggle').forEach(function (b) {
      b.classList.toggle('active', b === btn);
      b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
    });
  });
});

document.querySelectorAll('.keyword').forEach(function (el) {
  el.addEventListener('click', function (e) {
    e.stopPropagation();
    var key = el.getAttribute('data-key');
    var column = el.closest('.lyrics-line-pl') ? 'pl' : el.closest('.lyrics-line-ru') ? 'ru' : 'pl';
    var phrase = (el.textContent || '').trim();
    openReference(key, column, phrase);
  });
});

if (closeRef) {
  closeRef.addEventListener('click', function () {
    referencePanel.classList.remove('open');
    if (referenceTitle) {
      referenceTitle.textContent = 'Справка';
      referenceTitle.classList.remove('reference-phrase');
    }
    referenceContent.innerHTML = '<p class="reference-placeholder">Кликни на выделенное слово в тексте, чтобы увидеть справку.</p>';
  });
}

document.addEventListener('click', function (e) {
  if (referencePanel && referencePanel.classList.contains('open') && !referencePanel.contains(e.target) && !e.target.closest('.keyword')) {
    referencePanel.classList.remove('open');
  }
});

// Отступ справки от хедера: считаем высоту хедера и задаём top/max-height динамически
function updateReferencePanelOffset() {
  var header = document.querySelector('.track-top-bar');
  var panel = document.getElementById('referencePanel');
  if (!header || !panel) return;
  var headerHeight = header.getBoundingClientRect().height;
  var gap = 16; // 1rem
  var topPx = headerHeight + gap;
  panel.style.setProperty('top', topPx + 'px');
  panel.style.setProperty('max-height', 'calc(100vh - ' + topPx + 'px - 0.5rem)');
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', updateReferencePanelOffset);
} else {
  updateReferencePanelOffset();
}
window.addEventListener('resize', updateReferencePanelOffset);
window.addEventListener('load', updateReferencePanelOffset);

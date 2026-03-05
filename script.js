// Данные справочника (по data-key) — ссылки на сноски из PDF
const references = {
  0: {
    title: 'Szlugi',
    text: 'Сленговое слово для сигарет/окурков. Даёт ощущение подъездного, уличного запаха, в отличие от нейтральных «papierosy».'
  },
  1: {
    title: 'Dokument o prostytucji w PRL',
    text: 'Фрагмент из документального фильма о проституции в ПНР. Создаёт документальный, мрачный фон варшавской ночи.'
  },
  2: {
    title: 'Czesław Śliwa — oszust z PRL',
    text: 'Сэмпл — рассказ жены Чеслава Шливы, легендарного мошенника времён ПНР. Она говорит о нём без злобы, всё ещё им восхищаясь.'
  },
  3: {
    title: 'Szlugi i kalafiory — zapach klatki',
    text: 'По словам Taco: «Smród kalafiora i papierosów to zapach polskiej klatki schodowej». Калафьор и сигареты как грустный, очень польский запах.'
  },
  4: {
    title: 'Miasto pachnie szlugami i kalafiorami',
    text: 'Для героя весь город пахнет так же, как его подъезд — смесью сигарет и цветной капусты. Образ сломанного сердца, когда весь мир пахнет так же несвежо.'
  },
  5: {
    title: '„Panie władzo”',
    text: 'Буквально «господин власть» — вежливое, но чуть язвительное обращение к людям при власти: полицейским, чиновникам, бюрократам.'
  },
  6: {
    title: 'Kraina mlekiem i miodem płynąca',
    text: 'Отсылка к библейскому «земля, где течёт молоко и мёд» — образ Земли Обетованной. Здесь контрастирует с реальностью, полной дыма и смальца.'
  },
  7: {
    title: 'Wygadam się Tobie',
    text: 'Герой будто ломает «четвёртую стену» и обращается прямо к слушателю, выговариваясь ему, потому что «не знает, кому ещё».'
  },
  8: {
    title: 'Kim jest Piotr?',
    text: 'По словам Taco, Piotr — собирательный образ человека, в которого влюбилась наша несбывшаяся любовь. Символ комплекса героя, а не конкретный враг.'
  }
};

// Треки альбома
const tracks = [
  { id: 'szlugi-i-kalafiory', title: 'Szlugi i Kalafiory', album: 'Trójkąt Warszawski', file: 'trojkat warszawski/01 - Taco Hemingway - Szlugi i Kalafiory - 2024 Remaster.mp3' },
  { id: 'marsz-marsz', title: 'Marsz, Marsz', album: 'Trójkąt Warszawski', file: 'trojkat warszawski/02 - Taco Hemingway - Marsz, Marsz - 2024 Remaster.mp3' },
  { id: 'wszystko-jedno', title: 'Wszystko Jedno', album: 'Trójkąt Warszawski', file: 'trojkat warszawski/03 - Taco Hemingway - Wszystko Jedno - 2024 Remaster.mp3' },
  { id: 'trojkat', title: 'Trojkat', album: 'Trójkąt Warszawski', file: 'trojkat warszawski/04 - Taco Hemingway - Trojkat - 2024 Remaster.mp3' },
  { id: 'przerywnik', title: '(Przerywnik)', album: 'Trójkąt Warszawski', file: 'trojkat warszawski/05 - Taco Hemingway - (Przerywnik) - 2024 Remaster.mp3' },
  { id: 'mieso', title: 'Mieso', album: 'Trójkąt Warszawski', file: 'trojkat warszawski/06 - Taco Hemingway - Mieso - 2024 Remaster.mp3' },
  { id: '900729', title: '900729', album: 'Trójkąt Warszawski', file: 'trojkat warszawski/07 - Taco Hemingway - 900729 - 2024 Remaster.mp3' }
];

// Навигация
const landing = document.getElementById('landing');
const albumPage = document.getElementById('albumPage');
const trackSection = document.getElementById('trackSection');
const navArrowRight = document.getElementById('navArrowRight');
const navArrowBack = document.getElementById('navArrowBack');
const navArrowToTracks = document.getElementById('navArrowToTracks');
const navArrowBackToAlbum = document.getElementById('navArrowBackToAlbum');
const albumButton = document.getElementById('albumButton');
const albumDropdown = document.getElementById('albumDropdown');

function showSection(section) {
  landing.classList.remove('hidden');
  albumPage.classList.remove('visible');
  trackSection.classList.remove('visible');
  document.body.classList.remove('track-view');
  if (albumDropdown) {
    albumDropdown.classList.remove('open');
  }
  if (section === 'landing') {
    landing.classList.remove('hidden');
  } else if (section === 'album') {
    landing.classList.add('hidden');
    albumPage.classList.add('visible');
  } else if (section === 'track') {
    landing.classList.add('hidden');
    trackSection.classList.add('visible');
    document.body.classList.add('track-view');
  }
}

navArrowRight.addEventListener('click', () => showSection('album'));
navArrowBack.addEventListener('click', () => showSection('landing'));
navArrowToTracks.addEventListener('click', () => showSection('track'));
navArrowBackToAlbum.addEventListener('click', () => showSection('album'));

// Выпадающее меню альбома из плеера
if (albumButton && albumDropdown) {
  albumButton.addEventListener('click', (e) => {
    e.stopPropagation();
    albumDropdown.classList.toggle('open');
  });
}

// Клик по треку в списке
document.querySelectorAll('.track-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const hash = link.getAttribute('href').slice(1); // #track-szlugi-i-kalafiory -> track-szlugi-i-kalafiory
    const trackId = hash.replace('track-', '');
    const track = tracks.find(t => t.id === trackId);
    if (track) {
      loadTrack(track);
    }
    showSection('track');
  });
});

function loadTrack(track) {
  const audio = document.getElementById('audio');
  const source = audio.querySelector('source');
  source.src = track.file;
  audio.load();
  document.getElementById('playerTrackTitle').textContent = track.title;
  document.getElementById('playerAlbumTitle').textContent = track.album;
}

// Плеер
const audio = document.getElementById('audio');
const playPauseBtn = document.getElementById('playPause');
const iconPlay = playPauseBtn.querySelector('.icon-play');
const iconPause = playPauseBtn.querySelector('.icon-pause');

playPauseBtn.addEventListener('click', () => {
  if (audio.paused) {
    audio.play();
    iconPlay.classList.add('hidden');
    iconPause.classList.remove('hidden');
  } else {
    audio.pause();
    iconPlay.classList.remove('hidden');
    iconPause.classList.add('hidden');
  }
});

audio.addEventListener('play', () => {
  iconPlay.classList.add('hidden');
  iconPause.classList.remove('hidden');
});

audio.addEventListener('pause', () => {
  iconPlay.classList.remove('hidden');
  iconPause.classList.add('hidden');
});

// Справочник: клик по ключевому слову
const referencePanel = document.getElementById('referencePanel');
const referenceContent = document.getElementById('referenceContent');
const closeReference = document.getElementById('closeReference');

document.querySelectorAll('.keyword').forEach(el => {
  el.addEventListener('click', (e) => {
    e.stopPropagation();
    const key = el.getAttribute('data-key');
    const ref = references[key];
    if (ref) {
      referenceContent.innerHTML = `<h5>${ref.title}</h5><p>${ref.text}</p>`;
      referencePanel.classList.add('open');
    }
  });
});

closeReference.addEventListener('click', () => {
  referencePanel.classList.remove('open');
  referenceContent.innerHTML = '<p class="reference-placeholder">Кликни на выделенное слово в тексте, чтобы увидеть справку.</p>';
});

document.addEventListener('click', (e) => {
  if (referencePanel.classList.contains('open') && !referencePanel.contains(e.target) && !e.target.closest('.keyword')) {
    referencePanel.classList.remove('open');
  }
  if (albumDropdown && albumDropdown.classList.contains('open') && !albumDropdown.contains(e.target) && e.target !== albumButton) {
    albumDropdown.classList.remove('open');
  }
});

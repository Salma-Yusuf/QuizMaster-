// QuizMaster quiz navigation: one question at a time, palette, progress, timer.
(function () {
  const form = document.getElementById('quiz-form');
  const qs = [...form.querySelectorAll('.question')];
  const total = qs.length;
  const prev = document.getElementById('prev'), next = document.getElementById('next'), finish = document.getElementById('finish');
  const counter = document.getElementById('counter'), bar = document.getElementById('bar');
  const palette = [...document.querySelectorAll('#palette button')];
  const answeredEl = document.getElementById('answered');
  let cur = 0;

  function isAnswered(i) { return !!qs[i].querySelector('input:checked'); }

  function render() {
    qs.forEach((q, i) => q.classList.toggle('active', i === cur));
    counter.textContent = `Question ${cur + 1} of ${total}`;
    bar.style.width = `${((cur + 1) / total) * 100}%`;
    prev.disabled = cur === 0;
    next.hidden = cur === total - 1;
    finish.hidden = cur !== total - 1;
    let done = 0;
    palette.forEach((b, i) => {
      const a = isAnswered(i); done += a;
      b.classList.toggle('answered', a);
      if (i === cur) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current');
    });
    answeredEl.textContent = done;
  }
  function go(i) { cur = Math.max(0, Math.min(total - 1, i)); render(); window.scrollTo({ top: 0 }); }

  prev.addEventListener('click', () => go(cur - 1));
  next.addEventListener('click', () => go(cur + 1));
  palette.forEach(b => b.addEventListener('click', () => go(+b.dataset.go)));
  form.addEventListener('change', render);

  // keyboard: arrows move between questions, 1-4 / a-d pick an option
  document.addEventListener('keydown', e => {
    if (e.target.matches('input[type=text], textarea')) return;
    if (e.key === 'ArrowRight') go(cur + 1);
    else if (e.key === 'ArrowLeft') go(cur - 1);
    else {
      const map = { '1': 0, '2': 1, '3': 2, '4': 3, a: 0, b: 1, c: 2, d: 3 };
      const idx = map[e.key.toLowerCase()];
      if (idx !== undefined) {
        const r = qs[cur].querySelectorAll('input[type=radio]')[idx];
        if (r) { r.checked = true; render(); }
      }
    }
  });

  // warn before submitting with blanks
  form.addEventListener('submit', e => {
    const blank = qs.map((_, i) => i).filter(i => !isAnswered(i));
    if (blank.length && !confirm(`You left ${blank.length} question${blank.length > 1 ? 's' : ''} unanswered. Finish anyway?`)) {
      e.preventDefault(); go(blank[0]);
    } else { window.onbeforeunload = null; }
  });
  window.onbeforeunload = () => 'Your answers will be lost.';

  // timer
  const t0 = Date.now(), timer = document.getElementById('timer');
  setInterval(() => {
    const s = Math.floor((Date.now() - t0) / 1000);
    timer.textContent = `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  }, 1000);

  render();
})();

const bodyParts = ['p-head','p-body','p-larm','p-rarm','p-lleg','p-rleg'];
let word, guessed, lives, over;

function initGame() {
  word = SPECIES_LIST[Math.floor(Math.random() * SPECIES_LIST.length)].toUpperCase().replace(/\s+/g, ' ').trim();
  guessed = [];
  lives = 6;
  over = false;
  bodyParts.forEach(id => document.getElementById(id).setAttribute('display', 'none'));
  document.getElementById('hm-msg').textContent = '';
  document.getElementById('hm-msg').className = 'hm-msg';
  document.getElementById('hm-restart-wrap').style.display = 'none';
  renderWord();
  renderKeyboard();
  renderLives();
  renderGuessed();
}

function renderWord() {
  const el = document.getElementById('hm-word');
  el.innerHTML = word.split('').map(l => {
    const show = l === ' ' || guessed.includes(l) || over;
    return `<div class="hm-letter"><span>${show ? l : ''}</span>${l !== ' ' ? '<hr>' : ''}</div>`;
  }).join('');
}

function renderLives() {
  document.getElementById('hm-lives').textContent = `Lives: ${lives}`;
}

function renderGuessed() {
  const wrong = guessed.filter(l => !word.includes(l));
  document.getElementById('hm-guessed').textContent = wrong.length ? `Wrong: ${wrong.join(', ')}` : '';
}

function renderKeyboard() {
  const kb = document.getElementById('hm-keyboard');
  kb.innerHTML = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(l => {
    const used = guessed.includes(l);
    const isRight = used && word.includes(l);
    const isWrong = used && !word.includes(l);
    return `<button class="hm-key${isRight ? ' right' : isWrong ? ' wrong' : ''}" ${used || over ? 'disabled' : ''} data-letter="${l}">${l}</button>`;
  }).join('');
  kb.querySelectorAll('.hm-key:not(:disabled)').forEach(btn => {
    btn.addEventListener('click', () => guess(btn.dataset.letter));
  });
}

function guess(letter) {
  if (over || guessed.includes(letter)) return;
  guessed.push(letter);
  if (!word.includes(letter)) {
    lives--;
    document.getElementById(bodyParts[6 - lives - 1]).setAttribute('display', 'inline');
  }
  const won = word.split('').filter(l => l !== ' ').every(l => guessed.includes(l));
  const lost = lives === 0;
  if (won || lost) {
    over = true;
    const msg = document.getElementById('hm-msg');
    msg.textContent = won ? `You won! The species was: ${word}` : `Game over! The species was: ${word}`;
    msg.className = 'hm-msg ' + (won ? 'win' : 'lose');
    document.getElementById('hm-restart-wrap').style.display = 'block';
  }
  renderWord();
  renderKeyboard();
  renderLives();
  renderGuessed();
}

document.addEventListener('keydown', e => {
  const l = e.key.toUpperCase();
  if (/^[A-Z]$/.test(l) && !over) guess(l);
});

document.getElementById('hm-restart').addEventListener('click', initGame);

initGame();
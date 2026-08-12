// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let currentSolution = [];
let timerId = null;
let elapsedSeconds = 0;

function formatTime(seconds) {
  const mins = String(Math.floor(seconds / 60)).padStart(2, '0');
  const secs = String(seconds % 60).padStart(2, '0');
  return `${mins}:${secs}`;
}

function updateTimerLabel() {
  document.getElementById('timer').innerText = `Time: ${formatTime(elapsedSeconds)}`;
}

function resetTimer() {
  if (timerId) {
    clearInterval(timerId);
  }
  elapsedSeconds = 0;
  updateTimerLabel();
  timerId = setInterval(() => {
    elapsedSeconds += 1;
    updateTimerLabel();
  }, 1000);
}

function saveLeaderboardEntry(name, difficulty, time) {
  const entry = {name, difficulty, time};
  const leaderboard = loadLeaderboard();
  leaderboard.push(entry);
  leaderboard.sort((a, b) => a.time - b.time);
  const trimmed = leaderboard.slice(0, 10);
  localStorage.setItem('sudokuLeaderboard', JSON.stringify(trimmed));
  renderLeaderboard();
}

function loadLeaderboard() {
  const saved = localStorage.getItem('sudokuLeaderboard');
  return saved ? JSON.parse(saved) : [];
}

function renderLeaderboard() {
  const rows = loadLeaderboard();
  const body = document.getElementById('leaderboard-body');
  body.innerHTML = '';
  rows.forEach((row, index) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${index + 1}</td>
      <td>${row.name}</td>
      <td>${row.difficulty}</td>
      <td>${formatTime(row.time)}</td>
    `;
    body.appendChild(tr);
  });
}

function clearLeaderboard() {
  localStorage.removeItem('sudokuLeaderboard');
  renderLeaderboard();
}

function getDifficultyLabel() {
  const selector = document.getElementById('difficulty');
  return selector.options[selector.selectedIndex].text;
}

function getPlayerName() {
  const playerName = document.getElementById('player-name').value.trim();
  return playerName || 'Anonymous';
}

function setThemeButtonLabel(isDark) {
  const button = document.getElementById('toggle-theme');
  if (!button) return;
  button.innerText = isDark ? 'Light Mode' : 'Dark Mode';
}

function applyTheme(isDark) {
  document.body.classList.toggle('dark-mode', isDark);
  localStorage.setItem('sudokuTheme', isDark ? 'dark' : 'light');
  setThemeButtonLabel(isDark);
}

function loadTheme() {
  const savedTheme = localStorage.getItem('sudokuTheme');
  const isDark = savedTheme === 'dark';
  applyTheme(isDark);
}

function savePlayerName() {
  const name = document.getElementById('player-name').value.trim();
  localStorage.setItem('sudokuPlayerName', name);
}

function loadPlayerName() {
  const savedName = localStorage.getItem('sudokuPlayerName');
  if (savedName) {
    document.getElementById('player-name').value = savedName;
  }
}

function validateCell(inp) {
  if (!currentSolution.length || inp.disabled) {
    return;
  }

  inp.classList.remove('invalid');
  inp.classList.remove('incorrect');

  const value = inp.value;
  if (value === '') {
    return;
  }

  if (!/^[1-9]$/.test(value)) {
    inp.classList.add('invalid');
    return;
  }

  const row = parseInt(inp.dataset.row, 10);
  const col = parseInt(inp.dataset.col, 10);
  const intVal = parseInt(value, 10);
  if (currentSolution[row][col] !== intVal) {
    inp.classList.add('invalid');
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        validateCell(e.target);
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?clues=${difficulty}`);
  const data = await res.json();
  currentSolution = data.solution;
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  resetTimer();
}

function findHintCell() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = Array.from(boardDiv.getElementsByTagName('input'));
  const emptyCells = inputs.filter((inp) => !inp.disabled && inp.value === '');
  return emptyCells.length ? emptyCells[Math.floor(Math.random() * emptyCells.length)] : null;
}

function applyHint() {
  if (!currentSolution.length) {
    return;
  }
  const hintCell = findHintCell();
  const msg = document.getElementById('message');
  if (!hintCell) {
    msg.style.color = '#d32f2f';
    msg.innerText = 'No empty cells to hint.';
    return;
  }
  const row = parseInt(hintCell.dataset.row, 10);
  const col = parseInt(hintCell.dataset.col, 10);
  hintCell.value = currentSolution[row][col];
  hintCell.disabled = true;
  hintCell.classList.add('hinted');
  hintCell.classList.remove('invalid');
  msg.style.color = '#388e3c';
  msg.innerText = 'Hint filled one correct cell.';
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';

    const isComplete = board.every((row) => row.every((cell) => cell !== 0));
    if (isComplete) {
      saveLeaderboardEntry(getPlayerName(), getDifficultyLabel(), elapsedSeconds);
    }
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint-button').addEventListener('click', applyHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('clear-leaderboard').addEventListener('click', clearLeaderboard);
  document.getElementById('toggle-theme').addEventListener('click', () => applyTheme(!document.body.classList.contains('dark-mode')));
  document.getElementById('player-name').addEventListener('input', savePlayerName);
  loadPlayerName();
  loadTheme();
  renderLeaderboard();
  // initialize
  newGame();
});
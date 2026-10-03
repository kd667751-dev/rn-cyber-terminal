// Audio Context (initialized on user interaction)
let audioCtx = null;
let soundEnabled = false;

// Elements
const audioToggle = document.getElementById('audioToggle');
const screens = document.querySelectorAll('.screen');
const bootText = document.getElementById('bootText');
const bootFinal = document.getElementById('bootFinal');
const enterSystemBtn = document.getElementById('enterSystemBtn');

const navBtns = document.querySelectorAll('.nav-btn');
const backBtns = document.querySelectorAll('.back-btn');
const systemAlerts = document.getElementById('systemAlerts');
const logsTerminal = document.getElementById('logsTerminal');
const hexDump = document.getElementById('hexDump');

const unknownBtn = document.getElementById('unknownBtn');
const finalAccessBtn = document.getElementById('finalAccessBtn');
const abortFinalBtn = document.getElementById('abortFinalBtn');
const proceedFinalBtn = document.getElementById('proceedFinalBtn');

const finalContent = document.querySelector('.final-content');
const particles = document.getElementById('particles');

// Sounds (Synth)
function initAudio() {
  if (audioCtx) return;
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
}

function playBlip() {
  if (!soundEnabled || !audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'square';
  osc.frequency.setValueAtTime(800, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.05);
  gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.05);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.05);
}

function playGlitch() {
  if (!soundEnabled || !audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'sawtooth';
  osc.frequency.setValueAtTime(100, audioCtx.currentTime);
  osc.frequency.linearRampToValueAtTime(500, audioCtx.currentTime + 0.1);
  gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
  gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.2);
}

function playHeartbeat() {
  if (!soundEnabled || !audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'sine';
  osc.frequency.setValueAtTime(50, audioCtx.currentTime);
  gain.gain.setValueAtTime(0, audioCtx.currentTime);
  gain.gain.linearRampToValueAtTime(0.3, audioCtx.currentTime + 0.1);
  gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.3);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.4);
}

audioToggle.addEventListener('click', () => {
  initAudio();
  soundEnabled = !soundEnabled;
  audioToggle.textContent = soundEnabled ? '[ SOUND: ON ]' : '[ SOUND: OFF ]';
  if (soundEnabled && audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
});

// Boot Sequence Typing
const bootLines = [
  "INITIALIZING SYSTEM...",
  "Establishing secure connection...",
  "Bypassing firewall protocols...",
  "Loading encrypted modules...",
  "Scanning environment...",
  "Searching database...",
  "Match found.",
  "Identity detected."
];

async function typeBootSequence() {
  for (let i = 0; i < bootLines.length; i++) {
    const line = document.createElement('div');
    line.className = 'terminal-line';
    bootText.appendChild(line);
    
    const text = bootLines[i];
    for (let j = 0; j < text.length; j++) {
      line.textContent += text[j];
      if (Math.random() > 0.3) playBlip();
      await new Promise(r => setTimeout(r, Math.random() * 30 + 10));
    }
    await new Promise(r => setTimeout(r, 400));
  }
  
  await new Promise(r => setTimeout(r, 500));
  bootText.innerHTML += `<div class="terminal-line terminal-success">> SYSTEM READY</div>`;
  await new Promise(r => setTimeout(r, 800));
  
  bootText.classList.add('hidden');
  bootFinal.classList.remove('hidden');
  
  // Show button after a delay
  setTimeout(() => {
    enterSystemBtn.classList.remove('opacity-0');
    audioToggle.classList.remove('hidden');
  }, 2000);
}

// Screen Navigation
function showScreen(screenId) {
  screens.forEach(s => s.classList.remove('active', 'hidden'));
  screens.forEach(s => {
    if(s.id !== screenId) {
      s.classList.add('hidden');
    }
  });
  
  // Reflow to restart animations
  void document.getElementById(screenId).offsetWidth;
  document.getElementById(screenId).classList.add('active');
  playBlip();
}

enterSystemBtn.addEventListener('click', () => {
  initAudio();
  showScreen('mainHub');
});

backBtns.forEach(btn => {
  btn.addEventListener('click', () => showScreen('mainHub'));
});

// Main Hub Navigation
navBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    if (btn.classList.contains('locked')) return;
    const target = btn.getAttribute('data-target');
    
    if (target === 'systemLogs') {
      showScreen(target);
      runLogs();
    } else if (target === 'unknownSection') {
      showScreen(target);
      triggerGlitchEvent();
    } else if (target === 'finalAccess') {
      showScreen('finalWarning');
    } else {
      showScreen(target);
    }
  });
});

// Logs Logic
const logMessages = [
  "21:07:12 — Subject detected.",
  "21:08:43 — Attention redirected.",
  "21:09:15 — Analyzing neural patterns...",
  "21:10:02 — System behavior changed.",
  "21:11:29 — Repeated observation detected.",
  "21:12:04 — Reason: <span class='log-exception'>UNKNOWN</span>.",
  "21:12:45 — Attempting to process data...",
  "21:13:55 — Exception created.",
  "21:15:00 — Core protocol overridden."
];

let logsRun = false;
async function runLogs() {
  if (logsRun) return;
  logsRun = true;
  logsTerminal.innerHTML = '';
  
  for (let i = 0; i < logMessages.length; i++) {
    const div = document.createElement('div');
    div.className = 'log-entry';
    div.innerHTML = logMessages[i];
    logsTerminal.appendChild(div);
    playBlip();
    logsTerminal.scrollTop = logsTerminal.scrollHeight;
    await new Promise(r => setTimeout(r, Math.random() * 1000 + 500));
  }
  
  await new Promise(r => setTimeout(r, 1500));
  const finalDiv = document.createElement('div');
  finalDiv.className = 'log-entry log-exception';
  finalDiv.style.marginTop = '20px';
  finalDiv.innerHTML = 'SYSTEM NOTE: "There is only one exception."';
  logsTerminal.appendChild(finalDiv);
  playGlitch();
  
  // Unlock Final Access
  finalAccessBtn.classList.remove('locked');
  finalAccessBtn.classList.add('unlocked');
}

// Glitch Event Logic
function generateHex() {
  let hex = '';
  for(let i=0; i<300; i++) {
    hex += Math.floor(Math.random()*256).toString(16).padStart(2, '0').toUpperCase() + ' ';
  }
  return hex;
}

let glitchRunning = false;
function triggerGlitchEvent() {
  if(glitchRunning) return;
  glitchRunning = true;
  
  hexDump.textContent = generateHex();
  
  let glitchInterval = setInterval(() => {
    hexDump.textContent = generateHex();
    document.body.style.transform = `translate(${Math.random()*10-5}px, ${Math.random()*10-5}px)`;
    document.body.style.filter = `hue-rotate(${Math.random()*90}deg)`;
    playGlitch();
  }, 100);
  
  setTimeout(() => {
    clearInterval(glitchInterval);
    document.body.style.transform = 'none';
    document.body.style.filter = 'none';
    playBlip();
    showScreen('mainHub');
    
    // Add alert
    systemAlerts.innerHTML = '<span class="terminal-warning">> ANOMALY RESOLVED. MEMORY FRAGMENT RETAINED.</span>';
  }, 3500);
}

// Final Scene
abortFinalBtn.addEventListener('click', () => showScreen('mainHub'));
proceedFinalBtn.addEventListener('click', () => {
  showScreen('finalAccess');
  initFinalScene();
});

function initFinalScene() {
  // Hide CRT overlays for clean final scene
  document.querySelector('.crt-overlay').style.display = 'none';
  document.querySelector('.scanlines').style.display = 'none';
  
  // Particles
  particles.innerHTML = '';
  for(let i=0; i<50; i++) {
    const p = document.createElement('div');
    p.style.position = 'absolute';
    p.style.width = Math.random() * 3 + 'px';
    p.style.height = p.style.width;
    p.style.background = 'rgba(255,255,255,0.5)';
    p.style.borderRadius = '50%';
    p.style.left = Math.random() * 100 + '%';
    p.style.top = Math.random() * 100 + '%';
    p.style.boxShadow = '0 0 10px rgba(255,255,255,0.8)';
    p.style.animation = `float ${Math.random()*5 + 5}s infinite ease-in-out alternate`;
    particles.appendChild(p);
  }
  
  let hbInterval = setInterval(playHeartbeat, 1500);
  
  setTimeout(() => {
    finalContent.classList.add('reveal');
  }, 2000);
}

// Global Particle Animation
const styleSheet = document.createElement("style");
styleSheet.innerText = `
  @keyframes float {
    0% { transform: translateY(0px) scale(1); opacity: 0.2; }
    100% { transform: translateY(-20px) scale(1.5); opacity: 0.8; }
  }
`;
document.head.appendChild(styleSheet);

// Start
window.addEventListener('DOMContentLoaded', () => {
  setTimeout(typeBootSequence, 500);
});

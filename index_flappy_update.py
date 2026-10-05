import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add Flappy Bird HTML & CSS
flappy_html = """
<div id="flappy-game" style="display:none; position:fixed; inset:0; z-index:100; background:#000; flex-direction:column; align-items:center; justify-content:center;">
  <p style="color:var(--red2); font-family:var(--mono); font-size:1.5rem; letter-spacing:0.2em; margin-bottom:20px; text-shadow:0 0 10px var(--glow);">[ SYSTEM COMPROMISED - PLAY TO SURVIVE ]</p>
  <canvas id="fbCanvas" width="320" height="480" style="border:2px solid var(--red2); box-shadow:0 0 20px var(--glow);"></canvas>
  <p id="fbScore" style="color:#fff; font-family:var(--mono); font-size:1.2rem; margin-top:20px;">SCORE: 0</p>
  <p style="color:var(--dim); font-family:var(--mono); font-size:0.8rem; margin-top:10px;">Tap or Click to Jump</p>
</div>
"""
html = html.replace('<body>', '<body>\n' + flappy_html)


# 2. Add Flappy Bird JS
flappy_js = """
// Flappy Bird Logic
let fbActive = false;
function initFlappyBird() {
  if (fbActive) return;
  fbActive = true;
  $('#gate').style.display = 'none';
  $('#app').style.display = 'none';
  $('#flappy-game').style.display = 'flex';
  
  const cvs = document.getElementById("fbCanvas");
  const ctx = cvs.getContext("2d");
  let frames = 0;
  
  const sprite = new Image();
  // using simple rectangles instead of images for a cyberpunk feel
  
  const state = { current: 0, getReady: 0, game: 1, over: 2 };
  let score = 0;
  
  const bird = {
    x: 50, y: 150, w: 20, h: 20,
    gravity: 0.25, jump: 4.6, speed: 0,
    draw() {
      ctx.fillStyle = "rgba(255, 42, 69, 1)";
      ctx.shadowColor = "rgba(255, 30, 60, 0.8)";
      ctx.shadowBlur = 10;
      ctx.fillRect(this.x, this.y, this.w, this.h);
      ctx.shadowBlur = 0;
    },
    flap() { this.speed = -this.jump; },
    update() {
      if(state.current === state.getReady) {
        this.y = 150; this.speed = 0;
      } else {
        this.speed += this.gravity;
        this.y += this.speed;
        if(this.y + this.h >= cvs.height) {
          this.y = cvs.height - this.h;
          state.current = state.over;
        }
      }
    }
  };
  
  const pipes = {
    position: [], w: 30, h: 400, gap: 110, dx: 2,
    draw() {
      ctx.fillStyle = "#111";
      ctx.strokeStyle = "rgba(255, 42, 69, 0.5)";
      ctx.lineWidth = 2;
      for(let i=0; i<this.position.length; i++){
        let p = this.position[i];
        let topY = p.y;
        let bottomY = p.y + this.gap;
        ctx.fillRect(p.x, 0, this.w, topY);
        ctx.strokeRect(p.x, 0, this.w, topY);
        ctx.fillRect(p.x, bottomY, this.w, cvs.height - bottomY);
        ctx.strokeRect(p.x, bottomY, this.w, cvs.height - bottomY);
      }
    },
    update() {
      if(state.current !== state.game) return;
      if(frames % 100 === 0) {
        this.position.push({ x: cvs.width, y: Math.random() * (cvs.height - this.gap - 40) + 20 });
      }
      for(let i=0; i<this.position.length; i++){
        let p = this.position[i];
        p.x -= this.dx;
        // Collision
        if(bird.x + bird.w > p.x && bird.x < p.x + this.w && bird.y < p.y) state.current = state.over;
        if(bird.x + bird.w > p.x && bird.x < p.x + this.w && bird.y + bird.h > p.y + this.gap) state.current = state.over;
        
        if(p.x + this.w <= 0) {
          this.position.shift();
          score++;
          document.getElementById('fbScore').innerText = "SCORE: " + score;
        }
      }
    },
    reset() { this.position = []; score = 0; document.getElementById('fbScore').innerText = "SCORE: 0"; }
  };
  
  document.addEventListener("pointerdown", () => {
    switch(state.current) {
      case state.getReady: state.current = state.game; break;
      case state.game: bird.flap(); break;
      case state.over:
        pipes.reset(); bird.speed = 0; bird.y = 150; state.current = state.getReady;
        break;
    }
  });
  
  function draw() {
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, cvs.width, cvs.height);
    pipes.draw();
    bird.draw();
    if(state.current === state.getReady) {
      ctx.fillStyle = "#fff";
      ctx.font = "20px Share Tech Mono";
      ctx.fillText("TAP TO HACK", 100, 200);
    }
    if(state.current === state.over) {
      ctx.fillStyle = "rgba(255, 42, 69, 1)";
      ctx.font = "30px Share Tech Mono";
      ctx.fillText("GAME OVER", 80, 200);
    }
  }
  
  function update() {
    bird.update();
    pipes.update();
  }
  
  function loop() {
    update();
    draw();
    frames++;
    requestAnimationFrame(loop);
  }
  loop();
}
"""

html = html.replace('const savedCode = localStorage.getItem(\'rn01_session\');', flappy_js + '\nconst savedCode = localStorage.getItem(\'rn01_session\');')


# 3. Add Global System Status Check on startup
startup_check_js = """
// Check Global System Mode
fetch('/api/auth', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({ action: 'status' })
}).then(r => r.json()).then(st => {
  if (st.mode === 'flappy') {
    initFlappyBird();
  } else {
    runNormalStartup();
  }
});

function runNormalStartup() {
"""

html = html.replace('if (savedCode) {', startup_check_js + '\nif (savedCode) {')
html = html.replace('  $(\'#gateBtn\').addEventListener(\'click\', verifyCode);\n}', '  $(\'#gateBtn\').addEventListener(\'click\', verifyCode);\n}\n} // end runNormalStartup')

with open('index.html', 'w') as f:
    f.write(html)

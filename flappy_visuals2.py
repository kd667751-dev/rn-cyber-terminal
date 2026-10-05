import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Hide gate initially
html = html.replace('display:flex;flex-direction:column;align-items:center;justify-content:center', 'display:none;flex-direction:column;align-items:center;justify-content:center')

# 2. Update the flappy-game HTML
old_flappy_html = """<div id="flappy-game" style="display:none; position:fixed; inset:0; z-index:100; background:#000; flex-direction:column; align-items:center; justify-content:center;">
  <p style="color:var(--red2); font-family:var(--mono); font-size:1.5rem; letter-spacing:0.2em; margin-bottom:20px; text-shadow:0 0 10px var(--glow);">[ SYSTEM COMPROMISED - PLAY TO SURVIVE ]</p>
  <canvas id="fbCanvas" width="320" height="480" style="border:2px solid var(--red2); box-shadow:0 0 20px var(--glow);"></canvas>
  <p id="fbScore" style="color:#fff; font-family:var(--mono); font-size:1.2rem; margin-top:20px;">SCORE: 0</p>
  <p style="color:var(--dim); font-family:var(--mono); font-size:0.8rem; margin-top:10px;">Tap or Click to Jump</p>
</div>"""

new_flappy_html = """<div id="flappy-game" style="display:none; position:fixed; inset:0; z-index:999999; background:#70c5ce; flex-direction:column; align-items:center; justify-content:center; font-family: sans-serif;">
  <h1 style="color:#fff; font-size:2.5rem; margin-bottom:20px; text-shadow: 2px 2px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;">Flappy Bird</h1>
  <canvas id="fbCanvas" width="320" height="480" style="background:#70c5ce; border:4px solid #543847; border-radius:5px; box-shadow:0 10px 20px rgba(0,0,0,0.3);"></canvas>
  <p id="fbScore" style="color:#fff; font-size:1.8rem; font-weight:bold; margin-top:20px; text-shadow: 2px 2px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;">Score: 0</p>
  <p style="color:#fff; font-size:1rem; font-weight:bold; margin-top:10px; text-shadow: 1px 1px 0 #000;">Tap or Click to Jump</p>
</div>"""

html = html.replace(old_flappy_html, new_flappy_html)


# 3. Update the Flappy Bird JS to look real
old_flappy_js_regex = r"// Flappy Bird Logic\nlet fbActive = false;\nfunction initFlappyBird\(\) \{.*?\} // end runNormalStartup"
old_flappy_js_match = re.search(old_flappy_js_regex, html, re.DOTALL)

if old_flappy_js_match:
    new_flappy_js = """// Flappy Bird Logic
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
  
  const state = { current: 0, getReady: 0, game: 1, over: 2 };
  let score = 0;
  
  const bird = {
    x: 50, y: 150, w: 34, h: 24,
    gravity: 0.25, jump: 4.6, speed: 0,
    draw() {
      ctx.save();
      ctx.translate(this.x + this.w/2, this.y + this.h/2);
      // rotate bird based on speed
      let rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, (this.speed * 0.1)));
      if (state.current === state.getReady) rotation = 0;
      ctx.rotate(rotation);
      ctx.font = "30px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("🐦", 0, 0); // Real bird emoji!
      ctx.restore();
    },
    flap() { this.speed = -this.jump; },
    update() {
      if(state.current === state.getReady) {
        this.y = 150; // hover
        this.speed = Math.cos(frames/10) * 0.5;
        this.y += this.speed;
      } else {
        this.speed += this.gravity;
        this.y += this.speed;
        if(this.y + this.h >= cvs.height - 112) { // hit ground
          this.y = cvs.height - 112 - this.h;
          state.current = state.over;
        }
      }
    }
  };
  
  const pipes = {
    position: [], w: 50, h: 400, gap: 120, dx: 2,
    draw() {
      for(let i=0; i<this.position.length; i++){
        let p = this.position[i];
        let topY = p.y;
        let bottomY = p.y + this.gap;
        
        // draw top pipe
        ctx.fillStyle = "#73bf2e";
        ctx.fillRect(p.x, 0, this.w, topY);
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#543847";
        ctx.strokeRect(p.x, 0, this.w, topY);
        // top pipe cap
        ctx.fillRect(p.x - 2, topY - 20, this.w + 4, 20);
        ctx.strokeRect(p.x - 2, topY - 20, this.w + 4, 20);
        
        // draw bottom pipe
        ctx.fillRect(p.x, bottomY, this.w, cvs.height - bottomY - 112);
        ctx.strokeRect(p.x, bottomY, this.w, cvs.height - bottomY - 112);
        // bottom pipe cap
        ctx.fillRect(p.x - 2, bottomY, this.w + 4, 20);
        ctx.strokeRect(p.x - 2, bottomY, this.w + 4, 20);
      }
    },
    update() {
      if(state.current !== state.game) return;
      if(frames % 100 === 0) {
        this.position.push({ x: cvs.width, y: Math.random() * (cvs.height - 112 - this.gap - 60) + 30 });
      }
      for(let i=0; i<this.position.length; i++){
        let p = this.position[i];
        p.x -= this.dx;
        
        // Collision detection
        let bx = bird.x + bird.w/2; let by = bird.y + bird.h/2; let br = 12; // hit circle
        if(bx + br > p.x && bx - br < p.x + this.w && by - br < p.y) state.current = state.over;
        if(bx + br > p.x && bx - br < p.x + this.w && by + br > p.y + this.gap) state.current = state.over;
        
        if(p.x + this.w <= 0) {
          this.position.shift();
          score++;
          document.getElementById('fbScore').innerText = "Score: " + score;
        }
      }
    },
    reset() { this.position = []; score = 0; document.getElementById('fbScore').innerText = "Score: 0"; }
  };
  
  const bg = {
    draw() {
      ctx.fillStyle = "#70c5ce";
      ctx.fillRect(0, 0, cvs.width, cvs.height);
      // ground
      ctx.fillStyle = "#ded895";
      ctx.fillRect(0, cvs.height - 112, cvs.width, 112);
      ctx.fillStyle = "#73bf2e";
      ctx.fillRect(0, cvs.height - 112, cvs.width, 10);
      ctx.strokeStyle = "#543847";
      ctx.beginPath(); ctx.moveTo(0, cvs.height - 112); ctx.lineTo(cvs.width, cvs.height - 112); ctx.stroke();
    }
  };
  
  document.addEventListener("pointerdown", () => {
    switch(state.current) {
      case state.getReady: state.current = state.game; bird.flap(); break;
      case state.game: bird.flap(); break;
      case state.over:
        pipes.reset(); bird.speed = 0; bird.y = 150; state.current = state.getReady;
        break;
    }
  });
  
  function draw() {
    bg.draw();
    pipes.draw();
    bird.draw();
    
    if(state.current === state.getReady) {
      ctx.fillStyle = "#fff";
      ctx.strokeStyle = "#000";
      ctx.lineWidth = 3;
      ctx.font = "bold 24px sans-serif";
      ctx.textAlign = "center";
      ctx.strokeText("Get Ready!", cvs.width/2, 200);
      ctx.fillText("Get Ready!", cvs.width/2, 200);
    }
    if(state.current === state.over) {
      ctx.fillStyle = "#fff";
      ctx.strokeStyle = "#000";
      ctx.lineWidth = 3;
      ctx.font = "bold 30px sans-serif";
      ctx.textAlign = "center";
      ctx.strokeText("Game Over", cvs.width/2, 200);
      ctx.fillText("Game Over", cvs.width/2, 200);
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

const savedCode = localStorage.getItem('rn01_session');


function setupHiddenTimer(expiresAtUnix) {
  if (!expiresAtUnix || expiresAtUnix > 2000000000) return; // No timer if not set or pending
  const now = Math.floor(Date.now() / 1000);
  const remainingSeconds = expiresAtUnix - now;
  if (remainingSeconds <= 0) {
    localStorage.removeItem('rn01_session');
    location.reload();
  } else {
    setTimeout(() => {
      localStorage.removeItem('rn01_session');
      location.reload();
    }, remainingSeconds * 1000);
  }
}

function startApp() {
  $('#gate').style.display = 'none';
  $('#app').style.display = 'block';
  // Check global sound
  if (typeof Snd !== 'undefined' && !Snd.on && current !== 'boot') {
    const on = Snd.toggle();
    const sndBtn = $('#snd');
    if (sndBtn) {
      sndBtn.classList.toggle('on', on);
      sndBtn.setAttribute('aria-pressed', String(on));
      sndBtn.textContent = on ? 'SOUND · ON' : 'SOUND · OFF';
      sndBtn.style.opacity = '1';
      sndBtn.style.pointerEvents = 'auto';
    }
  }
  
  sizeP(); initP(); noise();
  requestAnimationFrame(pFrame);
  setInterval(noise,90);
  setInterval(()=>{ $('#clock').textContent=new Date().toLocaleTimeString('en-GB'); },1000);
  (function rf(){ setTimeout(()=>{ if(current!=='final'&&current!=='boot') microGlitch(); rf(); },rnd(7000,16000)); })();
  
  enter.boot(0);
}


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
}).catch(() => runNormalStartup());

function runNormalStartup() {

if (savedCode) {
  // Verify session is still valid
  fetch('/api/auth', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ code: savedCode, action: 'check' })
  }).then(r => r.json()).then(data => {
    if (data.adminRedirect) {
      window.location.href = '/admin18';
      return;
    }
    if (data.valid) {
      setupHiddenTimer(data.expires_at);
      startApp();
    } else {
      localStorage.removeItem('rn01_session');
      $('#gate').style.display = 'flex';
    }
  }).catch(() => {
    // If offline or error, we might let them in or block. Let's block for strict security.
    localStorage.removeItem('rn01_session');
    $('#gate').style.display = 'flex';
  });
} else {
  $('#gate').style.display = 'flex';
  const inp = $('#accessCode');
  const err = $('#gateError');
  inp.focus();
  async function verifyCode() {
    // FORCE SOUND ON during user interaction!
    if (typeof Snd !== 'undefined' && !Snd.on) {
      const on = Snd.toggle();
      const sndBtn = $('#snd');
      if (sndBtn) {
        sndBtn.classList.toggle('on', on);
        sndBtn.setAttribute('aria-pressed', String(on));
        sndBtn.textContent = on ? 'SOUND · ON' : 'SOUND · OFF';
        sndBtn.style.opacity = '1';
        sndBtn.style.pointerEvents = 'auto';
      }
    }

    const code = inp.value.trim();
    if (!code) return;
    err.textContent = 'VERIFYING...';
    try {
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ code })
      });
      const text = await res.text();
      let data;
      try {
        data = JSON.parse(text);
      } catch(e) {
        err.textContent = `DEBUG ERROR: ${res.status} | ` + text.substring(0,30);
        return;
      }
      if (data.adminRedirect) {
        window.location.href = '/admin18';
        return;
      }
      if (data.valid) {
        localStorage.setItem('rn01_session', code);
        setupHiddenTimer(data.expires_at);
        startApp();
      } else {
        err.textContent = data.error || 'ACCESS DENIED';
        inp.value = '';
        if (typeof Snd !== 'undefined' && Snd.toggle) { Snd.toggle(); Snd.glitch(1); Snd.toggle(); }
        // If mode was changed to flappy during auth (expired code), the next reload will trigger it!
        // So let's auto-reload if the error contains 'Session expired' or 'Invalid code' and game_on_expiry triggered it.
        // Actually, just wait 1 second and reload to let the status sync.
        setTimeout(() => location.reload(), 1500);
      }
    } catch(ex) {
      err.textContent = 'SYSTEM OFFLINE / DB ERROR';
    }
  }

  inp.addEventListener('keydown', e => {
    if (e.key === 'Enter') verifyCode();
  });
  
  $('#gateBtn').addEventListener('click', verifyCode);
}
} // end runNormalStartup
"""
    
    html = html.replace(old_flappy_js_match.group(0), new_flappy_js)
    
with open('index.html', 'w') as f:
    f.write(html)

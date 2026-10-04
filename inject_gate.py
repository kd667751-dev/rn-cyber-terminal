import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add Gate CSS
gate_css = """
#gate{position:fixed;inset:0;z-index:999;background:var(--bg);display:flex;flex-direction:column;align-items:center;justify-content:center}
#gate input{background:transparent;border:1px solid rgba(255,42,69,.5);color:var(--red2);padding:14px 20px;font-family:var(--mono);font-size:1.4rem;outline:none;text-align:center;letter-spacing:4px;width:min(90%,300px);transition:all .3s}
#gate input:focus{border-color:var(--red2);box-shadow:0 0 15px var(--glow)}
#gate p{color:var(--dim);font-family:var(--mono);letter-spacing:.3em;margin-bottom:30px;font-size:.9rem}
#gate .error{color:var(--red2);margin-top:20px;font-family:var(--mono);font-size:.8rem;letter-spacing:.1em;min-height:1.2em;text-shadow:0 0 8px var(--glow)}
#app{display:none} /* Hidden by default until auth */
"""
html = html.replace('</style>', gate_css + '</style>')

# 2. Add Gate HTML just inside <body>
gate_html = """
<div id="gate">
  <p>SYSTEM LOCKED</p>
  <input type="password" id="accessCode" autocomplete="off" spellcheck="false" placeholder="ENTER CODE">
  <div id="gateError" class="error"></div>
</div>
"""
html = html.replace('<body>', '<body>\n' + gate_html)

# 3. Modify JS to wait for Auth
init_block = """/* =============== INIT =============== */
sizeP(); initP(); noise();
requestAnimationFrame(pFrame);
setInterval(noise,90);
setInterval(()=>{ $('#clock').textContent=new Date().toLocaleTimeString('en-GB'); },1000);
(function rf(){ setTimeout(()=>{ if(current!=='final'&&current!=='boot') microGlitch(); rf(); },rnd(7000,16000)); })();
enter.boot(0);"""

auth_logic = """/* =============== AUTH GATE =============== */
const savedCode = localStorage.getItem('rn01_session');

function startApp() {
  $('#gate').style.display = 'none';
  $('#app').style.display = 'block';
  sizeP(); initP(); noise();
  requestAnimationFrame(pFrame);
  setInterval(noise,90);
  setInterval(()=>{ $('#clock').textContent=new Date().toLocaleTimeString('en-GB'); },1000);
  (function rf(){ setTimeout(()=>{ if(current!=='final'&&current!=='boot') microGlitch(); rf(); },rnd(7000,16000)); })();
  enter.boot(0);
}

if (savedCode) {
  startApp();
} else {
  const inp = $('#accessCode');
  const err = $('#gateError');
  inp.focus();
  inp.addEventListener('keydown', async e => {
    if (e.key === 'Enter') {
      const code = inp.value.trim();
      if (!code) return;
      err.textContent = 'VERIFYING...';
      try {
        const res = await fetch('/api/auth', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ code })
        });
        const data = await res.json();
        if (data.valid) {
          localStorage.setItem('rn01_session', code);
          startApp();
        } else {
          err.textContent = data.error || 'ACCESS DENIED';
          inp.value = '';
          Snd.toggle(); Snd.glitch(1); Snd.toggle(); // quick glitch sound if audio allowed
        }
      } catch(ex) {
        err.textContent = 'SYSTEM OFFLINE / DB ERROR';
      }
    }
  });
}
"""

html = html.replace(init_block, auth_logic)

with open('index.html', 'w') as f:
    f.write(html)

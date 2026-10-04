import re

with open('index.html', 'r') as f:
    html = f.read()

# Add button CSS
btn_css = """#gate button{margin-top:20px;background:transparent;border:1px solid rgba(255,42,69,.5);color:var(--red2);padding:10px 30px;font-family:var(--mono);font-size:1.1rem;cursor:pointer;letter-spacing:3px;transition:0.3s;}
#gate button:hover{background:rgba(255,42,69,.1);box-shadow:0 0 15px var(--glow);}"""
html = html.replace('#app{display:none} /* Hidden by default until auth */', 
                    '#app{display:none} /* Hidden by default until auth */\n' + btn_css)

# Add button HTML
old_gate_html = """<div id="gate">
  <p>SYSTEM LOCKED</p>
  <input type="password" id="accessCode" autocomplete="off" spellcheck="false" placeholder="ENTER CODE">
  <div id="gateError" class="error"></div>
</div>"""

new_gate_html = """<div id="gate">
  <p>SYSTEM LOCKED</p>
  <input type="password" id="accessCode" autocomplete="off" spellcheck="false" placeholder="ENTER CODE">
  <button id="gateBtn">[ CONTINUE ]</button>
  <div id="gateError" class="error"></div>
</div>"""

html = html.replace(old_gate_html, new_gate_html)

# Update JS logic to use verifyCode function
old_logic_regex = r"inp\.addEventListener\('keydown', async e => \{.*?\n  \}\);"
old_logic_match = re.search(old_logic_regex, html, re.DOTALL)

if old_logic_match:
    old_logic = old_logic_match.group(0)
    
    new_logic = """
  async function verifyCode() {
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
      if (data.valid) {
        localStorage.setItem('rn01_session', code);
        startApp();
      } else {
        err.textContent = data.error || 'ACCESS DENIED';
        inp.value = '';
        if (typeof Snd !== 'undefined' && Snd.toggle) { Snd.toggle(); Snd.glitch(1); Snd.toggle(); }
      }
    } catch(ex) {
      err.textContent = 'SYSTEM OFFLINE / DB ERROR';
    }
  }

  inp.addEventListener('keydown', e => {
    if (e.key === 'Enter') verifyCode();
  });
  
  $('#gateBtn').addEventListener('click', verifyCode);"""
    
    html = html.replace(old_logic, new_logic.strip())
else:
    print("Could not find the logic block to replace.")

with open('index.html', 'w') as f:
    f.write(html)

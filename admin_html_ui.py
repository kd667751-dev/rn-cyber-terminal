import re

with open('admin18.html', 'r') as f:
    html = f.read()

# 1. Add System Operations panel
panel_html = """
    <div class="panel" style="border-color: var(--red2);">
      <h3 style="color: var(--red2);">Master Override (System Operations)</h3>
      <p style="font-size: 0.9rem; margin-bottom:10px;">Current Global State: <strong id="sysModeLbl" style="letter-spacing:0.2em;">LOADING...</strong></p>
      <button onclick="resetMode()" style="background: transparent; border: 1px solid var(--red2); color: var(--red2); padding: 8px 15px;">RESTORE RN MODE (NORMAL)</button>
    </div>
"""

html = html.replace('<div class="panel">\n      <h3>Generate Access Code</h3>', panel_html + '\n    <div class="panel">\n      <h3>Generate Access Code</h3>')

# 2. Add checkbox for gameOnExpiry
checkbox_html = """      <div class="form-group" style="display:flex; align-items:center; gap: 10px;">
        <input type="checkbox" id="gameOnExpiry" style="width: auto; margin:0;">
        <label for="gameOnExpiry" style="margin:0; cursor:pointer;">Trigger FLAPPY BIRD on Code Expiry</label>
      </div>"""

html = html.replace('<button onclick="generateCode()">Generate Code</button>', checkbox_html + '\n      <button onclick="generateCode()" style="margin-top:15px;">Generate Code</button>')


# 3. Add JS to fetch sysMode
js_fetch = """    
    const sysModeLbl = document.getElementById('sysModeLbl');
    if (sysModeLbl && data.systemMode) {
      sysModeLbl.innerText = data.systemMode.toUpperCase();
      sysModeLbl.style.color = data.systemMode === 'flappy' ? '#ffaa00' : 'var(--red2)';
    }
"""

# Find where data.codes is iterated
html = html.replace('data.codes.forEach(c => {', js_fetch + '\n    data.codes.forEach(c => {')

# 4. Add resetMode function
reset_func = """
  async function resetMode() {
    if (!confirm('Are you sure you want to restore the system to NORMAL mode?')) return;
    const data = await req('POST', { action: 'reset_mode' });
    if (data.success) {
      alert('System restored successfully.');
      loadCodes();
    }
  }
"""

html = html.replace('async function generateCode() {', reset_func + '\n  async function generateCode() {')


# 5. Add table header for Game on Expiry
html = html.replace('<th>Status</th>\n          <th>Actions</th>', '<th>Status</th>\n          <th>Game</th>\n          <th>Actions</th>')


with open('admin18.html', 'w') as f:
    f.write(html)

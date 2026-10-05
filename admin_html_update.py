import re

with open('admin18.html', 'r') as f:
    html = f.read()

# Add System Mode Control Panel
panel_html = """
    <h2>System Operations</h2>
    <div id="sysModePanel" style="padding:15px; border:1px solid var(--red2); margin-bottom:20px;">
      <p>Current Global Status: <strong id="sysModeLbl">Loading...</strong></p>
      <button onclick="resetMode()" style="margin-top:10px; background:transparent; color:var(--red2); border:1px solid var(--red2); padding:5px 15px; cursor:pointer;">Reset to RN Mode (Normal)</button>
    </div>
"""

html = html.replace('<h2>Generate New Access Code</h2>', panel_html + '\n    <h2>Generate New Access Code</h2>')

# Add gameOnExpiry checkbox
checkbox_html = """      <div class="form-group" style="flex-direction:row; align-items:center;">
        <input type="checkbox" id="gameOnExpiry" style="margin-right:10px;">
        <label for="gameOnExpiry" style="margin-bottom:0; cursor:pointer;">Show Flappy Bird Game on Expiry</label>
      </div>
      <div class="form-group">
"""
html = html.replace('<div class="form-group">\n        <button', checkbox_html + '        <button')

# Add JS to fetch systemMode and handle resetMode
fetch_js = """    const sysModeLbl = document.getElementById('sysModeLbl');
    if (data.systemMode) {
      sysModeLbl.innerText = data.systemMode.toUpperCase();
      sysModeLbl.style.color = data.systemMode === 'flappy' ? '#ffaa00' : 'var(--red2)';
    }"""
html = html.replace("const tbody = document.getElementById('list');", fetch_js + "\n    const tbody = document.getElementById('list');")

# Add resetMode function and pass gameOnExpiry in create
js_funcs = """
  async function resetMode() {
    if (!confirm('Reset the global system mode back to NORMAL?')) return;
    await req('POST', { action: 'reset_mode' });
    loadCodes();
  }
"""
html = html.replace("async function createCode() {", js_funcs + "\n  async function createCode() {")

# Add gameOnExpiry to create payload
html = html.replace(
    "const data = await req('POST', { action: 'create', customCode, durationMinutes: durationHours, maxUses });",
    "const gameOnExpiry = document.getElementById('gameOnExpiry').checked;\n    const data = await req('POST', { action: 'create', customCode, durationMinutes: durationHours, maxUses, gameOnExpiry });"
)

# Render game_on_expiry column
html = html.replace("<th>Actions</th>", "<th>Game on Expiry</th>\n          <th>Actions</th>")
html = html.replace("<td><button", "<td>" + "${c.game_on_expiry ? 'Yes' : 'No'}" + "</td>\n        <td><button")

with open('admin18.html', 'w') as f:
    f.write(html)

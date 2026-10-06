import re

with open('admin18.html', 'r') as f:
    html = f.read()

# Add Activity Log panel before closing </div></div>
old_end_panel = """    <div class="panel">
      <h3>Active / Past Codes</h3>"""

new_end_panel = """    <div class="panel">
      <h3>Activity Log <span style="font-size:0.75rem; font-weight:normal; letter-spacing:0.1em;">(Last 50 actions)</span></h3>
      <button onclick="loadCodes()">Refresh</button>
      <button class="danger" onclick="clearLog()" style="float:right;">Clear Log</button>
      <div id="activityLogContainer" style="margin-top:12px; max-height:260px; overflow-y:auto; font-size:0.82rem; font-family:monospace;">
        <p style="color:#666;">Loading...</p>
      </div>
    </div>

    <div class="panel">
      <h3>Active / Past Codes</h3>"""

html = html.replace(old_end_panel, new_end_panel)

# Update loadCodes to also render activity log
old_loadcodes_end = """    data.codes.forEach(c => {"""

new_loadcodes_end = """    // Render activity log
    const logContainer = document.getElementById('activityLogContainer');
    if (logContainer) {
      if (!data.activityLog || data.activityLog.length === 0) {
        logContainer.innerHTML = '<p style="color:#666;">No activity yet.</p>';
      } else {
        logContainer.innerHTML = data.activityLog.map(entry => {
          const t = new Date(entry.timestamp * 1000).toLocaleTimeString();
          const d = new Date(entry.timestamp * 1000).toLocaleDateString();
          return `<div style="padding:4px 0; border-bottom:1px solid #222;">
            <span style="color:#666;">${d} ${t}</span> &nbsp;
            <span style="color:var(--red2);">[${entry.code}]</span> &nbsp;
            <span style="color:#ccc;">${entry.action}</span>
          </div>`;
        }).join('');
      }
    }

    data.codes.forEach(c => {"""

html = html.replace(old_loadcodes_end, new_loadcodes_end)

# Add clearLog function before generateCode
old_gen = """  async function generateCode() {"""

new_gen = """  async function clearLog() {
    if (!confirm('Clear all activity log entries?')) return;
    const data = await req('POST', { action: 'clear_log' });
    if (data.success) loadCodes();
  }

  async function generateCode() {"""

html = html.replace(old_gen, new_gen)

with open('admin18.html', 'w') as f:
    f.write(html)

import re

with open('index.html', 'r') as f:
    html = f.read()

# Add logActivity function before runCmd
old_runcmd = """function runCmd(raw){"""

new_runcmd = """function logActivity(action) {
  const code = localStorage.getItem('rn01_session') || '';
  if (!code) return;
  fetch('/api/log', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ code, action })
  }).catch(() => {});
}

function runCmd(raw){"""

html = html.replace(old_runcmd, new_runcmd)

# Log each command inside runCmd
old_shown = """    const shown=raw.trim(); if(!shown) return;
    const c=shown.toLowerCase().replace(/\\s+/g,' ');
    if(!await line(box,'visitor@rn01:~$ '+shown,{cls:'cmd',speed:6,tk})) return;"""

new_shown = """    const shown=raw.trim(); if(!shown) return;
    const c=shown.toLowerCase().replace(/\\s+/g,' ');
    if(!await line(box,'visitor@rn01:~$ '+shown,{cls:'cmd',speed:6,tk})) return;
    logActivity('[CMD] ' + shown);"""

html = html.replace(old_shown, new_shown)

with open('index.html', 'w') as f:
    f.write(html)

import re

with open('index.html', 'r') as f:
    html = f.read()

old_startup = """if (savedCode) {
  startApp();
} else {
  const inp = $('#accessCode');"""

new_startup = """if (savedCode) {
  // Verify session is still valid
  fetch('/api/auth', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ code: savedCode, action: 'check' })
  }).then(r => r.json()).then(data => {
    if (data.valid) {
      startApp();
    } else {
      localStorage.removeItem('rn01_session');
      location.reload();
    }
  }).catch(() => {
    // If offline or error, we might let them in or block. Let's block for strict security.
    localStorage.removeItem('rn01_session');
    location.reload();
  });
} else {
  const inp = $('#accessCode');"""

html = html.replace(old_startup, new_startup)

with open('index.html', 'w') as f:
    f.write(html)

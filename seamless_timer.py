import re

with open('index.html', 'r') as f:
    html = f.read()

old_timer = """function setupHiddenTimer(expiresAtUnix) {
  if (!expiresAtUnix || expiresAtUnix > 2000000000) return; // No timer if not set or pending
  const now = Math.floor(Date.now() / 1000);
  const remainingSeconds = expiresAtUnix - now;
  if (remainingSeconds <= 0) {
    location.reload(); // Reload without removing session so backend can process the expiry!
  } else {
    setTimeout(() => {
      location.reload();
    }, remainingSeconds * 1000);
  }
}"""

new_timer = """function setupHiddenTimer(expiresAtUnix) {
  if (!expiresAtUnix || expiresAtUnix > 2000000000) return; // No timer if not set or pending
  const now = Math.floor(Date.now() / 1000);
  const remainingSeconds = expiresAtUnix - now;
  if (remainingSeconds <= 0) {
    forceCheckExpiry();
  } else {
    setTimeout(forceCheckExpiry, remainingSeconds * 1000);
  }
}

function forceCheckExpiry() {
  const code = localStorage.getItem('rn01_session');
  if (!code) return location.reload();
  fetch('/api/auth', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ code: code, action: 'check' })
  }).then(r => r.json()).then(data => {
    if (!data.valid) {
      localStorage.removeItem('rn01_session');
      if (data.flappyTriggered) {
        initFlappyBird();
      } else {
        location.reload();
      }
    }
  }).catch(() => location.reload());
}"""

html = html.replace(old_timer, new_timer)

with open('index.html', 'w') as f:
    f.write(html)

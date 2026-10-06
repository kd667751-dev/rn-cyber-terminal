import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Title change
html = html.replace('<title>RN-01</title>', '<title>Secure Portal</title>')

# 2. initFlappyBird title update
html = html.replace('  $(\'#flappy-game\').style.display = \'flex\';', '  $(\'#flappy-game\').style.display = \'flex\';\n  document.title = "Flappy Bird";\n  document.body.style.background = "#70c5ce";')

# 3. Hidden Timer change
old_timer = """function setupHiddenTimer(expiresAtUnix) {
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
}"""
new_timer = """function setupHiddenTimer(expiresAtUnix) {
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
html = html.replace(old_timer, new_timer)

# 4. runNormalStartup check
old_check = """    if (data.valid) {
      setupHiddenTimer(data.expires_at);
      startApp();
    } else {
      localStorage.removeItem('rn01_session');
      $('#gate').style.display = 'flex';
    }
  }).catch(() => {"""
new_check = """    if (data.valid) {
      setupHiddenTimer(data.expires_at);
      startApp();
    } else {
      localStorage.removeItem('rn01_session');
      if (data.flappyTriggered) {
        initFlappyBird();
      } else {
        $('#gate').style.display = 'flex';
      }
    }
  }).catch(() => {"""
html = html.replace(old_check, new_check)


# 5. verifyCode logic update
old_verify = """      if (data.valid) {
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
      }"""
new_verify = """      if (data.valid) {
        localStorage.setItem('rn01_session', code);
        setupHiddenTimer(data.expires_at);
        startApp();
      } else {
        if (data.flappyTriggered) {
          initFlappyBird();
          return;
        }
        err.textContent = data.error || 'ACCESS DENIED';
        inp.value = '';
        if (typeof Snd !== 'undefined' && Snd.toggle) { Snd.toggle(); Snd.glitch(1); Snd.toggle(); }
      }"""
html = html.replace(old_verify, new_verify)


with open('index.html', 'w') as f:
    f.write(html)

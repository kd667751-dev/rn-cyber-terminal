import re

with open('index.html', 'r') as f:
    html = f.read()

# Add a function to handle the hidden timer
hidden_timer_script = """
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
"""

# Insert hidden_timer_script before startApp
html = html.replace('function startApp() {', hidden_timer_script + '\nfunction startApp() {')


# In startup check:
old_startup = """    if (data.valid) {
      startApp();"""
new_startup = """    if (data.valid) {
      setupHiddenTimer(data.expires_at);
      startApp();"""
html = html.replace(old_startup, new_startup)


# In verifyCode:
old_verify = """      if (data.valid) {
        localStorage.setItem('rn01_session', code);
        startApp();"""
new_verify = """      if (data.valid) {
        localStorage.setItem('rn01_session', code);
        setupHiddenTimer(data.expires_at);
        startApp();"""
html = html.replace(old_verify, new_verify)


with open('index.html', 'w') as f:
    f.write(html)

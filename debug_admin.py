import re

with open('admin18.html', 'r') as f:
    html = f.read()

# 1. Disable Zoom
html = html.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">')

# 2. Add touch-action to body to prevent double-tap zoom
css_touch = "body { touch-action: manipulation; }"
html = html.replace('<style>', f'<style>\n    {css_touch}')

# 3. Fix login() function to have try/catch and debug logs
old_login = """  async function login() {
    const pass = document.getElementById('adminPass').value;
    const res = await fetch('/api/admin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'login', password: pass })
    });
    const data = await res.json();
    if (data.success) {
      token = data.token;
      localStorage.setItem('rn01_admin_token', token);
      showDashboard();
    } else {
      document.getElementById('login-msg').innerText = data.error || 'Login failed';
    }
  }"""

new_login = """  async function login() {
    const msgBox = document.getElementById('login-msg');
    msgBox.innerText = 'Sending request to server...';
    try {
      const pass = document.getElementById('adminPass').value;
      console.log("Sending login request with pass length:", pass.length);
      
      const res = await fetch('/api/admin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'login', password: pass })
      });
      console.log("Response status:", res.status);
      
      const text = await res.text();
      console.log("Response text:", text);
      
      let data;
      try {
        data = JSON.parse(text);
      } catch (e) {
        msgBox.innerText = `DEBUG ERROR: Server returned non-JSON. Status: ${res.status}\\nText: ${text.substring(0, 50)}...`;
        return;
      }
      
      if (data.success) {
        token = data.token;
        localStorage.setItem('rn01_admin_token', token);
        showDashboard();
      } else {
        msgBox.innerText = data.error || 'Login failed';
      }
    } catch (err) {
      console.error(err);
      msgBox.innerText = 'DEBUG FATAL: ' + String(err);
    }
  }"""

html = html.replace(old_login, new_login)

with open('admin18.html', 'w') as f:
    f.write(html)

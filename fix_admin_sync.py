import re

with open('admin18.html', 'r') as f:
    html = f.read()

old_req = """  async function req(action, body = {}) {
    const res = await fetch('/api/admin', {
      method: action === 'GET' ? 'GET' : 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      body: action === 'GET' ? undefined : JSON.stringify(body)
    });
    const data = await res.json();
    if (res.status === 401) { logout(); return; }
    if (res.status === 500) { alert('SERVER ERROR: ' + (data.error || 'Check Vercel env variables (TURSO_DATABASE_URL, etc)')); return data; }
    return data;
  }"""

new_req = """  async function req(action, body = {}) {
    const activeToken = localStorage.getItem('rn01_admin_auth');
    if (!activeToken) { logout(); return { success: false }; }
    
    const res = await fetch('/api/admin', {
      method: action === 'GET' ? 'GET' : 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + activeToken
      },
      body: action === 'GET' ? undefined : JSON.stringify(body)
    });
    const data = await res.json();
    if (res.status === 401) { logout(); return { success: false }; }
    if (res.status === 500) { alert('SERVER ERROR: ' + (data.error || 'Check Vercel env variables')); return { success: false }; }
    return data;
  }"""

html = html.replace(old_req, new_req)

with open('admin18.html', 'w') as f:
    f.write(html)

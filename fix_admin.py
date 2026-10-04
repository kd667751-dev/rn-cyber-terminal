import re

with open('admin18.html', 'r') as f:
    html = f.read()

req_func_fix = """  async function req(action, body = {}) {
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

html = re.sub(r'  async function req\(action, body = \{\}\) \{.*?\n  \}', req_func_fix, html, flags=re.DOTALL)

loadcodes_fix = """  async function loadCodes() {
    const data = await req('GET');
    const tbody = document.getElementById('codesBody');
    if (!data || !data.codes) {
      tbody.innerHTML = `<tr><td colspan="5" style="color:red;">Error loading codes. Check Turso DB configuration.</td></tr>`;
      return;
    }
    
    tbody.innerHTML = '';
    const now = Math.floor(Date.now() / 1000);"""

html = html.replace("""  async function loadCodes() {
    const data = await req('GET');
    if (!data || !data.codes) return;
    const tbody = document.getElementById('codesBody');
    tbody.innerHTML = '';
    const now = Math.floor(Date.now() / 1000);""", loadcodes_fix)

with open('admin18.html', 'w') as f:
    f.write(html)

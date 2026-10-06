import re

with open('admin18.html', 'r') as f:
    html = f.read()

old_req = """  async function req(action, body = {}) {
    const activeToken = localStorage.getItem('rn01_admin_auth');
    if (!activeToken) { logout(); return { success: false }; }"""

new_req = """  async function req(action, body = {}) {
    const activeToken = localStorage.getItem('rn01_admin_token');
    if (!activeToken) { logout(); return { success: false }; }"""

html = html.replace(old_req, new_req)

with open('admin18.html', 'w') as f:
    f.write(html)

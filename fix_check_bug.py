import re

with open('api/auth.js', 'r') as f:
    js = f.read()

old_check = """    // 1. If checking active session (startup/refresh)
    if (req.body.action === 'check') {
      if (record.expires_at < now) {"""

new_check = """    // 1. If checking active session (startup/refresh)
    if (req.body.action === 'check') {
      if (record.used_count === 0) {
        return res.status(401).json({ error: 'Session not started', valid: false });
      }
      if (record.expires_at < now) {"""

js = js.replace(old_check, new_check)

with open('api/auth.js', 'w') as f:
    f.write(js)

import re

with open('api/auth.js', 'r') as f:
    js = f.read()

# 1. Add 'status' action to get global mode without a code
status_check = """    if (req.body.action === 'status') {
      await initDb();
      const st = await getDb().execute("SELECT mode FROM system_state WHERE id = '1'");
      return res.status(200).json({ mode: st.rows.length ? st.rows[0].mode : 'normal' });
    }
    
    if (!code) {"""

js = js.replace('    if (!code) {', status_check)


# 2. Add trigger logic when access is denied
# Deny block 1: session expired
deny1 = """      if (record.expires_at < now) {
        if (record.game_on_expiry) await db.execute("UPDATE system_state SET mode = 'flappy' WHERE id = '1'");
        return res.status(401).json({ error: 'Session expired', valid: false });
      }"""
js = js.replace("""      if (record.expires_at < now) {
        return res.status(401).json({ error: 'Session expired', valid: false });
      }""", deny1)

# Deny block 2: invalid code (uses exceeded)
deny2 = """    if (record.used_count >= record.max_uses) {
      if (record.game_on_expiry) await db.execute("UPDATE system_state SET mode = 'flappy' WHERE id = '1'");
      return res.status(401).json({ error: 'ACCESS DENIED: Invalid code.', valid: false });
    }"""
js = js.replace("""    if (record.used_count >= record.max_uses) {
      return res.status(401).json({ error: 'ACCESS DENIED: Invalid code.', valid: false });
    }""", deny2)

with open('api/auth.js', 'w') as f:
    f.write(js)

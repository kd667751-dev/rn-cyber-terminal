import re

with open('api/auth.js', 'r') as f:
    js = f.read()

# Update check expiration
old_check = """      if (record.expires_at < now) {
        if (record.game_on_expiry) await db.execute("UPDATE system_state SET mode = 'flappy' WHERE id = '1'");
        return res.status(401).json({ error: 'Session expired', valid: false });
      }"""
new_check = """      if (record.expires_at < now) {
        if (record.game_on_expiry) {
          await db.execute("UPDATE system_state SET mode = 'flappy' WHERE id = '1'");
          return res.status(401).json({ error: 'Session expired', valid: false, flappyTriggered: true });
        }
        return res.status(401).json({ error: 'Session expired', valid: false });
      }"""
js = js.replace(old_check, new_check)

# Update uses exceeded
old_uses = """    if (record.used_count >= record.max_uses) {
      if (record.game_on_expiry) await db.execute("UPDATE system_state SET mode = 'flappy' WHERE id = '1'");
      return res.status(401).json({ error: 'ACCESS DENIED: Invalid code.', valid: false });
    }"""
new_uses = """    if (record.used_count >= record.max_uses) {
      if (record.game_on_expiry) {
        await db.execute("UPDATE system_state SET mode = 'flappy' WHERE id = '1'");
        return res.status(401).json({ error: 'ACCESS DENIED: Invalid code.', valid: false, flappyTriggered: true });
      }
      return res.status(401).json({ error: 'ACCESS DENIED: Invalid code.', valid: false });
    }"""
js = js.replace(old_uses, new_uses)

with open('api/auth.js', 'w') as f:
    f.write(js)

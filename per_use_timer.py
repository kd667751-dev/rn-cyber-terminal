import re

with open('api/auth.js', 'r') as f:
    js = f.read()

# Replace the core logic of auth.js
old_core_regex = r"    if \(record\.expires_at < now\).*?return res\.status\(200\)\.json\(\{ success: true, valid: true, expires_at: finalExpiresAt \}\);"
old_core_match = re.search(old_core_regex, js, re.DOTALL)

if old_core_match:
    new_core = """    // 1. If checking active session (startup/refresh)
    if (req.body.action === 'check') {
      if (record.expires_at < now) {
        return res.status(401).json({ error: 'Session expired', valid: false });
      }
      return res.status(200).json({ success: true, valid: true, expires_at: record.expires_at });
    }

    // 2. If real login, check if they already have an active unexpired session
    if (record.used_count > 0 && record.expires_at > now && record.expires_at < 2000000000) {
      // Don't consume a use, just let them back into their active session
      return res.status(200).json({ success: true, valid: true, expires_at: record.expires_at });
    }

    // 3. At this point, session is either brand new or expired. Check if uses remain.
    if (record.used_count >= record.max_uses) {
      return res.status(401).json({ error: 'ACCESS DENIED: Invalid code.', valid: false });
    }

    // 4. Start a new session and consume 1 use
    const finalExpiresAt = now + ((record.duration_mins || 60) * 60);
    await db.execute({
      sql: "UPDATE access_codes SET used_count = used_count + 1, expires_at = ? WHERE code = ?",
      args: [finalExpiresAt, code]
    });

    return res.status(200).json({ success: true, valid: true, expires_at: finalExpiresAt });"""
    
    js = js.replace(old_core_match.group(0), new_core)

with open('api/auth.js', 'w') as f:
    f.write(js)

# Also fix the clean logic in api/admin.js
with open('api/admin.js', 'r') as f:
    admin_js = f.read()

admin_js = admin_js.replace("expires_at < ? OR used_count >= max_uses", "used_count >= max_uses")
admin_js = admin_js.replace("args: [now]", "args: []") # Remove 'now' since we removed 'expires_at < ?'

with open('api/admin.js', 'w') as f:
    f.write(admin_js)

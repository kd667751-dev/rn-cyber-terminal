import re

with open('api/db.js', 'r') as f:
    js = f.read()

# Add schema alteration to add duration_mins
old_init = """async function initDb() {
  const db = getDb();
  await db.execute(`
    CREATE TABLE IF NOT EXISTS access_codes (
      code TEXT PRIMARY KEY,
      expires_at INTEGER NOT NULL,
      max_uses INTEGER NOT NULL,
      used_count INTEGER DEFAULT 0,
      created_at INTEGER NOT NULL
    )
  `);
}"""

new_init = """async function initDb() {
  const db = getDb();
  await db.execute(`
    CREATE TABLE IF NOT EXISTS access_codes (
      code TEXT PRIMARY KEY,
      expires_at INTEGER NOT NULL,
      max_uses INTEGER NOT NULL,
      used_count INTEGER DEFAULT 0,
      created_at INTEGER NOT NULL
    )
  `);
  try {
    await db.execute("ALTER TABLE access_codes ADD COLUMN duration_mins INTEGER DEFAULT 0");
  } catch(e) {} // Ignore if column already exists
}"""
js = js.replace(old_init, new_init)

with open('api/db.js', 'w') as f:
    f.write(js)


# ------------------------------
# Update api/admin.js
# ------------------------------
with open('api/admin.js', 'r') as f:
    admin_js = f.read()

# Instead of expiresAt = now + duration, set it to 9999999999 and store duration_mins
admin_create_old = """        const { durationMinutes, maxUses, customCode } = req.body;
        const code = customCode || generateCode();
        const now = Math.floor(Date.now() / 1000);
        const expiresAt = now + (parseInt(durationMinutes) * 60);
        const limit = parseInt(maxUses) || 1;

        try {
          await client.execute({
            sql: "INSERT INTO access_codes (code, expires_at, max_uses, used_count, created_at) VALUES (?, ?, ?, 0, ?)",
            args: [code, expiresAt, limit, now]
          });"""

admin_create_new = """        const { durationMinutes, maxUses, customCode } = req.body;
        const code = customCode || generateCode();
        const now = Math.floor(Date.now() / 1000);
        const duration = parseInt(durationMinutes) || 1;
        const expiresAt = 9999999999; // Will be set on first use
        const limit = parseInt(maxUses) || 1;

        try {
          await client.execute({
            sql: "INSERT INTO access_codes (code, expires_at, max_uses, used_count, created_at, duration_mins) VALUES (?, ?, ?, 0, ?, ?)",
            args: [code, expiresAt, limit, now, duration]
          });"""
admin_js = admin_js.replace(admin_create_old, admin_create_new)

with open('api/admin.js', 'w') as f:
    f.write(admin_js)


# ------------------------------
# Update api/auth.js
# ------------------------------
with open('api/auth.js', 'r') as f:
    auth_js = f.read()

auth_logic_old = """    if (record.used_count >= record.max_uses) {
      return res.status(401).json({ error: 'ACCESS DENIED: Code usage limit exceeded.', valid: false });
    }

    // Increment usage
    await db.execute({
      sql: "UPDATE access_codes SET used_count = used_count + 1 WHERE code = ?",
      args: [code]
    });

    return res.status(200).json({ success: true, valid: true });"""

auth_logic_new = """    if (record.used_count >= record.max_uses) {
      return res.status(401).json({ error: 'ACCESS DENIED: Code usage limit exceeded.', valid: false });
    }

    if (record.used_count === 0 && req.body.action !== 'check') {
      // FIRST USE! Start the timer now.
      const newExpiresAt = now + (record.duration_mins * 60);
      await db.execute({
        sql: "UPDATE access_codes SET used_count = 1, expires_at = ? WHERE code = ?",
        args: [newExpiresAt, code]
      });
    } else if (req.body.action !== 'check') {
      // Just increment usage
      await db.execute({
        sql: "UPDATE access_codes SET used_count = used_count + 1 WHERE code = ?",
        args: [code]
      });
    }

    return res.status(200).json({ success: true, valid: true });"""

auth_js = auth_js.replace(auth_logic_old, auth_logic_new)

with open('api/auth.js', 'w') as f:
    f.write(auth_js)


# ------------------------------
# Update admin18.html to show "Pending First Use"
# ------------------------------
with open('admin18.html', 'r') as f:
    html = f.read()

html_old = """      const expDate = new Date(c.expires_at * 1000).toLocaleString();
      const status = isExpired ? 'Expired' : (isUsedUp ? 'Used Up' : 'Active');"""

html_new = """      const isPending = c.used_count === 0 && c.expires_at > 2000000000;
      const expDate = isPending ? `Starts on 1st use (${c.duration_mins}m)` : new Date(c.expires_at * 1000).toLocaleString();
      const status = isExpired ? 'Expired' : (isUsedUp ? 'Used Up' : (isPending ? 'Pending' : 'Active'));"""

html = html.replace(html_old, html_new)

with open('admin18.html', 'w') as f:
    f.write(html)

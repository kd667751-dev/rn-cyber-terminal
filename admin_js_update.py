import re

with open('api/admin.js', 'r') as f:
    js = f.read()

# 1. Update GET method to return system mode
old_get = """    // 4. Handle GET (List)
    if (req.method === 'GET') {
      try {
        const rs = await client.execute("SELECT * FROM access_codes ORDER BY created_at DESC");
        return res.status(200).json({ codes: rs.rows });"""

new_get = """    // 4. Handle GET (List)
    if (req.method === 'GET') {
      try {
        const stateRs = await client.execute("SELECT mode FROM system_state WHERE id = '1'");
        const sysMode = stateRs.rows.length > 0 ? stateRs.rows[0].mode : 'normal';
        const rs = await client.execute("SELECT * FROM access_codes ORDER BY created_at DESC");
        return res.status(200).json({ codes: rs.rows, systemMode: sysMode });"""

js = js.replace(old_get, new_get)

# 2. Update POST create to handle gameOnExpiry
old_create = """      if (action === 'create') {
        const { durationMinutes, maxUses, customCode } = req.body;
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

new_create = """      if (action === 'create') {
        const { durationMinutes, maxUses, customCode, gameOnExpiry } = req.body;
        const code = customCode || generateCode();
        const now = Math.floor(Date.now() / 1000);
        const duration = parseInt(durationMinutes) || 1;
        const expiresAt = 9999999999; // Will be set on first use
        const limit = parseInt(maxUses) || 1;
        const gameFlag = gameOnExpiry ? 1 : 0;

        try {
          await client.execute({
            sql: "INSERT INTO access_codes (code, expires_at, max_uses, used_count, created_at, duration_mins, game_on_expiry) VALUES (?, ?, ?, 0, ?, ?, ?)",
            args: [code, expiresAt, limit, now, duration, gameFlag]
          });"""

js = js.replace(old_create, new_create)

# 3. Add reset_mode action
reset_logic = """      if (action === 'clean') {"""

new_reset = """      if (action === 'reset_mode') {
        await client.execute("UPDATE system_state SET mode = 'normal' WHERE id = '1'");
        return res.status(200).json({ success: true });
      }
      if (action === 'clean') {"""

js = js.replace(reset_logic, new_reset)


with open('api/admin.js', 'w') as f:
    f.write(js)

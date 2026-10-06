import re

with open('api/admin.js', 'r') as f:
    js = f.read()

# Add activity_log support in GET 
old_get = """    if (req.method === 'GET') {
      try {
        const stateRs = await client.execute("SELECT mode FROM system_state WHERE id = '1'");
        const sysMode = stateRs.rows.length > 0 ? stateRs.rows[0].mode : 'normal';
        const rs = await client.execute("SELECT * FROM access_codes ORDER BY created_at DESC");
        return res.status(200).json({ codes: rs.rows, systemMode: sysMode });
      } catch(e) {
        return res.status(500).json({ error: 'DB READ ERROR: ' + e.message });
      }
    }"""

new_get = """    if (req.method === 'GET') {
      try {
        const stateRs = await client.execute("SELECT mode FROM system_state WHERE id = '1'");
        const sysMode = stateRs.rows.length > 0 ? stateRs.rows[0].mode : 'normal';
        const rs = await client.execute("SELECT * FROM access_codes ORDER BY created_at DESC");
        const logRs = await client.execute("SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT 50");
        return res.status(200).json({ codes: rs.rows, systemMode: sysMode, activityLog: logRs.rows });
      } catch(e) {
        return res.status(500).json({ error: 'DB READ ERROR: ' + e.message });
      }
    }"""

js = js.replace(old_get, new_get)

# Add clear_log action
old_clean = """      if (action === 'clean') {
        const now = Math.floor(Date.now() / 1000);
        await client.execute({
          sql: "DELETE FROM access_codes WHERE used_count >= max_uses",
          args: []
        });
        return res.status(200).json({ success: true });
      }"""

new_clean = """      if (action === 'clean') {
        const now = Math.floor(Date.now() / 1000);
        await client.execute({
          sql: "DELETE FROM access_codes WHERE used_count >= max_uses",
          args: []
        });
        return res.status(200).json({ success: true });
      }

      if (action === 'clear_log') {
        await client.execute("DELETE FROM activity_log");
        return res.status(200).json({ success: true });
      }"""

js = js.replace(old_clean, new_clean)

with open('api/admin.js', 'w') as f:
    f.write(js)

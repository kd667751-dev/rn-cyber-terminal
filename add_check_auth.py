import re

with open('api/auth.js', 'r') as f:
    js = f.read()

# Add check logic
old_logic = """    if (record.used_count >= record.max_uses) {
      return res.status(401).json({ error: 'ACCESS DENIED: Code usage limit exceeded.', valid: false });
    }

    // Increment usage
    await db.execute({
      sql: "UPDATE access_codes SET used_count = used_count + 1 WHERE code = ?",
      args: [code]
    });

    return res.status(200).json({ success: true, valid: true });"""

new_logic = """    if (req.body.action === 'check') {
      // Just verifying if it's still valid time-wise (we ignore usage limit for checking an already active session, OR we can check it too)
      // Actually, if it's expired time-wise, block it.
      return res.status(200).json({ success: true, valid: true });
    }

    if (record.used_count >= record.max_uses) {
      return res.status(401).json({ error: 'ACCESS DENIED: Code usage limit exceeded.', valid: false });
    }

    // Increment usage
    await db.execute({
      sql: "UPDATE access_codes SET used_count = used_count + 1 WHERE code = ?",
      args: [code]
    });

    return res.status(200).json({ success: true, valid: true });"""

js = js.replace(old_logic, new_logic)

with open('api/auth.js', 'w') as f:
    f.write(js)

import re

with open('api/auth.js', 'r') as f:
    js = f.read()

old_logic = """    if (record.used_count === 0 && req.body.action !== 'check') {
      // FIRST USE! Start the timer now.
      const newExpiresAt = now + ((record.duration_mins || 60) * 60);
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

new_logic = """    let finalExpiresAt = record.expires_at;

    if (record.used_count === 0 && req.body.action !== 'check') {
      // FIRST USE! Start the timer now.
      finalExpiresAt = now + ((record.duration_mins || 60) * 60);
      await db.execute({
        sql: "UPDATE access_codes SET used_count = 1, expires_at = ? WHERE code = ?",
        args: [finalExpiresAt, code]
      });
    } else if (req.body.action !== 'check') {
      // Just increment usage
      await db.execute({
        sql: "UPDATE access_codes SET used_count = used_count + 1 WHERE code = ?",
        args: [code]
      });
    }

    return res.status(200).json({ success: true, valid: true, expires_at: finalExpiresAt });"""

# Also need to update the check block earlier in the file to send expires_at
old_check = """    if (req.body.action === 'check') {
      // Just verifying if it's still valid time-wise (we ignore usage limit for checking an already active session, OR we can check it too)
      // Actually, if it's expired time-wise, block it.
      return res.status(200).json({ success: true, valid: true });
    }"""

new_check = """    if (req.body.action === 'check') {
      // Just verifying if it's still valid time-wise
      return res.status(200).json({ success: true, valid: true, expires_at: record.expires_at });
    }"""

js = js.replace(old_logic, new_logic)
js = js.replace(old_check, new_check)

with open('api/auth.js', 'w') as f:
    f.write(js)

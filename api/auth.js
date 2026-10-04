const { getDb, initDb } = require('./db');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    await initDb();
    const db = getDb();
    const { code } = req.body;

    if (!code) {
      return res.status(400).json({ error: 'Code is required', valid: false });
    }

    const rs = await db.execute({
      sql: "SELECT * FROM access_codes WHERE code = ?",
      args: [code]
    });

    if (rs.rows.length === 0) {
      return res.status(401).json({ error: 'ACCESS DENIED: Invalid code.', valid: false });
    }

    const record = rs.rows[0];
    const now = Math.floor(Date.now() / 1000);

    if (record.expires_at < now) {
      return res.status(401).json({ error: 'ACCESS DENIED: Code has expired.', valid: false });
    }

    if (req.body.action === 'check') {
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

    return res.status(200).json({ success: true, valid: true });
  } catch (error) {
    console.error("Auth error:", error);
    // If DB is not configured, we might want to let them in or block them.
    // Let's block them if DB is not configured, asking admin to set it up.
    return res.status(500).json({ error: 'SYSTEM ERROR: Database not configured.', valid: false });
  }
};

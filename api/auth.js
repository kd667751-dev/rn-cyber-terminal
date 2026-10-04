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

    // Secret Admin Backdoor
    const adminPass = process.env.ADMIN_PASSWORD;
    if (adminPass && code === adminPass) {
      return res.status(200).json({ adminRedirect: true, valid: false });
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

    // 1. If checking active session (startup/refresh)
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

    return res.status(200).json({ success: true, valid: true, expires_at: finalExpiresAt });
  } catch (error) {
    console.error("Auth error:", error);
    // If DB is not configured, we might want to let them in or block them.
    // Let's block them if DB is not configured, asking admin to set it up.
    return res.status(500).json({ error: 'SYSTEM ERROR: Database not configured.', valid: false });
  }
};

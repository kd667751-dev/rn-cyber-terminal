const { getDb, initDb } = require('./db');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    await initDb();
    const db = getDb();
    const { code, action } = req.body;

    if (!code || !action) {
      return res.status(400).json({ error: 'Missing code or action' });
    }

    // Verify the code is valid before logging
    const adminPass = process.env.ADMIN_PASSWORD;
    let isValid = false;

    if (adminPass && code === adminPass) {
      isValid = true;
    } else {
      const rs = await db.execute({
        sql: "SELECT * FROM access_codes WHERE code = ?",
        args: [code]
      });
      if (rs.rows.length > 0) {
        const record = rs.rows[0];
        const now = Math.floor(Date.now() / 1000);
        if (record.expires_at > now) isValid = true;
      }
    }

    if (!isValid) {
      return res.status(401).json({ error: 'ACCESS DENIED' });
    }

    const now = Math.floor(Date.now() / 1000);
    await db.execute({
      sql: "INSERT INTO activity_log (code, action, timestamp) VALUES (?, ?, ?)",
      args: [code, action.substring(0, 120), now]
    });

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error("Activity log error:", error);
    return res.status(500).json({ error: 'LOG ERROR' });
  }
};

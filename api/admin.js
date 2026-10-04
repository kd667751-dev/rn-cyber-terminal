const { getDb, initDb } = require('./db');
const { v4: uuidv4 } = require('uuid');

function checkAdminAuth(req) {
  const authHeader = req.headers.authorization;
  const adminPass = process.env.ADMIN_PASSWORD;
  
  if (!adminPass) {
    throw new Error('ADMIN_PASSWORD environment variable not set.');
  }
  
  if (!authHeader || authHeader !== `Bearer ${adminPass}`) {
    return false;
  }
  return true;
}

module.exports = async (req, res) => {
  try {
    if (req.method === 'POST' && req.body && req.body.action === 'login') {
      const { password } = req.body;
      const adminPass = process.env.ADMIN_PASSWORD;
      if (!adminPass) return res.status(500).json({ error: 'Admin password not configured on server' });
      
      if (password === adminPass) {
        return res.status(200).json({ success: true, token: adminPass });
      }
      return res.status(401).json({ error: 'Invalid admin password' });
    }

    if (!checkAdminAuth(req)) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    await initDb();
    const db = getDb();

    if (req.method === 'GET') {
      // List codes
      const rs = await db.execute("SELECT * FROM access_codes ORDER BY created_at DESC");
      return res.status(200).json({ codes: rs.rows });
    } 
    
    if (req.method === 'POST') {
      const { action } = req.body;
      
      if (action === 'create') {
        const { durationHours, maxUses, customCode } = req.body;
        const code = customCode || uuidv4().substring(0, 8).toUpperCase();
        const now = Math.floor(Date.now() / 1000);
        const expiresAt = now + (parseInt(durationHours) * 3600);
        const limit = parseInt(maxUses) || 1;

        await db.execute({
          sql: "INSERT INTO access_codes (code, expires_at, max_uses, used_count, created_at) VALUES (?, ?, ?, 0, ?)",
          args: [code, expiresAt, limit, now]
        });

        return res.status(200).json({ success: true, code, expiresAt, maxUses: limit });
      }
      
      if (action === 'delete') {
        const { code } = req.body;
        await db.execute({
          sql: "DELETE FROM access_codes WHERE code = ?",
          args: [code]
        });
        return res.status(200).json({ success: true });
      }
      
      if (action === 'clean') {
        const now = Math.floor(Date.now() / 1000);
        await db.execute({
          sql: "DELETE FROM access_codes WHERE expires_at < ? OR used_count >= max_uses",
          args: [now]
        });
        return res.status(200).json({ success: true });
      }

      return res.status(400).json({ error: 'Invalid action' });
    }

    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {
    console.error("Admin error:", error);
    return res.status(500).json({ error: error.message });
  }
};

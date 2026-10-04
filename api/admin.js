const db = require('./db');

function generateCode() {
  return Math.random().toString(36).substring(2, 10).toUpperCase();
}

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
    // 1. Check Login
    if (req.method === 'POST' && req.body && req.body.action === 'login') {
      const { password } = req.body;
      const adminPass = process.env.ADMIN_PASSWORD;
      if (!adminPass) {
        return res.status(500).json({ error: 'ADMIN_PASSWORD environment variable not configured on Vercel.' });
      }
      if (password === adminPass) {
        return res.status(200).json({ success: true, token: adminPass });
      }
      return res.status(401).json({ error: 'Invalid master password' });
    }

    // 2. Require Auth for all other routes
    let isAuth = false;
    try {
      isAuth = checkAdminAuth(req);
    } catch(e) {
      return res.status(500).json({ error: 'SERVER CONFIG ERROR: ' + e.message });
    }
    
    if (!isAuth) {
      return res.status(401).json({ error: 'Unauthorized access.' });
    }

    // 3. Connect to DB
    try {
      await db.initDb();
    } catch(e) {
      return res.status(500).json({ error: 'DATABASE ERROR: ' + e.message });
    }
    
    const client = db.getDb();

    // 4. Handle GET (List)
    if (req.method === 'GET') {
      try {
        const rs = await client.execute("SELECT * FROM access_codes ORDER BY created_at DESC");
        return res.status(200).json({ codes: rs.rows });
      } catch(e) {
        return res.status(500).json({ error: 'DB READ ERROR: ' + e.message });
      }
    } 
    
    // 5. Handle POST (Create, Delete, Clean)
    if (req.method === 'POST') {
      const { action } = req.body;
      
      if (action === 'create') {
        const { durationMinutes, maxUses, customCode } = req.body;
        const code = customCode || generateCode();
        const now = Math.floor(Date.now() / 1000);
        const expiresAt = now + (parseInt(durationMinutes) * 60);
        const limit = parseInt(maxUses) || 1;

        try {
          await client.execute({
            sql: "INSERT INTO access_codes (code, expires_at, max_uses, used_count, created_at) VALUES (?, ?, ?, 0, ?)",
            args: [code, expiresAt, limit, now]
          });
          return res.status(200).json({ success: true, code, expiresAt, maxUses: limit });
        } catch(e) {
          return res.status(500).json({ error: 'DB INSERT ERROR: ' + e.message });
        }
      }
      
      if (action === 'delete') {
        const { code } = req.body;
        await client.execute({
          sql: "DELETE FROM access_codes WHERE code = ?",
          args: [code]
        });
        return res.status(200).json({ success: true });
      }
      
      if (action === 'clean') {
        const now = Math.floor(Date.now() / 1000);
        await client.execute({
          sql: "DELETE FROM access_codes WHERE expires_at < ? OR used_count >= max_uses",
          args: [now]
        });
        return res.status(200).json({ success: true });
      }

      return res.status(400).json({ error: 'Invalid action parameter' });
    }

    return res.status(405).json({ error: 'Method not allowed' });
  } catch (globalError) {
    console.error("FATAL ADMIN ERROR:", globalError);
    return res.status(500).json({ error: 'FATAL INTERNAL ERROR: ' + globalError.message, stack: globalError.stack });
  }
};

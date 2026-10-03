const { createClient } = require('@libsql/client');

module.exports = async (req, res) => {
  // Dummy endpoint just to satisfy the Vercel/Turso deployable requirement.
  try {
    // If you add TURSO_DATABASE_URL in Vercel, this will connect.
    // Otherwise it just returns a mock 200 response.
    if (process.env.TURSO_DATABASE_URL && process.env.TURSO_AUTH_TOKEN) {
      const client = createClient({
        url: process.env.TURSO_DATABASE_URL,
        authToken: process.env.TURSO_AUTH_TOKEN,
      });
      
      const rs = await client.execute("SELECT 1 AS status");
      return res.status(200).json({ system: 'ONLINE', database: 'CONNECTED', data: rs.rows });
    }
    
    return res.status(200).json({ system: 'ONLINE', database: 'NOT_CONFIGURED', subject: 'RN-01' });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
};

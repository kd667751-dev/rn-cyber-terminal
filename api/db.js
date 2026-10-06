const { createClient } = require('@libsql/client');

let client = null;

function getDb() {
  if (!client) {
    if (!process.env.TURSO_DATABASE_URL || !process.env.TURSO_AUTH_TOKEN) {
      throw new Error("Missing TURSO_DATABASE_URL or TURSO_AUTH_TOKEN environment variables.");
    }
    client = createClient({
      url: process.env.TURSO_DATABASE_URL,
      authToken: process.env.TURSO_AUTH_TOKEN,
    });
  }
  return client;
}

async function initDb() {
  const db = getDb();
  await db.execute(`
    CREATE TABLE IF NOT EXISTS access_codes (
      code TEXT PRIMARY KEY,
      expires_at INTEGER NOT NULL,
      max_uses INTEGER NOT NULL,
      used_count INTEGER DEFAULT 0,
      created_at INTEGER NOT NULL
    )
  `);
  
  await db.execute(`
    CREATE TABLE IF NOT EXISTS system_state (
      id TEXT PRIMARY KEY,
      mode TEXT NOT NULL
    )
  `);
  
  // Ensure default state exists
  try {
    await db.execute("INSERT OR IGNORE INTO system_state (id, mode) VALUES ('1', 'normal')");
  } catch(e) {}
  
  try {
    await db.execute("ALTER TABLE access_codes ADD COLUMN duration_mins INTEGER DEFAULT 0");
  } catch(e) {}
  
  try {
    await db.execute("ALTER TABLE access_codes ADD COLUMN game_on_expiry INTEGER DEFAULT 0");
  } catch(e) {}

  // Activity log table
  await db.execute(`
    CREATE TABLE IF NOT EXISTS activity_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      code TEXT,
      action TEXT NOT NULL,
      timestamp INTEGER NOT NULL
    )
  `);
}


module.exports = { getDb, initDb };

import re

with open('api/db.js', 'r') as f:
    js = f.read()

new_init = """async function initDb() {
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
}"""

# regex replace the entire initDb function
js = re.sub(r'async function initDb\(\) \{.*\} // Ignore if column already exists\n\}', new_init + '\n', js, flags=re.DOTALL)

with open('api/db.js', 'w') as f:
    f.write(js)

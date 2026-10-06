import re

with open('api/db.js', 'r') as f:
    js = f.read()

old_end = """  try {\r
    await db.execute("ALTER TABLE access_codes ADD COLUMN game_on_expiry INTEGER DEFAULT 0");\r
  } catch(e) {}\r
}\r
\r
\r
module.exports = { getDb, initDb };\r
""" if False else """  try {
    await db.execute("ALTER TABLE access_codes ADD COLUMN game_on_expiry INTEGER DEFAULT 0");
  } catch(e) {}
}


module.exports = { getDb, initDb };
"""

new_end = """  try {
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
"""

js = js.replace(old_end, new_end)

with open('api/db.js', 'w') as f:
    f.write(js)

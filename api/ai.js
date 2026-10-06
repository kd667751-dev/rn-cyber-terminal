const { getDb, initDb } = require('./db');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    await initDb();
    const db = getDb();
    const { code, message } = req.body;

    if (!code || !message) {
      return res.status(400).json({ error: 'Missing code or message' });
    }

    // 1. Authenticate the code
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
        // Ensure session is active and not expired
        if (record.expires_at > now) {
          isValid = true;
        }
      }
    }

    if (!isValid) {
      return res.status(401).json({ error: 'ACCESS DENIED. AI MODULE LOCKED.' });
    }

    // 2. Check for GROQ API KEY
    const groqKey = process.env.GROQ_API_KEY;
    if (!groqKey) {
      return res.status(503).json({ reply: '[SYSTEM] AI Module is currently OFFLINE. (API Key not configured in Vercel)' });
    }

    // 3. Call Groq API
    const systemPrompt = "You are a highly classified, advanced Artificial Intelligence embedded within a restricted cyber-terminal. You are speaking to an authorized user named Raj Nandani. Your tone is cold, professional, mysterious, and hacker-like. Keep your responses relatively concise (under 3 sentences unless complex explanation is needed). DO NOT use emojis. DO NOT act like a typical cheerful AI.";
    
    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${groqKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'llama3-8b-8192',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: message }
        ],
        temperature: 0.7,
        max_tokens: 150
      })
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("Groq API Error:", errText);
      return res.status(500).json({ reply: '[SYSTEM] AI Module encountered a critical error during cognitive processing.' });
    }

    const data = await response.json();
    const reply = data.choices[0].message.content;

    return res.status(200).json({ reply });

  } catch (error) {
    console.error("AI API Error:", error);
    return res.status(500).json({ reply: '[SYSTEM] FATAL ERROR CONNECTING TO AI CORE.' });
  }
};

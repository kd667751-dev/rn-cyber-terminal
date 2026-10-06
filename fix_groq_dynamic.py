import re

with open('api/ai.js', 'r') as f:
    js = f.read()

old_fetch = """    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${groqKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'mixtral-8x7b-32768',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: message }
        ],
        temperature: 0.7,
        max_tokens: 150
      })
    });"""

new_fetch = """    // Auto-detect available Groq model
    let modelId = 'llama3-8b-8192';
    try {
      const mRes = await fetch('https://api.groq.com/openai/v1/models', { headers: { 'Authorization': `Bearer ${groqKey}` } });
      if (mRes.ok) {
        const mData = await mRes.json();
        if (mData.data && mData.data.length > 0) {
          const pref = mData.data.find(m => m.id.includes('llama-3.3') || m.id.includes('llama-3.1') || m.id.includes('llama3'));
          modelId = pref ? pref.id : mData.data[0].id;
        }
      }
    } catch(e) {}

    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${groqKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: modelId,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: message }
        ],
        temperature: 0.7,
        max_tokens: 150
      })
    });"""

js = js.replace(old_fetch, new_fetch)

with open('api/ai.js', 'w') as f:
    f.write(js)

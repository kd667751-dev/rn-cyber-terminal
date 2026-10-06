import re

with open('api/ai.js', 'r') as f:
    js = f.read()

old_logic = """    // Auto-detect available Groq model
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
    } catch(e) {}"""

new_logic = """    // Auto-detect available Groq model prioritizing Qwen (doesn't require Meta's terms acceptance)
    let modelId = 'qwen-2.5-32b';
    try {
      const mRes = await fetch('https://api.groq.com/openai/v1/models', { headers: { 'Authorization': `Bearer ${groqKey}` } });
      if (mRes.ok) {
        const mData = await mRes.json();
        if (mData.data && mData.data.length > 0) {
          const pref = mData.data.find(m => m.id.toLowerCase().includes('qwen'));
          modelId = pref ? pref.id : mData.data[0].id;
        }
      }
    } catch(e) {}"""

js = js.replace(old_logic, new_logic)

with open('api/ai.js', 'w') as f:
    f.write(js)

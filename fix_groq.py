import re

with open('api/ai.js', 'r') as f:
    js = f.read()

# Update the model name and the error response
js = js.replace("model: 'llama3-8b-8192'", "model: 'llama-3.1-8b-instant'")

old_err = """    if (!response.ok) {
      const errText = await response.text();
      console.error("Groq API Error:", errText);
      return res.status(500).json({ reply: '[SYSTEM] AI Module encountered a critical error during cognitive processing.' });
    }"""
new_err = """    if (!response.ok) {
      const errText = await response.text();
      console.error("Groq API Error:", errText);
      // Expose part of the error so the user can see if it's an Auth issue or Model issue
      return res.status(500).json({ reply: '[SYSTEM] AI API ERROR:\\n' + errText.substring(0, 150) });
    }"""
js = js.replace(old_err, new_err)

with open('api/ai.js', 'w') as f:
    f.write(js)

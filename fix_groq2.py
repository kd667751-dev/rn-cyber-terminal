import re

with open('api/ai.js', 'r') as f:
    js = f.read()

# Try mixtral which is very reliable on Groq
js = js.replace("model: 'llama-3.1-8b-instant'", "model: 'mixtral-8x7b-32768'")

with open('api/ai.js', 'w') as f:
    f.write(js)

import re

with open('api/auth.js', 'r') as f:
    js = f.read()

# Fallback duration for old rows
js = js.replace('const newExpiresAt = now + (record.duration_mins * 60);',
                'const newExpiresAt = now + ((record.duration_mins || 60) * 60);')

with open('api/auth.js', 'w') as f:
    f.write(js)

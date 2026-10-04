import re

with open('api/auth.js', 'r') as f:
    js = f.read()

# Replace specific error messages with generic "Invalid code"
js = js.replace("'ACCESS DENIED: Code has expired.'", "'ACCESS DENIED: Invalid code.'")
js = js.replace("'ACCESS DENIED: Code usage limit exceeded.'", "'ACCESS DENIED: Invalid code.'")

with open('api/auth.js', 'w') as f:
    f.write(js)

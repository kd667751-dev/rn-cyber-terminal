import re

with open('api/auth.js', 'r') as f:
    js = f.read()

admin_backdoor = """    if (!code) {
      return res.status(400).json({ error: 'Code is required', valid: false });
    }

    // Secret Admin Backdoor
    const adminPass = process.env.ADMIN_PASSWORD;
    if (adminPass && code === adminPass) {
      return res.status(200).json({ adminRedirect: true, valid: false });
    }"""

js = js.replace("""    if (!code) {
      return res.status(400).json({ error: 'Code is required', valid: false });
    }""", admin_backdoor)

with open('api/auth.js', 'w') as f:
    f.write(js)

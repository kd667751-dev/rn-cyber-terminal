import re

with open('api/admin.js', 'r') as f:
    js = f.read()

# Replace durationHours with durationMinutes and adjust multiplier
js = js.replace('const { durationHours, maxUses, customCode } = req.body;',
                'const { durationMinutes, maxUses, customCode } = req.body;')
js = js.replace('const expiresAt = now + (parseInt(durationHours) * 3600);',
                'const expiresAt = now + (parseInt(durationMinutes) * 60);')

with open('api/admin.js', 'w') as f:
    f.write(js)

import re

with open('admin18.html', 'r') as f:
    html = f.read()

# Change label
html = html.replace('<label>Validity Duration (Hours):</label>', '<label>Validity Duration (Minutes):</label>')

# Change POST body param
html = html.replace('const data = await req(\'POST\', { action: \'create\', customCode, durationHours, maxUses });',
                    'const data = await req(\'POST\', { action: \'create\', customCode, durationMinutes: durationHours, maxUses });')

with open('admin18.html', 'w') as f:
    f.write(html)

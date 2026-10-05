import re

with open('admin18.html', 'r') as f:
    html = f.read()

html = html.replace('<th>Status</th>\n            <th>Action</th>', '<th>Status</th>\n            <th>Game?</th>\n            <th>Action</th>')

with open('admin18.html', 'w') as f:
    f.write(html)

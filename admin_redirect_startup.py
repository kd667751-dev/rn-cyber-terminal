import re

with open('index.html', 'r') as f:
    html = f.read()

redirect_logic = """  }).then(r => r.json()).then(data => {
    if (data.adminRedirect) {
      window.location.href = '/admin18';
      return;
    }
    if (data.valid) {"""

html = html.replace("""  }).then(r => r.json()).then(data => {
    if (data.valid) {""", redirect_logic)

with open('index.html', 'w') as f:
    f.write(html)

import re

with open('admin18.html', 'r') as f:
    html = f.read()

css_fix = """
    * { -webkit-tap-highlight-color: transparent; user-select: none; -webkit-user-select: none; -webkit-touch-callout: none; }
    input, textarea { -webkit-user-select: auto; user-select: auto; }
    ::selection { background: transparent; }
    ::-moz-selection { background: transparent; }
"""

# Insert right after <style>
html = html.replace('<style>', '<style>\n' + css_fix)

with open('admin18.html', 'w') as f:
    f.write(html)

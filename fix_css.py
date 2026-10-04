import re

with open('index.html', 'r') as f:
    html = f.read()

# Add user-select none to global styles to prevent text selection and long-press blue highlight
css_fix = """
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;user-select:none;-webkit-user-select:none;-webkit-touch-callout:none;}
input,textarea{-webkit-user-select:auto;user-select:auto;}
::selection{background:transparent;}
::-moz-selection{background:transparent;}
"""

# The original has: *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
html = html.replace('*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}', css_fix)

with open('index.html', 'w') as f:
    f.write(html)

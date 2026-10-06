import re

with open('index.html', 'r') as f:
    html = f.read()

old_overlay = """<div id="security-overlay">
  [ SECURITY PROTOCOL ENGAGED ]<br><br>UNAUTHORIZED CAPTURE ATTEMPT DETECTED
</div>"""

new_overlay = """<div id="security-overlay">
  <span style="color:var(--red2);">[ SECURITY PROTOCOL ENGAGED ]</span><br><br>
  UNAUTHORIZED CAPTURE ATTEMPT DETECTED<br><br>
  <span style="font-size: 0.7em; color: var(--dim);">PLEASE REFRESH THE PAGE</span>
</div>"""

html = html.replace(old_overlay, new_overlay)

with open('index.html', 'w') as f:
    f.write(html)

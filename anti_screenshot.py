import re

with open('index.html', 'r') as f:
    html = f.read()

anti_screenshot_css = """
/* Anti-screenshot & Print prevention */
@media print {
  html, body { display: none !important; }
}
#security-overlay {
  position: fixed; inset: 0; z-index: 99999; background: #000;
  display: flex; align-items: center; justify-content: center;
  color: var(--red2); font-family: var(--mono); font-size: 1.5rem;
  letter-spacing: 0.2em; text-align: center; padding: 20px;
  opacity: 0; pointer-events: none; transition: 0.2s;
  text-shadow: 0 0 15px var(--glow);
}
#security-overlay.active {
  opacity: 1; pointer-events: auto;
}
"""
html = html.replace('</style>', anti_screenshot_css + '</style>')

anti_screenshot_html = """
<div id="security-overlay">
  [ SECURITY PROTOCOL ENGAGED ]<br><br>UNAUTHORIZED CAPTURE ATTEMPT DETECTED
</div>
"""
html = html.replace('<body>', '<body>\n' + anti_screenshot_html)

anti_screenshot_js = """
// Anti-screenshot & Security Measures
document.addEventListener('contextmenu', e => e.preventDefault());
document.addEventListener('keydown', e => {
  if (e.key === 'PrintScreen' || (e.ctrlKey && ['p','s','c','u','i'].includes(e.key.toLowerCase()))) {
    e.preventDefault();
    triggerSecurity();
  }
});
document.addEventListener('keyup', e => {
  if (e.key === 'PrintScreen') triggerSecurity();
});

const secOverlay = document.getElementById('security-overlay');
function triggerSecurity() {
  secOverlay.classList.add('active');
  if (typeof Snd !== 'undefined' && Snd.glitch) Snd.glitch(2);
  setTimeout(() => secOverlay.classList.remove('active'), 3000);
}

// When window loses focus (Snipping tool, backgrounding app), hide content
window.addEventListener('blur', () => {
  secOverlay.classList.add('active');
});
window.addEventListener('focus', () => {
  secOverlay.classList.remove('active');
});
"""

# Insert before the end of the script
html = html.replace('})();\n</script>', anti_screenshot_js + '\n})();\n</script>')

with open('index.html', 'w') as f:
    f.write(html)

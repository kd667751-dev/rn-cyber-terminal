import re

with open('index.html', 'r') as f:
    html = f.read()

# Add a global click listener to enable sound on first interaction
global_sound_script = """
document.addEventListener('pointerdown', () => {
  if (typeof Snd !== 'undefined' && !Snd.on && current !== 'boot') {
    const on = Snd.toggle();
    const sndBtn = $('#snd');
    if (sndBtn) {
      sndBtn.classList.toggle('on', on);
      sndBtn.setAttribute('aria-pressed', String(on));
      sndBtn.textContent = on ? 'SOUND · ON' : 'SOUND · OFF';
      sndBtn.style.opacity = '1';
      sndBtn.style.pointerEvents = 'auto';
    }
  }
}, {once: true});
"""

# Insert just before the end of the IIFE
html = html.replace('})();\n</script>', global_sound_script + '})();\n</script>')

with open('index.html', 'w') as f:
    f.write(html)

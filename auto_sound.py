import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace verifyCode with sound enabling logic
old_verify = """  async function verifyCode() {
    const code = inp.value.trim();
    if (!code) return;
    err.textContent = 'VERIFYING...';
    try {"""

new_verify = """  async function verifyCode() {
    // FORCE SOUND ON during user interaction!
    if (typeof Snd !== 'undefined' && !Snd.on) {
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

    const code = inp.value.trim();
    if (!code) return;
    err.textContent = 'VERIFYING...';
    try {"""

html = html.replace(old_verify, new_verify)

# Make the Snd.drone and overall Snd.master volume LOUDER!
# It was 0.85, let's make it 1.2
html = html.replace('this.master.gain.value=0.85', 'this.master.gain.value=1.5')

# Make the drone louder
html = html.replace('this.drone.gain.value=.08', 'this.drone.gain.value=.15')
html = html.replace('this.drone.gain.value=.15', 'this.drone.gain.value=.25') # Just in case it was already .15

# Make the typing louder
html = html.replace('g.gain.setValueAtTime(.05,t);', 'g.gain.setValueAtTime(.2,t);')
html = html.replace('g.gain.linearRampToValueAtTime(0,t+.02);', 'g.gain.linearRampToValueAtTime(0,t+.04);')

with open('index.html', 'w') as f:
    f.write(html)

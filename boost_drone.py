import re

with open('index.html', 'r') as f:
    html = f.read()

# Make the drone louder
html = html.replace('g.gain.exponentialRampToValueAtTime(.05,c.currentTime+3);',
                    'g.gain.exponentialRampToValueAtTime(.25,c.currentTime+3);')

# Make the tick/typing sound louder
html = html.replace('this.burst(.015,4200,6,.08)', 'this.burst(.015,4200,6,.3)')

# Make thump louder
html = html.replace('this.thump(t,70,.7)', 'this.thump(t,70,1.2)')

with open('index.html', 'w') as f:
    f.write(html)

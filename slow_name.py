import re

with open('index.html', 'r') as f:
    html = f.read()

old_end = """  const idb=$('#bootid'); idb.hidden=false;
  const s1=$('#bid1'); s1.textContent=''; s1.classList.add('typing');
  const ok=await typeInto(s1,'SUBJECT IDENTIFIED',15,tk); s1.classList.remove('typing'); if(!ok) return;
  await sleep(150); if(tk!==token) return;
  $('#bid2').classList.add('on'); Snd.glitch(.8); microGlitch();
  await sleep(600); if(tk!==token) return;
  idb.classList.add('out'); await sleep(200); if(tk!==token) return; idb.hidden=true;

  const nm=$('#bootname'); nm.hidden=false; void nm.offsetWidth; nm.classList.add('reveal'); Snd.glitch(.5);
  await sleep(600); if(tk!==token) return;
  nm.classList.add('distort'); Snd.glitch(1); microGlitch();
  await sleep(300); nm.classList.remove('distort');
  await sleep(500); if(tk!==token) return;
  go('hub');"""

new_end = """  const idb=$('#bootid'); idb.hidden=false;
  const s1=$('#bid1'); s1.textContent=''; s1.classList.add('typing');
  const ok=await typeInto(s1,'SUBJECT IDENTIFIED',45,tk); s1.classList.remove('typing'); if(!ok) return;
  await sleep(500); if(tk!==token) return;
  $('#bid2').classList.add('on'); Snd.glitch(.8); microGlitch();
  await sleep(1500); if(tk!==token) return;
  idb.classList.add('out'); await sleep(500); if(tk!==token) return; idb.hidden=true;

  const nm=$('#bootname'); nm.hidden=false; void nm.offsetWidth; nm.classList.add('reveal'); Snd.glitch(.5);
  await sleep(1800); if(tk!==token) return;
  nm.classList.add('distort'); Snd.glitch(1); microGlitch();
  await sleep(800); nm.classList.remove('distort');
  await sleep(1500); if(tk!==token) return;
  go('hub');"""

html = html.replace(old_end, new_end)

with open('index.html', 'w') as f:
    f.write(html)

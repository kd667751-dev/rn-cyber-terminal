import re

with open('index.html', 'r') as f:
    html = f.read()

old_boot = """enter.boot=async tk=>{
  const L=$('#bootlog'); L.innerHTML='';
  await sleep(900); if(tk!==token) return;
  let el=await line(L,'INITIALIZING SYSTEM...',{speed:55,tk}); if(!el) return;
  const steps=[
    ['Establishing secure connection...','bar',1200],
    ['Loading encrypted modules...','bar',1500],
    ['Scanning environment...','ok'],
    ['Searching database...','bar',1800],
    ['Identity detected.','hit']
  ];
  for(const [t,kind,ms] of steps){
    await sleep(420); if(tk!==token) return;
    el=await line(L,t,{speed:24,tk}); if(!el) return;
    if(kind==='bar'){
      if(t.startsWith('Searching')) setTimeout(microGlitch,ms*.6);
      if(!await bar(L,ms,tk)) return;
    }else if(kind==='ok'){
      const s=document.createElement('span'); s.className='ok'; s.textContent='  [ CLEAR ]'; el.appendChild(s);
    }else{
      el.classList.add('hit'); Snd.glitch(.6); microGlitch();
    }
  }
  await sleep(900); if(tk!==token) return;
  L.classList.add('out'); await sleep(700); if(tk!==token) return; L.hidden=true;

  const idb=$('#bootid'); idb.hidden=false;
  const s1=$('#bid1'); s1.textContent=''; s1.classList.add('typing');
  const ok=await typeInto(s1,'SUBJECT IDENTIFIED',45,tk); s1.classList.remove('typing'); if(!ok) return;
  await sleep(500); if(tk!==token) return;
  $('#bid2').classList.add('on'); Snd.glitch(.8); microGlitch();
  await sleep(2100); if(tk!==token) return;
  idb.classList.add('out'); await sleep(700); if(tk!==token) return; idb.hidden=true;

  const nm=$('#bootname'); nm.hidden=false; void nm.offsetWidth; nm.classList.add('reveal'); Snd.glitch(.5);
  await sleep(2000); if(tk!==token) return;
  nm.classList.add('distort'); Snd.glitch(1); microGlitch();
  await sleep(950); nm.classList.remove('distort');
  await sleep(1700); if(tk!==token) return;
  go('hub');
};"""

new_boot = """enter.boot=async tk=>{
  const L=$('#bootlog'); L.innerHTML='';
  await sleep(200); if(tk!==token) return;
  let el=await line(L,'INITIALIZING SYSTEM...',{speed:15,tk}); if(!el) return;
  const steps=[
    ['Establishing secure connection...','bar',300],
    ['Loading encrypted modules...','bar',400],
    ['Scanning environment...','ok'],
    ['Searching database...','bar',500],
    ['Identity detected.','hit']
  ];
  for(const [t,kind,ms] of steps){
    await sleep(100); if(tk!==token) return;
    el=await line(L,t,{speed:10,tk}); if(!el) return;
    if(kind==='bar'){
      if(t.startsWith('Searching')) setTimeout(microGlitch,ms*.6);
      if(!await bar(L,ms,tk)) return;
    }else if(kind==='ok'){
      const s=document.createElement('span'); s.className='ok'; s.textContent='  [ CLEAR ]'; el.appendChild(s);
    }else{
      el.classList.add('hit'); Snd.glitch(.6); microGlitch();
    }
  }
  await sleep(200); if(tk!==token) return;
  L.classList.add('out'); await sleep(200); if(tk!==token) return; L.hidden=true;

  const idb=$('#bootid'); idb.hidden=false;
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
  go('hub');
};"""

html = html.replace(old_boot, new_boot)

with open('index.html', 'w') as f:
    f.write(html)

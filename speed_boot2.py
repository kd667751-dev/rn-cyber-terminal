import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace the steps in enter.boot
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

  $('#skip').classList.add('show');
  const H=$('#rnhead'); H.hidden=false; H.classList.remove('out');"""

new_boot = """enter.boot=async tk=>{
  const L=$('#bootlog'); L.innerHTML='';
  await sleep(200); if(tk!==token) return;
  let el=await line(L,'INITIALIZING SYSTEM...',{speed:25,tk}); if(!el) return;
  const steps=[
    ['Establishing secure connection...','bar',400],
    ['Loading encrypted modules...','bar',500],
    ['Scanning environment...','ok'],
    ['Searching database...','bar',500],
    ['Identity detected.','hit']
  ];
  for(const [t,kind,ms] of steps){
    await sleep(150); if(tk!==token) return;
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
  await sleep(400); if(tk!==token) return;
  L.classList.add('out'); await sleep(300); if(tk!==token) return; L.hidden=true;

  const H=$('#rnhead'); H.hidden=false; H.classList.remove('out');"""

html = html.replace(old_boot, new_boot)

with open('index.html', 'w') as f:
    f.write(html)

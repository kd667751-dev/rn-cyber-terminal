import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the SKIP button from HTML
html = re.sub(r'<button id="skip"[^>]*>\[ SKIP SEQUENCE \]<\/button>', '', html)

# 2. Remove JS references to skip button
html = html.replace("$('#skip').classList.add('show');", "")
html = html.replace("$('#skip').classList.remove('show');", "")
html = re.sub(r"\$\('#skip'\)\.addEventListener\('click',[^;]+;\s*", "", html)

# 3. Speed up the boot animation
old_boot = """enter.boot=async tk=>{
  const box=$('#mbox');
  
  await logLine(box,'SYS.INIT','Establishing secure tunnel...',30,tk);
  await wait(800,tk);
  await logLine(box,'NET.CHK','Bypassing standard firewalls...',30,tk);
  await wait(800,tk);
  await logLine(box,'AUTH.KEY','Decrypting visitor profile...',30,tk);
  await wait(1200,tk);
  
  if(tk!==token) return;
  box.innerHTML='';
  await line(box,'WARNING: CLASSIFIED SYSTEM',{cls:'red',speed:25,tk});
  await line(box,'UNAUTHORIZED ACCESS IS STRICTLY PROHIBITED.',{cls:'red',speed:25,tk});
  await wait(1500,tk);
  
  if(tk!==token) return;
  box.innerHTML='';
  await line(box,'IDENTITY MATCH FOUND:',{speed:35,tk});
  await wait(600,tk);
  await line(box,'RAJ NANDANI',{cls:'rn glitch-btn',speed:60,tk});
  await wait(1500,tk);
  
  if(tk!==token) return;
  
  go('hub');
};"""

new_boot = """enter.boot=async tk=>{
  const box=$('#mbox');
  
  await logLine(box,'SYS.INIT','Establishing secure tunnel...',15,tk);
  await wait(300,tk);
  await logLine(box,'NET.CHK','Bypassing standard firewalls...',15,tk);
  await wait(300,tk);
  await logLine(box,'AUTH.KEY','Decrypting visitor profile...',15,tk);
  await wait(400,tk);
  
  if(tk!==token) return;
  box.innerHTML='';
  await line(box,'WARNING: CLASSIFIED SYSTEM',{cls:'red',speed:12,tk});
  await line(box,'UNAUTHORIZED ACCESS IS STRICTLY PROHIBITED.',{cls:'red',speed:12,tk});
  await wait(600,tk);
  
  if(tk!==token) return;
  box.innerHTML='';
  await line(box,'IDENTITY MATCH FOUND:',{speed:15,tk});
  await wait(200,tk);
  await line(box,'RAJ NANDANI',{cls:'rn glitch-btn',speed:40,tk});
  await wait(800,tk);
  
  if(tk!==token) return;
  
  go('hub');
};"""

html = html.replace(old_boot, new_boot)

with open('index.html', 'w') as f:
    f.write(html)

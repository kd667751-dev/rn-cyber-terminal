import re

with open('index.html', 'r') as f:
    html = f.read()

old_cmd = """    const out=CMDS[c];
    if(!out){ await line(box,c+': command not found',{cls:'dim',speed:10,tk}); return; }
    for(const l of out){ if(tk!==token) return; await line(box,l,{speed:12,tk}); }
  });
}"""

new_cmd = """    const out=CMDS[c];
    if(!out){ 
      await line(box, '[OMEGA-AI] PROCESSING QUERY...', {cls:'dim', speed:15, tk});
      try {
        const authCode = localStorage.getItem('rn01_session') || '';
        const res = await fetch('/api/ai', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ code: authCode, message: shown })
        });
        const data = await res.json();
        const reply = data.reply || '[SYSTEM] OMEGA CORE OFFLINE.';
        const lines = reply.split('\\n');
        for (let r of lines) {
           if(tk!==token) return; 
           if (r.trim()) await line(box, r, {speed:20, tk}); 
        }
      } catch (e) {
        if(tk!==token) return; 
        await line(box, '[SYSTEM] CONNECTION LOST. OMEGA UNREACHABLE.', {cls:'dim',speed:10,tk}); 
      }
      return; 
    }
    for(const l of out){ if(tk!==token) return; await line(box,l,{speed:12,tk}); }
  });
}"""

html = html.replace(old_cmd, new_cmd)

with open('index.html', 'w') as f:
    f.write(html)

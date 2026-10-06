import re

with open('index.html', 'r') as f:
    html = f.read()

old_cmd = """    if(!out){ 
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
    }"""

new_cmd = """    if(!out){ 
      const loadEl = await line(box, '[OMEGA-AI] LINKING ', {cls:'dim', speed:15, tk});
      if(!loadEl) return;
      let loadFrame = 0;
      const spinner = ['|', '/', '-', '\\\\'];
      const loadInt = setInterval(() => {
        loadEl.textContent = '[OMEGA-AI] PROCESSING ' + spinner[loadFrame];
        loadFrame = (loadFrame + 1) % spinner.length;
      }, 100);

      try {
        const authCode = localStorage.getItem('rn01_session') || '';
        const res = await fetch('/api/ai', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ code: authCode, message: shown })
        });
        const data = await res.json();
        clearInterval(loadInt);
        loadEl.textContent = '[OMEGA-AI] RESPONSE ESTABLISHED.';
        const reply = data.reply || '[SYSTEM] OMEGA CORE OFFLINE.';
        const lines = reply.split('\\n');
        for (let r of lines) {
           if(tk!==token) return; 
           if (r.trim()) await line(box, r, {speed:20, tk}); 
        }
      } catch (e) {
        clearInterval(loadInt);
        loadEl.textContent = '[OMEGA-AI] CONNECTION FAILED.';
        if(tk!==token) return; 
        await line(box, '[SYSTEM] CONNECTION LOST. OMEGA UNREACHABLE.', {cls:'dim',speed:10,tk}); 
      }
      return; 
    }"""

html = html.replace(old_cmd, new_cmd)

with open('index.html', 'w') as f:
    f.write(html)

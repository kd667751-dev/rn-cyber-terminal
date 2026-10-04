import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Disable Zoom
html = html.replace('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
                    '<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1.0,user-scalable=no,viewport-fit=cover">')

# 2. Add touch-action to prevent double tap zoom
css_touch = "body { touch-action: manipulation; }"
html = html.replace('<style>', f'<style>\n{css_touch}')

# 3. Add debug to login gate
auth_regex = r"const res = await fetch\('/api/auth'.*?const data = await res\.json\(\);"
auth_debug = """const res = await fetch('/api/auth', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ code })
        });
        const text = await res.text();
        let data;
        try {
          data = JSON.parse(text);
        } catch(e) {
          err.textContent = `DEBUG ERROR: ${res.status} | ` + text.substring(0,30);
          return;
        }"""
html = re.sub(auth_regex, auth_debug, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)

import re

with open('admin18.html', 'r') as f:
    html = f.read()

old_logic = """      const isExpired = c.expires_at < now;
      const isUsedUp = c.used_count >= c.max_uses;
      const invalid = isExpired || isUsedUp;
      
      const tr = document.createElement('tr');
      if (invalid) tr.className = 'expired';
      
      const isPending = c.used_count === 0 && c.expires_at > 2000000000;
      const expDate = isPending ? `Starts on 1st use (${c.duration_mins}m)` : new Date(c.expires_at * 1000).toLocaleString();
      const status = isExpired ? 'Expired' : (isUsedUp ? 'Used Up' : (isPending ? 'Pending' : 'Active'));"""

new_logic = """      const isPending = c.used_count === 0 && c.expires_at > 2000000000;
      const isUsedUp = c.used_count >= c.max_uses;
      const isCurrentlyRunning = c.expires_at > now && c.expires_at < 2000000000;
      const hasUsesLeft = c.used_count > 0 && c.used_count < c.max_uses;
      
      const invalid = isUsedUp && !isCurrentlyRunning;
      
      const tr = document.createElement('tr');
      if (invalid) tr.className = 'expired';
      
      let expDate = new Date(c.expires_at * 1000).toLocaleString();
      let status = '';
      
      if (isPending) {
        expDate = `Starts on 1st use (${c.duration_mins}m)`;
        status = 'Pending';
      } else if (isCurrentlyRunning) {
        status = 'Currently Active';
      } else if (hasUsesLeft) {
        expDate = `Next use will run for ${c.duration_mins}m`;
        status = 'Ready for Next Use';
      } else {
        status = 'Used Up';
      }"""

html = html.replace(old_logic, new_logic)

with open('admin18.html', 'w') as f:
    f.write(html)

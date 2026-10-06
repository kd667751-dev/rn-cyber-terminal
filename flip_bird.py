import re

with open('index.html', 'r') as f:
    html = f.read()

old_draw = """    draw() {
      ctx.save();
      ctx.translate(this.x + this.w/2, this.y + this.h/2);
      // rotate bird based on speed
      let rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, (this.speed * 0.1)));
      if (state.current === state.getReady) rotation = 0;
      ctx.rotate(rotation);
      ctx.font = "30px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("🐦", 0, 0); // Real bird emoji!
      ctx.restore();
    },"""

new_draw = """    draw() {
      ctx.save();
      ctx.translate(this.x + this.w/2, this.y + this.h/2);
      // rotate bird based on speed
      let rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, (this.speed * 0.1)));
      if (state.current === state.getReady) rotation = 0;
      ctx.rotate(rotation);
      
      // Flip horizontally so the bird faces right instead of left
      ctx.scale(-1, 1);
      
      ctx.font = "30px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("🐦", 0, 0); // Real bird emoji!
      ctx.restore();
    },"""

html = html.replace(old_draw, new_draw)

with open('index.html', 'w') as f:
    f.write(html)

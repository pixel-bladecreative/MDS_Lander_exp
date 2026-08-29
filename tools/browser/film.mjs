import { launch } from './launch.mjs';
import { mkdirSync } from 'node:fs';
const [,, URL_, OUT, W, H, TAG] = process.argv;
mkdirSync(OUT,{recursive:true});
const b = await launch();
const ctx = await b.newContext({viewport:{width:+W,height:+H}});
const p = await ctx.newPage();
await p.goto(URL_,{waitUntil:'load',timeout:90000});
await p.waitForFunction(()=>window.__ready===true,{timeout:90000});
const filmH = await p.evaluate(()=>document.getElementById('film').offsetHeight - innerHeight);
const samples = [];
for (const f of [0,0.12,0.28,0.44,0.60,0.76,0.92,1.0]){
  const y = Math.round(filmH*f);
  await p.evaluate(v=>window.scrollTo(0,v), y);
  await p.evaluate(()=>window.__settle());
  await p.waitForTimeout(500);
  // read the canvas centre: three different colours means it is genuinely scrubbing
  const px = await p.evaluate(()=>{ const c=document.getElementById('frames');
    const d=c.getContext('2d').getImageData(c.width>>1,c.height>>1,1,1).data;
    return [d[0],d[1],d[2]].join(','); });
  const st = await p.evaluate(()=>window.__filmStats());
  samples.push({f, y, px, frame:st.displayed, loaded:st.loaded, bmp:st.bitmaps});
  await p.screenshot({path:`${OUT}/${TAG}-${String(Math.round(f*100)).padStart(3,'0')}.png`});
}
console.table(samples);
const uniq = new Set(samples.map(s=>s.px));
console.log(uniq.size >= samples.length-1 ? `SCRUB OK — ${uniq.size}/${samples.length} distinct centre pixels`
                                          : `SUSPECT — only ${uniq.size} distinct centre pixels`);
await b.close();

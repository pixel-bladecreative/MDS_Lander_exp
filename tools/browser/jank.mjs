import { launch } from './launch.mjs';
const b = await launch();
const ctx = await b.newContext({viewport:{width:1440,height:900}});
const p = await ctx.newPage();
await p.goto('http://localhost:8899/index.html',{waitUntil:'load',timeout:90000});
await p.waitForFunction(()=>window.__ready===true,{timeout:90000});
await p.evaluate(()=>{ window.__d=[]; let last=performance.now();
  (function loop(){ const t=performance.now(); window.__d.push(t-last); last=t;
    requestAnimationFrame(loop); })(); });
// drive a real scroll through the whole film
const filmH = await p.evaluate(()=>document.getElementById('film').offsetHeight - innerHeight);
for (let i=0;i<=60;i++){
  await p.evaluate(v=>window.scrollTo(0,v), Math.round(filmH*i/60));
  await p.waitForTimeout(60);
}
const s = await p.evaluate(()=>{
  const d=window.__d.slice(5).sort((a,b)=>a-b);
  const q=f=>d[Math.floor(d.length*f)];
  return {frames:d.length, p50:+q(.5).toFixed(1), p95:+q(.95).toFixed(1),
          max:+d[d.length-1].toFixed(1), stats:window.__filmStats()};
});
console.log(JSON.stringify(s,null,1));
console.log(s.p95 < 50 ? `JANK OK — p95 ${s.p95}ms (target <50)` : `JANK HIGH — p95 ${s.p95}ms`);
await b.close();

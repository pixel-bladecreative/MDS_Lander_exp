import { launch } from './launch.mjs';
import { mkdirSync } from 'node:fs';
const [,, URL_, OUT, W, H, TAG] = process.argv;
mkdirSync(OUT, {recursive:true});
const b = await launch();
const ctx = await b.newContext({viewport:{width:+W,height:+H}});
const p = await ctx.newPage();
const errs=[]; p.on('pageerror',e=>errs.push(String(e).slice(0,200)));
p.on('console',m=>{ if(m.type()==='error') errs.push(m.text().slice(0,200)); });
await p.goto(URL_, {waitUntil:'load', timeout:60000});
await p.waitForTimeout(2500);
// jump past the film to audit the sections that don't need frames
const ids = ['how','menu','why','who','terms','book'];
for (const id of ids){
  await p.evaluate(i=>{ const e=document.getElementById(i);
    e.classList.add('in'); e.scrollIntoView({block:'start'}); }, id);
  await p.waitForTimeout(700);
  await p.screenshot({path:`${OUT}/${TAG}-${id}.png`});
}
console.log('errors:', errs.length); errs.slice(0,8).forEach(e=>console.log('  ',e));
console.log(JSON.stringify(await p.evaluate(()=>({
  scrollH: document.documentElement.scrollHeight,
  filmH: document.getElementById('film').offsetHeight,
  fontsOk: document.fonts ? [...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family).filter((v,i,a)=>a.indexOf(v)===i) : null,
})), null, 1));
await b.close();

import { launch } from './launch.mjs';
import { mkdirSync } from 'node:fs';

const URL = process.argv[2];
const OUT = process.argv[3] || 'shots';
const W   = +(process.argv[4] || 1440);
const H   = +(process.argv[5] || 900);
const TAG = process.argv[6] || 'd';
const N   = +(process.argv[7] || 8);
mkdirSync(OUT, { recursive: true });

const b = await launch();
const ctx = await b.newContext({ viewport:{width:W,height:H}, deviceScaleFactor:1 });
const page = await ctx.newPage();

const errors = [], failed = [], slow = [];
page.on('console', m => { if (m.type()==='error') errors.push(m.text().slice(0,300)); });
page.on('pageerror', e => errors.push('PAGEERROR: '+String(e).slice(0,300)));
page.on('requestfailed', r => failed.push(`${r.failure()?.errorText} ${r.url().slice(0,160)}`));
page.on('response', r => { if (r.status()>=400) slow.push(`${r.status()} ${r.url().slice(0,160)}`); });

await page.goto(URL, { waitUntil:'load', timeout:90000 });
await page.waitForTimeout(3500);

const info = await page.evaluate(() => {
  const vids = [...document.querySelectorAll('video')].map(v => ({
    src: v.currentSrc || v.getAttribute('src') || '(none)',
    dataSrc: v.getAttribute('data-sc-src'),
    readyState: v.readyState, networkState: v.networkState,
    w: v.videoWidth, h: v.videoHeight, err: v.error ? v.error.code : null,
    rect: (r=>({w:Math.round(r.width),h:Math.round(r.height)}))(v.getBoundingClientRect()),
  }));
  return {
    scrollH: document.documentElement.scrollHeight,
    innerH: window.innerHeight,
    screens: +(document.documentElement.scrollHeight/window.innerHeight).toFixed(1),
    bodyBg: getComputedStyle(document.body).backgroundColor,
    htmlBg: getComputedStyle(document.documentElement).backgroundColor,
    vids,
    imgs: document.images.length,
    brokenImgs: [...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src.slice(0,120)),
  };
});
console.log(JSON.stringify(info,null,1));

const max = info.scrollH - info.innerH;
for (let i=0;i<N;i++){
  const y = Math.round(max * i/(N-1));
  await page.evaluate(v=>window.scrollTo(0,v), y);
  await page.waitForTimeout(1400);
  await page.screenshot({ path:`${OUT}/${TAG}${String(i).padStart(2,'0')}_y${y}.png` });
}
console.log('CONSOLE ERRORS:', errors.length); errors.slice(0,12).forEach(e=>console.log('  ',e));
console.log('FAILED REQ:', failed.length);    failed.slice(0,12).forEach(e=>console.log('  ',e));
console.log('HTTP>=400:', slow.length);       [...new Set(slow)].slice(0,12).forEach(e=>console.log('  ',e));
await b.close();

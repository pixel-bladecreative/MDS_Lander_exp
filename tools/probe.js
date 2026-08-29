#!/usr/bin/env node
/**
 * probe.js <url> <scrollPx> — report the engine's real internal state.
 *
 * A screenshot tells you what was painted; it does not tell you WHY. This
 * reports progress, the playhead, how many frames are actually loaded, which
 * frame the canvas is really showing, and the centre pixel — so "the film is
 * stuck" can be separated from "the frame it wants has not downloaded".
 */
const puppeteer = require(process.env.HOME +
  '/.claude/skills/synced/scroll-film-studio/scripts/node_modules/puppeteer-core');

(async () => {
  const [url, pos] = process.argv.slice(2);
  const browser = await puppeteer.launch({
    executablePath: process.env.CHROME_PATH || '/opt/pw-browsers/chromium',
    headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--hide-scrollbars'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
  page.on('console', (m) => { if (m.type() === 'error') console.error('PAGE ERR:', m.text()); });
  page.on('pageerror', (e) => console.error('PAGE THROW:', e.message));
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForFunction('window.__ready === true', { timeout: 20000 }).catch(() => {});
  await new Promise((r) => setTimeout(r, 800));

  // Headless throttles rAF to ~1fps, so the eased playhead would never arrive.
  // Scroll, then force-settle through the engine's own hook.
  await page.evaluate((y) => window.scrollTo(0, y), Number(pos));
  await new Promise((r) => setTimeout(r, 1500));
  await page.evaluate(() => window.__settle && window.__settle());
  await new Promise((r) => setTimeout(r, 400));
  await page.evaluate(() => window.__settle && window.__settle());

  const info = await page.evaluate(() => {
    const film = document.getElementById('film');
    const r = film.getBoundingClientRect();
    const span = r.height - innerHeight;
    const p = span <= 0 ? 0 : Math.max(0, Math.min(1, -r.top / span));
    const c = document.querySelector('canvas');
    const g = c.getContext('2d');
    const px = g.getImageData(Math.floor(c.width / 2), Math.floor(c.height / 2), 1, 1).data;
    const imgs = document.querySelectorAll('img');
    return {
      scrollY: Math.round(scrollY),
      filmHeight: Math.round(r.height),
      filmTop: Math.round(r.top),
      span: Math.round(span),
      progress: +p.toFixed(4),
      expectedFrame: Math.round(p * 599),
      centrePixel: `rgb(${px[0]},${px[1]},${px[2]})`,
      canvas: `${c.width}x${c.height}`,
      readout: document.getElementById('ch-label').textContent,
      beatOpacities: [...document.querySelectorAll('.beat')].map(
        (b) => +(b.style.opacity || 0)).map((n) => +n.toFixed(2)),
      brokenImages: [...imgs].filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.src.slice(-40)),
      stats: window.__filmStats ? window.__filmStats() : null,
    };
  });
  console.log(JSON.stringify(info, null, 1));
  await browser.close();
})();

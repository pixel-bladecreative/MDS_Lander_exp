#!/usr/bin/env node
/**
 * shot.js <url> <out.png> [w] [h] [scrollPx] — settled screenshot.
 *
 * The skill's shot.js waits 1.8s for the eased playhead to arrive. That is right
 * on a real browser and wrong here: headless Chromium throttles requestAnimationFrame
 * to roughly 1fps, so the lerp advances about four steps in four seconds and the
 * capture shows a frame from the middle of the easing. Every "the film is stuck"
 * reading in this build came from that, not from the film.
 *
 * So: scroll, then drive the engine's own __settle() hook, which skips the easing
 * and paints the frame the scroll position actually maps to.
 */
const fs = require('node:fs');
const path = require('node:path');
const puppeteer = require(process.env.HOME +
  '/.claude/skills/synced/scroll-film-studio/scripts/node_modules/puppeteer-core');

(async () => {
  const [url, out, w, h, pos] = process.argv.slice(2);
  if (!url || !out) {
    console.error('usage: shot.js <url> <out.png> [w] [h] [scrollPx]');
    process.exit(1);
  }
  const width = Number(w) || 1440;
  const height = Number(h) || 900;

  const browser = await puppeteer.launch({
    executablePath: process.env.CHROME_PATH || '/opt/pw-browsers/chromium',
    headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--hide-scrollbars'],
  });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width, height, deviceScaleFactor: 2 });
    const errors = [];
    page.on('pageerror', (e) => errors.push(e.message));
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    const ready = await page.waitForFunction('window.__ready === true', { timeout: 20000 })
      .then(() => true).catch(() => false);
    await new Promise((r) => setTimeout(r, 900));

    if (pos !== undefined) {
      await page.evaluate((y) => window.scrollTo(0, Number(y)), pos);
      // Sections below the film reveal on intersection; under throttled rAF the
      // observer still fires, but give it a beat before forcing the paint.
      await new Promise((r) => setTimeout(r, 1200));
      await page.evaluate(() => window.__settle && window.__settle());
      await new Promise((r) => setTimeout(r, 500));
      await page.evaluate(() => window.__settle && window.__settle());
      await new Promise((r) => setTimeout(r, 300));
    }

    fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
    await page.screenshot({ path: out });
    const info = await page.evaluate(() => {
      const c = document.querySelector('canvas');
      const doc = document.documentElement;
      return {
        innerWidth: window.innerWidth,
        scrollY: Math.round(window.scrollY),
        docHeight: Math.max(doc.scrollHeight, document.body.scrollHeight),
        canvas: c ? `${c.width}x${c.height}` : 'none',
        overflowX: doc.scrollWidth > window.innerWidth,
        stats: window.__filmStats ? window.__filmStats() : null,
      };
    });
    console.log(JSON.stringify({ out: path.basename(out), ready, ...info, errors }));
  } finally {
    await browser.close();
  }
})();

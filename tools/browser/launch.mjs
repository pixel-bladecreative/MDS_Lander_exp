import { chromium } from 'playwright';
import { existsSync, readdirSync } from 'node:fs';

export function chromePath() {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  const found = [];
  if (existsSync(root)) for (const d of readdirSync(root)) {
    if (!d.startsWith('chromium')) continue;
    for (const sub of ['chrome-linux/chrome','chrome-linux/headless_shell','chrome-linux64/chrome']) {
      const p = `${root}/${d}/${sub}`;
      if (existsSync(p)) found.push(p);
    }
  }
  found.sort((a,b) => (b.includes('/chrome') - a.includes('/chrome'))
                   || b.localeCompare(a, undefined, {numeric:true}));
  return found[0];
}

export async function launch({ offline = false, extra = [], ...opts } = {}) {
  const exe = chromePath();
  const args = ['--no-sandbox','--disable-dev-shm-usage','--ssl-version-max=tls1.2'];
  if (!offline && process.env.HTTPS_PROXY) args.push(`--proxy-server=${process.env.HTTPS_PROXY}`);
  return chromium.launch({ ...(exe ? {executablePath: exe} : {}), args: args.concat(extra), ...opts });
}

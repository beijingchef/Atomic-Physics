const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require('C:/Users/zhaok/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const dir = path.resolve('introductory_QM');
const source = fs.readFileSync(path.join(dir, '04-commutation-relations.qmd'), 'utf8');
const before = fs.readFileSync(path.join(dir, 'backups/04-commutation-relations.before-flow-revision.qmd'), 'utf8');
const anchors = s => [...s.matchAll(/\{#([^}]+)\}/g)].map(m => m[1]);
const all = fs.readdirSync(dir).filter(f => f.endsWith('.qmd')).map(f => fs.readFileSync(path.join(dir, f), 'utf8')).join('\n');
const labels = anchors(all);
const report = {
  preservedAnchors: JSON.stringify(anchors(source)) === JSON.stringify(anchors(before)),
  anchorCount: anchors(source).length,
  unresolvedChapterReferences: [...source.matchAll(/@(eq-[\w-]+)/g)].map(m => m[1]).filter(id => !labels.includes(id)),
  missingSourceAssets: [...source.matchAll(/\]\((assets\/[^)]+)\)/g)].map(m => m[1]).filter(f => !fs.existsSync(path.join(dir, f))),
};
(async () => {
  const browser = await chromium.launch({headless: true, channel: 'msedge'});
  try {
    const context = await browser.newContext({viewport: {width: 1440, height: 1000}, offline: true});
    const page = await context.newPage();
    await page.goto(pathToFileURL(path.join(dir, '_book/04-commutation-relations.html')).href, {waitUntil: 'load'});
    await page.waitForFunction(() => window.MathJax?.startup?.document, null, {timeout: 30000});
    await page.evaluate(() => window.MathJax.startup.promise);
    report.render = await page.evaluate(() => ({
      mathExpressions: document.querySelectorAll('mjx-container').length,
      sourceExpressions: document.querySelectorAll('.math').length,
      mathErrors: [...document.querySelectorAll('[data-mml-node="merror"], mjx-merror')].map(e => e.textContent),
      missingImages: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src),
      brokenCrossrefs: [...document.querySelectorAll('a.quarto-xref')].filter(a => a.textContent.includes('?')).map(a => a.textContent),
    }));
    report.groupedHeadings = await page.evaluate(() => [...document.querySelectorAll('.eigenstate-table table')].map(table => {
      const axis = table.querySelector('[rowspan]');
      const heading = table.querySelector('[colspan]');
      const style = getComputedStyle(axis);
      return {
        rowSpan: axis?.rowSpan,
        columnSpan: heading?.colSpan || null,
        axisText: axis?.textContent.trim(),
        horizontalAlignment: style.textAlign,
        verticalAlignment: style.verticalAlign,
        dots: (table.textContent.match(/●/g) || []).length,
        codeBlocks: table.querySelectorAll('pre').length,
      };
    }));
    await page.locator('.eigenstate-table').first().scrollIntoViewIfNeeded();
    await page.screenshot({path: path.join(dir, 'conversion_work/chapter4-grouped-headings.png')});
    await page.locator('.eigenstate-table').nth(3).scrollIntoViewIfNeeded();
    await page.screenshot({path: path.join(dir, 'conversion_work/chapter4-angular-headings.png')});
    await page.screenshot({path: path.join(dir, 'conversion_work/chapter4-revised-opening.png')});
    await page.locator('#measurement-paths-and-interference').scrollIntoViewIfNeeded();
    await page.screenshot({path: path.join(dir, 'conversion_work/chapter4-revised-interference.png')});
  } finally {
    await browser.close();
  }
  fs.writeFileSync(path.join(dir, 'conversion_work/chapter4-revision-validation.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
  if (!report.preservedAnchors || report.unresolvedChapterReferences.length || report.missingSourceAssets.length || report.render.mathErrors.length || report.render.missingImages.length || report.render.brokenCrossrefs.length) process.exitCode = 1;
})().catch(e => { console.error(e); process.exitCode = 1; });

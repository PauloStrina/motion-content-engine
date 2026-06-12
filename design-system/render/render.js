// Render de plantillas Motion a PNG. Uso: node render.js <template.html> <data.json> [outdir]
// Requiere: npm i puppeteer
const puppeteer = require('puppeteer'); const fs = require('fs'); const path = require('path');
(async () => {
  const [,, tpl, dataFile, outdir='out'] = process.argv;
  const data = JSON.parse(fs.readFileSync(dataFile,'utf8'));
  const slides = data.slides || [data]; fs.mkdirSync(outdir,{recursive:true});
  const browser = await puppeteer.launch({args:['--no-sandbox']});
  const page = await browser.newPage();
  await page.setViewport({width:1080, height:1350, deviceScaleFactor:1});
  for (let i=0;i<slides.length;i++){
    await page.goto('file://'+path.resolve(tpl));
    await page.evaluate(d=>{window.__DATA__=d; document.dispatchEvent(new Event('DOMContentLoaded'))}, slides[i]);
    await page.reload({waitUntil:'networkidle0'});
    await page.evaluate(d=>{window.__DATA__=d;}, slides[i]);
    await page.goto('file://'+path.resolve(tpl)+'#'+encodeURIComponent(JSON.stringify(slides[i])));
    // inyección robusta: reescribimos data y re-ejecutamos el script inline
    await page.evaluate(d=>{window.__DATA__=d; const s=document.querySelectorAll('script'); s.forEach(x=>eval(x.textContent));}, slides[i]);
    await page.screenshot({path: path.join(outdir, `slide-${String(i+1).padStart(2,'0')}.png`)});
  }
  await browser.close(); console.log(`OK: ${slides.length} slides → ${outdir}/`);
})();

from playwright.sync_api import sync_playwright
from pathlib import Path
import os,json,re
OUT=Path(__file__).parent
ROOT=OUT.parents[2]
routes=[]
for source in (ROOT/'Src/Portfolio_Core/Portfolio/Pages').rglob('*.cshtml'):
 if source.read_text(encoding='utf-8-sig').lstrip().startswith('@page'):
  route=source.relative_to(ROOT/'Src/Portfolio_Core/Portfolio/Pages').with_suffix('').as_posix()
  routes.append('/' if route=='Index' else '/'+route)
def ratio(a,b):
 def lum(c):
  rgb=[int(v)/255 for v in re.findall(r'\d+',c)[:3]]
  return sum(w*(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4) for x,w in zip(rgb,(.2126,.7152,.0722)))
 x,y=sorted((lum(a),lum(b)));return round((y+.05)/(x+.05),2)
records=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=str(Path(os.environ['LOCALAPPDATA'])/'ms-playwright/chromium-1234/chrome-win64/chrome.exe'))
 for theme in ('light','dark'):
  ctx=browser.new_context(color_scheme=theme)
  ctx.route('**/*',lambda r:r.continue_() if r.request.url.startswith('http://localhost:5187') else r.abort())
  page=ctx.new_page()
  for route in routes:
   page.goto('http://localhost:5187'+route);page.wait_for_load_state('networkidle')
   samples=page.locator('main a,main h1,main p,main .list-group-item-info,.navbar .nav-link,.navbar-brand,.theme-control label,main .btn').evaluate_all("els=>els.slice(0,200).filter(e=>e.getBoundingClientRect().width>0).map(e=>{let s=getComputedStyle(e),b=e;while(b.parentElement&&getComputedStyle(b).backgroundColor==='rgba(0, 0, 0, 0)')b=b.parentElement;return {text:e.innerText.slice(0,65),color:s.color,bg:getComputedStyle(b).backgroundColor,size:s.fontSize,weight:s.fontWeight}})")
   for item in samples:
    item.update(contrast=ratio(item['color'],item['bg']),route=route,theme=theme)
    item['threshold']=3 if float(item['size'][:-2])>=24 or (float(item['size'][:-2])>=18.66 and int(item['weight'])>=700) else 4.5
    item['passed']=item['contrast']>=item['threshold'];records.append(item)
  ctx.close()
 browser.close()
report={'samples':len(records),'routes':len(routes),'failures':[x for x in records if not x['passed']],'records':records,'limitations':['Computed solid foreground/background samples, up to200elements perroute; excludes hover/image overlays and does not constitute full accessibility certification.']}
(OUT/'contrast-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'samples':report['samples'],'routes':len(routes),'failures':report['failures']},indent=2))

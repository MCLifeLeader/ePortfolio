import json,os
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
OUT=Path(__file__).parent
SHOTS=OUT/'image-dependency-screenshots';SHOTS.mkdir(exist_ok=True)
BASE='http://localhost:5187'
report={'base':BASE,'checks':[],'browsers':{},'cases':[],'limitations':['Targeted local headless regression checks after image/CSS and dependency changes; previous complete page-layout checkpoint retained.','External requests blocked. No external-link availability, physical-device, Safari or production performance claims.']}
def check(name,passed,**details):report['checks'].append({'check':name,'passed':bool(passed),**details})
ROOT=OUT.parents[2]
project=ROOT/'Src/Portfolio_Core/Portfolio'
report['libman']=json.loads((project/'libman.json').read_text(encoding='utf-8'))
report['library_files']=sorted(str(p.relative_to(project/'wwwroot/lib')) for p in (project/'wwwroot/lib').rglob('*') if p.is_file())
check('minimal-libraries',len(report['library_files'])==8 and all('jquery' not in path.lower() for path in report['library_files']),files=report['library_files'])
with sync_playwright() as pw:
 for name in ('chromium','firefox'):
  engine=getattr(pw,name);cache=Path(os.environ['LOCALAPPDATA'])/'ms-playwright';executable=Path(engine.executable_path)
  if not executable.exists():executable=max(cache.glob('chromium-*/chrome-win64/chrome.exe' if name=='chromium' else 'firefox-*/firefox/firefox.exe'),key=lambda p:int(p.relative_to(cache).parts[0].split('-')[-1]))
  browser=engine.launch(headless=True,executable_path=str(executable));report['browsers'][name]={'version':browser.version,'executable':str(executable)}
  for width,height,label in ((1440,1000,'desktop'),(768,1024,'tablet'),(375,812,'mobile')):
   for theme in ('light','dark'):
    context=browser.new_context(viewport={'width':width,'height':height},color_scheme=theme,reduced_motion='reduce');requests=[];external=[];bad_responses=[];errors=[]
    def route_filter(route):
     if urlparse(route.request.url).hostname in ('localhost','127.0.0.1'):route.continue_()
     else:external.append(route.request.url);route.abort()
    context.route('**/*',route_filter)
    page=context.new_page();page.on('request',lambda request:requests.append(request.url));page.on('response',lambda response:bad_responses.append({'url':response.url,'status':response.status}) if response.status>=400 else None);page.on('pageerror',lambda error:errors.append(str(error)))
    for path,slug in (('/','home'),('/AboutMe','about'),('/Fun/HamRadioVHFGoKit','radio')):
     response=page.goto(BASE+path);page.wait_for_load_state('networkidle');page.evaluate('document.fonts.ready')
     data=page.evaluate('''() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,images:[...document.querySelectorAll('main img')].map(n=>{const r=n.getBoundingClientRect(),s=getComputedStyle(n);return {src:n.getAttribute('src'),alt:n.getAttribute('alt'),loaded:n.complete&&n.naturalWidth>0,naturalWidth:n.naturalWidth,naturalHeight:n.naturalHeight,width:r.width,height:r.height,left:r.left,right:r.right,objectFit:s.objectFit,borderRadius:s.borderRadius};}),icons:[...document.querySelectorAll('.bi')].map(n=>({hidden:n.getAttribute('aria-hidden'),font:getComputedStyle(n,'::before').fontFamily})),iconFontReady:document.fonts.check('16px bootstrap-icons')})''')
     case=f'{name}-{label}-{theme}-{slug}'
     check(case+'-http',response.status==200,status=response.status)
     check(case+'-overflow',data['scroll']<=width+2,width=width,scroll=data['scroll'])
     check(case+'-images',all(i['loaded'] and i['alt'] is not None for i in data['images']),images=data['images'])
     check(case+'-image-bounds',all(i['width']==0 or i['left']>=-2 and i['right']<=width+2 for i in data['images']))
     distortion=[i for i in data['images'] if i['width']>0 and i['height']>0 and i['objectFit']=='fill' and i['naturalHeight']>0 and abs(i['width']/i['height']-i['naturalWidth']/i['naturalHeight'])>0.04]
     check(case+'-image-aspect',not distortion,distorted=distortion)
     check(case+'-icons',bool(data['icons']) and data['iconFontReady'] and all(i['hidden']=='true' and 'bootstrap-icons' in i['font'] for i in data['icons']))
     report['cases'].append({'browser':name,'viewport':label,'theme':theme,'route':path,**data})
     page.screenshot(path=str(SHOTS/(case+'.png')),full_page=slug!='radio')
     if slug=='radio':
      for index in range(page.locator('.carousel').count()):
       gallery=page.locator('.carousel').nth(index);next_control=gallery.locator('[data-bs-slide="next"]')
       if not next_control.count():continue
       before=gallery.locator('.carousel-item.active img').get_attribute('src');next_control.first.click();page.wait_for_function('(id)=>!document.querySelector(id+" .carousel-item-next")',arg='#'+gallery.get_attribute('id'))
       after=gallery.locator('.carousel-item.active img').get_attribute('src');check(case+'-gallery-next-'+str(index),before!=after,before=before,after=after)
       page.screenshot(path=str(SHOTS/(case+'-gallery-'+str(index)+'.png')))
    check(f'{name}-{label}-{theme}-no-jquery-requests',not any('jquery' in request.lower() for request in requests),jquery_requests=[request for request in requests if 'jquery' in request.lower()])
    check(f'{name}-{label}-{theme}-no-js-errors',not errors,errors=errors)
    check(f'{name}-{label}-{theme}-no-local-resource-errors',not bad_responses,responses=bad_responses)
    context.close()
  browser.close()
report['failures']=[check for check in report['checks'] if not check['passed']]
report['summary']={'cases':len(report['cases']),'checks':len(report['checks']),'failures':len(report['failures'])}
(OUT/'image-dependency-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'summary':report['summary'],'failures':report['failures']},indent=2))
import json, time, os
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
SHOTS=OUT/'browser-screenshots'
SHOTS.mkdir(exist_ok=True)
BASE='http://localhost:5187'
pages_root=ROOT/'Src/Portfolio_Core/Portfolio/Pages'
routes=[]
for file in pages_root.rglob('*.cshtml'):
    text=file.read_text(encoding='utf-8-sig')
    if text.lstrip().startswith('@page'):
        relative=file.relative_to(pages_root).with_suffix('').as_posix()
        routes.append('/' if relative=='Index' else '/'+relative)
routes.sort()
report={'base':BASE,'routes':routes,'browsers':{},'checks':[], 'limitations':['Local headless browser checks; no physical device or assistive-technology testing.','External network requests are blocked; no external link availability validation.','Navigation timings are local observations, not production performance benchmarks.']}
def record(name, passed, **details):
    report['checks'].append({'check':name,'passed':bool(passed),**details})

def setup(context, blocked):
    def filter_request(route):
        parsed=urlparse(route.request.url)
        if parsed.hostname in ('localhost','127.0.0.1') or parsed.scheme in ('data','blob','about'):
            route.continue_()
        else:
            blocked.add(route.request.url)
            route.abort()
    context.route('**/*',filter_request)

with sync_playwright() as pw:
 for name in ('chromium','firefox'):
    engine=getattr(pw,name)
    try:
        cache_root=Path(os.environ['LOCALAPPDATA'])/'ms-playwright'
        candidates=list(cache_root.glob('chromium-*/chrome-win64/chrome.exe' if name=='chromium' else 'firefox-*/firefox/firefox.exe'))
        cached=Path(engine.executable_path)
        if not cached.exists() and candidates:
            cached=max(candidates,key=lambda item:int(item.relative_to(cache_root).parts[0].split('-')[-1]))
        browser=engine.launch(headless=True,executable_path=str(cached))
    except Exception as error:
        report['browsers'][name]={'available':False,'reason':str(error)}
        continue
    blocked=set()
    report['browsers'][name]={'available':True,'version':browser.version,'executable':str(cached),'layout':[]}
    for width,height,label in ((1440,1000,'desktop'),(768,1024,'tablet'),(375,812,'mobile')):
      for theme in ('light','dark'):
        context=browser.new_context(viewport={'width':width,'height':height},color_scheme=theme,reduced_motion='reduce')
        setup(context,blocked)
        page=context.new_page()
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        for route in routes:
            began=time.monotonic()
            response=page.goto(BASE+route)
            page.wait_for_load_state('networkidle')
            layout=page.evaluate('''() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,theme:document.documentElement.getAttribute('data-bs-theme'),h1:document.querySelector('main h1')?.innerText,overflow:[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+2||r.left< -2)}).slice(0,8).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,90)})),brokenImages:[...document.querySelectorAll('main img')].filter(e=>e.getAttribute('src')&&!e.complete||e.getAttribute('src')&&e.complete&&!e.naturalWidth).map(e=>e.getAttribute('src'))})''')
            report['browsers'][name]['layout'].append({'route':route,'viewport':label,'theme':theme,'status':response.status,'navigation_ms':round((time.monotonic()-began)*1000),**layout})
            (OUT/'browser-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
            if route=='/':
                page.screenshot(path=str(SHOTS/f'{name}-{label}-{theme}.png'),full_page=True)
        record(f'{name}-{label}-{theme}-javascript',not errors,errors=errors)
        context.close()
    context=browser.new_context(viewport={'width':1440,'height':1000},color_scheme='dark',reduced_motion='reduce')
    setup(context,blocked)
    page=context.new_page()
    page.goto(BASE)
    page.wait_for_load_state('networkidle')
    record(name+'-system-default',page.locator('html').get_attribute('data-bs-theme')=='dark')
    page.keyboard.press('Tab')
    record(name+'-skip-focus',page.evaluate("document.activeElement.classList.contains('skip-link')"),outline=page.evaluate("getComputedStyle(document.activeElement).outlineStyle"))
    page.keyboard.press('Enter')
    record(name+'-skip-target',page.evaluate("document.activeElement.id==='main-content'"))
    toggle=page.get_by_role('switch',name='Dark mode')
    toggle.uncheck()
    page.reload()
    page.wait_for_load_state('networkidle')
    record(name+'-stored-light-reload',page.locator('html').get_attribute('data-bs-theme')=='light' and not toggle.is_checked())
    toggle.check()
    page.reload()
    page.wait_for_load_state('networkidle')
    record(name+'-stored-dark-reload',page.locator('html').get_attribute('data-bs-theme')=='dark' and toggle.is_checked())
    page.set_viewport_size({'width':375,'height':812})
    menu=page.get_by_role('button',name='Toggle navigation')
    menu.focus()
    page.keyboard.press('Enter')
    page.wait_for_function("document.querySelector('#main-navigation').classList.contains('show')")
    record(name+'-keyboard-mobile-menu-open',menu.get_attribute('aria-expanded')=='true' and page.get_by_role('link',name='Architecture',exact=True).first.is_visible())
    page.keyboard.press('Enter')
    page.wait_for_function("!document.querySelector('#main-navigation').classList.contains('show')")
    record(name+'-keyboard-mobile-menu-close',menu.get_attribute('aria-expanded')=='false')
    page.goto(BASE+'/Contact');page.wait_for_load_state('networkidle')
    record(name+'-contact-truthful','not currently available' in page.locator('main').inner_text() and page.locator('main form').count()==0)
    links=page.locator('main a').evaluate_all('(nodes)=>nodes.map(n=>n.href)')
    record(name+'-social-links-retained',any('linkedin.com' in link for link in links) and any('github.com' in link for link in links))
    page.goto(BASE+'/Error');page.wait_for_load_state('networkidle')
    record(name+'-production-error-no-debug-instructions','Development Mode' not in page.locator('main').inner_text() and 'ASPNETCORE_ENVIRONMENT' not in page.locator('main').inner_text())
    page.goto(BASE+'/Fun/HamRadioVHFGoKit');page.wait_for_load_state('networkidle')
    galleries=page.locator('.carousel')
    for index in range(galleries.count()):
        gallery=galleries.nth(index)
        controls=gallery.locator('[data-bs-slide="next"]')
        if controls.count():
            before=gallery.locator('.carousel-item.active img').get_attribute('src')
            controls.first.click()
            page.wait_for_function('(id)=>!document.querySelector(id+" .carousel-item-next")', arg='#'+gallery.get_attribute('id'))
            after=gallery.locator('.carousel-item.active img').get_attribute('src')
            record(name+'-gallery-next-'+str(index),before!=after,before=before,after=after)
    page.goto(BASE+'/College/Cs364');page.wait_for_load_state('networkidle')
    documents=page.locator('main a[href$=".pdf"]').evaluate_all('(nodes)=>nodes.map(n=>n.href)')
    for document in documents:
        if urlparse(document).hostname=='localhost':
            response=context.request.get(document)
            body=response.body()
            record(name+'-internal-document',response.status==200 and body.startswith(b'%PDF'),url=document,size=len(body),content_type=response.headers.get('content-type'))
    context.close()
    for scheme in ('light','dark'):
        context=browser.new_context(viewport={'width':1440,'height':1000},color_scheme=scheme)
        setup(context,blocked)
        context.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})")
        page=context.new_page();page.goto(BASE);page.wait_for_load_state('networkidle')
        initial=page.locator('html').get_attribute('data-bs-theme')
        toggle=page.get_by_role('switch',name='Dark mode')
        toggle.set_checked(scheme!='dark')
        changed=page.locator('html').get_attribute('data-bs-theme')
        record(name+'-blocked-storage-'+scheme,initial==scheme and changed!=scheme,initial=initial,changed=changed)
        context.close()
    report['browsers'][name]['blocked_external_requests']=sorted(blocked)
    browser.close()
report['failures']=[check for check in report['checks'] if not check['passed']]
report['overflow']=[{'browser':name,**row} for name,data in report['browsers'].items() for row in data.get('layout',[]) if row['scroll']>row['width']+2]
report['bad_statuses']=[{'browser':name,**row} for name,data in report['browsers'].items() for row in data.get('layout',[]) if row['status']!=200]
report['broken_images']=[{'browser':name,'route':row['route'],'images':row['brokenImages']} for name,data in report['browsers'].items() for row in data.get('layout',[]) if row['brokenImages']]
(OUT/'browser-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'browsers':{name: data.get('available') for name,data in report['browsers'].items()},'routes':len(routes),'checks':len(report['checks']),'failures':report['failures'],'overflow':report['overflow'],'bad_statuses':report['bad_statuses'],'broken_images':report['broken_images']},indent=2))
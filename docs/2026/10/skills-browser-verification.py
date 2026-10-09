import json, time, os
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
SHOTS=OUT/'skills-screenshots'
SHOTS.mkdir(exist_ok=True)
BASE='http://localhost:5187'
JSON_NAME=os.environ.get('LAYOUT_BROWSER_JSON','skills-browser-verification.json')
BROWSER_NAMES=(os.environ['LAYOUT_BROWSER'],) if os.environ.get('LAYOUT_BROWSER') else ('chromium','firefox')
pages_root=ROOT/'Src/Portfolio_Core/Portfolio/Pages'
routes=[]
for file in pages_root.rglob('*.cshtml'):
    text=file.read_text(encoding='utf-8-sig')
    if text.lstrip().startswith('@page'):
        relative=file.relative_to(pages_root).with_suffix('').as_posix()
        routes.append('/' if relative=='Index' else '/'+relative)
routes=sorted(route for route in routes if route.startswith('/Skills/'))
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
 for name in BROWSER_NAMES:
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
        resource_errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('response',lambda response:resource_errors.append({'url':response.url,'status':response.status}) if response.status>=400 else None)
        for route in routes:
            began=time.monotonic()
            response=page.goto(BASE+route)
            page.wait_for_load_state('networkidle')
            layout=page.evaluate('''() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,theme:document.documentElement.getAttribute('data-bs-theme'),h1:document.querySelector('main h1')?.innerText,overflow:[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+2||r.left< -2)}).slice(0,8).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,90)})),brokenImages:[...document.querySelectorAll('main img')].filter(e=>e.getAttribute('src')&&!e.complete||e.getAttribute('src')&&e.complete&&!e.naturalWidth).map(e=>e.getAttribute('src'))})''')
            semantics=page.evaluate(r'''() => {
                const headings=[...document.querySelectorAll('main h1,main h2,main h3,main h4,main h5,main h6')];
                const skips=[]; for(let i=1;i<headings.length;i++){const previous=+headings[i-1].tagName[1],level=+headings[i].tagName[1];if(level>previous+1)skips.push({previous:headings[i-1].innerText,current:headings[i].innerText,previousLevel:previous,level});}
                const ids=[...document.querySelectorAll('[id]')].map(n=>n.id), duplicates=[...new Set(ids.filter((id,index)=>ids.indexOf(id)!==index))];
                const anchors=[...document.querySelectorAll('a[href]')];
                const badAnchors=anchors.map(n=>({url:new URL(n.href,location.href),label:n.textContent.trim()})).filter(item=>item.url.origin===location.origin&&item.url.pathname===location.pathname&&item.url.hash&&item.url.hash!=='#'&&!document.getElementById(decodeURIComponent(item.url.hash.slice(1)))) .map(item=>({href:item.url.href,label:item.label}));
                return {h1Count:document.querySelectorAll('main h1').length,headingSkips:skips,duplicateIds:duplicates,badAnchors,retiredLinks:anchors.filter(n=>{const u=new URL(n.href,location.href);return /resume\.pdf/i.test(n.href)||(/\/Experience\/ResumeHistory(?:\/?$|[?#])/i.test(n.href)&&!(u.pathname===location.pathname&&u.hash));}).map(n=>n.href),imagesWithoutAlt:[...document.querySelectorAll('img:not([alt])')].map(n=>n.getAttribute('src'))};
            }''')
            for check,passed,details in (
                ('one-h1',semantics['h1Count']==1,semantics['h1Count']),
                ('heading-hierarchy',not semantics['headingSkips'],semantics['headingSkips']),
                ('unique-ids',not semantics['duplicateIds'],semantics['duplicateIds']),
                ('same-page-anchors',not semantics['badAnchors'],semantics['badAnchors']),
                ('retired-resume-links',not semantics['retiredLinks'],semantics['retiredLinks']),
                ('image-alt-attributes',not semantics['imagesWithoutAlt'],semantics['imagesWithoutAlt'])):
                record(f'{name}-{label}-{theme}-{route}-{check}',passed,route=route,details=details)
            indexes=page.evaluate('''() => [...document.querySelectorAll('.reading-layout:has(> .section-nav)')].map(layout=>{const nav=layout.querySelector(':scope > .section-nav'), main=layout.querySelector(':scope > .reading-main'), aside=layout.querySelector(':scope > .reading-aside');return {firstDOM:layout.firstElementChild===nav,navigationBottom:nav.getBoundingClientRect().bottom,mainTop:main.getBoundingClientRect().top,mainBottom:main.getBoundingClientRect().bottom,resourcesTop:aside?.getBoundingClientRect().top??null};})''')
            record(f'{name}-{label}-{theme}-{route}-index-dom-order',all(item['firstDOM'] for item in indexes),route=route,details=indexes)
            if width<=991:
                record(f'{name}-{label}-{theme}-{route}-index-visual-order',all(item['navigationBottom']<=item['mainTop']+2 and (item['resourcesTop'] is None or item['mainBottom']<=item['resourcesTop']+2) for item in indexes),route=route,details=indexes)
            icons=page.evaluate('''() => {const icons=[...document.querySelectorAll('.bi')];return {count:icons.length,fontReady:document.fonts.check('16px bootstrap-icons'),invalid:icons.filter(n=>n.getAttribute('aria-hidden')!=='true'||!getComputedStyle(n,'::before').fontFamily.includes('bootstrap-icons')).map(n=>({className:n.className,ariaHidden:n.getAttribute('aria-hidden'),font:getComputedStyle(n,'::before').fontFamily}))};}''')
            record(f'{name}-{label}-{theme}-{route}-local-icons',icons['count']>0 and icons['fontReady'] and not icons['invalid'],route=route,details=icons)
            record(f'{name}-{label}-{theme}-{route}-page-http',response.status==200,route=route,status=response.status)
            record(f'{name}-{label}-{theme}-{route}-viewport-overflow',layout['scroll']<=width+2,route=route,scroll=layout['scroll'],width=width)
            record(f'{name}-{label}-{theme}-{route}-loaded-images',not layout['brokenImages'],route=route,images=layout['brokenImages'])
            layout.update(semantics)
            report['browsers'][name]['layout'].append({'route':route,'viewport':label,'theme':theme,'status':response.status,'navigation_ms':round((time.monotonic()-began)*1000),**layout})
            (OUT/JSON_NAME).write_text(json.dumps(report,indent=2),encoding='utf-8')
            if route in ('/Skills/Index','/Skills/Technologies','/Skills/SystemsIntegration','/Skills/DeveloperEnablement','/Skills/Containers','/Skills/Okta','/Skills/Zendesk') and ((name=='chromium' and label in ('desktop','mobile')) or (name=='firefox' and label=='mobile' and theme=='light')):
                page.screenshot(path=str(SHOTS/f'{name}-{label}-{theme}-{route.split('/')[-1]}.png'),full_page=True)
        record(f'{name}-{label}-{theme}-javascript',not errors,errors=errors)
        record(f'{name}-{label}-{theme}-resource-status',not resource_errors,errors=resource_errors)
        context.close()
    report['browsers'][name]['blocked_external_requests']=sorted(blocked)
    browser.close()
report['failures']=[check for check in report['checks'] if not check['passed']]
report['overflow']=[{'browser':name,**row} for name,data in report['browsers'].items() for row in data.get('layout',[]) if row['scroll']>row['width']+2]
report['bad_statuses']=[{'browser':name,**row} for name,data in report['browsers'].items() for row in data.get('layout',[]) if row['status']!=200]
report['broken_images']=[{'browser':name,'route':row['route'],'images':row['brokenImages']} for name,data in report['browsers'].items() for row in data.get('layout',[]) if row['brokenImages']]
report['summary']={'routes':len(routes),'page_layout_cases':sum(len(data.get('layout',[])) for data in report['browsers'].values()),'assertions':len(report['checks']),'failures':len(report['failures'])}
(OUT/JSON_NAME).write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'summary':report['summary'],'failures':report['failures'],'overflow':report['overflow'],'bad_statuses':report['bad_statuses'],'broken_images':report['broken_images']},indent=2))
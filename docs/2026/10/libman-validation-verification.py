raise SystemExit("Historical checkpoint superseded: validator dependencies were removed. Use final LibMan cleanup and integrated browser verification.")

from pathlib import Path
import json, os
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
OUT=Path('docs/2026/10')
BASE='http://localhost:5187'
scripts=['/lib/jquery/jquery.min.js','/lib/jquery-migrate/jquery-migrate.min.js','/lib/jquery-validate/jquery.validate.min.js','/lib/jquery-validation-unobtrusive/jquery.validate.unobtrusive.min.js']
form='''<!doctype html><html lang="en"><head><title>Offline validation compatibility fixture</title></head><body><form id="validation-fixture" novalidate>
<label>Name<input name="Name" id="Name" data-val="true" data-val-required="Name required"></label><span data-valmsg-for="Name" data-valmsg-replace="true"></span>
<label>Email<input name="Email" id="Email" data-val="true" data-val-required="Email required" data-val-email="Email invalid"></label><span data-valmsg-for="Email" data-valmsg-replace="true"></span>
<label>Password<input name="Password" id="Password" data-val="true" data-val-required="Password required"></label>
<label>Confirm<input name="Confirm" id="Confirm" data-val="true" data-val-required="Confirmation required" data-val-equalto="Passwords must match" data-val-equalto-other="*.Password"></label><span data-valmsg-for="Confirm" data-valmsg-replace="true"></span>
<button type="button">No submission</button></form></body></html>'''
report={'base':BASE,'scripts':scripts,'external_network':'blocked','fixture':'isolated in-memory DOM; no form submission','checks':[],'page_errors':[],'asset_responses':[]}
with sync_playwright() as pw:
 cache=Path(os.environ['LOCALAPPDATA'])/'ms-playwright'
 candidates=list(cache.glob('chromium-*/chrome-win64/chrome.exe'))
 exe=Path(pw.chromium.executable_path)
 if not exe.exists() and candidates:exe=max(candidates,key=lambda p:int(p.relative_to(cache).parts[0].split('-')[-1]))
 browser=pw.chromium.launch(headless=True,executable_path=str(exe))
 report['browser']=browser.version
 context=browser.new_context()
 context.route('**/*',lambda r:r.continue_() if urlparse(r.request.url).hostname in ('localhost','127.0.0.1') or urlparse(r.request.url).scheme in ('about','blob','data') else r.abort())
 page=context.new_page();page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
 page.on('response',lambda r:report['asset_responses'].append({'url':r.url,'status':r.status}) if '/lib/' in r.url else None)
 page.goto(BASE+'/Contact');page.wait_for_load_state('networkidle')
 contact=page.evaluate('''() => ({forms:document.querySelectorAll('main form').length,submits:document.querySelectorAll('main input[type=submit],main button[type=submit]').length})''')
 report['checks'].append({'name':'public-contact-remains-disabled','passed':contact['forms']==0 and contact['submits']==0,'actual':contact})
 page.set_content(form)
 for script in scripts:page.add_script_tag(url=BASE+script)
 page.evaluate('''() => { $.validator.unobtrusive.parse(document); }''')
 versions=page.evaluate('''() => ({jquery:$.fn.jquery,migrate:$.migrateVersion,validation:$.validator.version,unobtrusive:typeof $.validator.unobtrusive.parse,compatibility:{isFunction:typeof $.isFunction,proxy:typeof $.proxy,parseJSON:typeof $.parseJSON}})''')
 versions['validation_file_header']=page.request.get(BASE+'/lib/jquery-validate/jquery.validate.js').text().splitlines()[1].strip(); report['versions']=versions
 report['checks'].append({'name':'unobtrusive-parse-and-legacy-api-compatibility','passed':versions['jquery']=='4.0.0' and versions['migrate']=='4.0.2' and versions['unobtrusive']=='function' and all(v=='function' for v in versions['compatibility'].values())})
 empty=page.evaluate('''() => ({valid:$('#validation-fixture').valid(),errors:$('#validation-fixture').validate().errorList.map(e=>({field:e.element.name,message:e.message}))})''')
 report['checks'].append({'name':'required-empty-fields-rejected','passed':not empty['valid'] and len(empty['errors'])==4,'actual':empty})
 page.locator('#Name').fill('Example');page.locator('#Email').fill('invalid-email');page.locator('#Password').fill('one');page.locator('#Confirm').fill('two')
 bad=page.evaluate('''() => ({valid:$('#validation-fixture').valid(),errors:$('#validation-fixture').validate().errorList.map(e=>({field:e.element.name,message:e.message}))})''')
 report['checks'].append({'name':'email-and-equalto-rejected','passed':not bad['valid'] and {e['field'] for e in bad['errors']}=={'Email','Confirm'},'actual':bad})
 page.locator('#Email').fill('example@example.com');page.locator('#Confirm').fill('one')
 valid=page.evaluate('''() => ({valid:$('#validation-fixture').valid(),errors:$('#validation-fixture').validate().errorList.map(e=>e.message)})''')
 report['checks'].append({'name':'valid-required-email-equalto-accepted','passed':valid['valid'] and not valid['errors'],'actual':valid})
 bootstrap=page.request.get(BASE+'/lib/bootstrap/css/bootstrap.min.css')
 icons=page.request.get(BASE+'/lib/bootstrap-icons/font/bootstrap-icons.min.css')
 font=page.request.get(BASE+'/lib/bootstrap-icons/font/fonts/bootstrap-icons.woff2')
 report['checks'].append({'name':'bootstrap-css-icons-and-font-local-assets','passed':bootstrap.status==200 and 'v5.3.8' in bootstrap.text() and icons.status==200 and 'bootstrap-icons' in icons.text() and font.status==200,'statuses':[bootstrap.status,icons.status,font.status]})
 report['checks'].append({'name':'no-javascript-errors','passed':not report['page_errors']})
 browser.close()
report['passed']=all(c['passed'] for c in report['checks'])
(OUT/'libman-validation-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['passed'] else 1)

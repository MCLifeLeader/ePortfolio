"""Compare compiled page content before/after the HTML indentation pass."""
import argparse
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
PAGES = ROOT / "Src/Portfolio_Core/Portfolio/Pages"
BASE = "http://localhost:5187"
routes = sorted("/" if p.stem == "Index" and p.parent == PAGES else "/" + p.relative_to(PAGES).with_suffix("").as_posix()
                for p in PAGES.rglob("*.cshtml") if p.read_text(encoding="utf-8-sig").lstrip().startswith("@page"))
parser = argparse.ArgumentParser()
parser.add_argument("--phase", choices=("before", "after"), required=True)
args = parser.parse_args()
baseline_path = OUT / "formatting-render-baseline.json"
baseline = json.loads(baseline_path.read_text(encoding="utf-8")) if args.phase == "after" else {}
checks = []
errors = []

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, executable_path=str(Path(os.environ["LOCALAPPDATA"]) / "ms-playwright/chromium-1234/chrome-win64/chrome.exe"))
    for width, theme in ((1440, "light"),) if args.phase == "before" else ((1440, "light"), (375, "dark")):
        context = browser.new_context(viewport={"width": width, "height": 900}, color_scheme=theme, reduced_motion="reduce")
        context.route("**/*", lambda route: route.continue_() if route.request.url.startswith(BASE) else route.abort())
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        for route in routes:
            response = page.goto(BASE + route, wait_until="networkidle")
            signature = page.evaluate("""() => {
                const main = document.querySelector('main');
                for (const p of main.querySelectorAll('p')) if (p.textContent.includes('Request ID:')) p.remove();
                const clean = value => value.replace(/\\s+/g, ' ').trim();
                return {text:clean(main.innerText || main.textContent),
                    headings:[...main.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h=>[h.tagName,clean(h.textContent)]),
                    anchors:[...document.querySelectorAll('a')].map(a=>[a.getAttribute('href'),clean(a.textContent)]),
                    ids:[...document.querySelectorAll('[id]')].map(n=>n.id),
                    images:[...main.querySelectorAll('img')].map(i=>[i.getAttribute('src'),i.alt,i.getAttribute('width'),i.getAttribute('height')])};
            }""")
            assert response.status == 200, route
            if args.phase == "before":
                baseline[route] = signature
            else:
                differences = [key for key in signature if signature[key] != baseline[route][key]]
                overflow = page.evaluate("document.documentElement.scrollWidth > innerWidth + 2")
                checks.append({"route": route, "width": width, "theme": theme, "content_differences": differences, "overflow": overflow})
        context.close()
    browser.close()

if args.phase == "before":
    baseline_path.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    print(f"Captured compiled pre-format signatures for {len(baseline)} pages.")
else:
    failures = [check for check in checks if check["content_differences"] or check["overflow"]]
    report = {"routes": len(routes), "cases": checks, "failures": failures, "javascript_errors": errors,
              "limitations": ["Chromium desktop/light and mobile/dark checks; external requests blocked.", "Request-ID diagnostic paragraphs are excluded because IDs change for each request."]}
    (OUT / "formatting-render-verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(routes), "cases": len(checks), "failures": failures, "javascript_errors": errors}))
    assert not failures and not errors

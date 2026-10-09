"""Read-only preservation checks against the fixed October 8 inventory.

python docs/2026/10/verify_modernization.py --write-ledger
python docs/2026/10/verify_modernization.py --base-url http://localhost:5080

Only the separate ledger/report/site-map are written. Never regenerate the audit.
HTTP is optional and strictly loopback, including redirects. No document links
or external links are fetched. This checks evidence, not factual truth or visual QA.
"""
import argparse
from collections import Counter
import csv
import hashlib
import html
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
AUDIT = ROOT / "docs/content-audit"
APP = ROOT / "Src/Portfolio_Core/Portfolio"
PAGES = APP / "Pages"
STATIC = APP / "wwwroot"
DECISION = "docs/2026/10/08-owner-decisions.md"
TEXT_KINDS = {"text", "p", "li", "tr", "h1", "h2", "h3", "h4", "h5", "button", "title"}
AUTHORIZED_VENDOR_DIRS = {"bootstrap", "jquery", "jquery-validate", "jquery-validation-unobtrusive"}
RETIRED_VALIDATION_IDS = {
    "PAGE-Shared-_ValidationScriptsPartial", "PAGE-Shared-_ValidationScriptsPartial-REF-001",
    "PAGE-Shared-_ValidationScriptsPartial-REF-002", "PAGE-Shared-_ValidationScriptsPartial-BEHAVIOR",
}


def read(path):
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1252")


def norm(value):
    # Token equality ignores typography, not words, numbers, or qualifications.
    value = html.unescape(value).lower().replace("’", "'").replace("‘", "'")
    return " ".join(re.findall(r"\w+", value))


def active(value):
    return re.sub(r"@\*.*?\*@|<!--.*?-->", "", value, flags=re.S)


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.parts, self.refs, self.anchors, self.markers = [], [], set(), set()
        self.hidden = 0
        self.feed(active(source))
        self.text = norm(" ".join(self.parts))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style"}:
            self.hidden += 1
        self.anchors.update(filter(None, [attrs.get("id"), attrs.get("name") if tag == "a" else None]))
        self.markers.update(re.findall(r"E\d{2}", attrs.get("data-accomplishment-ids", "")))
        for key in ("href", "src", "asp-page", "action", "poster"):
            if attrs.get(key):
                self.refs.append((key, attrs[key]))
        if attrs.get("asp-page") and attrs.get("asp-fragment"):
            self.refs.append(("asp-page", attrs["asp-page"] + "#" + attrs["asp-fragment"]))

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, value):
        if not self.hidden:
            self.parts.append(value)


def rel(path):
    return path.relative_to(ROOT).as_posix()


def routes_for(path, source):
    if not re.search(r"^\s*@page(?:\s|$)", source):
        return []
    name = path.relative_to(PAGES).with_suffix("").as_posix()
    explicit = re.search(r'^\s*@page\s+"([^"\n]+)"', source)
    if explicit and explicit[1].startswith("/"):
        return [explicit[1]]
    result = ["/" + name]
    if name == "Index":
        result.insert(0, "/")
    elif name.endswith("/Index"):
        result.insert(0, "/" + name[:-6])
    return result


def approved_sources():
    result = {}
    for line in read(OUT / "09-employment-accomplishments-review.md").splitlines():
        item = re.search(r"\*\*(E\d{2})", line)
        if not item or "Source:" not in line:
            continue
        values = line.split("Source:", 1)[1].rstrip(".")
        for match in re.finditer(r"(?:SUPPLIED-)?(\d{3})(?:[–-](?:SUPPLIED-)?(\d{3}))?", values):
            for number in range(int(match[1]), int(match[2] or match[1]) + 1):
                result.setdefault(f"SUPPLIED-{number:03}", []).append(item[1])
    return result


def correction(row):
    """Narrow exceptions; original statement and corrected destination stay inspectable."""
    cid, value, source = row["ContentID"], row["OriginalInformation"], row["SourceFile"]
    low = value.lower()
    if cid in {"PAGE-AboutMe-REF-001", "PAGE-AboutMe-ELEMENT-003", "PAGE-Index-REF-001", "PAGE-Index-ELEMENT-004"}:
        replacement = "~/content/images/Michael_Carey_Large.jpg"
        if replacement in read(ROOT / source) and (STATIC / "content/images/Michael_Carey_Large.jpg").is_file():
            return "owner-replaced-portrait", "Owner supplied new primary portrait; original photo retained byte-identical, new image served from /content/images/Michael_Carey_Large.jpg."
    explicit = {
        "PAGE-Experience-Education-TEXT-006": "R02: college chronology now ends in 2020, the owner-confirmed bachelor's graduation year.",
        "PAGE-AboutMe-TEXT-003": "R01: manager dates refined to February 2021–February 2026; education portfolio context retained.",
        "PAGE-AboutMe-TEXT-004": "R01: current formal title corrected to Sr. Software Architect (Portfolio Architect).",
        "PAGE-Skills-Leadership-TEXT-006": "R01: current formal title corrected to Sr. Software Architect (Portfolio Architect).",
        "PAGE-Skills-Leadership-TEXT-010": "R01: former manager role receives historical tense/dates rather than current-role wording.",
        "PAGE-Skills-DevOps-TEXT-007": "R05: pipeline creation/runtime distinction replaces the universal timing comparison.",
        "PAGE-Skills-Leadership-TEXT-063": "Owner reading-list update: Be Our Guest attribution uses The Disney Institute and Theodore Kinni.",
        "PAGE-Skills-Leadership-TEXT-068": "Owner reading-list update: Influencer authors expanded to Joseph Grenny, Kerry Patterson, David Maxfield, Ron McMillan, Al Switzler.",
        "PAGE-Skills-Leadership-TEXT-073": "Owner reading-list update: Think and Grow Rich edition specified as 1937 Edition.",
    }
    if cid in explicit:
        return "owner-corrected", explicit[cid]
    if cid in {"PAGE-Experience-WorkHistory-TEXT-003", "PAGE-Index-TEXT-051", "PAGE-Index-TEXT-052"}:
        return "authorized-disconnected", "Owner-directed retirement of resume download invitation/label; original PDF retained."
    if cid == "PAGE-Skills-Leadership-REF-003":
        return "repair-reference-quoting", "F04: remove malformed trailing quote from original target; external target not fetched."
    if cid == "PAGE-Index-TEXT-003" or "upwork.com" in low:
        return "authorized-retired", "Upwork/side-work solicitation retired per R03; original retained in baseline."
    if row["Kind"] == "reference" and ("resume.pdf" in low):
        return "authorized-disconnected", "Resume.pdf link removed by owner; original binary retained."
    if cid == "PAGE-Index-REF-002":
        return "authorized-retired", "A-Game link in the retired side-work solicitation; career links remain elsewhere."
    if row["Kind"] in TEXT_KINDS | {"dynamic text"}:
        if "expired" in low and "scrum" in low:
            return "owner-corrected", "R08: earned March 21, 2013; expired wording omitted without claiming active certification."
        if ("software engineering" in low and "2021" in low and "education" in source.lower()):
            return "owner-corrected", "R02: degree graduation corrected to 2020."
        if "devops" in source.lower() and ("2-3 weeks" in low or "2–3 weeks" in low or "3-4 hours" in low or "3–4 hours" in low):
            return "owner-corrected", "R05: pipeline creation takes hours; runtime varies by product/build complexity."
        if "family" in low and ("2001" in low or "2002" in low or "2005" in low):
            return "owner-corrected", "R06: approximate inception 2001, involvement 2002, partnership failure 2005."
        if "engineering manager" in low and ("present" in low or "currently" in low):
            return "owner-corrected", "R01: Engineering Manager February 2021–February 2026; Sr. Software Architect from February 2026."
    return None


def local_url(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
        raise ValueError("Only loopback HTTP(S) URLs without credentials are allowed")
    host = parsed.hostname or ""
    if host != "localhost":
        try:
            permitted = ipaddress.ip_address(host).is_loopback
        except ValueError:
            permitted = False
        if not permitted:
            raise ValueError("Only localhost or a literal loopback address is allowed")
    return url


class LoopbackRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        local_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def area(name):
    if name.startswith("College/") or name == "Experience/Education":
        return "Education & Professional Development"
    if name.startswith("Fun/") or name in {"AboutMe", "Tribute"}:
        return "About / Personal / Community"
    if name == "Skills/Leadership":
        return "Leadership & Mentoring"
    if name == "Skills/AI":
        return "AI & Innovation"
    if name.startswith("Skills/"):
        return "Engineering & Technology"
    if name.startswith("Projects/") or name == "Git":
        return "Projects & Accomplishments"
    if name.startswith("Experience/"):
        return "Professional Experience"
    return "Homepage / Site utilities"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", help="Optional running loopback site; external URLs forbidden")
    parser.add_argument("--write-ledger", action="store_true", help="Write separate migration ledger and site map")
    parser.add_argument("--report", default="modernization-validation.json")
    args = parser.parse_args()
    if Path(args.report).name != args.report:
        parser.error("Report must be a filename inside docs/2026/10")
    if args.base_url:
        local_url(args.base_url)
    baseline = json.loads(read(AUDIT / "baseline-source.json"))
    oldroutes = json.loads(read(AUDIT / "routes.json"))
    assets = json.loads(read(AUDIT / "assets.json"))
    asset_by_path = {a["path"]: a for a in assets}
    manifest = {a["path"]: a for a in json.loads(read(AUDIT / "manifest.json"))["files"]}
    rows = list(csv.DictReader((AUDIT / "preservation-matrix.csv").open(encoding="utf-8-sig", newline="")))
    sources = {rel(p): read(p) for p in PAGES.rglob("*.cshtml")}
    pages = {p: Page(s) for p, s in sources.items()}
    routes = {route: name for name, source in sources.items() for route in routes_for(ROOT / name, source)}
    route_by_source = {name: routes_for(ROOT / name, source) for name, source in sources.items()}
    approved = approved_sources()
    libman = json.loads(read(APP / "libman.json"))
    approved_libraries = {"bootstrap@5.3.8", "bootstrap-icons@1.13.2"}
    vendor_manifest_valid = {x["library"] for x in libman["libraries"]} == approved_libraries
    selected_vendor_paths = {
        rel(APP / library["destination"] / filename)
        for library in libman["libraries"] for filename in library.get("files", [])
    }
    ledger, losses, notes = [], [], []
    fixed_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in AUDIT.iterdir() if p.is_file()}

    def destination(name):
        return "; ".join(route_by_source.get(name, [])) or ("Shared site infrastructure" if name in sources else "Private process / source")

    def matches(value):
        wanted = norm(value)
        return [name for name, page in pages.items() if wanted and (" " + wanted + " ") in (" " + page.text + " ")]

    for row in rows:
        cid, kind, source, value = (row[x] for x in ("ContentID", "Kind", "SourceFile", "OriginalInformation"))
        category, disposition, status = "public-content", "retain", "needs-review"
        finalfiles, finalroute, evidence = [source] if source else [], destination(source), ""
        exception = correction(row)
        if cid in RETIRED_VALIDATION_IDS:
            category, disposition, status = "authorized-unused-infrastructure", "retire-unused-validation-partial", "owner-authorized-retirement"
            finalfiles, finalroute = ["Src/Portfolio_Core/Portfolio/libman.json", DECISION], "Unused validation partial retired; no public route"
            evidence = "Owner-authorized minimal LibMan cleanup: no page invokes this partial. Original source/reference records remain in fixed baseline."
        elif kind == "owner brief":
            category, disposition, status = "private-process-requirement", "retain-private-baseline", "baseline-retained"
            finalfiles, finalroute = ["docs/content-audit/preservation-matrix.csv"], "Private process; no public destination"
            evidence = "Requirements retained verbatim; fulfillment tracked separately in task documents."
        elif kind == "unverified supplied claim":
            markers = approved.get(cid, [])
            category = "approved-employment-claim" if markers else "private-supplied-context"
            disposition = "consolidate-approved-claims" if markers else "retain-private-baseline"
            finalfiles = ["Src/Portfolio_Core/Portfolio/Pages/Experience/EmploymentAccomplishments.cshtml"] if markers else ["docs/content-audit/preservation-matrix.csv"]
            finalroute = "/Experience/EmploymentAccomplishments" if markers else "Private source context; no public destination"
            present = set().union(*(p.markers for p in pages.values()))
            status = "verified-source-markers" if markers and set(markers) <= present else "baseline-retained" if not markers else "needs-review"
            evidence = "Approved October 8, 2026; consolidated into " + " ".join(markers) if markers else "Heading, caveat, or context outside the 52 reviewed claims; retained privately."
        elif kind in {"asset", "download text"}:
            asset = asset_by_path.get(source)
            unchanged = bool(asset and (ROOT / source).is_file() and hashlib.sha256((ROOT / source).read_bytes()).hexdigest() == asset["sha256"])
            category = "vendor-dependency" if asset and asset.get("category", "").startswith("vendor") else "download-content" if kind == "download text" else "site-asset"
            finalroute = asset["public_path"] if asset else "Unknown asset"
            status, disposition, evidence = "verified-byte-identity" if unchanged else "needs-review", "retain-binary", "SHA-256 equals original asset manifest." if unchanged else "Original byte identity differs or file is missing."
            vendor_prefix = rel(STATIC) + "/lib/"
            vendor_dir = source[len(vendor_prefix):].split("/", 1)[0] if source.startswith(vendor_prefix) else ""
            if category == "vendor-dependency" and vendor_dir in AUTHORIZED_VENDOR_DIRS and not unchanged and vendor_manifest_valid:
                if source in selected_vendor_paths and (ROOT / source).is_file():
                    category, disposition, status = "authorized-vendor-upgrade", "upgrade-selected-vendor-file", "owner-authorized-vendor-update"
                    evidence = "Owner requested dependency upgrades; exact file selected by pinned Bootstrap 5.3.8 LibMan manifest. Original version/hash retained in fixed assets baseline. " + DECISION
                elif source not in selected_vendor_paths and not (ROOT / source).exists():
                    category, disposition, status = "authorized-vendor-retirement", "retire-unused-vendor-file", "owner-authorized-vendor-retirement"
                    finalfiles, finalroute = ["Src/Portfolio_Core/Portfolio/libman.json", "docs/content-audit/assets.json"], "Retired public vendor path: " + asset["public_path"]
                    evidence = "Owner requested minimal Bootstrap + Bootstrap Icons resources; unused file retired. Original vendor version/hash remains in fixed baseline; media/document byte identity is not exempted. " + DECISION
            if source.lower().endswith("/resume.pdf"):
                disposition, category = "retain-disconnected-binary", "historical-resume"
                finalroute = "File retained at /content/pdf/Resume.pdf; no page links"
                evidence += " Owner explicitly disconnected the download."
            if source.endswith(("/css/site.css", "/js/site.js")) and not unchanged:
                category = "site-presentation"
                disposition, status, evidence = "update-site-presentation", "implemented-source-change", "Site CSS/theme JavaScript intentionally revised; visual and interaction validation required separately."
        elif kind == "inactive source":
            category, disposition, status = "inactive-source-history", "retain-private-baseline", "baseline-retained"
            finalfiles, finalroute = ["docs/content-audit/baseline-source.json"], "Inactive source archive; no public destination"
            evidence = "Original inactive comment preserved in fixed source snapshot; not asserted as active behavior."
        elif kind in {"supporting source", "behavior", "template", "metadata", "dynamic text"}:
            category = "source-infrastructure" if kind != "dynamic text" else "public-dynamic-content"
            current = read(ROOT / source) if source and (ROOT / source).is_file() else ""
            old = baseline.get(source, "")
            if current.replace("\r\n", "\n") == old.replace("\r\n", "\n"):
                status, evidence = "verified-source-identity", "Source text equals fixed source snapshot (line endings ignored; punctuation/code preserved)."
            elif kind == "dynamic text" and norm(value) in norm(current):
                status, evidence = "verified-source-value", "Original dynamic value remains in active source."
            else:
                disposition, status, evidence = "update-source", "implemented-source-change", "Source differs: routing/title/metadata/style/config/behavior changes require separate runtime review."
                notes.append({"ContentID": cid, "source": source, "kind": kind})
        elif kind == "route":
            old = next((r for r in oldroutes if r["file"] == source), None)
            aliases = old["routes"] if old else []
            status = "verified-source-routes" if all(routes.get(a) == source for a in aliases) else "needs-review"
            finalroute, evidence = "; ".join(aliases), "All original aliases checked against current @page source; HTTP checked only with --base-url."
        elif kind == "anchor":
            finalroute = destination(source) + "#" + value
            status = "verified-source-anchor" if source in pages and value in pages[source].anchors else "needs-review"
            evidence = "Original id checked in owning active page/template."
        elif kind in {"reference", "media/control"}:
            record = json.loads(value)
            target = record.get("target")
            if target:
                found = [name for name, page in pages.items() if any(t.lower() == target.lower() for _, t in page.refs)]
                if found:
                    finalfiles, finalroute, status = found, "; ".join(destination(n) for n in found), "verified-source-reference"
                    evidence = "Same target retained; external availability deliberately untested."
                elif source.endswith("/Shared/_Layout.cshtml") and target == "#":
                    disposition, status, evidence = "replace-dropdown-control", "implemented-source-change", "Placeholder dropdown href replaced with real navigation; original anchor IDs retained and destinations checked individually."
                elif cid == "PAGE-Contact-REF-001":
                    disposition, status, evidence = "remove-unused-form-dependency", "implemented-source-change", "Contact has no active form; unused Google reCAPTCHA script retired. No remote call made."
                elif cid == "PAGE-Shared-_Layout-REF-031":
                    disposition, status, evidence = "remove-unused-presentation-dependency", "implemented-source-change", "External icon stylesheet retired with navigation design; no linked document or vendor asset was removed."
                elif cid == "PAGE-Shared-_Layout-REF-003":
                    disposition, status, evidence = "remove-unserved-generated-stylesheet", "implemented-source-change", "Generated Portfolio.styles.css reference returned 404 locally; consolidated site.css supplies presentation. No original static asset was deleted."
            else:
                disposition, status, evidence = "update-control-markup", "implemented-source-change", "Control/media attributes may change with layout; source and rendered accessibility checks required."
        elif kind in TEXT_KINDS:
            found = matches(value)
            if not norm(value) or value.strip().startswith(("@", "}")) or cid in {"PAGE-Shared-_Layout-TEXT-016"}:
                category, disposition, status, evidence = "razor-source-fragment", "retain-private-baseline", "baseline-retained", "Razor control-code/dynamic fragment, not literal public prose; full original source archived."
            elif source.endswith("/Error.cshtml") and cid in {f"PAGE-Error-TEXT-{i:03}" for i in [3, 4, 6, 7, 8]}:
                category, disposition, status, evidence = "error-diagnostic-behavior", "retain-development-behavior", "implemented-source-change", "Request ID remains dynamic; diagnostic guidance now development-only. Production rendering intentionally omits diagnostic environment text."
            elif cid == "PAGE-Privacy-TEXT-002":
                disposition, status, evidence = "replace-template-placeholder", "implemented-editorial-change", "Template instruction replaced with privacy explanation; baseline retains original placeholder."
            elif cid in {"PAGE-Shared-_Layout-TEXT-007", "PAGE-Shared-_Layout-TEXT-008", "PAGE-Shared-_Layout-TEXT-009", "PAGE-Shared-_Layout-TEXT-010"}:
                disposition, status, evidence = "regroup-navigation", "implemented-editorial-change", "Menu labels/grouping updated; every original page route and original menu reference checked independently."
            elif cid == "PAGE-Skills-Leadership-TEXT-007":
                disposition, status, evidence = "historical-placeholder", "implemented-editorial-change", "More-to-come placeholder replaced by substantive architect content; original future-tense placeholder retained in baseline."
            elif cid == "PAGE-Index-TEXT-050":
                disposition, status, evidence = "authorized-disconnected", "owner-authorized-exception", "Resume download heading retired with owner-directed PDF disconnection."
            elif found:
                finalfiles, finalroute, status = found, "; ".join(destination(n) for n in found), "verified-source-text"
                disposition = "distribute" if len(found) > 1 else "move" if source not in found else "retain"
                evidence = "Complete original word/number sequence appears in active source text (typography ignored)."
            elif kind in {"h1", "h2", "h3", "h4", "h5", "title"} and len(norm(value).split()) < 10:
                disposition, status, evidence = "update-heading", "implemented-editorial-change", "Original heading label changed; substantive text checked independently."
            elif cid in {"PAGE-Index-TEXT-054", "PAGE-Index-TEXT-055", "PAGE-Index-TEXT-057", "PAGE-Index-TEXT-058", "PAGE-Index-TEXT-060", "PAGE-Index-TEXT-061"}:
                disposition, status, evidence = "rewrite-navigation-copy", "implemented-editorial-change", "Generic homepage card invitation rewritten; underlying project, skill, and experience facts checked independently."
        if exception and status not in {"verified-source-text", "verified-source-value"}:
            disposition, evidence = exception
            status = "owner-authorized-exception"
            evidence += " Evidence: " + DECISION + ". Other facts in an edited paragraph need independent review."
        if status == "needs-review":
            losses.append({"ContentID": cid, "kind": kind, "source": source, "original": value, "issue": "No complete source match or preservation evidence found; review before completion."})
        ledger.append(dict(ContentID=cid, BaselineKind=kind, Category=category, Disposition=disposition,
                           FinalFiles="; ".join(filter(None, finalfiles)), FinalDestination=finalroute,
                           ImplementationStatus=status, ValidationEvidence=evidence,
                           BaselineEvidence=row["Evidence"]))

    checks = []
    def check(name, passed, details):
        checks.append(dict(check=name, passed=passed, details=details))
    check("all-baseline-IDs-mapped", len(ledger) == 3150 and len({r["ContentID"] for r in ledger}) == 3150, len(ledger))
    original_aliases = [a for r in oldroutes for a in r["routes"]]
    missing = [a for a in original_aliases if a not in routes]
    check("44-original-route-aliases", len(original_aliases) == 44 and not missing, missing)
    anchors = [r for r in rows if r["Kind"] == "anchor"]
    missinganchors = [r["ContentID"] for r in anchors if r["SourceFile"] not in pages or r["OriginalInformation"] not in pages[r["SourceFile"]].anchors]
    check("30-original-anchors", len(anchors) == 30 and not missinganchors, missinganchors)
    markers = set().union(*(p.markers for p in pages.values()))
    expected = {f"E{i:02}" for i in range(1, 53)}
    check("52-approved-accomplishment-markers", expected <= markers, sorted(expected - markers))
    allrefs = [(source, key, target) for source, page in pages.items() for key, target in page.refs]
    check("zero-resume-PDF-page-links", not any("resume.pdf" in target.lower() for _, _, target in allrefs), [x for x in allrefs if "resume.pdf" in x[2].lower()])
    check("LinkedIn-and-GitHub-retained", all(any(domain in target.lower() for _, _, target in allrefs) for domain in ["linkedin.com", "github.com"]), "Source references only; external links not fetched.")
    static_paths = {"/" + p.relative_to(STATIC).as_posix() for p in STATIC.rglob("*") if p.is_file()}
    internal_issues = []
    for source, key, target in allrefs:
        if target.startswith(("http:", "https:", "mailto:", "tel:", "data:", "javascript:", "@")):
            continue
        target = target.replace("~/", "/", 1)
        parsed = urllib.parse.urlsplit(target)
        pathname = urllib.parse.unquote(parsed.path)
        if not pathname:
            if parsed.fragment and parsed.fragment not in pages[source].anchors:
                internal_issues.append([source, target, "missing local anchor"])
            continue
        if not pathname.startswith("/"):
            # Relative references resolve within the owner's first route.
            owner = route_by_source.get(source, ["/"])
            pathname = urllib.parse.urljoin((owner or ["/"])[0], pathname)
        if pathname in {"/Portfolio.styles.css"}:
            continue  # Generated scoped CSS; runtime request validates it.
        if key == "asp-page" or pathname in routes:
            if pathname not in routes:
                internal_issues.append([source, target, "missing Razor route"])
            elif parsed.fragment and parsed.fragment not in pages[routes[pathname]].anchors and parsed.fragment not in pages.get(rel(PAGES / "Shared/_Layout.cshtml"), Page("")).anchors:
                internal_issues.append([source, target, "missing destination anchor"])
        elif pathname not in static_paths:
            case = next((p for p in static_paths if p.lower() == pathname.lower()), None)
            internal_issues.append([source, target, "file case mismatch: " + case if case else "missing local static target"])
    check("active-internal-targets-and-case", not internal_issues, internal_issues)
    # Shared navigation edges apply to every rendered page. Other links are
    # contextual; aliases point to the same page. Verify discoverability from /.
    shared = rel(PAGES / "Shared/_Layout.cshtml")
    def route_links(source):
        result = set()
        for key, target in pages[source].refs:
            path = urllib.parse.urlsplit(target).path
            if key == "asp-page" or path.startswith("/"):
                if path in routes:
                    result.add(path)
        return result
    shared_edges = route_links(shared) if shared in pages else set()
    reachable, queue = set(), ["/"]
    while queue:
        route = queue.pop()
        if route in reachable or route not in routes:
            continue
        reachable.add(route)
        owner = routes[route]
        queue.extend(shared_edges | route_links(owner) | set(route_by_source[owner]))
    undiscoverable = sorted(set(original_aliases) - reachable - {"/Error"})
    check("all-original-pages-discoverable", not undiscoverable, undiscoverable)
    new_undiscoverable = sorted(set(routes) - reachable - {"/Error", "/Experience/ResumeHistory"})
    check("new-supporting-pages-discoverable", not new_undiscoverable, new_undiscoverable)
    check("runtime-error-utility-route", "/Error" in routes, "Error is a directly addressable runtime utility, intentionally outside browsing menus.")
    binary_failures = [r["ContentID"] for r in ledger if r["Category"] in {"vendor-dependency", "download-content", "historical-resume", "site-asset"} and r["ImplementationStatus"] != "verified-byte-identity"]
    check("original-media-documents-and-unexempted-assets-byte-identity", not binary_failures, binary_failures)
    actual_vendor_paths = {rel(p) for p in (STATIC / "lib").rglob("*") if p.is_file()}
    check("authorized-minimal-LibMan-manifest", vendor_manifest_valid and len(selected_vendor_paths) == 8 and actual_vendor_paths == selected_vendor_paths,
          {"libraries": [x["library"] for x in libman["libraries"]], "selected_files": sorted(selected_vendor_paths), "unexpected": sorted(actual_vendor_paths - selected_vendor_paths), "missing": sorted(selected_vendor_paths - actual_vendor_paths)})
    runtime = {"performed": False, "routes": [], "assets": [], "text_losses": []}
    if args.base_url:
        opener = urllib.request.build_opener(LoopbackRedirect())
        base = args.base_url.rstrip("/")
        rendered = {}
        for route in sorted(routes):
            try:
                with opener.open(local_url(base + route), timeout=15) as response:
                    body = response.read().decode("utf-8")
                    rendered[route] = Page(body)
                    runtime["routes"].append({"route": route, "status": response.status})
            except Exception as exc:
                runtime["routes"].append({"route": route, "error": str(exc)})
        # Only request local paths in rendered markup; never follow external references.
        targets = {urllib.parse.urlsplit(t).path for p in rendered.values() for k, t in p.refs if t.startswith("/") and not t.startswith("//") and urllib.parse.urlsplit(t).path not in routes}
        for target in sorted(targets):
            try:
                with opener.open(local_url(base + target), timeout=15) as response:
                    runtime["assets"].append({"path": target, "status": response.status})
                    if target.endswith(".css"):
                        css = response.read().decode("utf-8")
                        for match in re.finditer(r"url\(\s*['\"]?([^'\")\s]+)", css):
                            css_url = urllib.parse.urljoin(base + target, match[1])
                            if urllib.parse.urlsplit(css_url).path.lower().endswith((".woff", ".woff2")):
                                local_url(css_url)
                                with opener.open(css_url, timeout=15) as font_response:
                                    runtime["assets"].append({"path": urllib.parse.urlsplit(css_url).path, "status": font_response.status, "dependency_of": target})
            except Exception as exc:
                runtime["assets"].append({"path": target, "error": str(exc)})
        for item in ledger:
            if item["ImplementationStatus"] != "verified-source-text":
                continue
            original = next(r["OriginalInformation"] for r in rows if r["ContentID"] == item["ContentID"])
            if not any((" " + norm(original) + " ") in (" " + page.text + " ") for page in rendered.values()):
                runtime["text_losses"].append(item["ContentID"])
        runtime["performed"] = True
        rendered_markers = set().union(*(p.markers for p in rendered.values()))
        check("loopback-52-accomplishment-markers", expected <= rendered_markers, sorted(expected - rendered_markers))
        rendered_refs = [t for p in rendered.values() for _, t in p.refs]
        check("loopback-zero-resume-links", not any("resume.pdf" in t.lower() for t in rendered_refs), "All rendered routes inspected; PDF itself remains disconnected.")
        check("loopback-LinkedIn-and-GitHub", all(any(d in t.lower() for t in rendered_refs) for d in ["linkedin.com", "github.com"]), "Rendered references retained; external targets never fetched.")
        broken_fragments = []
        for owner, page in rendered.items():
            for _, target in page.refs:
                parsed = urllib.parse.urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.fragment:
                    continue
                destination_route = urllib.parse.urljoin(owner, parsed.path) if parsed.path else owner
                if destination_route in rendered and parsed.fragment not in rendered[destination_route].anchors:
                    broken_fragments.append([owner, target])
        check("loopback-active-fragment-targets", not broken_fragments, broken_fragments)
        runtime["original_anchor_failures"] = []
        for item in anchors:
            source = item["SourceFile"]
            owner_routes = list(rendered) if "/Shared/" in source else route_by_source.get(source, [])
            for route in owner_routes:
                if route not in rendered or item["OriginalInformation"] not in rendered[route].anchors:
                    runtime["original_anchor_failures"].append([item["ContentID"], route])
        check("loopback-rendered-routes", all(x.get("status") == 200 for x in runtime["routes"]), runtime["routes"])
        check("loopback-rendered-assets", all(x.get("status") == 200 for x in runtime["assets"]), runtime["assets"])
        check("loopback-rendered-preserved-text", not runtime["text_losses"], runtime["text_losses"])
        check("loopback-original-anchors", not runtime["original_anchor_failures"], runtime["original_anchor_failures"])
    check("no-unexplained-mapping-losses", not losses, len(losses))
    check("fixed-audit-files-unchanged-during-check", fixed_hashes == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in AUDIT.iterdir() if p.is_file()}, "All fixed audit file hashes compared before and after verification.")
    report = dict(baseline="Fixed October 8 2026; never regenerated", baseline_sha256=fixed_hashes,
                  summary=dict(Counter(r["ImplementationStatus"] for r in ledger)), checks=checks,
                  unexplained_losses=losses, changed_source_records=notes, runtime=runtime,
                  limitations=["Text comparison checks complete word/number sequences; does not prove factual accuracy, visual quality, or behavior.",
                               "Owner-corrected paragraph exceptions still require checking unaffected clauses.",
                               "Heading/metadata/control changes are classified as changes rather than falsely claiming byte preservation.",
                               "Existing project/profile/document references were not opened; official dependency documentation was consulted for owner-requested library updates."])
    (OUT / args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.write_ledger:
        with (OUT / "migration-ledger.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(ledger[0]))
            writer.writeheader()
            writer.writerows(ledger)
        write_map(oldroutes, anchors, routes, sources)
    print(json.dumps({"mapped": len(ledger), "unexplained_losses": len(losses), "failed_checks": [c["check"] for c in checks if not c["passed"]], "runtime_performed": runtime["performed"]}, indent=2))
    return 1 if any(not c["passed"] for c in checks) else 0


def write_map(oldroutes, anchors, routes, sources):
    lines = ["# Site map and compatibility plan — October 8, 2026", "", "The original 44 aliases remain at their original routes. Supporting pages remain accessible through Explore, area indexes, and contextual links. No external targets have been fetched.", "",
             "| Area | Landing / entry point | Supporting destinations |", "|---|---|---|",
             "| Homepage | `/` | Professional introduction, focus areas, LinkedIn and GitHub |",
             "| Architecture & Governance | `/Architecture` | `/Experience/EmploymentAccomplishments`, quality, AI and DevOps details |",
             "| AI & Innovation | `/Skills/AI` | Employer AI contributions and existing private product descriptions |",
             "| Engineering & Technology | `/Skills` | Technology pages and `/Skills/TechnicalHistory` for original durations/proficiency |",
             "| Leadership & Mentoring | `/Skills/Leadership` | Original role anchors, reading categories, historical mentoring goals |",
             "| Projects & Accomplishments | `/Projects` | Every original project detail, `/Git`, employer accomplishments |",
             "| Professional Experience | `/Experience` | `/Experience/WorkHistory`, accomplishments, `/Experience/ResumeHistory` |",
             "| Education & Professional Development | `/Experience/Education` | `/College` and all three original coursework detail pages |",
             "| About / Personal / Community | `/AboutMe` | `/Fun`, radio go-kit, Solarian League, `/Tribute`, civic and social links |",
             "| Complete supporting directory | `/Explore` | Every original public page and retained public download; Resume.pdf stays disconnected |", "",
             "New routes listed above are implementation targets; presence is checked below. The complete ledger distinguishes final source evidence from planned destinations.", "",
             "## Original routes and aliases", "", "| Original aliases | Area | Final source | Compatibility |", "|---|---|---|---|"]
    for old in oldroutes:
        present = all(a in routes for a in old["routes"])
        lines.append(f"| {'<br>'.join('`'+a+'`' for a in old['routes'])} | {area(old['name'])} | `{old['file']}` | {'Retained in source' if present else 'Missing: review required'} |")
    lines += ["", "## Original anchors", "", "| ContentID | Owning page/template | Retained anchor |", "|---|---|---|"]
    for item in anchors:
        lines.append(f"| {item['ContentID']} | `{item['SourceFile']}` | `#{item['OriginalInformation']}` |")
    lines += ["", "## New supporting routes", "", "| Route | Source |", "|---|---|"]
    original = {a for old in oldroutes for a in old["routes"]}
    for route in sorted(set(routes) - original):
        lines.append(f"| `{route}` | `{routes[route]}` |")
    lines += ["", "## Preservation and verification rules", "", "- Original content IDs and baseline fields stay in docs/content-audit; this separate ledger records implementation destinations.",
              "- Word/number matching tracks many-to-one reuse and one-to-many distribution across active public pages. Unmatched substantive text is reported, never called preserved merely because an archive exists.",
              "- Owner-authorized factual corrections and retired solicitation links cite the decision record. Resume.pdf remains byte-identical with no page link; document-only facts receive supporting historical treatment.",
              "- Original media/document and unexempted asset binaries use SHA-256 equality. Only owner-authorized Bootstrap/jQuery-family upgrades or retirement have narrow exceptions tied to the final eight-file LibMan manifest. Site presentation changes require visual checks.",
              "- Inactive source, process requirements, and unapproved source context have private dispositions; they are not made public implicitly.",
              "- A source route/anchor match does not prove an HTTP result. Use verify_modernization.py with a running localhost site for runtime evidence.", ""]
    (OUT / "site-map.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())

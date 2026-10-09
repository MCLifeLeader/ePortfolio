"""Reproduce the local content audit without fetching any URLs or changing the site.

Run from the repository root: python docs/content-audit/build_inventory.py
Requires the already available pypdf package for local PDF text inspection.
"""
import csv
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/content-audit"
APP = ROOT / "Src/Portfolio_Core/Portfolio"
PAGES = APP / "Pages"
STATIC = APP / "wwwroot"
ATTACHMENTS = [
    ("BRIEF", Path("C:/Users/MichaelBCarey/.codex/attachments/a11ae667-c6a3-44b0-bd86-05f21f3e8dc1/Pasted text.txt")),
    ("SUPPLIED", Path("C:/Users/MichaelBCarey/.codex/attachments/2a66dfda-5f14-40c3-8d73-36b2fe37a4fb/Pasted text.txt")),
]


def rel(path):
    return path.relative_to(ROOT).as_posix()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(text):
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def read_source(path):
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        # Tribute contains legacy Windows punctuation; retain its byte hash.
        return path.read_text(encoding="cp1252")


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", "<br>")


def section_for(name):
    if name.startswith("College/") or name == "Experience/Education":
        return "Education & Professional Development"
    if name.startswith("Fun/") or name in ("AboutMe", "Tribute"):
        return "About / Personal / Community"
    if name == "Experience/WorkHistory" or name == "Experience/Index":
        return "Professional Experience"
    if name == "Skills/Leadership":
        return "Leadership & Mentoring"
    if name == "Skills/AI":
        return "AI & Innovation"
    if name.startswith("Skills/"):
        return "Engineering & Technology"
    if name.startswith("Projects/") or name == "Git":
        return "Projects & Accomplishments"
    if name == "Index":
        return "Homepage"
    if name == "Contact":
        return "Professional connections / Contact"
    return "Shared site infrastructure / " + name


rows = []


def add(cid, kind, location, information, proposed, evidence, change="retain", verification="preserved", notes="", source=""):
    rows.append(dict(ContentID=cid, Kind=kind, OriginalLocation=location,
                     OriginalInformation=information, ProposedLocation=proposed,
                     ChangeType=change, Evidence=evidence, Verification=verification,
                     Notes=notes, SourceFile=source))


class ContentParser(HTMLParser):
    """Group all text nodes by semantic container, retaining nested list items.

    No HTML is executed. Full source snapshots retain Razor syntax, comments,
    original whitespace, and any material outside semantic containers.
    """
    void = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    containers = {"p", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "button", "label", "title"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.blocks = []
        self.refs = []
        self.anchors = []
        self.metadata = []
        self.attrs = []
        self.heading = "Introduction"
        self.covered = 0

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        attr = dict(attrs)
        block = None
        if tag in self.containers:
            block = dict(tag=tag, line=line, parts=[], heading=self.heading)
            self.blocks.append(block)
        self.attrs.append(dict(tag=tag, line=line, attributes=attr))
        for key in ("href", "src", "asp-page", "action", "poster", "srcset"):
            if attr.get(key):
                self.refs.append(dict(line=line, tag=tag, attribute=key, target=attr[key], attributes=attr))
        if attr.get("id"):
            self.anchors.append(dict(line=line, id=attr["id"]))
        if tag == "meta":
            self.metadata.append(dict(line=line, attributes=attr))
        if tag not in self.void:
            self.stack.append((tag, block))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.void:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                block = self.stack[i][1]
                if block and re.fullmatch(r"h[1-6]", tag):
                    value = normalize(" ".join(block["parts"]))
                    if value and not value.startswith("@"):
                        self.heading = value
                        block["heading"] = value
                del self.stack[i:]
                break

    def handle_data(self, data):
        if any(t in ("script", "style") for t, _ in self.stack):
            return
        if not normalize(data):
            return
        self.covered += len(normalize(data))
        # A table row stays whole so years and technologies remain associated.
        block = next((b for t, b in self.stack if t == "tr"), None)
        if block is None:
            block = next((b for _, b in reversed(self.stack) if b), None)
        if block is None:
            block = dict(tag="text", line=self.getpos()[0], parts=[], heading=self.heading)
            self.blocks.append(block)
        block["parts"].append(data)


tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
tracked = sorted(p for p in tracked if p and not p.startswith("docs/content-audit/"))
commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
initial_status = subprocess.check_output(["git", "status", "--short", "--untracked-files=no"], cwd=ROOT).decode().strip()
manifest = []
snapshots = {}
for name in tracked:
    path = ROOT / name
    if not path.is_file():
        continue
    entry = dict(path=name, bytes=path.stat().st_size, sha256=digest(path))
    manifest.append(entry)
    try:
        snapshots[name] = path.read_text(encoding="utf-8-sig")
    except UnicodeError:
        if path.suffix.lower() in (".cshtml", ".cs", ".css", ".js", ".txt", ".md", ".json", ".yml", ".xml", ".csproj"):
            snapshots[name] = read_source(path)

routes = []
page_details = []
for path in sorted(PAGES.rglob("*.cshtml")):
    source = read_source(path)
    name = path.relative_to(PAGES).as_posix().removesuffix(".cshtml")
    cid = "PAGE-" + name.replace("/", "-")
    aliases = []
    if re.search(r"^@page\b", source, re.M):
        aliases = ["/" + name]
        if name == "Index":
            aliases.insert(0, "/")
        elif name.endswith("/Index"):
            aliases.insert(0, "/" + name.removesuffix("/Index"))
        custom = re.search(r'^@page\s+"([^"]+)"', source, re.M)
        if custom:
            aliases = [custom.group(1)]
    location = aliases[0] if aliases else "Shared template: " + name
    title = re.search(r'ViewData\["Title"\]\s*=\s*"([^"]+)"', source)
    area = section_for(name)
    destination = area + " > " + (title.group(1) if title else name)
    add(cid, "route" if aliases else "template", location, "Aliases: " + ", ".join(aliases) if aliases else name,
        destination + "; keep existing route(s)" if aliases else destination,
        rel(path), source=rel(path), notes="Source-derived routing; no HTTP request performed.")
    for j, match in enumerate(re.finditer(r'ViewData\["(Title|Message)"\]\s*=\s*"([^"]*)"', source), 1):
        line = source[:match.start()].count("\n") + 1
        add(f"{cid}-VALUE-{j:03}", "dynamic text", f"{location}; line {line}", match.group(2),
            destination + "; retain displayed " + match.group(1), f"{rel(path)}:{line}", source=rel(path))
    comments = list(re.finditer(r"@\*.*?\*@|<!--.*?-->", source, re.S))
    for i, match in enumerate(comments, 1):
        line = source[:match.start()].count("\n") + 1
        add(f"{cid}-COMMENT-{i:03}", "inactive source", f"{location}; line {line}", match.group(),
            "Source archive only; review before restoring to public page", f"{rel(path)}:{line}",
            notes="Commented content is not currently rendered; historical text retained separately.", source=rel(path))
    clean = re.sub(r"@\*.*?\*@|<!--.*?-->", lambda m: "\n" * m.group().count("\n"), source, flags=re.S)
    first_tag = clean.find("<")
    if first_tag >= 0:
        clean = "\n" * clean[:first_tag].count("\n") + clean[first_tag:]
    parser = ContentParser()
    parser.feed(clean)
    for i, block in enumerate(parser.blocks, 1):
        text = normalize(" ".join(block["parts"]))
        if not text:
            continue
        line = block["line"]
        proposed = destination + " > " + block["heading"]
        change = "retain"
        if name == "Index" and ("part-time" in text or "availability" in text):
            proposed = "About / Personal / Community > Entrepreneurial work and availability"
            change = "relocate"
        elif name == "Index" and ("community" in text or "government" in text):
            proposed = "About / Personal / Community > Civic engagement"
            change = "relocate"
        elif name == "Index" and (block["tag"] == "tr" or block["heading"] in ("Technical Experience", "Technologies and Skills:")):
            proposed = "Engineering & Technology > Historical experience and skill levels"
            change = "relocate"
        review = "preserved"
        note = "Baseline captured; destination proposed, migration not implemented."
        if name in ("AboutMe", "Experience/WorkHistory", "Skills/Leadership") and ("2026" in text or "Present" in text or "currently serve" in text):
            review = "needs review"
            note += " See owner review R01 (role transition/title/date conflict)."
        if name == "Index" and block["tag"] == "tr":
            review = "needs review"
            note += " See R03: preserve recorded duration; do not increase it automatically."
        if name == "Skills/AI" and ("private" in text or "technologies I am currently" in text):
            review = "needs review"
            note += " See R04: private product claims need scope/disclosure confirmation."
        if name == "Experience/Education" and "2021" in text:
            review = "needs review"
            note += " See R02: degree completion conflicts with historical resume."
        if "Family Key" in text or (name == "Projects/FamilyKey" and "2002" in text):
            review = "needs review"
            note += " See R06: distinguish project inception from owner's involvement."
        if name.startswith("Projects/") and any(v in text for v in ("under development", "ongoing project", "future plans", "As of this writing", "currently recommend")):
            review = "needs review"
            note += " See R07: time-sensitive historical status must not become a current claim."
        if name == "Projects/AzureServices" and "seconds" in text:
            review = "needs review"
            note += " See R05: retain reported measurement and scope without extrapolation."
        add(f"{cid}-TEXT-{i:03}", block["tag"], f"{location}; {block['heading']}; line {line}", text,
            proposed, f"{rel(path)}:{line}", change, review, note, rel(path))
    for i, ref in enumerate(parser.refs, 1):
        add(f"{cid}-REF-{i:03}", "reference", f"{location}; line {ref['line']}", json.dumps(ref, ensure_ascii=False),
            destination + "; retain reference with owning content", f"{rel(path)}:{ref['line']}",
            notes="Recorded only; target not opened or validated, per user instruction.", source=rel(path))
    for i, anchor in enumerate(parser.anchors, 1):
        add(f"{cid}-ANCHOR-{i:03}", "anchor", f"{location}#{anchor['id']}", anchor["id"],
            f"Retain {location}#{anchor['id']} with associated section", f"{rel(path)}:{anchor['line']}", source=rel(path))
    for i, meta in enumerate(parser.metadata, 1):
        add(f"{cid}-META-{i:03}", "metadata", f"{location}; line {meta['line']}", json.dumps(meta["attributes"], ensure_ascii=False),
            "Shared layout metadata; preserve baseline and review wording during revision", f"{rel(path)}:{meta['line']}", source=rel(path))
    for i, attr in enumerate(parser.attrs, 1):
        if attr["tag"] in ("img", "input", "video", "audio", "iframe", "button"):
            add(f"{cid}-ELEMENT-{i:03}", "media/control", f"{location}; line {attr['line']}", json.dumps(attr, ensure_ascii=False),
                destination + "; retain media/control semantics", f"{rel(path)}:{attr['line']}", source=rel(path))
    # Inline script/conditional Razor logic is retained exactly, not presented as visible prose.
    if "<script" in source or "@if" in source or 'ViewData["Message"]' in source:
        add(cid + "-BEHAVIOR", "behavior", location, "Full Razor source captured in baseline-source.json",
            destination + "; retain existing behavior subject to documented defect review", rel(path), source=rel(path))
    info = dict(id=cid, file=rel(path), name=name, routes=aliases,
                title=title.group(1) if title else name, destination=destination,
                blocks=len([b for b in parser.blocks if normalize(" ".join(b["parts"]))]),
                references=parser.refs, anchors=parser.anchors, visible_characters=parser.covered)
    page_details.append(info)
    if aliases:
        routes.append(info)

# Every text source supporting route behavior, styles, build, and deployment is captured.
for i, (name, text) in enumerate(sorted(snapshots.items()), 1):
    if name.endswith(".cshtml"):
        continue
    add(f"SOURCE-{i:03}", "supporting source", name, "Exact source in baseline-source.json; SHA-256 in manifest.json",
        "Retain current file and behavior; document any later changes separately", name, source=name)
    for j, match in enumerate(re.finditer(r'ViewData\["(Title|Message)"\]\s*=\s*"([^"]*)"', text), 1):
        line = text[:match.start()].count("\n") + 1
        add(f"SOURCE-{i:03}-VALUE-{j:03}", "dynamic text", f"{name}:{line}", match.group(2),
            "Retain displayed " + match.group(1) + " with owning page", f"{name}:{line}", source=name)

extracts = {}
assets = []
from pypdf import PdfReader
for i, path in enumerate(sorted(p for p in STATIC.rglob("*") if p.is_file()), 1):
    cid = f"ASSET-{i:03}"
    uri = "/" + path.relative_to(STATIC).as_posix()
    incoming = [f"{info['routes'][0] if info['routes'] else info['name']}:{ref['line']}" for info in page_details
                for ref in info["references"] if ref["target"].removeprefix("~").split("?")[0].split("#")[0].lower() == uri.lower()]
    asset = dict(id=cid, path=rel(path), public_path=uri, bytes=path.stat().st_size,
                 sha256=digest(path), incoming=incoming, tracked=rel(path) in tracked,
                 category="vendor dependency" if path.relative_to(STATIC).parts[0] == "lib" else "site asset")
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        extracts[rel(path)] = dict(type="pdf", pages=pages, metadata=str(reader.metadata))
        asset["pages"] = len(pages)
        for number, text in enumerate(pages, 1):
            add(f"{cid}-PAGE-{number:03}", "download text", f"{uri}; PDF page {number}", text,
                f"Keep complete original download at {uri}; supporting content remains in document", f"{rel(path)}; page {number}",
                verification="needs review" if path.name == "Resume.pdf" else "preserved",
                notes="Text extracted locally; original binary retained. Layout/embedded graphics are preserved by file hash, not text extraction." +
                      (" See R01/R02/R03/R08: stale resume and resume-only historical facts." if path.name == "Resume.pdf" else ""), source=rel(path))
    elif suffix == ".pptx":
        with zipfile.ZipFile(path) as archive:
            parts = sorted(n for n in archive.namelist() if re.fullmatch(r"ppt/(slides/slide|notesSlides/notesSlide)\d+\.xml", n))
            slides = {}
            for part in parts:
                xml = ET.fromstring(archive.read(part))
                text = "\n".join(e.text or "" for e in xml.iter() if e.tag.endswith("}t"))
                slides[part] = text
                add(f"{cid}-PART-{len(slides):03}", "download text", f"{uri}; {part}", text,
                    f"Keep original leadership development download at {uri}", f"{rel(path)}; {part}",
                    notes="Local slide/notes XML text; no hyperlinks followed. Binary retains visual objects and formatting.", source=rel(path))
            extracts[rel(path)] = dict(type="pptx", parts=slides)
            asset["slides"] = len([n for n in parts if "/slides/" in n])
    assets.append(asset)
    add(cid, "asset", uri, json.dumps(asset, ensure_ascii=False), "Keep exact asset at " + uri,
        rel(path), notes="No incoming references found; retain as existing public asset." if not incoming else "Retain all incoming uses with owning pages.", source=rel(path))

attachment_manifest = []
for prefix, path in ATTACHMENTS:
    if not path.exists():
        attachment_manifest.append(dict(id=prefix, path=str(path), status="unavailable"))
        continue
    text = path.read_text(encoding="utf-8-sig")
    attachment_manifest.append(dict(id=prefix, path=str(path), sha256=digest(path), bytes=path.stat().st_size))
    heading = "Supplied planning material"
    major_section = ""
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        # Strip link targets and autogenerated citation labels; never fetch targets.
        cleaned = re.sub(r'\]\(https?://[^\r\n]+?\)', '] [link ignored]', line)
        cleaned = re.sub(r'https?://\S+', '[link ignored]', cleaned)
        cleaned = re.sub(r'\[\\\[.*?\\\]\]', '', cleaned)
        cleaned = normalize(cleaned)
        if not cleaned:
            continue
        if cleaned.startswith("#"):
            heading = cleaned.lstrip("# ")
            if cleaned.startswith("## "):
                major_section = heading
        destination = "Planning requirements > " + heading if prefix == "BRIEF" else "Private claim review register; no public destination until verified and cleared"
        if prefix == "BRIEF":
            if major_section.startswith("2."):
                destination = "Homepage > Professional identity and background; Architecture & Governance > Portfolio responsibilities"
            elif major_section.startswith("3."):
                destination = "Architecture & Governance > " + heading
            elif major_section.startswith("4."):
                destination = "Leadership & Mentoring / Architecture & Governance > " + heading
            elif major_section.startswith("5."):
                destination = "AI & Innovation > Responsible AI principles and workflow"
        add(f"{prefix}-{number:03}", "owner brief" if prefix == "BRIEF" else "unverified supplied claim",
            f"{prefix} attachment; line {number}", cleaned, destination, f"{path}; line {number}",
            "expand" if prefix == "BRIEF" else "retain", "needs review" if prefix == "SUPPLIED" else "preserved",
            "Source text only; linked evidence deliberately ignored. Supplied summary is not independent verification; no employer claim approved for publication." if prefix == "SUPPLIED" else
            "Owner-stated positioning/philosophy and project requirements; formal employer titles remain subject to R01.")

# Resolve local source references only, without opening linked documents or requesting URLs.
local_findings = []
known_pages = {"/" + p["name"] for p in routes}
for info in page_details:
    for ref in info["references"]:
        target = ref["target"]
        if ref["attribute"] == "asp-page" and target not in known_pages:
            local_findings.append(dict(file=info["file"], line=ref["line"], target=target, issue="Razor target not found"))
        elif target.startswith("~/"):
            local = target[2:].split("?")[0].split("#")[0]
            if local == "Portfolio.styles.css" or local.startswith("lib/"):
                continue  # Build/LibMan output, not content missing from source.
            exact = STATIC / local
            if not exact.exists():
                alternatives = [a["public_path"] for a in assets if a["public_path"].lower() == "/" + local.lower()]
                local_findings.append(dict(file=info["file"], line=ref["line"], target=target,
                                           issue="Case mismatch" if alternatives else "Local target absent", alternatives=alternatives))
            else:
                actual = [a["public_path"] for a in assets if a["public_path"].lower() == "/" + local.lower()]
                if actual and "/" + local not in actual:
                    local_findings.append(dict(file=info["file"], line=ref["line"], target=target, issue="Case mismatch", alternatives=actual))

assert len({r["ContentID"] for r in rows}) == len(rows), "Duplicate IDs"
assert all(r["OriginalLocation"] and r["ProposedLocation"] and r["Evidence"] for r in rows)
assert all(digest(ROOT / item["path"]) == item["sha256"] for item in manifest), "Site source changed during audit"
assert all(digest(ROOT / item["path"]) == item["sha256"] for item in assets), "Static asset changed during audit"
counts = dict(Counter(r["Kind"] for r in rows))
OUT.mkdir(parents=True, exist_ok=True)


def write_json(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


write_json("manifest.json", dict(date="2026-10-08", commit=commit, initial_tracked_status=initial_status,
                                  files=manifest, attachments=attachment_manifest))
write_json("baseline-source.json", snapshots)
write_json("routes.json", routes)
write_json("assets.json", assets)
write_json("download-text.json", extracts)
write_json("local-reference-findings.json", local_findings)
write_json("audit-summary.json", dict(routes=len(routes), route_aliases=sum(len(p["routes"]) for p in routes),
                                       templates=len(page_details)-len(routes), files=len(manifest), assets=len(assets),
                                       site_assets=sum(a["category"] == "site asset" for a in assets),
                                       vendor_assets=sum(a["category"] == "vendor dependency" for a in assets),
                                       items=len(rows), counts=counts, local_findings=len(local_findings),
                                       source_hashes_unchanged=True, live_site_examined=False, links_followed=0))
with (OUT / "preservation-matrix.csv").open("w", encoding="utf-8-sig", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

inventory = ["# Content inventory", "", "Baseline: 2026-10-08. Source-derived local audit; linked targets and deployed site excluded by user instruction.", "",
             "Exact working-tree source is captured in `baseline-source.json`; asset identities in `assets.json`; all original information and destinations in `preservation-matrix.csv`.", "",
             "## Pages, routes, and navigation", "", "| Content ID | Source | Routes | Proposed content area | Text blocks |", "|---|---|---|---|---|"]
for info in page_details:
    inventory.append("| " + " | ".join(cell(v) for v in (info["id"], info["file"], ", ".join(info["routes"]) or "Shared template", info["destination"], info["blocks"])) + " |")
inventory += ["", "## Complete page text", "", "Each entry has a preservation-matrix ID. Inline formatting is normalized; original source and comments remain in the baseline. Dynamic Razor values and source behavior have separate records.", ""]
for info in page_details:
    inventory += ["### " + info["name"], ""]
    for row in rows:
        if row["ContentID"].startswith(info["id"] + "-TEXT-"):
            inventory.append(f"- **{row['ContentID']}** ({row['Evidence']}): {row['OriginalInformation']}")
    inventory.append("")
inventory += ["## Static assets and downloads", "", "| ID | Public path | Bytes | Incoming uses | Document units |", "|---|---|---|---|---|"]
for asset in assets:
    inventory.append("| " + " | ".join(cell(v) for v in (asset["id"], asset["public_path"], asset["bytes"], ", ".join(asset["incoming"]) or "No active incoming reference found", asset.get("pages", asset.get("slides", "")))) + " |")
inventory += ["", "PDF pages and PowerPoint slides/notes are individually mapped in the matrix and extracted in `download-text.json`. Raster images retain exact byte identity; descriptive intent is taken only from source attributes, not inferred from filenames.", "",
              "## Metadata and functionality", "", "Shared layout metadata, anchors, reference occurrences, image/control attributes, Razor conditional behavior, and all supporting source files each have matrix records. See README for behavior findings and owner-review.md for ambiguities.", ""]
(OUT / "content-inventory.md").write_text("\n".join(inventory), encoding="utf-8")
print(json.dumps(dict(items=len(rows), counts=counts, routes=len(routes), assets=len(assets), local_findings=local_findings), indent=2))

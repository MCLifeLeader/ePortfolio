"""Export rendered portfolio content into the separate GitHub wiki checkout.

Dependencies: beautifulsoup4, markdownify, markdown. Publication is a separate,
explicit git operation. Unrelated existing wiki pages are never deleted.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
from urllib.parse import quote, unquote, urljoin, urlsplit
from urllib.request import urlopen

from bs4 import BeautifulSoup, Comment
import markdown
from markdownify import MarkdownConverter

ROOT = Path(__file__).resolve().parents[3]
PAGES = ROOT / "Src/Portfolio_Core/Portfolio/Pages"
MEDIA = ROOT / "Src/Portfolio_Core/Portfolio/wwwroot"
WIKI = "https://github.com/MCLifeLeader/ePortfolio/wiki"
RAW = "https://raw.githubusercontent.com/wiki/MCLifeLeader/ePortfolio/"
EXCLUDED = {"Error", "Experience/ResumeHistory"}


class Converter(MarkdownConverter):
    def convert_td(self, el, text, parent_tags):
        if el.find(["ul", "ol"]):
            text = re.sub(r"\n+", "<br>", text.strip())
        return super().convert_td(el, text, parent_tags)

    def process_tag(self, node, parent_tags=None):
        text = super().process_tag(node, parent_tags)
        anchor = node.get("id")
        if anchor:
            text = f'\n\n<a name="{anchor}"></a>\n\n' + text
        return text


def tokens(text):
    return re.findall(r"\w+", text.casefold())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:5187")
    parser.add_argument("--wiki-dir", type=Path, default=ROOT / ".wiki-sync")
    args = parser.parse_args()
    checkout = args.wiki_dir.resolve()
    if not (checkout / ".git").is_dir():
        raise SystemExit("--wiki-dir must be an existing wiki git checkout")
    base = args.base_url.rstrip("/")
    if urlsplit(base).hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise SystemExit("Render from a local application to avoid publishing stale live content")
    routes = {}
    for source in sorted(PAGES.rglob("*.cshtml")):
        if not source.read_text(encoding="utf-8-sig").lstrip().startswith("@page"):
            continue
        key = source.relative_to(PAGES).with_suffix("").as_posix()
        if key in EXCLUDED:
            continue
        route = "/" if key == "Index" else "/" + key
        name = "Home" if key == "Index" else key.replace("/Index", "").replace("/", "-")
        routes[route] = {"name": name, "source": source.relative_to(ROOT).as_posix()}
    lookup = {}
    for route, item in routes.items():
        lookup[route.casefold()] = item["name"]
        if route.endswith("/Index"):
            lookup[route[:-6].casefold()] = item["name"]
    lookup["/index"] = "Home"
    snapshots = {}
    for route, item in routes.items():
        with urlopen(base + route, timeout=30) as response:
            soup = BeautifulSoup(response.read(), "html.parser")
        content = soup.select_one("main")
        if content is None:
            raise AssertionError(f"No main content: {route}")
        for unwanted in content.select("script, style, button, [aria-hidden='true']"):
            unwanted.decompose()
        for comment in content.find_all(string=lambda s: isinstance(s, Comment)):
            comment.extract()
        item["title"] = content.h1.get_text(" ", strip=True) if content.h1 else item["name"]
        for link in content.select("a + a"):
            sibling = link.previous_sibling
            while sibling is not None and not getattr(sibling, "name", None) and not str(sibling).strip():
                sibling = sibling.previous_sibling
            if getattr(sibling, "name", None) == "a":
                link.insert_before(" · ")
        for caption in list(content.select("table > caption")):
            paragraph = soup.new_tag("p")
            paragraph.string = caption.get_text(" ", strip=True)
            caption.parent.insert_before(paragraph)
            caption.decompose()
        snapshots[route] = content
    assets = {}
    report = []
    for route, content in snapshots.items():
        item = routes[route]
        expected_links, expected_images = [], []
        for element in content.select("a[href], img[src]"):
            attr = "href" if element.name == "a" else "src"
            value = element[attr]
            resolved = urlsplit(urljoin(base + route, value))
            if resolved.netloc == urlsplit(base).netloc:
                path = unquote(resolved.path)
                target = lookup.get(path.rstrip("/").casefold() or "/")
                if target:
                    value = WIKI + "/" + target
                    if resolved.fragment:
                        # GitHub sanitizes custom <a name> targets this way.
                        value += "#user-content-" + unquote(resolved.fragment).lower()
                else:
                    local = (MEDIA / path.lstrip("/")).resolve()
                    if not local.is_relative_to(MEDIA.resolve()) or not local.is_file():
                        raise AssertionError(f"Unmapped local link in {route}: {value}")
                    if local.name.casefold() == "resume.pdf":
                        raise AssertionError("The disconnected resume must not be published")
                    relative = Path("assets") / local.relative_to(MEDIA)
                    dest = checkout / relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(local, dest)
                    assets[relative.as_posix()] = hashlib.sha256(local.read_bytes()).hexdigest()
                    value = RAW + quote(relative.as_posix(), safe="/")
            element[attr] = value
            (expected_links if attr == "href" else expected_images).append(value)
        original_text = content.get_text(" ", strip=True)
        body = Converter(heading_style="ATX", bullets="-", escape_underscores=False).convert(str(content))
        # Check the actual Markdown round trip, including table content and emphasis.
        roundtrip = BeautifulSoup(markdown.markdown(body, extensions=["tables"]), "html.parser")
        if tokens(original_text) != tokens(roundtrip.get_text(" ", strip=True)):
            raise AssertionError(f"Text changed during Markdown conversion: {route}")
        actual_links = [a["href"] for a in roundtrip.select("a[href]")]
        actual_images = [i["src"] for i in roundtrip.select("img[src]")]
        if Counter(expected_links) != Counter(actual_links) or Counter(expected_images) != Counter(actual_images):
            raise AssertionError(f"Links or images lost during conversion: {route}")
        expected_anchors = {n["id"] for n in content.select("[id]")}
        if content.get("id"):
            expected_anchors.add(content["id"])
        actual_anchors = {n["name"] for n in roundtrip.select("a[name]")}
        if expected_anchors != actual_anchors:
            raise AssertionError(f"Section anchors changed: {route}")
        page_text = body.strip() + f"\n\n---\n\n[View this page on the website](https://mbcarey.com{route}) · [Portfolio home]({WIKI}/Home)\n"
        (checkout / (item["name"] + ".md")).write_text(page_text, encoding="utf-8", newline="\n")
        report.append({"route": route, **item, "text_tokens": len(tokens(original_text)),
                       "links": len(expected_links), "images": len(expected_images),
                       "anchors": sorted(expected_anchors)})
    # Cross-page fragments must resolve to preserved anchors or a GitHub heading.
    for route, content in snapshots.items():
        for a in content.select("a[href]"):
            value = a["href"]
            if value.startswith("#"):
                target_route, fragment = route, value[1:]
            elif value.startswith(WIKI + "/") and "#" in value:
                name, fragment = value[len(WIKI) + 1:].split("#", 1)
                target_route = next((r for r, i in routes.items() if i["name"] == name), None)
            else:
                continue
            raw_fragment = unquote(fragment).removeprefix("user-content-").lower()
            if target_route is None or not any(n["id"].lower() == raw_fragment for n in snapshots[target_route].select("[id]")):
                raise AssertionError(f"Unresolved wiki fragment: {value} from {route}")
    groups = [
        ("Portfolio", ["/", "/Architecture", "/Skills/AI"]),
        ("Engineering", ["/Skills/Technologies", "/Skills/Index", "/Skills/Leadership"] + [r for r in routes if r.startswith("/Skills/") and r not in {"/Skills/AI", "/Skills/Technologies", "/Skills/Index", "/Skills/Leadership"}]),
        ("Experience", ["/Experience/Index", "/Experience/WorkHistory", "/Experience/EmploymentAccomplishments", "/Experience/Education"]),
        ("Projects", ["/Projects/Index"] + [r for r in routes if r.startswith("/Projects/") and r != "/Projects/Index"] + ["/Git"]),
        ("Explore", ["/Explore", "/AboutMe"] + [r for r in routes if r.startswith(("/Fun/", "/College/"))] + ["/Tribute", "/Contact", "/Privacy"]),
    ]
    sidebar = ["## Michael B. Carey", f"[Website](https://mbcarey.com) · [Wiki home]({WIKI}/Home)", ""]
    for label, members in groups:
        sidebar += ["### " + label, ""]
        for route in members:
            i = routes[route]
            sidebar.append(f"- [{i['title']}]({WIKI}/{i['name']})")
        sidebar.append("")
    (checkout / "_Sidebar.md").write_text("\n".join(sidebar), encoding="utf-8", newline="\n")
    (checkout / "_Footer.md").write_text("[Website](https://mbcarey.com) · [GitHub project](https://github.com/MCLifeLeader/ePortfolio) · [Contact](https://github.com/MCLifeLeader/ePortfolio/wiki/Contact)\n", encoding="utf-8", newline="\n")
    result = {"source_commit": __import__("subprocess").check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "wiki_url": WIKI, "pages": report, "assets": assets,
              "checks": {"text_roundtrip": "passed", "links_and_images": "passed", "section_anchors": "passed", "cross_page_fragments": "passed"}}
    (Path(__file__).parent / "wiki-sync-verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(report)} wiki pages, sidebar, footer, and {len(assets)} media files. All preservation checks passed.")


if __name__ == "__main__":
    main()

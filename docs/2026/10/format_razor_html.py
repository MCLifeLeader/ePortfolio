"""Align Razor HTML without changing markup, attributes, or protected content."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAGES = ROOT / "Src/Portfolio_Core/Portfolio/Pages"
BLOCKS = "html|head|body|header|footer|main|nav|section|article|aside|div|ul|ol|li|table|thead|tbody|tfoot|tr|td|th|h[1-6]|p|figure|figcaption|button|form|fieldset|legend"
VOIDS = {"meta", "link", "img", "input", "hr"}
TOKENS = re.compile(r"(</?(?:" + BLOCKS + r"|meta|link|img|input|hr)\b[^>]*>|<!DOCTYPE[^>]*>)", re.I)
PROTECTED = re.compile(r"@\*[\s\S]*?\*@|<!--[\s\S]*?-->|<(script|style|pre|textarea)\b[^>]*>[\s\S]*?</\1\s*>", re.I)


def format_html(source):
    protected = []

    def protect(match):
        protected.append(match.group())
        return f"__RAZOR_PROTECTED_{len(protected) - 1}__"

    source = PROTECTED.sub(protect, source)
    lines, stack = [], []
    razor_depth = 0
    for part in TOKENS.split(source):
        if not part.strip():
            continue
        if TOKENS.fullmatch(part):
            name = re.match(r"</?([\w]+)", part)
            tag = name.group(1).lower() if name else "!doctype"
            closing = part.startswith("</")
            if closing:
                assert stack and stack[-1] == tag, (stack, part)
                stack.pop()
            lines.append("    " * (len(stack) + razor_depth) + part)
            if not closing and tag not in VOIDS and tag != "!doctype" and not part.endswith("/>"):
                stack.append(tag)
        else:
            for line in part.splitlines():
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped == "}":
                    razor_depth = max(0, razor_depth - 1)
                lines.append("    " * (len(stack) + razor_depth) + stripped)
                if stripped in ("{", "@{"):
                    razor_depth += 1
    assert not stack, stack
    result = "\n".join(lines) + "\n"
    for index, value in enumerate(protected):
        result = result.replace(f"__RAZOR_PROTECTED_{index}__", value)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Paths relative to the Pages directory")
    args = parser.parse_args()
    results = []
    for relative in args.paths:
        path = (PAGES / relative).resolve()
        assert path.is_relative_to(PAGES.resolve()) and path.suffix == ".cshtml", path
        before = path.read_text(encoding="utf-8-sig")
        after = format_html(before)
        assert re.sub(r"\s+", "", before) == re.sub(r"\s+", "", after), path
        assert [m.group() for m in PROTECTED.finditer(before)] == [m.group() for m in PROTECTED.finditer(after)], path
        path.write_text(after, encoding="utf-8", newline="\r\n")
        results.append({"path": relative, "non_whitespace_content_preserved": True})
    print(json.dumps(results))

# Repository and technical foundations

Implementation complete; evidence is recorded in [the implementation review](12-implementation-review.md), [technical report](technical-work.md), and [preservation report](traceability-work.md). These are local implementation tasks; they do not require resolving every factual review item first. Source: [audit findings](../../content-audit/README.md).

## F01 — Implementation isolation and recovery

- [x] Record current branch/status and preserve the preexisting Portfolio.csproj modification.
- [x] Establish a dedicated implementation branch or isolated checkout without disturbing user work.
- [x] Preserve the audit baseline, existing document/media binaries, and a recoverable original revision plus relevant working-tree changes.
- [x] Identify generated audit artifacts that contain private planning claims before any repository publication.

**Outputs:** Baseline/recovery notes, implementation branch identity, and disposition of preexisting changes. Do not publish private planning records implicitly.

**Done when:** Original source and assets can be restored and the audit has not been regenerated from revised content. Depends on I01.

## F02 — Build and runtime compatibility

- [x] Inspect installed SDK/runtime, the working-tree net10.0 target, Docker .NET 8 images, Copilot .NET 9 setup, and devcontainer .NET 8 settings.
- [x] Document the intended existing-platform target and make only the compatibility changes required to support it.
- [x] Verify restore/build/publish and the supported container path; confirm LibMan dependencies are available.
- [x] Record deployment pipeline behavior and distinguish source configuration from unverified production hosting.

**Outputs:** Compatible configuration changes and recorded local build/publish evidence. A container migration or hosting replacement is not an assumed requirement.

**Done when:** Supported local build/runtime paths agree, remaining limitations are explicit, and no undocumented framework/infrastructure replacement occurs. Depends on F01.

## F03 — Filename case compatibility

- [x] Remove homepage and WorkHistory PDF references under the owner's subsequent disconnection instruction; preserve Resume.pdf unchanged.
- [x] Correct the radio gallery's Image027.JPG reference to Image027.jpg.
- [x] Preserve the original asset bytes and account for old URL casing if the hosting behavior requires compatibility handling.

**Outputs:** Recorded retirement of the two resume references, a corrected radio-image reference, and case-sensitive compatibility verification.

**Done when:** The original resume file is retained without page links, the affected radio image resolves locally in the supported hosting environment, and owning ContentIDs have migration evidence. The radio-image casing change is implemented and Linux-tested. Depends on F01.

## F04 — Markup and encoding

- [x] Repair malformed quoting in the Leadership reading-list markup without changing the link target or book attribution.
- [x] Handle the Tribute page's legacy Windows punctuation correctly if converting source encoding.
- [x] Check affected nested lists and semantic containers while retaining every text item, reading category, and historical comment.

**Outputs:** Focused source corrections and a source-to-rendered-text comparison.

**Done when:** Markup parses as intended, punctuation is preserved, and no factual/editorial content is lost. External link availability remains untested. Depends on F01.

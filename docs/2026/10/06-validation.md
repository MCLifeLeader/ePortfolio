# Validation tasks

All tasks are open. Record actual evidence and failures; do not mark an unperformed check passed. Tests should verify preservation and user behavior rather than mirror implementation details.

## V01 — Complete substantive preservation

- [ ] Compare revised content with the fixed inventory and original source, including document-only information.
- [ ] Verify each inventory ID's implemented destination or explicit retained/withheld/nonpublic disposition.
- [ ] Review merged/relocated text for lost dates, technologies, qualifiers, collaborators, outcomes, project status, and meaningful perspectives. Distinguish owner-authorized removals/corrections recorded October 8 from unexplained loss; verify the original information remains in the baseline.
- [ ] Compare retained binary hashes and ensure historical documents/credits remain accessible.
- [ ] Check factual decisions and ensure unverified or uncleared supplied claims have not entered public content.

**Output:** A preservation report distinguishing captured, implemented, and verified items, with an explicit unexplained-loss count.

**Done when:** No substantive item is silently lost, every ID has evidence/disposition, and the unexplained-loss count is zero. Process requirements, vendor files, and private planning records need explicit dispositions rather than artificial public destinations. Depends on C01–C10 and U01–U03.

## V02 — Local routes, anchors, references, downloads

- [ ] Exercise all 44 original route aliases and 30 anchors on the local implementation, including compatibility redirects where introduced.
- [ ] Verify active internal navigation and reference targets, exact filename casing, media, and all downloads.
- [ ] Check new routes and menu/landing-page discoverability, including pages outside primary navigation.
- [ ] Record external references as untested under the owner's instruction; do not open links embedded in documents.

**Output:** Route/anchor/download results and an internal-reference report with actionable failures.

**Done when:** Original local entry points reach preserved information and every active internal/download target works. External status and deployed-site parity remain explicitly unverified. Depends on U01–U03 and F03.

## V03 — Accessibility, responsive layouts, behavior

- [ ] Inspect desktop, tablet, and mobile layouts in both themes.
- [ ] Verify keyboard navigation, focus visibility, headings/landmarks, contrast, labels, readable tables/timelines, and image alternatives.
- [ ] Exercise responsive menus, theme switching/system default/stored preference, gallery carousel, and downloads.
- [ ] Check that incomplete features are presented honestly and that supporting historical content remains discoverable.

**Output:** Accessibility/responsive/behavior findings with screenshots or equivalent evidence for relevant states.

**Done when:** Material usability/accessibility defects are corrected and all retained useful behavior is verified. Depends on U01–U03.

## V04 — Build, browser behavior, performance, and verification report

- [ ] Run the appropriate final restore/build/publish/container checks after implementation changes.
- [ ] Check supported browsers, console/runtime errors, asset loading, and relevant performance regressions.
- [ ] Verify metadata and crawler outputs locally; distinguish configuration evidence from deployed SEO behavior.
- [ ] Consolidate V01–V03 and technical checks into a verification report with outcomes, remaining issues, and scope exclusions.

**Output:** Final verification report and reproducible commands/scenarios for material checks.

**Done when:** Required checks pass or material unresolved limitations are clearly identified for review; no excluded checks are represented as passing. Depends on F02 and V01–V03.

# Presentation and functionality

All tasks are open. Implement incrementally within Razor Pages after destinations and content are mapped. Retain useful existing behavior and avoid unnecessary dependencies or decorative complexity.

## U01 — Shared design, navigation, and themes

- [ ] Implement reusable typography, spacing, page hierarchy, supporting navigation, project/experience layouts, and responsive presentation.
- [ ] Implement the concrete A01 menu/landing-page structure while preserving old routes and anchors.
- [ ] Preserve light/dark switching, system preference, localStorage persistence, labels, and keyboard access.
- [ ] Apply revised section content incrementally and update the migration ledger as each page is implemented.

**Outputs:** Reviewable layouts/components and implemented pages in the existing framework.

**Done when:** Implemented content is accessible through navigation, themes remain usable, and mobile/tablet/desktop layouts are ready for V03 verification. Depends on F01/F02, A01/A02, and the content task for each implemented page.

## U02 — Contact, Privacy, and Error

- [ ] Present Contact's actual available connection options without implying that the disabled form works.
- [ ] Decide whether to retain the unfinished form as inactive history or implement a separately specified feature; form delivery is not assumed by this backlog.
- [ ] Address the Privacy placeholder with factual handling based on actual site behavior; do not invent data collection or consent practices.
- [ ] Retain Error handling and avoid production disclosure of development details.

**Outputs:** Honest user-facing utility pages and documented decisions about incomplete functionality.

**Done when:** Every utility route remains functional and descriptions match implementation. No message-sending feature is claimed without implementation and verification. Depends on F01/F02 and A01/A02.

## U03 — Metadata, media, and download presentation

- [ ] Update titles/descriptions and appropriate metadata using supported positioning while retaining original metadata in the baseline.
- [ ] Document canonical/sitemap/structured-data decisions and implement only justified additions; no new SEO claim should fabricate professional facts.
- [ ] Preserve image/media identity, alt/title/caption meaning, gallery order, carousel behavior, downloads, and original file paths.
- [ ] Keep dependency references maintainable and record any dependency changes; do not substitute new assets for historical evidence.

**Outputs:** Metadata and media implementation mapped to original IDs, plus recorded SEO/dependency decisions.

**Done when:** Page titles/metadata correspond to content, all original assets are accounted for, and download/media entry points are usable. Depends on U01, F03/F04, and C09.

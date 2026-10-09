# Content inventory and preservation matrix

Completed local source inventory: **2026-10-08**. No page restructuring, content revision, framework migration, or deployment was performed.

This audit examines the working-tree repository and both supplied text documents. Following the owner's instruction to ignore all document links, no URLs were opened, no linked evidence was retrieved, and the deployed website was not crawled. This is a complete inventory of the local source and installed static assets, not a claim that deployed-only content or external evidence has been examined. Live-versus-repository differences remain outside this audit's scope.

## Deliverables

| File | Purpose |
|---|---|
| [content-inventory.md](content-inventory.md) | All source-derived pages/routes, full normalized page text, and static asset register |
| [preservation-matrix.csv](preservation-matrix.csv) | 3,150 individual mappings, including original information, destination, change type, evidence, and verification status |
| [owner-review.md](owner-review.md) | Specific factual conflicts, publication concerns, and supported options |
| [manifest.json](manifest.json) | Baseline commit, preexisting tracked modification, attachment identities, and SHA-256 for 202 repository files |
| [baseline-source.json](baseline-source.json) | Exact decoded text of original tracked source/configuration files; byte hashes remain authoritative |
| [routes.json](routes.json) | Route aliases, source files, titles, anchors, and reference occurrences |
| [assets.json](assets.json) | Every installed static asset, byte count, hash, ownership category, and incoming uses |
| [download-text.json](download-text.json) | Text from every local PDF page and PowerPoint slide/notes part |
| [local-reference-findings.json](local-reference-findings.json) | Filename case discrepancies found by local inspection |
| [audit-summary.json](audit-summary.json) | Machine-readable coverage and scope |
| [build_inventory.py](build_inventory.py) | Reproducible, offline inventory generator |

Audit documents are outside `wwwroot`. The supplied accomplishments register contains potentially non-public employer information and is planning evidence only. It has not been added to a public page, committed, pushed, or deployed.

## Coverage

| Category | Examined / recorded |
|---|---|
| Razor pages | 38, including placeholder and error pages |
| Source-derived route aliases | 44, including directory Index aliases |
| Shared templates | 4 |
| Repository baseline | 202 tracked files |
| Static assets | 369: 94 site assets and 275 installed vendor dependency files |
| References in active source markup | 324 occurrences; recorded, never followed |
| Fragment anchors | 30 |
| Image and control elements | 99 |
| Metadata declarations | 13 |
| Inactive source comments | 21, retained separately from visible content |
| PDFs | 4 files, all 418 pages text-extracted |
| PowerPoint | 1 file, 55 slides and 33 notes parts text-extracted |
| Supplied brief | 363 nonempty source-line records, including positioning, philosophy, and process requirements |
| Supplied accomplishments summary | 131 nonempty source-line records, held as unverified planning material |

Every public file actually present beneath `wwwroot` is accounted for, including ignored LibMan dependencies. Images, document diagrams, slide objects, and other binary content remain in their original files with hashes; text extraction does not replace those assets or establish visual/layout fidelity. No PDF page was empty after text extraction. Image meaning has not been inferred from filenames. The original source records image alt/title attributes, captions, and gallery order.

## Preservation rules and matrix interpretation

`ContentID` is unique within this baseline. `OriginalLocation` identifies the original route/section/line, public asset path, document page, or attachment line. `OriginalInformation` contains actual text, the reference/control attributes, or the asset record. `Evidence` points to local source. `SourceFile` allows filtering by source page. IDs use original page names and source order; reuse this baseline when revising rather than regenerating IDs from changed content.

`ProposedLocation` names the destination area and section, or explicitly retains the original asset/route. Destinations are proposals, not implemented pages. Every existing page route and directory Index alias is retained in the proposal. Every asset keeps its existing public path. Content moved from the homepage is assigned to a discoverable supporting area. If a later implementation changes routes or anchors, record the exact redirect/anchor compatibility strategy before removing the original entry point.

`ChangeType` uses retain, relocate, or expand for this baseline. Actual rewriting and consolidation have not occurred. Repeated content occurrences retain distinct IDs, so merging them later must account for all source facts and references. Table rows keep years, technologies, and descriptions together; nested skill lists retain proficiency qualifiers such as "Light Exposure."

`Verification=preserved` means **captured and unchanged in the original baseline**, not migrated, independently fact-checked, or approved for publication. `needs review` flags specific conflicts and supplied claims. Links are explicitly unvalidated, regardless of baseline capture status. Full source snapshots retain Razor conditions, dynamic values, comments, legacy Windows text encoding, and material outside semantic text blocks. Commented-out links/content remain source history and are not proposed for automatic public restoration.

For downloads, each original binary is a preservation unit and each page/slide/notes part has a supporting text record. The proposal retains the complete original document, including graphics and credits. Any future replacement must account for document-only information and retain a clearly labeled historical copy where appropriate.

## Proposed organization, without changing page structure

| Destination | Source material and preservation treatment |
|---|---|
| Homepage | Owner-stated portfolio architect identity, multidisciplinary background, concise philosophy, evidence-based highlights, resume/contact entry points |
| Architecture & Governance | New owner-stated philosophy: maintainability → correctness → delivery speed; domain-aligned mini-services; integration/API contracts; ecosystem impact; strangler modernization; innovation evaluation; debt; documentation/standards; guided autonomy and risk communication |
| AI & Innovation | Existing Skills/AI content, public-tool descriptions, responsible AI workflow from the brief; employer summary held for verification/disclosure review |
| Engineering & Technology | All skill-detail pages and technology overview; complete homepage skill rows/list, older languages and tooling, proficiency qualifiers, QA guidance and historical technical experience |
| Leadership & Mentoring | Complete leadership chronology, mentoring and hiring examples, Citizen Developer initiative, governance approach, personality profiles, seminars/trainings/audio, all reading-list categories, original Scrum Master deck |
| Projects & Accomplishments | Every project/index entry and detail page, including entries without detail routes: translation support, WordPress, SwipeClock, membership synchronization, and other work; all Git repository descriptions and coursework foundations retained |
| Professional Experience | Complete WorkHistory chronology, responsibilities, employer-specific skills, contract roles, ventures, and original anchors; role/date contradictions remain flagged |
| Education & Professional Development | Early self-directed learning; General Studies associate's degree; Software Engineering bachelor's record; complete college coursework and team attribution; original SRS/SDD/ECR downloads |
| About / Personal / Community | Biography and entrepreneurial perspective; freelance availability with historical context; civic engagement; amateur-radio build instructions/gallery/parts; Solarian League gaming/learning context; service mission; tribute; resume-only personal achievements |
| Shared site infrastructure | Existing Contact, Privacy, Error, layout, navigation, titles, metadata, styles, themes, local dependency references, and deployment configuration |

Project outcomes must remain distinct: prototypes and exploratory work are not completed enterprise deployments; discontinued projects remain historical entries. AI aspirations in the A-Game page remain goals. A past recommendation or "current" status must not be silently turned into a newly verified claim.

## Repository and functionality findings

- ASP.NET Core Razor Pages app, with source-derived routing through `MapRazorPages`, static-file serving, HTTPS redirection, and production exception handling/HSTS. No alternate route registrations or custom page templates were found.
- Working-tree project targets `net10.0`. The project file was already modified before this audit; it was preserved. Docker images still target .NET 8, the Copilot setup workflow selects .NET 9, and the devcontainer includes .NET 8 runtime settings. Compatibility needs validation in a later implementation phase, not a framework decision during this inventory.
- LibMan defines Bootstrap 5.3.3, jQuery 3.7.1, jquery-validation-unobtrusive 3.2.10, and jquery-validate 1.20.0. Installed files are inventoried independently. The layout also references external Bootstrap Icons; it was not fetched.
- Navigation is generated from the shared layout and includes nested Experience, Projects, College, and Skills menus, Git, Contact, Tribute, and the theme control. Index pages and some detail routes exist beyond primary navigation; they are included in the inventory.
- Light/dark selection uses `data-bs-theme`, system preference, and `localStorage` persistence. Preserve the switch, labels, stored preference, responsive navbar behavior, gallery carousel, and PDF/download entry points.
- Contact displays "Coming Soon"; its form is commented out, and its PageModel has only `OnGet`. A reCAPTCHA script reference remains. Do not describe the site as having functioning form submission.
- Privacy is a template placeholder, not a completed privacy policy. Error is the framework error/development guidance page. Both are inventoried as existing source.
- Layout metadata includes page title, description, keywords, reply-to, language, robots, copyright, and other historical meta declarations. `robots.txt` allows crawling. No sitemap file or canonical/structured-data implementation was found in the source baseline.
- The GitHub production deployment workflow is commented out. The Azure DevOps YAML builds/publishes artifacts; it does not prove the current production hosting environment or deployed revision. No hosting replacement or deployment occurred.
- Three local case mismatches: homepage and WorkHistory use `resume.pdf` but the file is `Resume.pdf`; the radio gallery uses `Image027.JPG` but the file is `Image027.jpg`. These may affect case-sensitive hosting. No fixes were made during this audit.
- The radio article explicitly says its template diagram has not been created and contains unspecified parts quantities. Preserve the incomplete status and do not fabricate measurements or a missing download.
- A reading-list link has malformed quoting in the original markup. References and original markup are retained; external availability is not assessed.

## Verification and boundaries

The generator checked unique IDs, nonempty original/destination/evidence fields, and unchanged SHA-256 values for every baseline repository file and every installed static asset. A separate readback checked artifact counts, coverage of every Razor source and static file, and matrix evidence/destination completeness. Source route targets were resolved against local Razor files; local asset references were compared with exact filenames. No missing active Razor targets were found.

All substantive source content is captured with a proposed preservation destination. The source inventory and matrix are complete within the stated local scope. New-page preservation, route compatibility over HTTP, external-link status, browser behavior, visual PDF/slide rendering, accessibility, build/deployment health, deployed-site parity, and professional claim verification have not been certified. These checks are not needed to write this documentation baseline and must not be represented as passing.

Before significant restructuring, use this matrix as the fixed baseline and resolve the factual/publication choices that affect the content being changed. A later content revision should add revised source/destination evidence and migration verification for each relevant ID, and demonstrate that every historical fact, asset, qualifier, and meaningful perspective remains accessible. Production deployment still requires the explicit owner approval specified in the brief.

To reproduce the original local extraction, run `python docs/content-audit/build_inventory.py` with `pypdf` available and the two original attachments accessible. This overwrites generated audit artifacts; do not use it to reset the baseline after restructuring. No network requests are made.

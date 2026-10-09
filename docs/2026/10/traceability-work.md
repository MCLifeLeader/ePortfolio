# Traceability implementation — October 8, 2026

This implements the separate A01/A02 compatibility map and migration ledger. The fixed inventory, its 3,150 IDs, original fields, source snapshots, and download extraction remain in `docs/content-audit` unchanged. This work does not regenerate `build_inventory.py`, change website source, build the site, or publish anything.

## Outputs

- [Site map](site-map.md): professional areas, supporting entry points, every original route alias, every original anchor, and new routes found in source.
- [Migration ledger](migration-ledger.csv): one row for every original ContentID; category, explicit disposition, actual destination/source, implementation status, and evidence.
- [Reusable verifier](verify_modernization.py): source checks and optional loopback rendering checks; writes a separate [validation report](modernization-validation.json).

Run from the repository root:

```powershell
python docs/2026/10/verify_modernization.py --write-ledger
python docs/2026/10/verify_modernization.py --write-ledger --base-url http://localhost:5187
```

The report records failures without modifying the fixed baseline. A nonzero exit means at least one check needs attention. The optional HTTP mode permits localhost and literal loopback addresses only, validates redirects too, and does not fetch external references or document links. Binary reads are local.

## Coverage rules

Public prose is checked as complete word/number sequences against active page text. Typography is ignored; technology names, numbers, qualifiers, and words are retained. Every matching destination is recorded, so many-to-one consolidation and one-to-many distribution remain traceable. Unmatched substantive text receives a specific review finding instead of passing merely because an archive exists.

The ledger explicitly separates active public prose from source infrastructure, dynamic Razor fragments, unchanged dependencies, original downloads, inactive comments, private process requirements, and supplied source context. All 52 reviewed accomplishments have source and rendered markers. The underlying approved source records are mapped to those markers; headings/caveats outside the approved claim list remain private baseline context. No new completed-delivery status or measurement is inferred.

The original homepage technology table and list move to `/Skills/TechnicalHistory` with their recorded durations and proficiency distinctions. Civic text and social references move to `/AboutMe`. The current reading additions supplement the original reading categories. LinkedIn and GitHub remain referenced.

Original media, documents, and unexempted vendor assets use the audit SHA-256 identity. The owner's subsequent minimal LibMan instruction narrowly authorizes upgrades/retirement within the original Bootstrap/jQuery-family vendor directories and retirement of the unused validation partial. The final manifest selects exactly eight Bootstrap/Bootstrap Icons files. The original Resume.pdf remains byte-identical and deliberately disconnected from all page links. Its source extraction is retained with that explicit historical disposition; the new resume-history page supplies supporting context. The site CSS and theme JavaScript are intentional presentation changes and are classified separately from binary preservation.

## Explicit corrections and changes

Owner-authorized exceptions cite [the decision record](08-owner-decisions.md): title/date reconciliation, degree completion in 2020, pipeline creation versus execution timing, Family Key chronology, earned-date Scrum wording, removed Upwork solicitation, and disconnected resume invitations. Reading-list corrections cite the owner's subsequent supplied titles/authors. Original information remains inspectable by ContentID in the fixed matrix.

The edited AboutMe manager/architect paragraphs retain the education portfolios, organization, global program context, architecture focus, and educator/student responsibilities. The Leadership manager paragraph retains the original SDET contract origin, application/interview history, approximate thirty-plus engineers, and varied seniority; current-role learning language receives historical tense. The DevOps correction retains Academy Mortgage's adoption/evaluation context, prior TFS experience, GO/CD/Chef maintenance comparison, later promotion, and governance responsibilities while correcting the timing claim. These are narrowly identified owner-corrected records; the verifier does not claim literal paragraph equality for them.

Template and navigation changes have explicit implementation dispositions: privacy template instruction replaced with content; generic homepage card invitations rewritten; parent menu labels regrouped while routes/references remain checked independently; inactive-form reCAPTCHA and unused icon dependency retired; footer/year Razor expressions remain dynamic. Original layout anchor IDs remain present. `/Error` stays directly addressable as a runtime utility outside the visitor directory, and detailed environment diagnostics remain development-only.

An initial loopback run found a genuine 404 for generated `Portfolio.styles.css`. That link was removed from the layout because presentation is centralized in `site.css`; its retirement is recorded separately from original asset preservation. The final report must be produced against the rebuilt server after all parallel changes finish.

## Final verification result

The final command ran against the rebuilt site at `http://localhost:5187` and exited successfully: **3,150 mapped IDs, zero unexplained losses, and zero failed checks**. All 49 current route aliases returned HTTP 200, including the 44 original aliases. All 30 original anchors and all 52 approved accomplishment markers appeared in rendered output. All 80 local asset/font requests returned HTTP 200. No rendered page linked Resume.pdf; LinkedIn and GitHub were retained. All fixed audit files had identical hashes before and after the check.

Following the complete page-layout and minimal LibMan passes, the implementation statuses distinguish 989 complete source-text matches, 598 byte-identity records, 112 approved-source-to-accomplishment mappings, 27 owner-authorized content/presentation exceptions, four selected vendor upgrades, 271 unused vendor retirements, four unused-validation-partial retirements, 15 editorial changes, 172 infrastructure/behavior/presentation source changes, and the remaining original routes, anchors, references, values, unchanged source, or private baseline records. The latest rebuilt-site report passes all 22 preservation checks. These categories do not imply every record is public prose or that every changed behavior has been independently tested.

## Limits of the evidence

Source text/markers, exact document/dependency hashes, route reachability, route HTTP responses, rendered anchors, local asset responses, and rendered preserved text are distinct checks. Source capture status is never represented as runtime success. The JSON report records whether loopback verification actually ran and includes the exact unresolved IDs if any.

This tooling cannot establish external link availability, production parity, visual polish, keyboard/screen-reader quality, actual employment impact, or JavaScript behavior. Those remain separate implementation/review tasks. Edited metadata, control markup, and technical source changes are listed as changes requiring their own review, rather than described as unchanged behavior.

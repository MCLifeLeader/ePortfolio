# Information architecture and traceability

Implementation complete; evidence is recorded in [the implementation review](12-implementation-review.md), [technical report](technical-work.md), and [preservation report](traceability-work.md). The audit's proposed areas are a starting point; define concrete destinations before significant page restructuring.

## A01 — Site map, navigation, and compatibility plan

- [x] Specify the homepage and Architecture & Governance, AI & Innovation, Engineering & Technology, Leadership & Mentoring, Projects & Accomplishments, Professional Experience, Education & Professional Development, and About/Personal/Community areas.
- [x] Assign each existing page, including placeholders, coursework, historical projects, and pages outside primary navigation, an accessible destination.
- [x] Decide which areas need new landing pages and which can reuse current routes.
- [x] Account for all 44 source-derived route aliases and 30 anchors with retained routes or explicit compatibility mappings.
- [x] Specify menu hierarchy, supporting navigation, and entry points for every project, download, historical subsection, and personal perspective.

**Outputs:** A concrete site map and original-to-final route/anchor table. No route should disappear because its page is absent from the primary menu.

**Done when:** Every original route and substantive section has a destination and a discoverable path; the map supports professional positioning while retaining the complete history. Depends on I01.

## A02 — Fixed baseline and implementation mapping

- [x] Preserve the original 3,150 inventory IDs and baseline fields unchanged.
- [x] Add a separate migration ledger keyed by ContentID with revised file/section/anchor, factual review disposition, implementation status, and validation evidence.
- [x] Distinguish public content, unchanged vendor assets, inactive source history, process requirements, and withheld supplied claims in the ledger.
- [x] Record owner-authorized public removal of Upwork/contract-work solicitation and availability, and the directed Scrum certification presentation change, using the October 8 decision record as evidence. Preserve the original baseline information.
- [x] Document many-to-one consolidation and one-to-many distribution so all original facts remain accounted for.
- [x] Define how unchanged downloads retain binary identity and how new resume content supplements historical files.

**Outputs:** A migration ledger and coverage rules supporting the final preservation report.

**Done when:** Every baseline ID has an explicit disposition; proposed, implemented, and verified statuses are distinct; capture status is never mistaken for successful migration. Depends on A01.

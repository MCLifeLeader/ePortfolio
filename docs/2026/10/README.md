# ePortfolio modernization tasks

Created October 8, 2026. This backlog breaks the modernization into reviewable tasks; it does not begin page restructuring. The local inventory is complete. **33 follow-up tasks remain open. R04 employment disclosure review is complete.**

The fixed baseline is [the content audit](../../content-audit/README.md), including the [preservation matrix](../../content-audit/preservation-matrix.csv) and [owner review findings](../../content-audit/owner-review.md). Document links remain ignored. Deployed-site parity and external target availability are unverified and outside the current scope; do not mark them tested or follow those links without a changed instruction.

## Task index

| ID | Task | Status | Depends on |
|---|---|---|---|
| I01 | Local inventory and preservation proposals | Done | — |
| R01 | Resolve role titles and transition dates | Current roles confirmed; contract title unanswered | I01 |
| R02 | Resolve degree/resume discrepancy | Graduation year confirmed; application pending | I01 |
| R03 | Resolve skill durations, levels, availability | Solicitation removal authorized; retain recorded skill levels | I01 |
| R04 | Review employer/private AI claims and disclosure | Done: all 52 employment items approved and integrated | I01 |
| R05 | Clarify quantitative outcome scope | Pipeline creation clarified; retain other historical wording | I01 |
| R06 | Clarify Family Key timeline | Timeline confirmed; application pending | I01 |
| R07 | Contextualize historical project status | No updates; historical treatment confirmed | I01 |
| R08 | Preserve resume-only history and credential status | Credential wording confirmed; mapping/application pending | I01 |
| F01 | Establish isolated implementation and recovery baseline | Open | I01 |
| F02 | Align and verify existing .NET build/runtime configuration | Open | F01 |
| F03 | Fix three local filename case mismatches | Open | F01 |
| F04 | Repair malformed markup and preserve source encoding | Open | F01 |
| A01 | Specify site map, navigation, route/anchor compatibility | Open | I01 |
| A02 | Establish implementation traceability for every inventory ID | Open | A01 |
| C01 | Draft Architecture & Governance content | Open | A02 |
| C02 | Revise AI & Innovation content | Open | A02; R04 for affected claims |
| C03 | Organize complete engineering and QA history | Open | A02; R03 for current levels |
| C04 | Organize leadership, mentoring, and development material | Open | A02; R01/R05/R07/R08 where affected |
| C05 | Organize every project and repository description | Open | A02; R05/R06/R07 where affected |
| C06 | Reconcile professional experience | Open | A02; R01/R03/R05 where affected |
| C07 | Organize education and coursework | Open | A02; R02 |
| C08 | Preserve personal, entrepreneurial, and community content | Open | A02; R03/R07/R08 where affected |
| C09 | Rewrite focused homepage | Open | C01–C08; R01/R05 for selected claims |
| C10 | Update online resume and retain disconnected PDF | Open | C06/C07; R01/R02/R03/R08 |
| U01 | Implement shared design, navigation, and themes | Open | F01/F02; A01/A02; content tasks for pages implemented |
| U02 | Handle Contact, Privacy, and Error honestly | Open | F01/F02; A01/A02 |
| U03 | Implement metadata and asset presentation | Open | U01; F03/F04; C09 |
| V01 | Verify complete substantive preservation | Open | C01–C10; U01–U03 |
| V02 | Verify local routes, anchors, and downloads | Open | U01–U03; F03 |
| V03 | Verify accessibility, responsive layouts, and behavior | Open | U01–U03 |
| V04 | Verify build, browser behavior, performance, and reports | Open | F02; V01–V03 |
| D01 | Prepare reviewable change and final issue list | Open | V04 |
| D02 | Obtain explicit production deployment approval | Open: approval required | D01 |
| D03 | Deploy, verify, and retain rollback | Open | D02 |

## Detailed task files

- [01 — Factual and publication decisions](01-factual-review.md)
- [02 — Repository and technical foundations](02-technical-foundations.md)
- [03 — Information architecture and traceability](03-information-architecture.md)
- [04 — Content by section](04-content-modernization.md)
- [05 — Presentation and functionality](05-presentation-and-functionality.md)
- [06 — Validation](06-validation.md)
- [07 — Review and deployment](07-review-and-deployment.md)
- [08 — Owner decisions, October 8](08-owner-decisions.md)
- [09 — Approved employment accomplishments](09-employment-accomplishments-review.md)
- [10 — Employment content integration and validation](10-employment-integration.md)

## Execution rules

Start with F01–F04 and the architecture proposal A01–A02. Owner decisions can be collected alongside this work. A review item blocks only the claim it affects: retain historical wording or withhold a new unverified claim while progressing on supported content. R04 can be satisfied by an explicit decision to keep supplied employer claims in planning only; it does not require their publication.

Implement one section at a time after its content mapping is concrete. Preserve the existing ASP.NET Core Razor Pages architecture unless a documented technical need justifies changing it. Preserve substantive information, asset identities, historical details, proficiency qualifiers, meaningful perspectives, and discoverability, subject to the explicit owner decisions in file 08. The owner has authorized discontinuing public Upwork/contract-work solicitation and removing expired wording from the certification presentation; original information remains in the audit baseline.

An open task becomes done only when its listed outputs and completion criteria are met. Record decisions, changed files, relevant ContentIDs, and validation evidence with the task. A proposed destination or captured baseline is not proof of successful migration. Do not regenerate the original inventory from revised pages or overwrite it with migration results.

Production approval is the final authorization step after the implementation is reviewable. This planning request authorizes the task breakdown; it does not authorize production deployment.

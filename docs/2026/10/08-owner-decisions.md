# Owner decisions — October 8, 2026

Evidence: the owner's answers in this conversation on October 8, 2026. These decisions supersede conflicting source text for future revisions. The original inventory, matrix, source snapshots, and downloads remain unchanged as the historical baseline.

| Review | Confirmed decision | Implementation treatment | Remaining issue |
|---|---|---|---|
| R01 | Engineering Manager: February 2021–February 2026. Sr. Software Architect (Portfolio Architect): February 2026–Present. | Apply these titles/dates consistently to biography, leadership, work history, and any revised resume. | The August 2020–February 2021 contract title was not answered; retain original SDET wording without inventing a correction. |
| R02 | Software Engineering bachelor's degree: graduated in 2020. The online resume is more current. | Correct the web education year from 2021 to 2020. Prefer owner-confirmed information and current online content over the older PDF where they conflict. | No new PDF resume was supplied; do not imply an updated file exists. |
| R03 | Discontinue details around Upwork/contract work. | Remove current Upwork solicitation, contract/side-work advertising, availability windows, and associated promotional links from public presentation. Preserve their original information in the audit baseline as an owner-authorized exception. | No new skill durations/proficiency were supplied; retain recorded qualifications without increasing years. Historical contract employment and entrepreneurial history remain career facts, not current solicitation. |
| R04 | The supplied employment details are direct records of current-employment work. The owner requests a list to scrub sensitive information. | All 52 items in the sensitivity review were subsequently approved for public use and integrated without fetching document links. | Disclosure review complete. Preserve the distinction between completed work, discussions, recommendations, and ongoing initiatives. |
| R05 | Pipelines can typically be created in hours. Pipeline execution duration varies by product and build/deployment complexity. | Describe pipeline creation effort separately from run duration. Do not advertise a universal execution time or turn the original comparison into a newly quantified speedup. | Other historical outcomes remain reported source statements; no new measurements or attribution were provided. |
| R06 | Family Key started around 2001; owner involvement began around 2002; partnership failure terminated it in 2005. | Use approximate inception/involvement dates and preserve the termination context and original non-launch statement. | None for the clarified timeline. |
| R07 | No updates to project statuses at this time. | Retain existing project descriptions with historical context; keep aspirations, prototypes, closures, and incomplete work distinct. | No new status claims are authorized. |
| R08 | Show when Scrum certification was earned; omit expired wording. Extra Class amateur radio license is current. No other credential updates. | State Scrum certification earned March 21, 2013, using the original recorded date; do not imply current Scrum certification. State current Extra Class amateur radio licensing per owner confirmation. Preserve the older expired-status statement in the baseline. | Resume-only information is now preserved in /Experience/ResumeHistory with historical qualifiers. |

## Approved wording for later content revision

- **Engineering Manager — February 2021 to February 2026.**
- **Sr. Software Architect (Portfolio Architect) — February 2026 to Present.**
- **Bachelor's degree in Software Engineering — graduated in 2020.**
- **I can typically create build and deployment pipelines in hours. Execution time depends on the product and the complexity of the build and deployment.**
- **Family Key began around 2001. I became involved around 2002, and the project ended in 2005 following a partnership failure.**
- **Scrum Master certification earned March 21, 2013.**
- **Current Extra Class licensed amateur radio operator, KB7PPB.**

These decisions were recorded before content application. Subsequent page changes are documented in the integration report; the original PDF remains unchanged. Preserve existing source qualifiers where the owner has not supplied an update.

## Subsequent presentation decisions

The owner explicitly requested retaining LinkedIn and GitHub connections and leaving the original Resume.pdf file in place while removing every link to it. These instructions supersede the earlier proposed historical-download links. Preserve the PDF byte identity and record its disconnected treatment in the migration ledger; do not offer a new or historical resume download without a later instruction.

## Disclosure review

Subsequently on October 8, 2026, the owner approved every item in the [employment accomplishments review](09-employment-accomplishments-review.md): “All of those look fine, proceed with using Employment accomplishments — sensitivity review.” All E01–E52 are cleared for use. The earlier R04 row records the decision state before this approval. Implementation and validation are recorded in [10-employment-integration.md](10-employment-integration.md). Production deployment has not been authorized or performed.

## Primary portrait update

The owner supplied Michael_Carey_Large.JPG and explicitly requested it as the primary image. Homepage and About Me now reference /content/images/Michael_Carey_Large.jpg. The supplied image is copied byte-for-byte; the earlier fbMichael_B_Carey.jpg remains unchanged as historical media. This supersedes the original two portrait references and their image-element records, while preserving the subject and alternative text.

## Remove remaining résumé entry points

The owner reiterated removal of résumé links. The running local pages had no Resume.pdf hyperlink, but Explore, Experience, and Fun still linked to /Experience/ResumeHistory. Those entry points were removed or redirected to the technical-experience page; the historical details remain discoverable under /Skills/TechnicalHistory, including personal achievements. Resume.pdf remains unchanged and disconnected. The previous historical page URL remains addressable for compatibility but has no page links.

## Library and icon update

The owner explicitly requested Bootstrap Icons and updates to Bootstrap, jQuery, and the LibMan-managed libraries. Dependency upgrades supersede byte-identity preservation for the affected wwwroot/lib/bootstrap, jquery, jquery-validate, and jquery-validation-unobtrusive vendor assets only; original versions/hashes remain in the fixed baseline. Historical document/media binaries remain unchanged. New libraries are restored locally and pinned in libman.json. Bootstrap Icons decorate existing visible labels, and jQuery Migrate is scoped to the validation partial to support the remaining unobtrusive-validator legacy APIs. No contact form is enabled.
## Final client-library scope and image presentation

The owner authorized removing unused LibMan resources while retaining Bootstrap and Bootstrap Icons. The final manifest contains Bootstrap 5.3.8 and Bootstrap Icons 1.13.2, with eight required files. Unused jQuery, migration and validation libraries and the unused validation partial are retired. This supersedes the intermediate library upgrade; original inventory records remain intact. Bootstrap navigation and galleries remain available.

The owner requested appealing, responsive image styling. Portraits use rounded frames, while article photos and diagrams retain their proportions with consistent borders, spacing and shadows. Gallery images remain contained within their frames. Intrinsic image dimensions and asynchronous decoding were added to the radio article without changing image files, alternative text or gallery order.

## Portfolio wiki reference

The owner supplied https://github.com/MCLifeLeader/ePortfolio/wiki and requested links from the root README and website. The shared footer and ePortfolio repository card now reference that URL. The wiki is intended as an alternate format of the website content; the owner plans to synchronize it after merging into main. No wiki contents were opened or edited. The root README now documents the application purpose, stack, local setup, build/package commands, content maintenance, and verification.

Release build and preservation checks passed. Eight browser cases verified desktop/mobile footer links in both themes with no overflow; local README links resolve. Evidence: [wiki-reference-verification.json](wiki-reference-verification.json). The temporary verification server was stopped.
## ICS employment, CES support and student systems

The owner clarified that they are an ICS (Information Communication Services) employee of The Church of Jesus Christ of Latter-day Saints with a direct assignment to support CES (Church Education Services) services and applications. Their Global Education work includes BYU-Pathway and Seminaries and Institutes. This is stated in Work History, Employment Accomplishments, About Me and the Global Education project entry; CES is identified as the supported education organization rather than the employer.

The owner also reported growing experience with Student Information Systems (SIS), helping develop and support student education, and use of Okta for identity. Work History, Employment Accomplishments and About Me reflect that experience while retaining the growing-experience qualifier. Okta was added to the current architectural role's technology list. No specific SIS vendor, deployment outcome, certification or hosted identity acceptance result was inferred.

ICS/CES clarification validation: Release build passed with zero warnings and errors. Source and rendered preservation checks passed, mapping all 3,150 baseline IDs with zero unexplained losses. The final rendered Work History, Employment Accomplishments, About Me and Projects pages were checked for the ICS assignment and both education portfolios; the first three also include growing SIS experience and Okta identity management. The temporary verification server was stopped.
## Skills, Okta and Zendesk clarification

The owner requested a review of every Skills section and addition of missing skills, explicitly including Docker and Podman. Separate Okta and Zendesk pages were requested. Okta experience consists of wiring OAuth and OpenID Connect into a starter application. Zendesk is a third-party platform used for help-center documentation and training; its integration connects internal services providing custom role-based access and is independent of Okta. These direct owner statements supplement the prior wiki references. See [17 — Skills review](17-skills-review.md).

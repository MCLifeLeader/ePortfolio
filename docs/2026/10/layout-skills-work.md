# Skills page layout work — October 8, 2026

All 13 Skills Razor pages were individually reorganized within the existing application. No external links were followed, no PDF links were added, and this thread did not edit CSS, JavaScript, shared layout, PageModels, or other content areas.

| Page | Layout treatment | Source text nodes retained | Original IDs retained | Original link attributes retained |
|---|---|---|---|---|
| AI.cshtml | Narrative headings indexed in compact side navigation; proficiency summary and original resources grouped in aside; original skill-specific prose and links retained. | 33 | 1 | 6 |
| CPlus.cshtml | Narrative headings indexed in compact side navigation; proficiency summary and original resources grouped in aside; original skill-specific prose and links retained. | 32 | 0 | 7 |
| CSharp.cshtml | Narrative headings indexed in compact side navigation; proficiency summary and original resources grouped in aside; original skill-specific prose and links retained. | 29 | 0 | 6 |
| Database.cshtml | Narrative headings indexed in compact side navigation; proficiency summary and original resources grouped in aside; original skill-specific prose and links retained. | 24 | 0 | 4 |
| DevOps.cshtml | Narrative headings indexed in compact side navigation; proficiency summary and original resources grouped in aside; original skill-specific prose and links retained. | 24 | 0 | 5 |
| Index.cshtml | Capability hub rebuilt as three distinct cards beneath retained architecture/engineering introduction and deeper-history links. | 19 | 1 | 6 |
| Java.cshtml | Narrative headings indexed in compact side navigation; proficiency summary and original resources grouped in aside; original skill-specific prose and links retained. | 16 | 0 | 2 |
| Leadership.cshtml | Role history arranged as a single readable timeline; original role anchors/dates retained; personality and strengths preserved; reading categories promoted to headings; training and audio resources moved to compact aside. | 160 | 10 | 37 |
| QA.cshtml | Full-width narrative within dominant reading column; indexed teaching sections with preserved test-case states, severity definitions, and manual/automated examples; summary and Selenium resource aside. | 59 | 0 | 1 |
| TechnicalHistory.cshtml | Two duration snapshots retained as captioned, horizontally scrollable tables; historical qualifications, employment, and personal sections indexed by a compact side navigation. | 163 | 4 | 6 |
| Technologies.cshtml | Dominant narrative column for current profile, public work, language foundation, and career alignment; compact focus/repository aside; nine skill detail cards; recorded technical-history link retained. | 89 | 1 | 26 |
| Web.cshtml | Narrative headings indexed in compact side navigation; proficiency summary and original resources grouped in aside; original skill-specific prose and links retained. | 23 | 0 | 4 |
| WebApi.cshtml | Narrative headings indexed in compact side navigation; proficiency summary and original resources grouped in aside; original skill-specific prose and links retained. | 23 | 0 | 4 |

## Validation and handoff

Before writing each page, normalized content-bearing source text nodes, original IDs, and original href / asp-page / asp-fragment destinations were checked against the revised source. All passed. These checks confirm preservation and source structure, not rendered usability. Original names, dates, qualifications, book authors/categories, technical descriptions, and source comments remain. Empty dynamic Message headings were removed; model code does not populate Message. Paragraphs containing lists or headings were changed to neutral prose containers to repair invalid HTML. Top-level narrative headings now follow h1 with h2, with subordinate h3 headings. Existing page directives and PageModels remain.

Shared CSS must support page-header, page-kicker, reading-layout, reading-main, reading-aside, content-panel, section-nav, tag-list, resource-list, project-grid, project-card, timeline, timeline-entry, and prose. Final build, rendered checks, mobile overflow checks, theme contrast, and integrated preservation coverage are root responsibilities.

A second source check confirmed balanced div / section / aside / nav / ul / ol / table / p tags and no duplicate IDs on all 13 pages. Sidebar repository and external-resource links now use semantic resource lists without button styling; original destinations and link labels remain.

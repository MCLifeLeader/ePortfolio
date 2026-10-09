# Project and repository layout modernization — October 8, 2026

Scope: all nine Pages/Projects/*.cshtml pages and Pages/Git.cshtml. Shared styles, scripts, layout, configuration, models, assets and build commands are owned by the coordinator and were not changed here.

## Page treatment

- Projects index: 13 original entries retained in enterprise-delivery and independent-work card grids, including summaries without active detail links. Added clear access to the existing Startup, A Game Empowerment and repository pages.
- Git repositories: all 12 original entries retained in three groups: platform/developer foundations, portfolio/teaching, and programming/web coursework. Each card retains its complete description and every public repository/site link, with links grouped in semantic resource lists.
- AdverTran: product-history narrative beside the original summary/technology and links panels.
- A Game Empowerment: mentoring/SaaS narrative beside the full technology list; original historical-context note and service links retained.
- Azure Services: separate anchored Message Bus, Amy Email API and Dev Connect data-sync narratives, with the complete original technology list beside the data-sync section.
- Encompass: anchored product context, plugin development, SDK development and platform services sections. Development narratives sit beside their corresponding original technology lists.
- MLMLinkup: anchored 2016 and 2019 iterations with full narrative, collaborator attribution, recorded status and corresponding technology asides.
- Family Key: full timeline/partnership narrative and inactive-product statement beside its technical list.
- Redhead Mobile: retained the complete 2017 integration/licensing narrative, recorded status and all historical service/dashboard links.
- Startup: retained the work-in-progress explanation, forthcoming-detail statement and GitHub project link in a focused reading panel.

Each detail page has a concise contextual header and related links back to Projects and public repositories. Empty unassigned ViewData Message heading placeholders were removed after confirming no project/repository model assigns that value. Original substantive headings remain, with levels adjusted to fit the semantic page hierarchy. All technology lists were moved out of paragraph elements and no longer render as Bootstrap list-group walls.

## Preservation and verification

A temporary prechange source snapshot for these ten pages is stored as eportfolio-project-layout-baseline.json in the machine temporary directory. An exact normalized-text multiset comparison confirmed that every original substantive paragraph/list-item remains; a separate comparison confirmed every original href, asp-page, src and id remains, including original Razor-commented historical destinations. Original descriptive headings were also checked individually. Dates, metrics, technology names, collaborators, project status and full explanatory prose were retained without editorial shortening.

External URLs were retained as source data and never opened. No résumé PDF link was introduced. No binaries were changed. Source files are UTF-8. Build, browser rendering, responsiveness and final integration validation are handled by the coordinator against the new shared stylesheet.
## Final integrated layout validation

After the coordinator completed all 43 page layouts, reading-order corrections, local decorative icons, Bootstrap 5.3.8, jQuery 4 and corresponding validator/Migrate updates, final Chromium 151.0.7922.34 and Firefox 153.0 checks ran independently in parallel against the stable production-mode local server.

The merged layout-browser-verification.json records 516 page/layout cases (43 routes, three sizes, two themes, two browsers) and 4,516 passing assertions. There were no failed assertions, viewport overflow, page HTTP failures, broken images, or uncaught JavaScript errors. Assertions cover one h1, heading hierarchy, unique IDs, same-page anchors, absence of incoming Resume.pdf/ResumeHistory links, image alt attributes, actual first-in-DOM section navigation and narrow-screen navigation-before-main/resources-after layout, local icon font readiness/decorative accessibility, plus theme/storage, keyboard menu/skip-link, gallery and PDF flows. Fragment navigation within the directly accessed historical résumé route is permitted; that route is not offered through public page links.

The new layout-browser-verification.py, per-browser JSON files, merged JSON, and layout-screenshots/ preserve this checkpoint separately from the earlier browser-verification evidence. Twelve final homepage screenshots and thirteen representative project/repository/technical screenshots were saved. The mobile QA viewport was visually checked: its decorative icon, title, section navigation and narrative fit without clipping.

The final .NET 10 Linux Docker restore, Release build and publish passed with zero warnings/errors. Local image eportfolio-modernization:local manifest-list digest: 70f0ab5e76f92f63d7b7f5c905f4696c791fff95ef951cba32f6a2883d36dd68. No image push or deployment occurred.

All browser external requests were blocked. These headless local checks do not establish Safari/WebKit, physical-device or assistive-technology conformance, production performance, hosted workflow execution or deployed hosting behavior. Font readiness and alt-attribute presence checks do not independently judge the semantic quality of every icon/image description.
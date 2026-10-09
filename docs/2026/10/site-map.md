# Site map and compatibility plan — October 8, 2026

The original 44 aliases remain at their original routes. Supporting pages remain accessible through Explore, area indexes, and contextual links. No external targets have been fetched.

| Area | Landing / entry point | Supporting destinations |
|---|---|---|
| Homepage | `/` | Professional introduction, focus areas, LinkedIn and GitHub |
| Architecture & Governance | `/Architecture` | `/Experience/EmploymentAccomplishments`, quality, AI and DevOps details |
| AI & Innovation | `/Skills/AI` | Employer AI contributions and existing private product descriptions |
| Engineering & Technology | `/Skills` | Technology pages and `/Skills/TechnicalHistory` for original durations/proficiency |
| Leadership & Mentoring | `/Skills/Leadership` | Original role anchors, reading categories, historical mentoring goals |
| Projects & Accomplishments | `/Projects` | Every original project detail, `/Git`, employer accomplishments |
| Professional Experience | `/Experience` | `/Experience/WorkHistory`, accomplishments, `/Experience/ResumeHistory` |
| Education & Professional Development | `/Experience/Education` | `/College` and all three original coursework detail pages |
| About / Personal / Community | `/AboutMe` | `/Fun`, radio go-kit, Solarian League, `/Tribute`, civic and social links |
| Complete supporting directory | `/Explore` | Every original public page and retained public download; Resume.pdf stays disconnected |

New routes listed above are implementation targets; presence is checked below. The complete ledger distinguishes final source evidence from planned destinations.

## Original routes and aliases

| Original aliases | Area | Final source | Compatibility |
|---|---|---|---|
| `/AboutMe` | About / Personal / Community | `Src/Portfolio_Core/Portfolio/Pages/AboutMe.cshtml` | Retained in source |
| `/College/Cit261` | Education & Professional Development | `Src/Portfolio_Core/Portfolio/Pages/College/Cit261.cshtml` | Retained in source |
| `/College/Cs313` | Education & Professional Development | `Src/Portfolio_Core/Portfolio/Pages/College/Cs313.cshtml` | Retained in source |
| `/College/Cs364` | Education & Professional Development | `Src/Portfolio_Core/Portfolio/Pages/College/Cs364.cshtml` | Retained in source |
| `/College`<br>`/College/Index` | Education & Professional Development | `Src/Portfolio_Core/Portfolio/Pages/College/Index.cshtml` | Retained in source |
| `/Contact` | Homepage / Site utilities | `Src/Portfolio_Core/Portfolio/Pages/Contact.cshtml` | Retained in source |
| `/Error` | Homepage / Site utilities | `Src/Portfolio_Core/Portfolio/Pages/Error.cshtml` | Retained in source |
| `/Experience/Education` | Education & Professional Development | `Src/Portfolio_Core/Portfolio/Pages/Experience/Education.cshtml` | Retained in source |
| `/Experience`<br>`/Experience/Index` | Professional Experience | `Src/Portfolio_Core/Portfolio/Pages/Experience/Index.cshtml` | Retained in source |
| `/Experience/WorkHistory` | Professional Experience | `Src/Portfolio_Core/Portfolio/Pages/Experience/WorkHistory.cshtml` | Retained in source |
| `/Fun/HamRadioVHFGoKit` | About / Personal / Community | `Src/Portfolio_Core/Portfolio/Pages/Fun/HamRadioVHFGoKit.cshtml` | Retained in source |
| `/Fun`<br>`/Fun/Index` | About / Personal / Community | `Src/Portfolio_Core/Portfolio/Pages/Fun/Index.cshtml` | Retained in source |
| `/Fun/SolarianLeague` | About / Personal / Community | `Src/Portfolio_Core/Portfolio/Pages/Fun/SolarianLeague.cshtml` | Retained in source |
| `/Git` | Projects & Accomplishments | `Src/Portfolio_Core/Portfolio/Pages/Git.cshtml` | Retained in source |
| `/`<br>`/Index` | Homepage / Site utilities | `Src/Portfolio_Core/Portfolio/Pages/Index.cshtml` | Retained in source |
| `/Privacy` | Homepage / Site utilities | `Src/Portfolio_Core/Portfolio/Pages/Privacy.cshtml` | Retained in source |
| `/Projects/AdverTran` | Projects & Accomplishments | `Src/Portfolio_Core/Portfolio/Pages/Projects/AdverTran.cshtml` | Retained in source |
| `/Projects/AGameEmpowerment` | Projects & Accomplishments | `Src/Portfolio_Core/Portfolio/Pages/Projects/AGameEmpowerment.cshtml` | Retained in source |
| `/Projects/AzureServices` | Projects & Accomplishments | `Src/Portfolio_Core/Portfolio/Pages/Projects/AzureServices.cshtml` | Retained in source |
| `/Projects/Encompass` | Projects & Accomplishments | `Src/Portfolio_Core/Portfolio/Pages/Projects/Encompass.cshtml` | Retained in source |
| `/Projects/FamilyKey` | Projects & Accomplishments | `Src/Portfolio_Core/Portfolio/Pages/Projects/FamilyKey.cshtml` | Retained in source |
| `/Projects`<br>`/Projects/Index` | Projects & Accomplishments | `Src/Portfolio_Core/Portfolio/Pages/Projects/Index.cshtml` | Retained in source |
| `/Projects/MlmLinkup` | Projects & Accomplishments | `Src/Portfolio_Core/Portfolio/Pages/Projects/MlmLinkup.cshtml` | Retained in source |
| `/Projects/RedheadMobile` | Projects & Accomplishments | `Src/Portfolio_Core/Portfolio/Pages/Projects/RedheadMobile.cshtml` | Retained in source |
| `/Projects/Startup` | Projects & Accomplishments | `Src/Portfolio_Core/Portfolio/Pages/Projects/Startup.cshtml` | Retained in source |
| `/Skills/AI` | AI & Innovation | `Src/Portfolio_Core/Portfolio/Pages/Skills/AI.cshtml` | Retained in source |
| `/Skills/CPlus` | Engineering & Technology | `Src/Portfolio_Core/Portfolio/Pages/Skills/CPlus.cshtml` | Retained in source |
| `/Skills/CSharp` | Engineering & Technology | `Src/Portfolio_Core/Portfolio/Pages/Skills/CSharp.cshtml` | Retained in source |
| `/Skills/Database` | Engineering & Technology | `Src/Portfolio_Core/Portfolio/Pages/Skills/Database.cshtml` | Retained in source |
| `/Skills/DevOps` | Engineering & Technology | `Src/Portfolio_Core/Portfolio/Pages/Skills/DevOps.cshtml` | Retained in source |
| `/Skills`<br>`/Skills/Index` | Engineering & Technology | `Src/Portfolio_Core/Portfolio/Pages/Skills/Index.cshtml` | Retained in source |
| `/Skills/Java` | Engineering & Technology | `Src/Portfolio_Core/Portfolio/Pages/Skills/Java.cshtml` | Retained in source |
| `/Skills/Leadership` | Leadership & Mentoring | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | Retained in source |
| `/Skills/QA` | Engineering & Technology | `Src/Portfolio_Core/Portfolio/Pages/Skills/QA.cshtml` | Retained in source |
| `/Skills/Technologies` | Engineering & Technology | `Src/Portfolio_Core/Portfolio/Pages/Skills/Technologies.cshtml` | Retained in source |
| `/Skills/Web` | Engineering & Technology | `Src/Portfolio_Core/Portfolio/Pages/Skills/Web.cshtml` | Retained in source |
| `/Skills/WebApi` | Engineering & Technology | `Src/Portfolio_Core/Portfolio/Pages/Skills/WebApi.cshtml` | Retained in source |
| `/Tribute` | About / Personal / Community | `Src/Portfolio_Core/Portfolio/Pages/Tribute.cshtml` | Retained in source |

## Original anchors

| ContentID | Owning page/template | Retained anchor |
|---|---|---|
| PAGE-Experience-Education-ANCHOR-001 | `Src/Portfolio_Core/Portfolio/Pages/Experience/Education.cshtml` | `#EarlySelfDirected` |
| PAGE-Experience-Education-ANCHOR-002 | `Src/Portfolio_Core/Portfolio/Pages/Experience/Education.cshtml` | `#BYUIdaho` |
| PAGE-Experience-Education-ANCHOR-003 | `Src/Portfolio_Core/Portfolio/Pages/Experience/Education.cshtml` | `#Associates` |
| PAGE-Experience-Education-ANCHOR-004 | `Src/Portfolio_Core/Portfolio/Pages/Experience/Education.cshtml` | `#SoftwareEngineering` |
| PAGE-Experience-WorkHistory-ANCHOR-001 | `Src/Portfolio_Core/Portfolio/Pages/Experience/WorkHistory.cshtml` | `#LDSChurch03` |
| PAGE-Experience-WorkHistory-ANCHOR-002 | `Src/Portfolio_Core/Portfolio/Pages/Experience/WorkHistory.cshtml` | `#AcademyMortgage` |
| PAGE-Experience-WorkHistory-ANCHOR-003 | `Src/Portfolio_Core/Portfolio/Pages/Experience/WorkHistory.cshtml` | `#AGameEmpowerment` |
| PAGE-Experience-WorkHistory-ANCHOR-004 | `Src/Portfolio_Core/Portfolio/Pages/Experience/WorkHistory.cshtml` | `#LDSChurch02` |
| PAGE-Experience-WorkHistory-ANCHOR-005 | `Src/Portfolio_Core/Portfolio/Pages/Experience/WorkHistory.cshtml` | `#SwipeClock` |
| PAGE-Experience-WorkHistory-ANCHOR-006 | `Src/Portfolio_Core/Portfolio/Pages/Experience/WorkHistory.cshtml` | `#LDSChurch01` |
| PAGE-Experience-WorkHistory-ANCHOR-007 | `Src/Portfolio_Core/Portfolio/Pages/Experience/WorkHistory.cshtml` | `#Microsoft` |
| PAGE-Experience-WorkHistory-ANCHOR-008 | `Src/Portfolio_Core/Portfolio/Pages/Experience/WorkHistory.cshtml` | `#CareyAndAssoc` |
| PAGE-Experience-WorkHistory-ANCHOR-009 | `Src/Portfolio_Core/Portfolio/Pages/Experience/WorkHistory.cshtml` | `#Kumusoft` |
| PAGE-Fun-HamRadioVHFGoKit-ANCHOR-001 | `Src/Portfolio_Core/Portfolio/Pages/Fun/HamRadioVHFGoKit.cshtml` | `#AllRadioParts` |
| PAGE-Shared-_Layout-ANCHOR-001 | `Src/Portfolio_Core/Portfolio/Pages/Shared/_Layout.cshtml` | `#ExperienceDropDown` |
| PAGE-Shared-_Layout-ANCHOR-002 | `Src/Portfolio_Core/Portfolio/Pages/Shared/_Layout.cshtml` | `#ProjectsDropDown` |
| PAGE-Shared-_Layout-ANCHOR-003 | `Src/Portfolio_Core/Portfolio/Pages/Shared/_Layout.cshtml` | `#CollegeDropDown` |
| PAGE-Shared-_Layout-ANCHOR-004 | `Src/Portfolio_Core/Portfolio/Pages/Shared/_Layout.cshtml` | `#SkillsDropDown` |
| PAGE-Shared-_Layout-ANCHOR-005 | `Src/Portfolio_Core/Portfolio/Pages/Shared/_Layout.cshtml` | `#themeLabel` |
| PAGE-Shared-_Layout-ANCHOR-006 | `Src/Portfolio_Core/Portfolio/Pages/Shared/_Layout.cshtml` | `#themeToggle` |
| PAGE-Skills-Leadership-ANCHOR-001 | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | `#SwEngArch` |
| PAGE-Skills-Leadership-ANCHOR-002 | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | `#EngMgr` |
| PAGE-Skills-Leadership-ANCHOR-003 | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | `#QAManager` |
| PAGE-Skills-Leadership-ANCHOR-004 | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | `#DevOpsManager` |
| PAGE-Skills-Leadership-ANCHOR-005 | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | `#DevManager` |
| PAGE-Skills-Leadership-ANCHOR-006 | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | `#ScrumMaster` |
| PAGE-Skills-Leadership-ANCHOR-007 | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | `#DevLead` |
| PAGE-Skills-Leadership-ANCHOR-008 | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | `#TwoYearMission` |
| PAGE-Skills-Leadership-ANCHOR-009 | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | `#PersonalityProfile` |
| PAGE-Skills-Leadership-ANCHOR-010 | `Src/Portfolio_Core/Portfolio/Pages/Skills/Leadership.cshtml` | `#Books` |

## New supporting routes

| Route | Source |
|---|---|
| `/Architecture` | `Src/Portfolio_Core/Portfolio/Pages/Architecture.cshtml` |
| `/Experience/EmploymentAccomplishments` | `Src/Portfolio_Core/Portfolio/Pages/Experience/EmploymentAccomplishments.cshtml` |
| `/Experience/ResumeHistory` | `Src/Portfolio_Core/Portfolio/Pages/Experience/ResumeHistory.cshtml` |
| `/Explore` | `Src/Portfolio_Core/Portfolio/Pages/Explore.cshtml` |
| `/Skills/TechnicalHistory` | `Src/Portfolio_Core/Portfolio/Pages/Skills/TechnicalHistory.cshtml` |

## Preservation and verification rules

- Original content IDs and baseline fields stay in docs/content-audit; this separate ledger records implementation destinations.
- Word/number matching tracks many-to-one reuse and one-to-many distribution across active public pages. Unmatched substantive text is reported, never called preserved merely because an archive exists.
- Owner-authorized factual corrections and retired solicitation links cite the decision record. Resume.pdf remains byte-identical with no page link; document-only facts receive supporting historical treatment.
- Vendor assets and document binaries use SHA-256 equality. Site CSS changes are classified separately and require visual checks.
- Inactive source, process requirements, and unapproved source context have private dispositions; they are not made public implicitly.
- A source route/anchor match does not prove an HTTP result. Use verify_modernization.py with a running localhost site for runtime evidence.

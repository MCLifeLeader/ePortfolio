# GitHub wiki synchronization — October 8, 2026

The owner requested that the same website content be replicated into the [project wiki](https://github.com/MCLifeLeader/ePortfolio/wiki), with navigation that is similar where useful. This request authorizes publishing the resulting portfolio wiki to `https://github.com/MCLifeLeader/ePortfolio.wiki.git`.

## Content scope

The website remains the content source. `sync_wiki.py` reads rendered local pages rather than publishing Razor source, shared templates, or private reference documents. The initial sync generates 46 public portfolio pages, `_Sidebar.md`, `_Footer.md`, and 73 referenced media files under `assets`.

The copy includes the introduction, architecture, employment accomplishments, work history, education and coursework, skills and technical history, leadership and reading lists, projects and repository references, personal interests, tribute, contact information, privacy page, and Explore directory. The error page and disconnected résumé-history page are excluded. The historical résumé PDF remains disconnected.

The sidebar groups pages into Portfolio, Engineering, Experience, Projects, and Explore. Each page retains its own section navigation and links to related content. Website page links are rewritten to their corresponding wiki destinations. Referenced images and downloadable resources are copied byte-for-byte into the wiki repository and linked through its raw-content URLs. LinkedIn, GitHub, existing book links, and other external references remain external links.

The generator updates its generated page set and preserves unrelated wiki pages. Review direct edits to generated wiki pages before running another sync; website content replaces those page files.

## Repeatable workflow

Run these commands from the repository root. Python dependencies are `beautifulsoup4`, `markdownify`, and `markdown`:

```powershell
python -m pip install beautifulsoup4 markdownify markdown
git clone https://github.com/MCLifeLeader/ePortfolio.wiki.git .wiki-sync
```

Run the website in another terminal. The normal HTTP launch profile serves port 5085:

```powershell
dotnet run --project Src/Portfolio_Core/Portfolio/Portfolio.csproj --launch-profile http
```

Generate and review the wiki:

```powershell
python docs/2026/10/sync_wiki.py --base-url http://localhost:5085 --wiki-dir .wiki-sync
git -C .wiki-sync diff --stat
git -C .wiki-sync diff
git -C .wiki-sync status --short
```

Open newly generated files for review as well; untracked file contents are absent from a regular Git diff. Commit and publish from the wiki repository after the review:

```powershell
git -C .wiki-sync add --all
git -C .wiki-sync commit -m "Synchronize portfolio content from website"
git -C .wiki-sync push origin HEAD
```

For subsequent syncs, pull the latest wiki changes first. Temporary verification may use a different local port, for example `--base-url http://localhost:5187`; the resulting wiki links should still reference the public website rather than localhost.

## Route-to-page mapping

| Website route | Wiki page | Title |
|---|---|---|
| `/AboutMe` | [AboutMe](https://github.com/MCLifeLeader/ePortfolio/wiki/AboutMe) | About Me |
| `/Architecture` | [Architecture](https://github.com/MCLifeLeader/ePortfolio/wiki/Architecture) | Architecture & Governance |
| `/College/Cit261` | [College-Cit261](https://github.com/MCLifeLeader/ePortfolio/wiki/College-Cit261) | CIT 261 |
| `/College/Cs313` | [College-Cs313](https://github.com/MCLifeLeader/ePortfolio/wiki/College-Cs313) | CS 313 |
| `/College/Cs364` | [College-Cs364](https://github.com/MCLifeLeader/ePortfolio/wiki/College-Cs364) | CS 364 |
| `/College/Index` | [College](https://github.com/MCLifeLeader/ePortfolio/wiki/College) | College |
| `/Contact` | [Contact](https://github.com/MCLifeLeader/ePortfolio/wiki/Contact) | Contact |
| `/Experience/Education` | [Experience-Education](https://github.com/MCLifeLeader/ePortfolio/wiki/Experience-Education) | Education |
| `/Experience/EmploymentAccomplishments` | [Experience-EmploymentAccomplishments](https://github.com/MCLifeLeader/ePortfolio/wiki/Experience-EmploymentAccomplishments) | Employment Accomplishments |
| `/Experience/Index` | [Experience](https://github.com/MCLifeLeader/ePortfolio/wiki/Experience) | Experience |
| `/Experience/WorkHistory` | [Experience-WorkHistory](https://github.com/MCLifeLeader/ePortfolio/wiki/Experience-WorkHistory) | Work History |
| `/Explore` | [Explore](https://github.com/MCLifeLeader/ePortfolio/wiki/Explore) | Explore the Portfolio |
| `/Fun/HamRadioVHFGoKit` | [Fun-HamRadioVHFGoKit](https://github.com/MCLifeLeader/ePortfolio/wiki/Fun-HamRadioVHFGoKit) | VHF / HF Ham Radio Go-Kit |
| `/Fun/Index` | [Fun](https://github.com/MCLifeLeader/ePortfolio/wiki/Fun) | Fun Projects |
| `/Fun/SolarianLeague` | [Fun-SolarianLeague](https://github.com/MCLifeLeader/ePortfolio/wiki/Fun-SolarianLeague) | Solarian League |
| `/Git` | [Git](https://github.com/MCLifeLeader/ePortfolio/wiki/Git) | Git Repo List |
| `/` | [Home](https://github.com/MCLifeLeader/ePortfolio/wiki/Home) | Michael B. Carey |
| `/Privacy` | [Privacy](https://github.com/MCLifeLeader/ePortfolio/wiki/Privacy) | Privacy |
| `/Projects/AdverTran` | [Projects-AdverTran](https://github.com/MCLifeLeader/ePortfolio/wiki/Projects-AdverTran) | AdverTran |
| `/Projects/AGameEmpowerment` | [Projects-AGameEmpowerment](https://github.com/MCLifeLeader/ePortfolio/wiki/Projects-AGameEmpowerment) | A Game Empowerment |
| `/Projects/AzureServices` | [Projects-AzureServices](https://github.com/MCLifeLeader/ePortfolio/wiki/Projects-AzureServices) | Azure Services |
| `/Projects/Encompass` | [Projects-Encompass](https://github.com/MCLifeLeader/ePortfolio/wiki/Projects-Encompass) | Ellie Mae Encompass |
| `/Projects/FamilyKey` | [Projects-FamilyKey](https://github.com/MCLifeLeader/ePortfolio/wiki/Projects-FamilyKey) | Family Key |
| `/Projects/Index` | [Projects](https://github.com/MCLifeLeader/ePortfolio/wiki/Projects) | Projects |
| `/Projects/MlmLinkup` | [Projects-MlmLinkup](https://github.com/MCLifeLeader/ePortfolio/wiki/Projects-MlmLinkup) | MLMLinkup |
| `/Projects/RedheadMobile` | [Projects-RedheadMobile](https://github.com/MCLifeLeader/ePortfolio/wiki/Projects-RedheadMobile) | Redhead Mobile Apps |
| `/Projects/Startup` | [Projects-Startup](https://github.com/MCLifeLeader/ePortfolio/wiki/Projects-Startup) | Startup Examples |
| `/Skills/AI` | [Skills-AI](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-AI) | AI Technologies |
| `/Skills/Containers` | [Skills-Containers](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-Containers) | Docker and Podman |
| `/Skills/CPlus` | [Skills-CPlus](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-CPlus) | C/C++ |
| `/Skills/CSharp` | [Skills-CSharp](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-CSharp) | C#, ASP.NET, .NET Core |
| `/Skills/Database` | [Skills-Database](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-Database) | Database |
| `/Skills/DeveloperEnablement` | [Skills-DeveloperEnablement](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-DeveloperEnablement) | Developer Enablement |
| `/Skills/DevOps` | [Skills-DevOps](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-DevOps) | Azure DevOps / VSTS / TFS |
| `/Skills/Index` | [Skills](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills) | Skills |
| `/Skills/Java` | [Skills-Java](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-Java) | Java |
| `/Skills/Leadership` | [Skills-Leadership](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-Leadership) | Leadership |
| `/Skills/Okta` | [Skills-Okta](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-Okta) | Okta, OAuth and OpenID Connect |
| `/Skills/QA` | [Skills-QA](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-QA) | Quality Assurance |
| `/Skills/SystemsIntegration` | [Skills-SystemsIntegration](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-SystemsIntegration) | Systems and API Integration |
| `/Skills/TechnicalHistory` | [Skills-TechnicalHistory](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-TechnicalHistory) | Technical experience record |
| `/Skills/Technologies` | [Skills-Technologies](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-Technologies) | Development Technologies |
| `/Skills/Web` | [Skills-Web](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-Web) | Web |
| `/Skills/WebApi` | [Skills-WebApi](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-WebApi) | Web API / REST Services |
| `/Skills/Zendesk` | [Skills-Zendesk](https://github.com/MCLifeLeader/ePortfolio/wiki/Skills-Zendesk) | Zendesk Integration |
| `/Tribute` | [Tribute](https://github.com/MCLifeLeader/ePortfolio/wiki/Tribute) | Tribute |

## Validation and publication

The [generated verification report](wiki-sync-verification.json) records every source route, wiki page, page title, text-token count, link count, image count, and preserved anchor, plus the SHA-256 hashes of 73 copied media files. Generation passed all four checks: Markdown text round-trip preservation, link/image preservation, section-anchor preservation, and cross-page fragment resolution. These checks compare the generated Markdown against rendered local public pages; they do not claim that GitHub's published rendering has been verified.

Published to the [ePortfolio wiki](https://github.com/MCLifeLeader/ePortfolio/wiki) in wiki commit `947bde49bf18c9e56c18ca3990a7e774813fbf61`. The wiki repository push succeeded. Navigation follows the website's major sections, with a wiki sidebar and footer.

Live Playwright MCP checks verified Home, Leadership, Technical History, the radio build guide, and Employment Accomplishments. All five returned HTTP 200, with no broken authored section links or loaded images. GitHub sanitizes custom anchors by lowercasing them and adding `user-content-`; generated fragment links account for this behavior. This live check samples five pages; the complete 46-page conversion and media preservation are checked locally.

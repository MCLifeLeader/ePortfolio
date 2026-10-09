# Michael Carey's ePortfolio

This repository contains Michael B. Carey's personal portfolio website for **mbcarey.com**. It documents portfolio architecture, engineering leadership, hands-on software delivery, quality engineering, AI-enabled development, and the experience behind that work.

The project began as a CS 308 Technical Communication assignment and has evolved into a professional portfolio, project archive, and record of continued learning.

**Alternate portfolio format:** [GitHub wiki](https://github.com/MCLifeLeader/ePortfolio/wiki)

The wiki is intended to present the same portfolio information in wiki format. After these changes are merged into `main`, the owner plans to synchronize the wiki with the website content. Visitors can then choose either format.

## What the site includes

- Architecture and governance principles grounded in maintainable systems and product delivery.
- Work history, education, and employment accomplishments, including full-stack production applications, shared application foundations, systems integrations, QA automation, and developer tooling.
- Engineering skills, AI experience, leadership, mentoring, and reading lists.
- Project case studies, public GitHub repositories, coursework, and personal interests.
- Responsive layouts, light and dark themes, Bootstrap Icons, accessible navigation, and responsive image presentation.

The site remains an evolving project. Historical projects and recorded experience retain their context alongside current work.

## Technology stack

| Area | Implementation |
|---|---|
| Application | C# / .NET 10 / ASP.NET Core Razor Pages |
| UI | Razor templates, custom CSS, Bootstrap 5.3.8 |
| Icons | Bootstrap Icons 1.13.2 |
| Browser behavior | Native JavaScript for theme preferences and navigation |
| Client libraries | LibMan, with build-time restoration |
| Containers | Multi-stage Linux Docker build using .NET 10 images |
| Development | Visual Studio, VS Code, and a .NET 10 Dev Container |
| Delivery configuration | Azure DevOps build/publish pipeline; GitHub Copilot setup workflow |

The current site serves file-based content and static assets without a database requirement. The Contact page directs visitors to LinkedIn and GitHub; its email form is inactive.

## Run locally

Install the .NET 10 SDK. Run these commands from the repository root:

```powershell
dotnet restore Portfolio.sln
dotnet build Portfolio.sln --configuration Debug
dotnet run --project Src/Portfolio_Core/Portfolio/Portfolio.csproj --launch-profile http
```

Open **http://localhost:5085**. Stop the running application with **Ctrl+C** before rebuilding if the executable is locked.

For HTTPS development, trust the development certificate and use the HTTPS profile:

```powershell
dotnet dev-certs https --trust
dotnet run --project Src/Portfolio_Core/Portfolio/Portfolio.csproj --launch-profile https
```

The HTTPS profile serves **https://localhost:7035** and **http://localhost:5085**. Visual Studio users can open `Portfolio.sln` and select the corresponding launch profile.

LibMan restores the libraries declared in [libman.json](Src/Portfolio_Core/Portfolio/libman.json) during the build. Generated files under `wwwroot/lib` are ignored by Git; initial restoration requires network access to the configured providers.

## Repository layout

| Path | Purpose |
|---|---|
| [Portfolio.sln](Portfolio.sln) | Solution entry point |
| [Src/Portfolio_Core/Portfolio](Src/Portfolio_Core/Portfolio) | Razor Pages application |
| [Pages](Src/Portfolio_Core/Portfolio/Pages) | Page content, page models, and shared layout |
| [wwwroot](Src/Portfolio_Core/Portfolio/wwwroot) | CSS, JavaScript, images, and historical documents |
| [.devcontainer](.devcontainer) | Container-based development setup |
| [devops](devops) | Azure DevOps build and artifact publishing configuration |
| [docs/content-audit](docs/content-audit) | Fixed content inventory and preservation baseline |
| [docs/2026/10](docs/2026/10) | Modernization tasks, decisions, source mappings, and validation evidence |

## Build and package

Create a Release build and publish output:

```powershell
dotnet build Portfolio.sln --configuration Release
dotnet publish Src/Portfolio_Core/Portfolio/Portfolio.csproj --configuration Release --output artifacts/publish
```

The Dockerfile expects `Src/Portfolio_Core` as its build context:

```powershell
docker build --file Src/Portfolio_Core/Portfolio/Dockerfile --tag eportfolio:local Src/Portfolio_Core
docker run --rm --publish 8080:80 eportfolio:local
```

Open **http://localhost:8080**. HTTPS requires hosting-specific certificate or reverse-proxy configuration.

The [Azure DevOps pipeline](devops/Project-Build.yml) builds and publishes artifacts. Deployment remains a separate action.

## Content maintenance and verification

Edit public content in `Pages`, shared styling in `wwwroot/css/site.css`, and browser behavior in `wwwroot/js/site.js`. Preserve existing routes, section anchors, substantive historical information, and original media unless an owner-approved change calls for otherwise. The historical résumé PDF remains stored without public page links.

The original content audit is fixed. Record subsequent content mappings and authorized changes in the separate migration ledger and decision documents.

With Python installed, run source preservation verification from the repository root:

```powershell
python docs/2026/10/verify_modernization.py --write-ledger
```

To also verify rendered pages, run the application with its HTTP profile in another terminal:

```powershell
python docs/2026/10/verify_modernization.py --write-ledger --base-url http://localhost:5085
```

Additional browser and contrast scripts under `docs/2026/10` use Python Playwright and installed browser engines. Their reports document the tested scope; the project currently has no dedicated .NET test project.

Read the [modernization task index](docs/2026/10/README.md), [layout review](docs/2026/10/14-layout-modernization-review.md), and [architectural delivery highlights](docs/2026/10/16-architecture-delivery-highlights.md) for implementation details and evidence. The [GitHub wiki](https://github.com/MCLifeLeader/ePortfolio/wiki) is also linked from the site's footer and ePortfolio repository entry.

## License

This repository includes an [MIT license](LICENSE).

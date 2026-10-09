# Technical foundation implementation — October 8, 2026

## Recovery and isolation (F01)

Work continued on the owner's existing implementation branch `feature/mbc/2026/10/08/history-update`, baseline commit `826067475cff6a3845c2c12aec3e9d9c0564c5fd`. Initial working-tree status was clean. The existing .NET 10 target and package versions in Portfolio.csproj were preserved unchanged. Separate files were assigned to parallel threads; no commit, push, or deployment was performed.

A byte-preserving copy of all tracked files existing before these technical edits, including audit documents and original media/document binaries, was archived outside the repository:

`C:\Users\MICHAE~1\AppData\Local\Temp\eportfolio-baseline-80db5d43f9ee4885b81dcd70bdc8523e.zip`

SHA256: `7234A64FA91DC37664F7EAF6DA1A0BE8BC5B8E365983E6BFD3290ABA3823C7A6`.

Restore individual relative-path files from this ZIP as needed; the baseline commit provides permanent tracked recovery. The ZIP is temporary machine-local storage and is not a durable off-machine backup. Parallel presentation/content changes may have started during the archive copy; the ZIP is guaranteed to precede this thread's focused technical mutations, while the commit is the exact complete preimplementation recovery point. The audit baseline was not regenerated.

The employment sensitivity review has owner approval for public claims. The source planning attachments, audit records, owner decisions, and employment mapping/review documents still contain internal planning context. None were copied to wwwroot or published. Repository publication requires reviewing planning files separately from website content.

## .NET 10 compatibility (F02)

Installed host SDKs include 10.0.303 and 10.0.401. The existing net10.0 project and package references were retained.

- Docker SDK and ASP.NET runtime images changed from 8.0 to 10.0.
- Docker explicitly sets ASPNETCORE_HTTP_PORTS=80 to match its existing exposed HTTP port. Modern ASP.NET images otherwise default to 8080; see [Microsoft's container port documentation](https://learn.microsoft.com/en-us/dotnet/core/compatibility/containers/8.0/aspnet-port). This documentation lookup did not follow any user-supplied document links.
- Copilot setup uses the 10.0.x SDK. Its root-level restore/build/test commands use the existing root Portfolio.sln.
- Devcontainer uses SDK 10.0, runtime settings 10.0, and TARGET net10.0. Its missing ./src/PostCreate.ps1 command was replaced with dotnet restore Portfolio.sln.
- No global.json was introduced: the project's target, CI SDK, and container SDK establish the required major version without locking the owner's installed SDK patch.

The existing Azure DevOps pipeline builds and publishes Portfolio.sln using the self-hosted default pool, then uploads a zipped drop artifact. It contains no release/deployment stage. The coordinator handles its SDK installation and stale VS Code debugger target. No assumptions were made about deployed production runtime, certificates, or container use.

Validation command:

`docker build --progress plain -f Src/Portfolio_Core/Portfolio/Dockerfile -t eportfolio-modernization:local Src/Portfolio_Core`

Docker Desktop's Linux engine completed restore, Release build (zero warnings, zero errors), publish, and final image creation successfully. The local image remained available for review. This build took its source snapshot before the other threads finished their presentation/content edits; final integrated build validation belongs to the coordinator.

The image was briefly started on loopback 127.0.0.1:5187 mapped to container port 80, then stopped and removed. HTTP 200 checks passed for /, /Tribute, /Fun/HamRadioVHFGoKit, /content/images/Image027.jpg, Bootstrap CSS and bundle JS, jQuery, jquery-validate, and jquery-validation-unobtrusive. LibMan's actual paths were verified from libman.json and the shared layout; a guessed /dist/ URL was discarded after a 404. All four libraries were present in the published image.

The production-mode local HTTP smoke logs included expected warnings about temporary Data Protection key storage and absence of an HTTPS certificate/port in this test container. Production reverse-proxy/TLS/key storage configuration was not changed or verified. The complete devcontainer feature installation and hosted GitHub/Azure workflow runs were not executed locally.

## Case-sensitive media (F03)

Only the equipment image reference at HamRadioVHFGoKit.cshtml line 130 changed: Image027.JPG to the existing Image027.jpg. The source BOM, remaining markup, prose, images, and image asset bytes were retained. The image and owning page returned HTTP 200 under Linux case-sensitive hosting.

Preservation IDs: PAGE-Fun-HamRadioVHFGoKit-REF-049 and PAGE-Fun-HamRadioVHFGoKit-ELEMENT-131. This is a source-reference repair; no binary rename or redirect was needed. Existing external bookmarks using the wrong asset casing are unverified. Resume.pdf remains present; no PDF page link was introduced.

## Lossless encoding (F04 portion)

Tribute.cshtml failed strict UTF8 decoding before the change. Its bytes were decoded as Windows-1252 and saved as UTF8 without any source-text edits. Exact ordinal decoded-string equality passed immediately after conversion, preserving all em dashes, curly quotes, apostrophes, paragraphs, markup, and historical content. The rendered Linux response contained the preserved Enemy’s punctuation and returned HTTP 200.

Preservation IDs: PAGE-Tribute and its VALUE/TEXT/ELEMENT/REF descendants retain their text and semantics. Leadership markup and other nested-list corrections are assigned to the content thread, so this report does not assert completion of every F04 criterion.

The five files assigned to this technical thread passed git diff --check, and the devcontainer JSON parsed successfully. Final integrated validation is recorded by the coordinator.
## Integrated browser validation

The coordinator announced use of the webapp-testing skill; its native Python Playwright reconnaissance/action workflow was followed. Browser evidence is in browser-verification.py, browser-verification.json, and browser-screenshots/ alongside this report.

The local production-mode server at http://localhost:5187 was tested with existing cached headless Chromium 151.0.7922.34 and Firefox 153.0. The Python package's expected browser revisions were absent, so installed cached revisions were selected explicitly; no browser installation or external-site browsing was needed.

All 43 discovered Razor page routes passed HTTP 200 in both browsers across desktop 1440x1000, tablet 768x1024, and mobile 375x812, in both light and dark themes: 516 page/layout cases. No document viewport overflow, broken page images, or uncaught JavaScript errors were found. All 44 interaction assertions passed: system theme, stored-theme reload, blocked-storage fallback/toggling, keyboard skip-link focus/activation, keyboard mobile-menu open/close and ARIA state, truthful contact/social links, production error copy, radio carousel Next, and three local coursework PDF responses with real PDF signatures. External network requests were blocked throughout; external targets were not followed.

The sweep identified Tribute's missing first-level heading. The coordinator added the heading without editing the original tribute prose; that change requires the final targeted post-restart check recorded by the coordinator. Live stylesheet color/contrast adjustments during the sweep were inspected separately by the coordinator. Browser timings include Playwright network-idle waits and local cached resources; they are not production performance measurements. Physical devices, Safari/WebKit, screen readers, hosted CI, and deployed production hosting were not verified.

Chromium desktop-light and mobile-dark homepage screenshots were visually inspected: navigation, text, actions, portrait, sections, social links and footer fit without clipping. Additional browser/size/theme screenshots remain available for review.
Final targeted verification after the coordinator's last server rebuild passed in both Chromium and Firefox, in both light and dark themes: Tribute displays its new Tribute h1; the historical Scrum button renders white text on rgb(0, 102, 94), matching the corrected contrast treatment. These eight additional assertions raise the total to 52 passing interaction/targeted assertions. The original 516-case layout sweep records the earlier missing Tribute h1 accurately; the final targeted checks in browser-verification.json document its correction. All 12 homepage screenshots were refreshed against the final server and stylesheet. The coordinator separately verified 2,806 contrast samples across all 43 routes and both themes.

The final integrated Docker restore/build/publish completed with zero warnings/errors after Tribute and button corrections. Local image eportfolio-modernization:local manifest-list digest: ef20d95d62edecf3da96b177ce0749a03018a25b0c0764ef1c3a612ca56df6fd. No image was pushed or site deployed.
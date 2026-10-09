---
name: website-wiki-sync
description: Synchronize this ePortfolio website's rendered public content to its GitHub wiki, preserving text, media, links, and section targets. Use for preparing, reviewing, or publishing portfolio wiki updates.
---

# Website to wiki synchronization

Use the website as the content source and the existing generator rather than rewriting portfolio prose or copying Razor files into the wiki. Run commands from the repository root.

## Repositories and scope

- Main repository: `https://github.com/MCLifeLeader/ePortfolio`.
- Wiki git repository: `https://github.com/MCLifeLeader/ePortfolio.wiki.git`.
- Public wiki: `https://github.com/MCLifeLeader/ePortfolio/wiki`.
- Local wiki checkout: `.wiki-sync/`, ignored by the main repository.
- Generator: [`docs/2026/10/sync_wiki.py`](../../../docs/2026/10/sync_wiki.py).
- Detailed workflow and initial route mapping: [`docs/2026/10/19-github-wiki-sync.md`](../../../docs/2026/10/19-github-wiki-sync.md). Read when changing mappings or investigating conversion behavior.

Preparation, main-repository changes, and wiki publication are distinct operations. Follow the user's requested scope and existing session authorization. Creating or invoking this skill alone does not authorize a wiki push. A request to synchronize or publish the wiki authorizes the corresponding wiki update; do not require a second confirmation when that authorization is already clear. Preview-only requests stop before publishing.

## Prepare a current local rendering

Inspect main-repository status and the requested source branch or commit. Use the intended website version; do not assume the live website or an old Release executable contains current edits. If source selection is ambiguous, prepare what can be reviewed and clarify the version before publication.

Install missing Python dependencies: `beautifulsoup4`, `markdownify`, and `markdown`. The website requires the .NET 10 SDK and its build-time LibMan restore. Start a fresh build and application instance from the intended source:

```powershell
dotnet run --project Src/Portfolio_Core/Portfolio/Portfolio.csproj --configuration Release --no-launch-profile --urls http://localhost:5187
```

Keep the process/session handle so it can be stopped afterward. Choose another unused local port if necessary and pass it to the generator. Reuse a running instance only after confirming that it serves the intended source. Do not stop unrelated user processes or leave an agent-started server running; a Portfolio executable left running can block later builds.

## Prepare the wiki checkout

Clone the separate wiki repository if the checkout is absent:

```powershell
git clone https://github.com/MCLifeLeader/ePortfolio.wiki.git .wiki-sync
```

For an existing checkout, inspect `git -C .wiki-sync status --short`, its current branch, and `git -C .wiki-sync remote -v`. Confirm its origin is the wiki repository above. Preserve local changes, including edits to generated pages; generation overwrites those files. With a clean checkout on its publication branch, fetch and pull with `--ff-only` before generation. The initial wiki branch is `master`; inspect the actual branch rather than assuming that it shares the main repository's branch name. If histories diverge, reconcile the specific changes before pushing; do not force-push.

## Generate and review

```powershell
python docs/2026/10/sync_wiki.py --base-url http://localhost:5187 --wiki-dir .wiki-sync
git -C .wiki-sync status --short
git -C .wiki-sync diff --stat
git -C .wiki-sync diff
```

The generator accepts localhost only. It exports public `@page` routes using rendered `<main>` content, excludes `Error` and `Experience/ResumeHistory`, and refuses a linked `resume.pdf`. Shared navigation, scripts, commented-out content, and interactive controls are not portfolio prose. Retain LinkedIn, GitHub, reading-list links, historical context, and all substantive public content.

Route naming: `/` becomes `Home`; section `/Index` routes become their section name; remaining slashes become hyphens, for example `/Experience/WorkHistory` becomes `Experience-WorkHistory`. The wiki sidebar follows Portfolio, Engineering, Experience, Projects, and Explore. It need not duplicate the website's navigation layout. Unrelated wiki pages and assets are preserved; route removals require an explicit review because the generator does not delete stale files.

Images and downloadable resources are copied byte-for-byte under `assets/` and referenced through `https://raw.githubusercontent.com/wiki/MCLifeLeader/ePortfolio/`. Do not use main-repository raw URLs or relative wiki attachment URLs. Original IDs are emitted as named anchors, while links use GitHub's sanitized `#user-content-` prefix and lowercase target, for example `#user-content-books`.

Use `wwwroot/content/images/fbMichael_B_Carey.jpg` for Michael's portrait on all wiki pages that show his image. This owner-approved wiki presentation choice is applied by the generator; the website's portrait remains independently maintained.

The Home/default wiki page begins with a synchronization record: the remote `main` SHA checked at generation, the actual rendered source SHA (and whether application edits were uncommitted), and the selected portrait `fbMichael_B_Carey.jpg`. The generator queries GitHub for `refs/heads/main` and records these fields in the verification JSON too. Treat the Home note as the previous sync checkpoint, not a continuously updated live branch reference. On a new sync request, compare it with the current remote `main` and inspect changes from the recorded rendered source to the intended source. Do not label a feature-branch sync as content copied from `main`, or advance the rendered-source checkpoint after a metadata-only edit. Confirm the note and portrait are correct before publishing.

Read the newly written `docs/2026/10/wiki-sync-verification.json`, not an old successful report after a failed run. It records source commit, route mapping, media hashes, text-token round-trip checks, link/image counts, preserved anchors, and cross-page fragment checks. The first sync had 46 content pages and 73 assets; these are historical counts, not limits on future additions. Inspect new untracked files separately because normal `git diff` omits them. Check reading lists, captions, historical tables, image galleries, and adjacent links for readable Markdown formatting. A failed conversion may leave a partially updated checkout; resolve the cause and rerun successfully before staging.

## Commit, publish, and verify

After review, stage only the intended generated wiki changes. Inspect `git -C .wiki-sync diff --cached --check` and the staged diff, including new files and media. Commit in the wiki checkout. When publication is authorized, push its inspected publication branch without force, for example:

```powershell
git -C .wiki-sync commit -m "Synchronize portfolio content from website"
git -C .wiki-sync push origin HEAD
```

If there are no wiki changes, confirm the local HEAD matches the remote instead of making an empty commit. If the push is rejected because the remote moved, fetch, review incoming edits, and reconcile them; stop before overwriting conflicting content. Other publication failures should be reported with the specific blocker rather than treated as success.

Verify the remote SHA and clean checkout. Check representative live wiki pages using available browser tools: Home, Leadership, Technical History, Employment Accomplishments, and a media-heavy page such as the radio build guide. Check HTTP success, authored section-link targets, and image loading. GitHub generates its own heading permalinks; distinguish those from the generator's custom section links. Refresh or use a cache-busting query when checking just-pushed updates. Local conversion checks alone do not establish that GitHub rendered the pages correctly.

Record the published wiki commit and actual verification scope in the synchronization documentation. Update the live verification evidence when performing new live checks; do not relabel historical results as current. Commit generator/documentation/report changes separately in the main repository when they are part of the requested task. A main-repository push does not publish wiki changes, and a wiki push does not deploy the website.

Stop any application instance started for this task. Report the wiki URL, commit, verification results, and any remaining publication blocker. For preview-only work, identify the prepared checkout and explicitly state that it was not published.

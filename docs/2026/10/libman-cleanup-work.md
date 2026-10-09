# LibMan resource cleanup — October 8, 2026

The final LibMan manifest retains only Bootstrap 5.3.8 and Bootstrap Icons 1.13.2, using the already verified current releases. Unused jQuery, jQuery Migrate, jQuery Validation, and jQuery Unobtrusive Validation were removed from the manifest and disk. The unused Pages/Shared/_ValidationScriptsPartial.cshtml was removed; no page invoked it, and the Contact form remains inactive.

## Retained resources

| Library | Provider | Files under wwwroot/lib |
|---|---|---|
| Bootstrap 5.3.8 | cdnjs | bootstrap/css/bootstrap.min.css; bootstrap/css/bootstrap.min.css.map; bootstrap/js/bootstrap.bundle.min.js; bootstrap/js/bootstrap.bundle.min.js.map |
| Bootstrap Icons 1.13.2 | unpkg | bootstrap-icons/font/bootstrap-icons.min.css; bootstrap-icons/font/fonts/bootstrap-icons.woff; bootstrap-icons/font/fonts/bootstrap-icons.woff2; bootstrap-icons/LICENSE |

The bundle includes Bootstrap's required Popper support. Only the active minified CSS and JavaScript and their source maps remain; alternate Bootstrap builds, unminified variants, localization files, and obsolete validator dependencies were removed. The Icons CSS keeps its relative font paths and package license.

## Cleanup and verification

All deletion targets were resolved and verified inside C:/Code/git/ePortfolio/Src/Portfolio_Core/Portfolio/wwwroot/lib and the authorized workspace before native PowerShell Remove-Item operations. Active Bootstrap and Icons assets were retained throughout; no global LibMan clean was used. The unused partial's resolved path was separately verified inside the workspace.

LibMan restore completed successfully for the final two-library manifest, reporting files already up to date. Exactly eight vendor files remain. Before/after SHA256 checks confirm every retained asset is byte-identical. A source search across Pages, application JavaScript, and libman.json found no remaining jQuery or validation-partial references. See [libman-cleanup-verification.json](libman-cleanup-verification.json).

The earlier [LibMan upgrade report](libman-upgrade-work.md) and validator test results describe an intermediate checkpoint. That validator stack was subsequently removed under the owner's cleanup instruction; its test is superseded and is not a verification of the final deployed dependency set. No active forms were introduced. The root thread owns the final application build and integrated Bootstrap/Icons browser checks.

No production deployment was performed.

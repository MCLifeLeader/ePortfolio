# LibMan dependency upgrade — October 8, 2026

**Historical checkpoint, superseded by owner-requested cleanup.** The final manifest retains only Bootstrap and Bootstrap Icons. jQuery, Migrate, both validation packages, and the unused validation partial were subsequently removed. See [the final cleanup report](libman-cleanup-work.md). The validation checks below describe the intermediate upgrade only.

Updated the existing client-library restore configuration and validation partial; no package references, application framework, CSS, JavaScript application code, or shared layout were changed by this thread.

## Versions and primary sources

Versions were independently confirmed using the package authors' published latest records in the npm registry on October 8, 2026. Existing libraries retain their cdnjs providers and destination paths; their whole-library selection remains unchanged.

| Library | Previous | Updated | Release metadata |
|---|---|---|---|
| Bootstrap | 5.3.3 | 5.3.8 | [Author-published npm metadata](https://registry.npmjs.org/bootstrap/latest) |
| jQuery | 3.7.1 | 4.0.0 | [Author-published npm metadata](https://registry.npmjs.org/jquery/latest) |
| jQuery Validation | 1.20.0 | 1.22.1 | [Author-published npm metadata](https://registry.npmjs.org/jquery-validation/latest) |
| jQuery Unobtrusive Validation | 3.2.10 | 4.0.0 | [Author-published npm metadata](https://registry.npmjs.org/jquery-validation-unobtrusive/latest) |
| jQuery Migrate | New dependency | 4.0.2 | [Author-published npm metadata](https://registry.npmjs.org/jquery-migrate/latest) |
| Bootstrap Icons | New dependency | 1.13.2 | [Author-published npm metadata](https://registry.npmjs.org/bootstrap-icons/latest) |

Bootstrap Icons uses the unpkg provider because cdnjs does not offer the latest 1.13.2 release. Its selected files are font/bootstrap-icons.min.css, font/fonts/bootstrap-icons.woff, font/fonts/bootstrap-icons.woff2, and LICENSE. The stylesheet is available locally at /lib/bootstrap-icons/font/bootstrap-icons.min.css with the expected relative font paths.

## Compatibility

jQuery Validation 1.22.1 declares support for jQuery 4 in its peer dependencies. jQuery Migrate 4.0.2 declares jQuery >=4 <5. The restored Unobtrusive Validation 4.0.0 source still calls $.isFunction, $.proxy, and $.parseJSON. jQuery Migrate restores those compatibility APIs. The validation partial therefore loads jQuery, Migrate, Validation, then Unobtrusive Validation, in that order. These dependencies are scoped to the validation partial rather than globally loaded on every page.

The partial paths are /lib/jquery/jquery.min.js, /lib/jquery-migrate/jquery-migrate.min.js, /lib/jquery-validate/jquery.validate.min.js, and /lib/jquery-validation-unobtrusive/jquery.validate.unobtrusive.min.js. Existing public Contact behavior remains disabled; no form submission was activated.

## Restore and verification

LibMan CLI 3.0.71 restored all six libraries successfully from Src/Portfolio_Core/Portfolio in 6.14 seconds. Updated files are libman.json, Pages/Shared/_ValidationScriptsPartial.cshtml, and restored files under wwwroot/lib/bootstrap, jquery, jquery-validate, jquery-validation-unobtrusive, jquery-migrate, and bootstrap-icons.

Using the webapp-testing skill, a native Python Playwright Chromium test loaded the restored files from the already-running local application at http://localhost:5187. External network requests were blocked. The test replaced its own browser tab's DOM with an isolated, in-memory fixture and performed no submission. Required empty fields were rejected; invalid email and unequal confirmation were rejected; valid values were accepted. Unobtrusive parsing and restored compatibility APIs worked, with no JavaScript errors. Bootstrap 5.3.8 CSS, Icons CSS, and the woff2 font returned HTTP 200. The public Contact page still rendered no active form or submit control.

All seven checks passed. Reproducible script: [libman-validation-verification.py](libman-validation-verification.py). Results: [libman-validation-verification.json](libman-validation-verification.json). The plugin's validation version is not exposed as $.validator.version; the served script header independently reports 1.22.1.

Final application rebuild, integrated page/Bootstrap behavior checks, and Bootstrap Icons presentation remain the root thread's integration responsibilities. No deployment was performed.

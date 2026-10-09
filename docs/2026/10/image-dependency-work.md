# Final image and dependency regression — October 8, 2026

The final local server was checked after image presentation updates and the minimal LibMan configuration. This targeted regression supplements the preserved full 43-page layout checkpoint.

Home, About Me and the VHF/HF radio kit page passed 36 browser/viewport/theme cases: Chromium 151.0.7922.34 and Firefox 153.0; desktop 1440×1000, tablet 768×1024 and mobile 375×812; light and dark themes. All 265 assertions passed.

Checks verified successful page and image loading, alt attributes, viewport overflow, image bounds, natural aspect ratios where default fill applies, decorative local Bootstrap Icons and loaded icon fonts, radio gallery Next, and absence of jQuery network requests. No local resource HTTP errors or uncaught JavaScript errors were observed. The eight-file library tree matched Bootstrap 5.3.8 and Bootstrap Icons 1.13.2, without any jQuery files.

Evidence: image-dependency-verification.py, image-dependency-verification.json, and image-dependency-screenshots/ alongside this report. Forty-eight screenshots capture the three pages and gallery navigation states across the tested combinations. The final desktop-light homepage was visually inspected: its portrait renders at 320×390 with cover fit and rounded corners; navigation, actions, narrative panels and footer fit without clipping. The mobile-dark gallery state was also visually inspected.

The final .NET 10 Linux Docker restore, Release build and publish completed with zero warnings and zero errors. Local image eportfolio-modernization:local manifest-list digest: 234e9a57dfb24d02430b1d2bcc2b94a11708720c5ed654ed6ebea51fbd4da47a. No image push or deployment was performed.

External requests were blocked throughout. This regression does not establish physical-device, Safari/WebKit, assistive-technology or deployed-hosting behavior, and its local timings are not production performance measurements. Original media-byte preservation is covered by the coordinator's preservation audit rather than inferred from image rendering.
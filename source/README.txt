BACKUP SITE SOURCE CODE READ ME (Glamourless Systems, Nov 5 2026)

WHAT THIS IS
A backup copy of the four GS assessments (Start, Change, Choose, Fix) that does not depend on HighLevel, plus the code of the seven static pages on the systeme.io backup funnel.

WHERE IT LIVES
Assessments: GitHub Pages, free. Repository dsexton24-web/glamourless-backup (public, required for free Pages).
Live URLs: https://dsexton24-web.github.io/glamourless-backup/ then start.html, change.html, choose.html, fix.html, checkout.html.
Search engines blocked by robots.txt and a noindex tag on every page.
systeme.io pages: account a2ff-admin, funnel steps home, about, faq, contact, privacy-policy, terms, refund-policy. Code sits in each step's Page settings > Tracking > footer code. Static HTML and CSS only, no scripts (safe rule after the Nov 5 block).

HOW IT WAS MADE
The assessment code is copied byte for byte from the live HighLevel pages (the custom code element on each assessment page), Nov 5 2026. The Desktop folder GS Website Staging holds an OLDER version; do not use it for the backup.
Build script: Backup Site Build Script.py in this folder. It re-downloads the live pages and rebuilds the four assessment files.
Changes from live: same name-field order fix the live head script gs-name-later applies; the Fix page loads only its own styles; product links go to checkout.html instead of HighLevel.

CHECKOUT
checkout.html?sku=GS-XXXX looks up payhip-links.js. If the SKU has a Payhip URL it redirects there. If not, it shows the product code and asks the buyer to email admin@glamourlesssystems.com.
TO ADD A PAYHIP LINK: edit payhip-links.js in the repository, add "GS-0001":"https://payhip.com/b/XXXX", commit. Live in about a minute.

KNOWN GAPS
Lead capture still posts to the HighLevel webhook (same as live). If HighLevel is lost those leads stop arriving.
Payhip links not filled in yet (waiting on the store link).
Library, blueprint pages and checkout ladder are not part of this backup yet.

FILES IN THIS FOLDER
Backup Site All Source Code.txt: every file of the backup site and all seven systeme.io footer blocks in one file, each between START and END markers.
Backup Site Build Script.py: rebuilds the assessment pages from the live site.

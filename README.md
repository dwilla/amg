# amg

Static site for Acute Med Gas

All content and layouts should be copied from the current live site here: [AMG](https://www.acutemedgas.com/)

Using this repo template for laying out the codebase: [MGTI Codebase](https://github.com/dwilla/mgti)

## Tech

Static HTML built with [Bulma](https://bulma.io/) (via CDN), Font Awesome, and Google Fonts. No build dependencies beyond Python 3 — `build.py` stamps shared partials into each page template.

## Structure

```
src/
  partials/      reusable fragments: banner, header, nav, footer
  pages/         one source file per page (with <!-- include:* --> markers)
shared/
  styles.css     all custom styling (AMG brand colors + components)
build.py         stamps partials into pages, writes built HTML to repo root
*.html           generated output (do not edit by hand)
```

Each page source sets `data-page="<key>"` on `<body>`. `build.py` uses that key to
mark the matching nav link active, and `PAGE_GROUPS` to highlight the parent dropdown
for pages that live inside one.

## Building

```sh
python3 build.py
```

This regenerates every `*.html` at the repo root. Open `index.html` in a browser to view.

## Pages

- **Home** (`index.html`)
- **About Us** — About, Clients, Our Team, Our History, Memberships & Associations
- **Our Services** — overview, Testing & Verification, Consulting, Sales & Installation, Service & Maintenance
- **Products & Equipment**
- **Training** — overview, Classroom, Online, Customized
- **In The News** — overview, Speaking Engagements
- **Contact Us**

Content is adapted from the live site at https://www.acutemedgas.com/.

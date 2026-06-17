#!/usr/bin/env python3
"""Stamp shared partials into every page template and write built HTML to the root."""

import re
from pathlib import Path

SRC        = Path('src')
PARTIALS   = SRC / 'partials'
PAGES      = SRC / 'pages'
OUT        = Path('.')

# Pages that live inside a nav dropdown — maps data-page value → data-nav-group value
PAGE_GROUPS = {
    'about-page':     'about',
    'clients':        'about',
    'team':           'about',
    'history':        'about',
    'memberships':    'about',
    'services-page':  'services',
    'testing':        'services',
    'consulting':     'services',
    'sales':          'services',
    'maintenance':    'services',
    'training-page':  'training',
    'classroom':      'training',
    'online':         'training',
    'customized':     'training',
    'news-page':      'news',
    'speaking':       'news',
}


def partial(name: str) -> str:
    return (PARTIALS / f'{name}.html').read_text()


def build_nav(page_key: str) -> str:
    nav = partial('nav')

    # Activate the direct link matching this page
    def activate_link(m):
        tag = m.group(0)
        if f'data-nav="{page_key}"' not in tag:
            return tag
        return re.sub(r'class="([^"]*)"', lambda c: f'class="{c.group(1)} is-active"', tag, count=1)

    nav = re.sub(r'<a [^>]*data-nav="[^"]*"[^>]*>', activate_link, nav)

    # Activate the dropdown parent if this page lives inside one
    group = PAGE_GROUPS.get(page_key)
    if group:
        def activate_group(m):
            tag = m.group(0)
            if f'data-nav-group="{group}"' not in tag:
                return tag
            # Use a custom class — not is-active, which Bulma uses to force the dropdown open
            return re.sub(r'class="([^"]*)"', lambda c: f'class="{c.group(1)} is-current-section"', tag, count=1)
        nav = re.sub(r'<div [^>]*data-nav-group="[^"]*"[^>]*>', activate_group, nav)

    return nav


def build_page(src_file: Path) -> None:
    content = src_file.read_text()

    m = re.search(r'<body[^>]*data-page="([^"]*)"', content)
    page_key = m.group(1) if m else ''

    replacements = {
        'banner': partial('banner'),
        'header': partial('header'),
        'nav':    build_nav(page_key),
        'footer': partial('footer'),
    }

    for name, html in replacements.items():
        content = content.replace(f'<!-- include:{name} -->', html)

    out = OUT / src_file.name
    out.write_text(content)
    print(f'  {src_file.name}')


def main():
    pages = sorted(PAGES.glob('*.html'))
    if not pages:
        print('No pages found in src/pages/')
        return
    print(f'Building {len(pages)} pages...')
    for page in pages:
        build_page(page)
    print('Done.')


if __name__ == '__main__':
    main()

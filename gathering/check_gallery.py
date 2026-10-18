#!/usr/bin/env python3
"""Check static gallery records, ordering and local image/link targets offline."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from verify import jpeg_size

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'


class Gallery(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.cards, self.images, self.links = [], [], [], []
        self.external_dependencies = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'article':
            self.cards.append(attrs['id'])
        if tag == 'img':
            assert attrs.get('alt'), 'missing image alternative text'
            assert attrs.get('width') == attrs.get('height') == '512'
            self.images.append(attrs['src'])
        if tag == 'a':
            self.links.append(attrs['href'])
        if tag in ('script', 'link', 'iframe'):
            self.external_dependencies.append(tag)


def main():
    page = (DIST / 'index.html').read_text(encoding='utf-8')
    parsed = Gallery()
    parsed.feed(page)
    assert len(parsed.ids) == len(set(parsed.ids)), 'duplicate HTML id'
    assert not parsed.external_dependencies
    assert len(page.encode()) <= 100_000
    expected = []
    walls = {}
    for wall in ('gathering', 'line-1', 'line-2', 'line-3', 'line-4'):
        paths = sorted((DIST / wall).glob('[0-9][0-9].json'), reverse=True)
        painted, future = [], []
        for path in paths:
            record = json.loads(path.read_text())
            (future if record['name'] == 'Not painted yet' else painted).append(path)
        expected.extend(f'{wall}-{p.stem}' for p in painted + future)
        walls[wall] = {'painted': len(painted), 'future': len(future)}
    assert parsed.cards == expected, 'missing records or incorrect order'
    for src in parsed.images:
        target = (DIST / src).resolve()
        assert target.is_relative_to(DIST.resolve()) and target.is_file()
        assert jpeg_size(target.read_bytes()) == (512, 512)
    for href in parsed.links:
        if href.startswith('#'):
            assert href == '#' or href[1:] in parsed.ids
        elif href.startswith('https://'):
            assert re.fullmatch(r'https://api\.imd\.fun/artifacts/[0-9a-f]{64}', href)
        else:
            target = (DIST / href).resolve()
            assert target.is_relative_to(DIST.resolve()) and target.is_file(), href
    result = {'checks_passed': True, 'method': 'Python HTMLParser, record comparison and JPEG frame inspection; no browser or network',
              'numbered_cards': len(expected), 'local_image_references': len(parsed.images),
              'unique_local_previews': len(set(parsed.images)), 'walls': walls,
              'all_records_in_descending_painted_then_future_order': True,
              'all_local_links_and_previews_resolve': True, 'external_script_style_font_dependencies': 0,
              'html_bytes': len(page.encode()),
              'limitations': ['No browser layout, responsive rendering or accessibility certification is claimed.']}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

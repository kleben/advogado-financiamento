#!/usr/bin/env python3
"""Generate static SEO from confirmed configuration; never changes DNS or audience."""
import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]

def generate(config, directory):
    directory = Path(directory)
    page = directory / 'index.html'
    content = page.read_text()
    mode = config.get('mode')
    if mode not in ('review', 'production'):
        raise ValueError('mode must be review or production')
    public = mode == 'production'
    origin = config['production_url']
    parsed = urlsplit(origin)
    if (parsed.scheme != 'https' or parsed.hostname != 'advogadofinanciamento.com.br'
            or parsed.path != '/' or parsed.query or parsed.fragment or parsed.username
            or parsed.password or parsed.port):
        raise ValueError('Expected clean HTTPS production URL from the client brief')
    if public and not (config.get('domain_verified') is True and config.get('public_release_authorized') is True):
        raise ValueError('Production requires operational domain and authorized public release')
    tags = [] if public else ['<meta name="robots" content="noindex">']
    if public:
        tags.append(f'<link rel="canonical" href="{html.escape(origin, quote=True)}">')
    token = config.get('search_console_token')
    if public and token:
        if not re.fullmatch(r'[A-Za-z0-9_-]+', token):
            raise ValueError('Invalid Search Console HTML token')
        tags.append(f'<meta name="google-site-verification" content="{token}">')
    visible_address = ''
    business = config['business']
    if business.get('confirmed'):
        address = business.get('address') or {}
        keys = ('streetAddress', 'addressLocality', 'addressRegion', 'postalCode', 'addressCountry')
        if not all(isinstance(address.get(k), str) and address[k].strip() for k in keys):
            raise ValueError('Confirmed business requires complete real PostalAddress')
        if address['addressCountry'] != 'BR':
            raise ValueError('Expected Brazilian office')
        for key in ('name', 'telephone', 'email'):
            if not business.get(key):
                raise ValueError(f'Missing business {key}')
        if business['name'] != 'Alcântara Advogados' or business['telephone'] != '+558589414720' or business['email'] != 'advogadofortaleza@gmail.com':
            raise ValueError('Update visible branding/contact and validation before changing business identity')
        text = (f"{address['streetAddress']} — {address['addressLocality']} / "
                f"{address['addressRegion']} — CEP {address['postalCode']} — Brasil")
        visible_address = '<p class="office-address">'+html.escape(text)+'</p>'
        if public:
            schema = {
                '@context': 'https://schema.org', '@type': 'LegalService',
                '@id': origin+'#escritorio', 'name': business['name'], 'url': origin,
                'telephone': business['telephone'], 'email': business['email'],
                'address': {'@type':'PostalAddress', **{k: address[k] for k in keys}},
                'areaServed': [{'@type':'City','name':'Fortaleza'}, {'@type':'Country','name':'Brasil'}]
            }
            data = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
            tags.append('<script type="application/ld+json">'+data+'</script>')
    for name, value in [('SEO', '\n'.join(tags)), ('ADDRESS', visible_address)]:
        pattern = rf'<!-- {name}:START -->.*?<!-- {name}:END -->'
        if len(re.findall(pattern, content, flags=re.S)) != 1:
            raise ValueError(f'Expected one {name} managed block')
        content = re.sub(pattern, lambda _: f'<!-- {name}:START -->\n{value}\n<!-- {name}:END -->', content, flags=re.S)
    # All configuration validation occurs before any mutation.
    page.write_text(content)
    sitemap = directory/'sitemap.xml'
    if public:
        sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f'  <url><loc>{escape(origin)}</loc></url>\n</urlset>\n')
        (directory/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+origin+'sitemap.xml\n')
    else:
        # noindex remains readable to crawlers; real privacy is enforced by hosting.
        (directory/'robots.txt').write_text('User-agent: *\nAllow: /\n')
        sitemap.unlink(missing_ok=True)
    return {'mode':mode, 'canonical':public, 'sitemap':public,
            'legal_service':bool(public and business.get('confirmed'))}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT/'config/seo.json')
    parser.add_argument('--directory', type=Path, default=ROOT/'dist')
    args = parser.parse_args()
    try:
        print(json.dumps(generate(json.loads(args.config.read_text()), args.directory)))
    except (ValueError, KeyError) as exc:
        parser.exit(1, f'SEO configuration error: {exc}\n')

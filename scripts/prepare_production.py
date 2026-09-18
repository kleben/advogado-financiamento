#!/usr/bin/env python3
"""Generate root entrypoints for Hostinger from the Sites-compatible dist source."""
import json
import re
import shutil
import tempfile
from pathlib import Path
from prepare_seo import generate

ROOT=Path(__file__).resolve().parents[1]

def build():
    config=json.loads((ROOT/'config/seo-production.json').read_text())
    if config.get('mode')!='production':
        raise ValueError('Production configuration required')
    with tempfile.TemporaryDirectory() as temp:
        stage=Path(temp)
        shutil.copyfile(ROOT/'dist/index.html',stage/'index.html')
        generate(config,stage)
        content=(stage/'index.html').read_text()
        # CSS images resolve relative to their own stylesheet in dist/assets.
        content=re.sub(r'((?:src|href)=")assets/',r'\1dist/assets/',content)
        (ROOT/'index.html').write_text(content)
        for name in ('robots.txt','sitemap.xml'):
            shutil.copyfile(stage/name,ROOT/name)
    print('Generated root index.html, robots.txt and sitemap.xml for production.')

if __name__=='__main__':build()

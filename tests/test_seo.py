"""Offline contract checks; fixtures never enter dist or deployment."""
import copy
import importlib.util
import json
import re
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('seo',ROOT/'scripts/prepare_seo.py')
seo=importlib.util.module_from_spec(spec);spec.loader.exec_module(seo)

class SEOTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out=Path(self.temp.name)
        shutil.copy(ROOT/'dist/index.html',self.out/'index.html')
        self.config=json.loads((ROOT/'config/seo.json').read_text())
    def production(self):
        self.config.update(mode='production',domain_verified=True,public_release_authorized=True)
    def test_review_no_production_claims(self):
        seo.generate(self.config,self.out)
        html=(self.out/'index.html').read_text()
        self.assertIn('content="noindex"',html)
        self.assertNotIn('rel="canonical"',html)
        self.assertNotIn('application/ld+json',html)
        self.assertFalse((self.out/'sitemap.xml').exists())
    def test_production_blocked_until_confirmed(self):
        self.config['mode']='production'
        before=(self.out/'index.html').read_bytes()
        with self.assertRaises(ValueError):seo.generate(self.config,self.out)
        self.assertEqual(before,(self.out/'index.html').read_bytes())
    def test_clean_canonical_sitemap_and_idempotence(self):
        self.production();seo.generate(self.config,self.out)
        before=(self.out/'index.html').read_bytes()
        seo.generate(self.config,self.out)
        self.assertEqual(before,(self.out/'index.html').read_bytes())
        self.assertEqual(before.count(b'rel="canonical"'),1)
        self.assertNotIn(b'noindex',before)
        xml=ET.parse(self.out/'sitemap.xml')
        self.assertEqual([e.text for e in xml.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')],[self.config['production_url']])
        self.assertIn('Sitemap: '+self.config['production_url']+'sitemap.xml',(self.out/'robots.txt').read_text())
    def test_incomplete_address_fails_before_writing(self):
        self.production();self.config['business']['confirmed']=True
        before=(self.out/'index.html').read_bytes()
        with self.assertRaises(ValueError):seo.generate(self.config,self.out)
        self.assertEqual(before,(self.out/'index.html').read_bytes())
    def test_complete_fixture_schema_matches_visible_address(self):
        self.production();business=self.config['business'];business['confirmed']=True
        business['address']={'streetAddress':'TEST FIXTURE <script> & 123','addressLocality':'Fortaleza','addressRegion':'CE','postalCode':'00000-000','addressCountry':'BR'}
        seo.generate(self.config,self.out);html=(self.out/'index.html').read_text()
        data=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)[1])
        self.assertEqual(data['@type'],'LegalService')
        self.assertEqual(data['address']['streetAddress'],business['address']['streetAddress'])
        self.assertIn('TEST FIXTURE &lt;script&gt; &amp; 123',html)
        self.assertNotIn('aggregateRating',data)
    def test_reverting_review_removes_public_outputs(self):
        self.production();seo.generate(self.config,self.out)
        self.config['mode']='review';seo.generate(self.config,self.out)
        self.assertFalse((self.out/'sitemap.xml').exists())
        self.assertNotIn('rel="canonical"',(self.out/'index.html').read_text())
    def test_parameters_not_allowed_in_canonical(self):
        self.production();self.config['production_url']+='?utm_source=test'
        with self.assertRaises(ValueError):seo.generate(self.config,self.out)
    def test_html_assets_contacts_and_no_empty_verification(self):
        class Parse(HTMLParser):
            tags=[]
            def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
        parser=Parse();parser.feed((ROOT/'dist/index.html').read_text());tags=parser.tags
        self.assertEqual(sum(t=='h1' for t,a in tags),1)
        self.assertFalse(any(a.get('name')=='google-site-verification' and not a.get('content') for t,a in tags))
        contacts=[a for t,a in tags if a.get('data-contact')]
        self.assertEqual(len(contacts),9)
        for a in contacts:
            if a['data-contact']=='phone':self.assertEqual(a['href'],'tel:+558589414720')
            else:self.assertEqual(parse_qs(urlparse(a['href']).query)['text'][0],'Olá! Encontrei vocês pelo site e gostaria de tirar uma dúvida sobre o financiamento do meu veículo.')
        for t,a in tags:
            for key in ('src','href'):
                if a.get(key,'').startswith('assets/'):self.assertTrue((ROOT/'dist'/a[key]).is_file())
        self.assertEqual(sum('data-icon' in a for t,a in tags),sum(t=='svg' for t,a in tags))

if __name__=='__main__':unittest.main()

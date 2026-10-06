#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse, unquote
import csv, re

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'images' / 'projects'
OUT.mkdir(parents=True, exist_ok=True)

PROJECTS = [
    ('bonafide', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bc953a9d628c948d183fcf_hello-bonafide.jpg'),
    ('dry-farm-wines', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/668c2aca4165e3779f60c1f5_dfw_web-dark.jpg'),
    ('fair-harbor-clothing', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bdb34e9a701b062fbe9e0c_fairharbor-cover.jpg'),
    ('fort-eden', 'https://cdn.prod.website-files.com/638c3e829a16183d93ad3b5d/690a5d3e3e47cba04c2861f8_fort-eden.jpg'),
    ('fourtillfour-coffee', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bc5dd4aad4703e43e644cf_Screen%20Shot%202023-01-09%20at%2011.32.36%20AM.png'),
    ('frost', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bcec158d77f25b07312ffd_Cover%20(1).png'),
    ('glory-gains-gym', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bc9819588335d0aa6c5fa9_GGG-cover.jpg'),
    ('innbeauty', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bc5bd69d4b0457659909a2_Cover.png'),
    ('kate-mcleod', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bc804483a5bc1209f56592_KM-Mockup.jpg'),
    ('loops-beauty', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bc6be4db157d80692f6316_Loops_Mockup.jpg'),
    ('paper-plane', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bcf201c7e2f1aeb9015883_Screen%20Shot%202023-01-09%20at%2010.04.23%20PM.png'),
    ('rad-furniture', 'https://cdn.prod.website-files.com/638c3e829a16183d93ad3b5d/690a6021489e0cb7be6026ef_Rad_furniture.jpg'),
    ('rumpl', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bdb041a55d322ed8cf373b_rumpl-cover.jpg'),
    ('vb', 'https://uploads-ssl.webflow.com/638c3e829a16183d93ad3b5d/63bc8cac1cbb4debe622c6b1_vb-cover.jpg'),
    ('ordinary-habit', 'https://cdn.prod.website-files.com/638c3e829a16183d93ad3b5d/699779469b25a94cefe2ba30_Screenshot%202026-02-19%20at%2012.56.51%E2%80%AFPM.png'),
]

# A legacy Webflow-hosted social image is referenced on non-home pages.
LEGACY_OG = 'https://uploads-ssl.webflow.com/627b764dac68b05a1a0edfd0/628524907b7b700f4c690dd3_irene-opengraph-image.png'

def extension(url):
    ext = Path(unquote(urlparse(url).path)).suffix.lower()
    return ext if ext in {'.jpg','.jpeg','.png','.webp','.gif','.svg'} else '.jpg'

def download(url, dest):
    print(f'Downloading {dest.name}...')
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=60) as r, open(dest, 'wb') as f:
        f.write(r.read())

mapping = {}
for slug, url in PROJECTS:
    dest = OUT / f'{slug}{extension(url)}'
    download(url, dest)
    mapping[url] = f'images/projects/{dest.name}'

# Download the legacy OG asset too so no page depends on Webflow-hosted images.
og_dest = ROOT / 'images' / 'social-preview.png'
download(LEGACY_OG, og_dest)
mapping[LEGACY_OG] = 'images/social-preview.png'

for html in ROOT.glob('*.html'):
    text = html.read_text(encoding='utf-8')
    original = text
    for remote, local in mapping.items():
        text = text.replace(remote, local)
    if text != original:
        html.write_text(text, encoding='utf-8')
        print(f'Updated {html.name}')

print('\nDone. All portfolio CMS thumbnails and the legacy social image are local.')
print('You can verify remaining Webflow-hosted images with:')
print("  grep -R 'uploads-ssl.webflow.com\\|cdn.prod.website-files.com' *.html")

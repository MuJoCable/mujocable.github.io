"""Check bilingual navigation, resource paths and command parity without a browser."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.links=[]; self.lang=None
        self.feed(text)
    def handle_starttag(self, tag, pairs):
        attrs=dict(pairs)
        if tag=='html': self.lang=attrs.get('lang')
        if 'id' in attrs:self.ids.append(attrs['id'])
        for name in ('href','src','poster'):
            if name in attrs:self.links.append(attrs[name])

expected=[f'step-{i}' for i in range(16)]
sources=[]
for filename, language in [('index.html','en'),('zh.html','zh-CN')]:
    file=ROOT/'tutorials/windows'/filename
    text=file.read_text(encoding='utf-8'); page=Page(text)
    assert page.lang==language
    assert len(page.ids)==len(set(page.ids)), 'duplicate HTML ids'
    assert all(anchor in page.ids for anchor in expected)
    assert ('zh.html' if language=='en' else './') in page.links
    for link in page.links:
        parsed=urlsplit(link)
        if parsed.scheme or parsed.netloc: continue
        if not parsed.path:
            assert not parsed.fragment or unquote(parsed.fragment) in page.ids, link
            continue
        target=(ROOT/parsed.path.lstrip('/') if parsed.path.startswith('/') else file.parent/parsed.path)
        assert target.exists(), (file,link)
    assert 'file:///' not in text and '/Users/' not in text
    assert not re.search(r'指导教师|指导老师|指导者|老师|研究生|同学',text)
    for archive in ('MuJoCable_Elbow_Windows_Project.zip','MuJoCable_Windows_x64.zip','MuJoCable_plugin_Windows_x64.zip'):
        assert 'releases/download/windows-tutorial-v1/'+archive in text
    sources.append((ROOT/'docs/windows'/('en.md' if language=='en' else 'zh.md')).read_text())
commands=[re.findall(r'```powershell\n(.*?)\n```',s,re.S) for s in sources]
assert commands[0]==commands[1], 'English and Chinese PowerShell commands differ'
home=(ROOT/'index.html').read_text()
assert '/assets/windows-tutorial-links.js' in home
assert '/tutorials/windows/' in home and '/tutorials/windows/zh.html' in home
print('PASS: language metadata, 16 shared sections, command parity, local resources, homepage entry, public download links, neutral wording')

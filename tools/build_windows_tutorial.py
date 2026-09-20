"""Build the bilingual static tutorial. Run: python tools/build_windows_tutorial.py"""
from pathlib import Path
import re
import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tutorials/windows'

def render(language):
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'],
                           extension_configs={'toc': {'toc_depth': '2-2'}})
    content = md.convert((ROOT / f'docs/windows/{language}.md').read_text(encoding='utf-8'))
    headings = re.findall(r'<h2 id="([^"]+)">', content)
    assert len(headings) == 16
    toc = md.toc
    for index, old in enumerate(headings):
        new = f'step-{index}'
        content = content.replace(f'<h2 id="{old}">', f'<h2 id="{new}">')
        toc = toc.replace(f'href="#{old}"', f'href="#{new}"')
    zh = language == 'zh'
    title = 'Windows 完整教程 · MuJoCable' if zh else 'Windows tutorial · MuJoCable'
    description = ('在 Windows 上安装 VS Code、Python、MuJoCo 和 MuJoCable，复现肘关节绳驱动仿真。' if zh else
                   'Set up VS Code, Python, MuJoCo and MuJoCable on Windows, then reproduce a cable-driven elbow simulation.')
    own = 'zh.html' if zh else ''
    alternate = './' if zh else 'zh.html'
    home = '项目主页' if zh else 'Project home'
    download = '下载项目包' if zh else 'Download project'
    print_label = '打印 / 保存 PDF' if zh else 'Print / save PDF'
    toc_label = '目录' if zh else 'Contents'
    source_label = 'Markdown 原稿' if zh else 'Markdown source'
    switch_label = 'English' if zh else '中文'
    footer = 'Windows x64 · MuJoCo 3.4.0 · MuJoCable v0.2.0 + elbow routing patch'
    html = f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{description}">
<title>{title}</title><link rel="icon" href="/favicon.jpg">
<link rel="canonical" href="https://mujocable.github.io/tutorials/windows/{own}">
<link rel="alternate" hreflang="en" href="https://mujocable.github.io/tutorials/windows/">
<link rel="alternate" hreflang="zh-CN" href="https://mujocable.github.io/tutorials/windows/zh.html">
<link rel="alternate" hreflang="x-default" href="https://mujocable.github.io/tutorials/windows/">
<link rel="stylesheet" href="guide.css"><script defer src="guide.js"></script>
</head><body>
<a class="skip-link" href="#content">{'跳到正文' if zh else 'Skip to content'}</a>
<header class="site-header"><a class="brand" href="/">MuJoCable</a><nav aria-label="{'教程导航' if zh else 'Tutorial navigation'}"><a href="/">{home}</a><span class="platform">Windows x64</span><a class="language-switch" href="{alternate}" lang="{'en' if zh else 'zh-CN'}" hreflang="{'en' if zh else 'zh-CN'}">{switch_label}</a></nav></header>
<div class="layout"><aside><strong>{toc_label}</strong>{toc}</aside>
<main id="content"><div class="eyebrow">WINDOWS · SETUP &amp; SIMULATION</div>
<div class="toolbar"><a class="primary" href="https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_Elbow_Windows_Project.zip">{download}</a><a href="../../docs/windows/{language}.md">{source_label}</a><button class="print-button" type="button">{print_label}</button></div>
{content}<footer>{footer}</footer></main></div></body></html>'''
    (OUT / ('zh.html' if zh else 'index.html')).write_text(html, encoding='utf-8')

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for language in ('en', 'zh'): render(language)

// This repository contains a prebuilt homepage. Keep tutorial navigation separate
// from its generated React bundle so future source builds can adopt these links.
function addTutorialLinks() {
  const navigation = document.querySelector('.top-nav > div');
  const resources = document.querySelector('.paper-links');
  if (!navigation || !resources) return false;
  if (!navigation.querySelector('[data-windows-tutorial]')) {
    const link = document.createElement('a');
    link.href = '/tutorials/windows/';
    link.textContent = 'Windows tutorial';
    link.dataset.windowsTutorial = '';
    navigation.append(link);
  }
  if (!resources.querySelector('[data-windows-tutorial]')) {
    for (const [text, href, language] of [
      ['Windows tutorial', '/tutorials/windows/', 'en'],
      ['Windows 中文教程', '/tutorials/windows/zh.html', 'zh-CN'],
    ]) {
      const link = document.createElement('a');
      link.href = href;
      link.textContent = text;
      link.lang = language;
      link.hreflang = language;
      link.dataset.windowsTutorial = '';
      resources.append(link);
    }
  }
  return true;
}
if (!addTutorialLinks()) {
  const observer = new MutationObserver(() => {
    if (addTutorialLinks()) observer.disconnect();
  });
  observer.observe(document.getElementById('root'), { childList: true, subtree: true });
}

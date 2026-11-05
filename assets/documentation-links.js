// Add documentation access without rewriting the compiled project homepage.
function addDocumentationLinks() {
  const navigation = document.querySelector('.top-nav > div');
  const resources = document.querySelector('.paper-links');
  if (!navigation || !resources) return false;
  for (const parent of [navigation, resources]) {
    for (const [language, title, href] of [
      ['en', 'Documentation', '/docs/en/'],
    ]) {
      if (!parent.querySelector(`[data-documentation="${language}"]`)) {
        const link = document.createElement('a');
        link.href = href;
        link.textContent = title;
        link.lang = language;
        link.hreflang = language;
        link.dataset.documentation = language;
        parent.append(link);
      }
    }
  }
  return true;
}
if (!addDocumentationLinks()) {
  const observer = new MutationObserver(() => {
    if (addDocumentationLinks()) observer.disconnect();
  });
  observer.observe(document.getElementById('root'), {childList: true, subtree: true});
}

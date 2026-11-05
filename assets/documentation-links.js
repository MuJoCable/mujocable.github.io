// Add documentation access without rewriting the compiled project homepage.
function addDocumentationLinks() {
  const navigation = document.querySelector('.top-nav > div');
  const resources = document.querySelector('.paper-links');
  if (!navigation || !resources) return false;
  for (const parent of [navigation, resources]) {
    if (!parent.querySelector('[data-documentation]')) {
      const link = document.createElement('a');
      link.href = '/docs/';
      link.textContent = 'Documentation';
      link.dataset.documentation = '';
      parent.append(link);
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

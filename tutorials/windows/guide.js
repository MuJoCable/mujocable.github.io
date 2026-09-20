const chinese = document.documentElement.lang.startsWith('zh');
const languageLink = document.querySelector('.language-switch');
const languageBase = languageLink.getAttribute('href');
function updateLanguageLink() {
  // Both languages use step-0 ... step-15 so switching retains the current section.
  languageLink.setAttribute('href', languageBase + location.hash);
}
updateLanguageLink();
window.addEventListener('hashchange', updateLanguageLink);
document.querySelector('.print-button').addEventListener('click', () => window.print());

document.querySelectorAll('pre > code').forEach(code => {
  const button = document.createElement('button');
  button.className = 'copy-button';
  button.type = 'button';
  const label = chinese ? '复制' : 'Copy';
  button.textContent = label;
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = chinese ? '已复制' : 'Copied';
    } catch {
      button.textContent = chinese ? '请选中复制' : 'Select to copy';
    }
    setTimeout(() => { button.textContent = label; }, 1600);
  });
  code.parentElement.append(button);
});

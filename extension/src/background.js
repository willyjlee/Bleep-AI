chrome.tabs.onUpdated.addListener((id, info, tab) => {
  if (/youtube\.com/.test(tab.url)) {
    window.location.reload()
    chrome.pageAction.show(tab.id);
  }
});

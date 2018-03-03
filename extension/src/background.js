chrome.tabs.onUpdated.addListener((id, info, tab) => {
  if (/youtube\.com/.test(tab.url)) {
    chrome.pageAction.show(tab.id);
  }
});

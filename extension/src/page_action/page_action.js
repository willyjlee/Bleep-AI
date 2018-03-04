let egg = document.getElementById('egg');
let easter = document.getElementById('easter');
let custom = document.getElementById('custom');
let radios = document.getElementsByClassName('radio');
let rows = document.getElementsByClassName('row');

custom.addEventListener('keyup', () => {
  chrome.storage.sync.set({ settings: { activeIndex: 3, custom: custom.value.split(',').map(t => t.trim()).join(', ') } });
})

egg.addEventListener('click', () => {
  easter.style.height = '7.5rem';
  easter.style.opacity = 1;
  easter.style.overflow = '';
});

for (let index in rows) {
  let row = rows[index];
  if (row.addEventListener) {
    row.addEventListener('click', () => {
      resetActive();
      if (index === 3) {
        custom.focus();
      }
      row.classList.add('active');
      chrome.storage.sync.set({ settings: { activeIndex: index }});
    });
  }
}

function resetActive() {
  for (let row of rows) {
    row.classList.remove('active');
  }
}

document.addEventListener('DOMContentLoaded', function() {
  chrome.storage.sync.get('settings', ({ settings }) => {
    rows[settings.activeIndex || 0].classList.add('active');
    custom.value = settings.custom;
  });
});

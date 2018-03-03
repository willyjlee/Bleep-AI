let egg = document.getElementById('egg');
let easter = document.getElementById('easter');
let custom = document.getElementById('custom');
let radios = document.getElementsByClassName('radio');
let rows = document.getElementsByClassName('row');

custom.addEventListener('keyup', () => {
  resetActive();
  rows[3].classList.add('active');
  let words = custom.value.split(',').map(t => t.trim())
  console.log(words);
})

egg.addEventListener('click', () => {
  easter.style.height = '7.5rem';
  easter.style.opacity = 1;
  easter.style.overflow = '';
});

for (let index in radios) {
  let radio = radios[index];
  if (radio.addEventListener) {
    radio.addEventListener('click', () => {
      resetActive();
      if (index === 3) {
        custom.focus();
      }
      rows[index].classList.add('active');
    });
  }
}

function resetActive() {
  for (let row of rows) {
    row.classList.remove('active');
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // chrome.storage.sync.get('activeIndex', data => {
    console.log(chrome.storage);
  // });
});

let transcript = fake.map(({ word, start, end }) => ({ word, start: start - 0.2, end: end - 0.2 }));
let paused = false;
let previousTime = 0;
let customText = [];
let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
let lastData = {};

let synth = new Tone.Oscillator({
	frequency: 1000,
	volume: -10
}).toMaster();


chrome.extension.sendMessage({}, response => {
	// fetch(`https://52.165.191.240:8080/path?id=${getJsonFromUrl().v}`)
  // .then(res => res.json())
  // .then(d => {
  //   transcript = d.map(({ word, start, end }) => ({ word, start: start - 0.2, end: end - 0.2 }));
  // })
  // .catch(e => console.log('e', e));

	let readyStateCheckInterval = setInterval(() => {
		let video = document.getElementsByClassName('video-stream')[0];
		video && video.pause();
		if (activeIndex !== 0 && document.readyState === "complete") {
			clearInterval(readyStateCheckInterval);
			video.play();
			setInterval(() => {
				let { currentTime } = video;
				if (!paused) {
					let data = getWord(currentTime, transcript);
					if (data && lastData != data) {
						let { word, start, end } = data;
						console.log(word, activeIndex === 3 && customText.includes(word))
						if ((activeIndex === 3 && customText.includes(word)) || (activeIndex === 1 && word.length > 1 && word.includes('*')) || (activeIndex === 2 && !word.includes('*'))) {
							synth.start();
							video.volume = 0;
		        } else {
							synth.stop();
							video.volume = 1;
		        }
					}
					lastData = data;
				}

				paused = currentTime === previousTime;
				if (paused) {
					synth.stop();
					video.volume = 1;
				}
				previousTime = currentTime;
			}, 40);
		}
	}, 10);
});

function getJsonFromUrl() {
  let query = location.search.substr(1);
  let result = {};
  query.split("&").forEach(part => {
    let item = part.split("=");
    result[item[0]] = decodeURIComponent(item[1]);
  });
  return result;
}



function getWord(time, data) {
  let min = 0;
  let max = data.length - 1;
  let i;

  while (min <= max) {
    i = ~~((min + max) / 2);

    if (data[i].end < time) {
      min = i + 1;
    }
    else if (data[i].start > time) {
      max = i - 1;
    }
    else if (time < data[i].end && time > data[i].start) {
      return data[i];
    } else {
			return null;
		}
  }
}

function NotePlayer(frequency) {
	let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
	this.oscillator = audioCtx.createOscillator();
	this.oscillator.type = 'square';
	this.oscillator.frequency.value = frequency;
	this.oscillator.connect(audioCtx.destination);
	this.oscillator.start();

	setTimeout(() => oscillator.stop(), duration);
}

function playNote(frequency, duration) {
	let oscillator = audioCtx.createOscillator();
	oscillator.type = 'square';
	oscillator.frequency.value = frequency;
	oscillator.connect(audioCtx.destination);
	oscillator.start();

	setTimeout(() => oscillator.stop(), duration);
}

chrome.storage.sync.get('settings', ({ settings }) => {
	activeIndex = Number(settings.activeIndex);
	customText = settings.custom.split(', ');
});

let transcript;//fake.map(({ word, start, end }) => ({ word, start: start - 0.2, end: end - 0.2 }));
let paused = false;
let video, container;
let previousTime = 0;
let customText = [];
let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
let lastData = {};

let synth = new Tone.Oscillator({
	frequency: 1000,
	volume: -30
}).toMaster();


chrome.extension.sendMessage({}, response => {
	let check = setInterval(() => {
		video = document.getElementsByClassName('video-stream')[0];
		if (video) {
			video.pause();
			clearInterval(check);
		}
	}, 100);

  // metadata collection here
  let title = document.getElementsByClassName('title')[0].textContent;
  let name = document.getElementById('owner-name').textContent;
  let link = document.getElementById('owner-name').childNodes[0].href;
  //select stuff here

	fetch(`https://52.165.191.240:8080/path?id=${getJsonFromUrl().v}&title=${title}&publisher=${name}&publisher_link=${link}`)
  .then(res => res.json())
  .then(d => {
    transcript = d.map(({ word, start, end }) => ({ word, start: start - 0.2, end: end - 0.2 }));
		let gradient = document.createElement('div');

		Object.assign(gradient.style,{
			// position: 'relative',
			display: 'flex',
			bottom: '0',
			justifySelf: 'flex-end',
			height: '5px',
			width: '100%',
			backgroundColor: 'white',
			backgroundImage: `linear-gradient(90deg, ${[...Array(50)].map((_, i) => `${interpolateColors([0,255,0], [255,0,0], Math.random())} ${~~(i / 49 * 100)}%`).join(', ')})`
			// backgroundImage: 'linear-gradient(90deg, rgb(0, 0, 0) 0%, #6284FF 50%, #FF0000 100%)'
		});

		let check2 = setInterval(() => {
			container = document.getElementById('player-container');
			if (container) {
				container.appendChild(gradient);
				console.log('CONTAINER', container)
				clearInterval(check2);
			}
		}, 100);
		video.play();
  })
  .catch(e => console.log('e', e));

	let readyStateCheckInterval = setInterval(() => {
		if (activeIndex !== 0 && video && document.readyState === "complete") {
			clearInterval(readyStateCheckInterval);
			setInterval(() => {
				let { currentTime } = video;
				if (transcript && !paused) {
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

function interpolateColors(color1, color2, progress) { // color is [r, g, b], progress is 0 - 1
	let rDiff = color2[0] - color1[0];
	let gDiff = color2[1] - color1[1];
	let bDiff = color2[2] - color1[2];
	return `rgb(${~~(color1[0] + rDiff * progress)}, ${~~(color1[1] + gDiff * progress)}, ${~~(color1[2] + bDiff * progress)})`;
}

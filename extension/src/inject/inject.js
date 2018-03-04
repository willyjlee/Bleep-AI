chrome.extension.sendMessage({}, response => {
	fetch('http://52.165.191.240:8080/path', {
		method: 'GET',
		credentials: 'include',
		mode: 'no-cors',
		params: {
			id: getJsonFromUrl().v
		}
	})
	.then(res => res.json())
	.then(data => {
		console.log('DATA', data)
	})
	.catch(e => console.log('e', e));

	let readyStateCheckInterval = setInterval(() => {
		if (document.readyState === "complete") {
			clearInterval(readyStateCheckInterval);
			let video = document.getElementsByClassName('video-stream')[0];
			// video.addEventListener('timeupdate', () => {
			// 	console.log(video.currentTime)
			// })

			// setInterval(() => {
			// 	// console.log(video.currentTime);
			// 	// video.currentTime = 0;
			// 	video.paused = true;
			// }, 100);

			// playNote(1000, 1);

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
    i = (min + max) / 2 | 0;

    if (data[i].endTime < time) {
      min = i + 1;
    }
    else if (data[i].beginTime > time) {
      max = i - 1;
    }
    else {
      return data[i].word;
    }
  }
}

let audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playNote(frequency, duration) {
	let oscillator = audioCtx.createOscillator();
	oscillator.type = 'square';
	oscillator.frequency.value = frequency;
	oscillator.connect(audioCtx.destination);
	oscillator.start();

	setTimeout(() => oscillator.stop(), duration);
}

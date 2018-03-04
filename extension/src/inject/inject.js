let transcript;//fake.map(({ word, start, end }) => ({ word, start: start - 0.2, end: end - 0.2 }));
let paused = false;
let video, container, title, name, link;
let previousTime = 0;
let activeIndex = null;
let customText = [];
let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
let lastData = {};

let synth = new Tone.Oscillator({
	frequency: 1000,
	volume: -30
}).toMaster();

window.onload = function() {
	if (location.href.includes('watch')) {
		return;
	}

	fetch('https://52.165.191.240:8080/fetch_entries')
	.then(res => res.json())
	.then(data => {

		var overallContainer = $("<div>", {
	    id: "overallContainer"
	  });
	  overallContainer.css({
	    display: "flex",
	    "flex-direction": "column"
	  });

	  var thumbnailContainer = $("<div>", {
	    id: "thumbnailContainer"
	  });
	  thumbnailContainer.css({
	    display: "flex"
	  });

	  var titleContainer = $("<div>", {
	    id: "titleContainer"
	  });
	  titleContainer.css({
	    display: "flex",
	    "margin-bottom": "20px",
	    "margin-top": "10px"
	  });

	  var create_thumbnail = (video_id = "", title = "", author = "", author_link="google.com", rating=0) => {
	    url =
	      "https://i.ytimg.com/vi/" + video_id + "/hqdefault.jpg?sqp=-oaymwEZCNACELwBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDH4jTHLG0t3N64dLBsBfQncpS_Rw"
	    text_style = (rating < 0.5)? "red": "green";
	    prompt_text = (rating > 0.5)? "Safe": "Explicit";
	    return `
	  <div style="width: 210px; height: auto; margin-right: 4px; display: flex; flex-direction: column">
	    <a href="http://youtube.com/watch?v=${video_id}">
	      <img src=${url} style="width: 210px; max-height: 117.5px "></img>
	    </a>
	    <div style="line-height: 1.6rem; font-size: 1.4rem; font-weight: 500">
	      <div style="margin-top: 10px; color: black"> ${title}</div>
	    </div>
	    <div style="line-height: 1.8rem; font-size: 1.3rem">
	      <a href=${author_link} style="text-decoration: none;">
	        <div style="margin-top: 8px; color: #6E6E6E"> ${author}</div>
	      </a>
	      <a href=${url} style="text-decoration: none;">
	        <div style="color: ${text_style}">Bleep: ${prompt_text} content</div>
	      </a>
	    </div>
	  </div>
	  `;
	  };

	  var title = `
	  <div style="font-size: 1.6rem; font-weight: 500; line-height: 2rem; max-height: 2rem;">
	    Evaluated by Bleep
	  </div>
	  `;

		data.forEach(({ sentiment, metadata, id }) => {
				var total = 0;
				for(let i = 0; i < sentiment.length; i++){
					total += sentiment[i].score;
				}
				let score = total / sentiment.length;
				thumbnailContainer.append(create_thumbnail(id, metadata.title, metadata.publishers, score));

		});



	  titleContainer.append(title);
	  overallContainer.append(titleContainer);
	  overallContainer.append(thumbnailContainer);

	  new_div = $("#contents").prepend(overallContainer);
	})
	.catch(e => console.log('e', e))
};


chrome.extension.sendMessage({}, response => {
	let check = setInterval(() => {
		video = document.getElementsByClassName('video-stream')[0];
		title = document.getElementsByClassName('title')[0];
		name = document.getElementById('owner-name');
		link = document.getElementById('owner-name');
		if (video) {
			video.pause();
		}
		if (title && name && link.childNodes[0]) {
			let url = `https://52.165.191.240:8080/path?id=${getJsonFromUrl().v}&title=${title.textContent}&publisher=${name.textContent}&publisher_link=${link.childNodes[0].href}`;

			fetch(url)
			.then(res => res.json())
			.then(({ transcript: transcriptData, sentiment, metadata }) => {
				transcript = transcriptData.map(({ word, start, end }) => ({ word, start: start - 0.2, end: end - 0.2 }));
				let gradient = document.createElement('div');

				Object.assign(gradient.style,{
					// position: 'relative',
					display: 'flex',
					bottom: '0',
					justifySelf: 'flex-end',
					height: '9px',
					width: '100%',
					backgroundColor: 'white',
					backgroundImage: `linear-gradient(90deg, ${sentiment.map((_, i) => `${interpolateColors([0,255,0], [255,0,0], _.score)} ${~~(i / (sentiment.length - 1) * 100)}%`).join(', ')})`
					// backgroundImage: 'linear-gradient(90deg, rgb(0, 0, 0) 0%, #6284FF 50%, #FF0000 100%)'
				});

				let check2 = setInterval(() => {
					container = document.getElementById('player-container');
					if (container) {
						container.appendChild(gradient);
						clearInterval(check2);
					}
				}, 100);
				video.play();
			})
			.catch(e => console.log('e', e));

			clearInterval(check);
		}
	}, 100);

	let readyStateCheckInterval = setInterval(() => {
		if (activeIndex !== 0 && video && document.readyState === "complete") {
			clearInterval(readyStateCheckInterval);
			setInterval(() => {
				let { currentTime } = video;
				if (transcript && !paused) {
					let data = getWord(currentTime, transcript);
					if (data && lastData != data) {
						let { word, start, end } = data;
						word = word.replace('.', '');
						console.log('WORD', word, activeIndex === 1 && word.length > 1 && word.includes('*') && !word.includes('*'.repeat(word.length)))
						if ((activeIndex === 3 && customText.includes(word)) || (activeIndex === 1 && word.length > 1 && word.includes('*') && !word.includes('*'.repeat(word.length))) || (activeIndex === 2 && !word.includes('*'))) {
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

chrome.storage.sync.get('settings', ({ settings = { activeIndex: 0, custom: '' } }) => {
	activeIndex = Number(settings.activeIndex);
	customText = (settings.custom).split(', ');
});

function interpolateColors(color1, color2, progress) { // color is [r, g, b], progress is 0 - 1
	let rDiff = color2[0] - color1[0];
	let gDiff = color2[1] - color1[1];
	let bDiff = color2[2] - color1[2];
	return `rgb(${~~(color1[0] + rDiff * progress)}, ${~~(color1[1] + gDiff * progress)}, ${~~(color1[2] + bDiff * progress)})`;
}

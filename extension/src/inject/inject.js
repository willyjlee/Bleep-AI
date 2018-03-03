var port = chrome.runtime.connect();

chrome.extension.sendMessage({}, response => {
	let player = document.getElementById('movie_player');
	player.innerHTML = '';
	let id = getJsonFromUrl().v;

	var readyStateCheckInterval = setInterval(() => {
		if (document.readyState === "complete") {
			clearInterval(readyStateCheckInterval);




			// console.log(YT)
			// setInterval(() => {
			// 	let time = document.getElementsByClassName('ytp-time-current')[0];
			// 	console.log('time', time.innerHTML);
			// }, 1000);


		}
	}, 10);
});

function getJsonFromUrl() {
  var query = location.search.substr(1);
  var result = {};
  query.split("&").forEach(part => {
    var item = part.split("=");
    result[item[0]] = decodeURIComponent(item[1]);
  });
  return result;
}

// window.shit = () => {
// 	console.log('hi')
// 	player = new YT.Player('player', {
// 		height: '390',
// 		width: '640',
// 		videoId: 'M7lc1UVf-VE',
// 		events: {
// 			'onReady': onPlayerReady,
// 			'onStateChange': onPlayerStateChange
// 		}
// 	});
// }

// window.addEventListener("message", function(event) {
//   // We only accept messages from ourselves
//   if (event.source != window)
//     return;
//
//   if (event.data.type && (event.data.type == "FROM_PAGE")) {
//     console.log("Content script received: " + event.data.text);
//     port.postMessage(event.data.text);
//   }
// }, false);
//
// window.onYouTubeIframeAPIReady = player => {
// 	console.log('player ready', player, player.getPlayerState(), player.getCurrentTime())
//
// 	if (player.getPlayerState() !== 3) {
// 		// don't pause too early
// 		console.log(player.getCurrentTime())
// 		bindPlayer(document.getElementsByTagName('video')[0])
// 	}
//
// 	if (original !== undefined) original()
// }

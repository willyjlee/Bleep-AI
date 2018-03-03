var port = chrome.runtime.connect();

chrome.extension.sendMessage({}, response => {

	let id = getJsonFromUrl().v;

	var readyStateCheckInterval = setInterval(() => {
		if (document.readyState === "complete") {
			clearInterval(readyStateCheckInterval);
			let player = document.getElementById('movie_player');
			console.log('PLAYER', Object.keys(Object.getPrototypeOf(player)))

			let top = document.getElementById('top');
			top.replaceChild(document.createTextNode('shit'), top.children[0]);


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

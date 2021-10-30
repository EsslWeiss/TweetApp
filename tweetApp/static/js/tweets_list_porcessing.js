
function addLike(tweet_id) {
	tweetBtn = document.getElementById('tweet-' + tweet_id);
	let currLike = parseInt(tweetBtn.innerHTML.match(/\d+/), 10);
	tweetBtn.innerHTML = (currLike += 1) + ' like';
	return;
}

function likeBtn(tweet) {
	return "<button id='tweet-" + tweet.id + "' class='btn btn-primary' onclick=addLike(" + tweet.id + ")>" + tweet.likes + " like</button>";
}

function loadTweetsToHTML() {
	let tweetsBar = document.getElementById('tweets-list');
	let tweetFormContainer = document.getElementById('tweet-form-container');
	let tweetForm = document.getElementById('tweet-form');

	let xhr = new XMLHttpRequest();
	xhr.responseType = 'json';
	xhr.open('GET', 'tweets/');
	xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
	xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

	xhr.onload = () => {
		let tweets = xhr.response.data;
		let tweetsList = '';
		for(let t in tweets) {
			tweetsList += '<p align="center"><small>' + tweets[t].date_created + '</small></p>';
			tweetsList += '<p align="center"><b>' + tweets[t].content + '</b> ' + likeBtn(tweets[t]) + '</p><br><br>';
		}
		tweetsBar.innerHTML = tweetsList;
	}
	xhr.send();
}

document.getElementById('load-tweets').addEventListener('click', loadTweetsToHTML);


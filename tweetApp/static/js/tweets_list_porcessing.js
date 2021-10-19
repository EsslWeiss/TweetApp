
function addLike(tweet_id) {
	tweetBtn = document.getElementById('tweet-' + tweet_id);
	let currLike = parseInt(tweetBtn.innerHTML.match(/\d+/), 10);

	tweetBtn.innerHTML = (currLike += 1) + ' like';
	return
}

function likeBtn(tweet) {
	return "<button id='tweet-" + tweet.id + "' class='btn btn-primary' onclick=addLike(" + tweet.id + ")>" + tweet.likes + " like</button>";
}

document.getElementById('load_tweets').addEventListener(
	'click', () => {
		let tweetsBar = document.getElementById('tweets_list');
		let tweetFormContainer = document.getElementById('tweet-form-container')
		let tweetForm = document.getElementById('tweet-form');

		let xhr = new XMLHttpRequest();
		xhr.responseType = 'json';
		xhr.open('GET', 'tweets/');
		xhr.onload = () => {
			let tweets = xhr.response.data;
			let tweetsList = '';

			let elem = document.getElementsByTagName('input')

			for(let t in tweets) {
				tweetsList += '<p align="center"><b>' + tweets[t].content + '</b> ' + likeBtn(tweets[t]) + '</p>';
			}
			tweetsBar.innerHTML = tweetsList;
			tweetFormContainer.innerHTML = tweetForm;
		}
		xhr.send();
	}
);


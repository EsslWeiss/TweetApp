
function addLike(tweet_id) {
	tweetBtn = document.getElementById('tweet-' + tweet_id);
	let currLike = parseInt(tweetBtn.innerHTML.match(/\d+/), 10);
	tweetBtn.innerHTML = (currLike += 1) + ' like';
	return;
}

function likeBtn(tweet) {
	return "<button id='tweet-" + tweet.id + "' class='btn btn-primary' onclick=addLike(" + tweet.id + ")>" + tweet.likes + " like</button>";
}

function sendTweetForm(e) {
	e.preventDefault();

	let textContent = document.getElementById('textContentInput').value;
	let toNextPage = document.getElementById('toNextPageInput').value;
	let csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

	csrfToken = 'csrfmiddlewaretoken=' + encodeURIComponent(csrfToken);
	toNextPage = 'to_next_page=' + encodeURIComponent(toNextPage);
	textContent = 'text_content=' + encodeURIComponent(textContent);
	const postData = csrfToken + '&' + toNextPage + '&' + textContent
	
	let xhr = new XMLHttpRequest();
	xhr.responseType = 'json';
	xhr.open('POST', '/', true);
	xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
	xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded');
	
	xhr.addEventListener("readystatechange", () => {
		if(xhr.readyState === 4 && xhr.status === 200) {       
 			document.getElementById('textContentInput').value = "";
			let tweetsBar = document.getElementById('tweets-list');
			const newTweet = xhr.response;
			if (tweetsBar.innerHTML.trim().length > 0) {
				let tweetDate = '<p align="center"><small>' + newTweet.date_created  + '</small></p>';
				let tweetElem = '<p align="center"><b>' + newTweet.content + '</b> ' + likeBtn(newTweet) + '</p><br><br>';
				tweetsBar.innerHTML = tweetDate + tweetElem + tweetsBar.innerHTML;
			} else { 
				return;
			}
		}
	});
	xhr.send(postData);
}

document.getElementById('sendButton').addEventListener(
	'click', sendTweetForm
);


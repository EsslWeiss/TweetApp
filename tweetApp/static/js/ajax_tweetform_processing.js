
function addLike(tweet_id) {
	tweetBtn = document.getElementById('tweet-' + tweet_id);
	let currLike = parseInt(tweetBtn.innerHTML.match(/\d+/), 10);
	tweetBtn.innerHTML = (currLike += 1) + ' like';
	return;
}

function likeBtn(tweet) {
	return "<button id='tweet-" + tweet.id + "' class='btn btn-primary' onclick=addLike(" + tweet.id + ")>" + tweet.likes + " like</button>";
}

function clearErrorContainer() {
	let errorContainer = document.getElementById('tweet-form-error');
	errorContainer.innerHTML = "";
	return;
}

function validationForm() {
	let textContent = document.getElementById('textContentInput').value;
	let errorContainer = document.getElementById('tweet-form-error');
	
	if(textContent.length === 0) {
		errorContainer.innerHTML = 'you forgot to tweet';
		return false;
	} else {
		return true;
	}
}

function sendTweetForm(e) {
	e.preventDefault(); 
	let xhr = new XMLHttpRequest();
	isValid = validationForm();
	if (isValid === false) {
		xhr.abort();
		return;
	}

	let textContent = document.getElementById('textContentInput').value;
	let csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	csrfToken = 'csrfmiddlewaretoken=' + encodeURIComponent(csrfToken);
	textContent = 'text_content=' + encodeURIComponent(textContent);
	const postData = csrfToken + '&' + textContent
	xhr.responseType = 'json';
	xhr.open('POST', '/', true);
	xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
	xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded');
	
	xhr.addEventListener("readystatechange", () => {
		if(xhr.readyState === 4 && xhr.status === 201) {
			clearErrorContainer();

 			document.getElementById('textContentInput').value = "";
			let tweetsBar = document.getElementById('tweets-list');
			let errorsContainer
			const newTweet = xhr.response;
			if (tweetsBar.innerHTML.trim().length > 0) {
				let tweetDate = '<p align="center"><small>' + newTweet.date_created  + '</small></p>';
				let tweetElem = '<p align="center"><b>' + newTweet.content + '</b> ' + likeBtn(newTweet) + '</p><br><br>';
				tweetsBar.innerHTML = tweetDate + tweetElem + tweetsBar.innerHTML;
			} else { 
				return;
			}
		}
		if(xhr.status === 400) {
			let errorContainer = document.getElementById('tweet-form-error');
			let errors = xhr.response;
			errorContainer.innerHTML = errors.text_content[0]
			return;
		}
	});
	
	xhr.send(postData);
}

document.getElementById('sendButton').addEventListener(
	'click', sendTweetForm
);


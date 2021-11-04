
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
	errorContainer.innerText = "";
	errorContainer.setAttribute('class', 'd-none alert alert-danger"');
	return;
}

function validationForm() {
	let textContent = document.getElementById('textContentInput').value;
	let errorContainer = document.getElementById('tweet-form-error');
	
	if(textContent.length === 0) {
		errorContainer.innerText = 'you forgot to tweet';
		errorContainer.setAttribute('class', 'alert alert-danger');
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
	console.log('start js');

	let textContent = document.getElementById('textContentInput').value;
	let csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	csrfToken = 'csrfmiddlewaretoken=' + encodeURIComponent(csrfToken);
	textContent = 'text_content=' + encodeURIComponent(textContent);
	const postData = csrfToken + '&' + textContent
	xhr.responseType = 'json';
	xhr.open('POST', '/tweet-create/', true);
	xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
	xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded');
	
	xhr.addEventListener("readystatechange", () => {
		console.log('send form');
		if(xhr.readyState === 4 && xhr.status === 201) {
			clearErrorContainer();

 			document.getElementById('textContentInput').value = "";
			let tweetsBar = document.getElementById('tweets-list');
			const newTweet = xhr.response;
			console.log(111);
			console.log(newTweet);
			if (tweetsBar.innerHTML.trim().length > 0) {
				let tweetDate = '<p align="center"><small>' + newTweet.date_created  + '</small></p>';
				let tweetElem = '<p align="center"><b>' + newTweet.text_content + '</b> ' + likeBtn(newTweet) + '</p><br><br>';
				tweetsBar.innerHTML = tweetDate + tweetElem + tweetsBar.innerHTML;
			} else { 
				return;
			}
		}
		if(xhr.status === 400) {
			console.log('status code 400!');
			let errorContainer = document.getElementById('tweet-form-error');
			let errors = xhr.response;
			if(errors) {
				errorContainer.setAttribute('class', 'alert alert-danger');
				errorContainer.setAttribute('style', 'margin: 50px');
				errorContainer.innerText = errors.text_content[0]
			}
			return;
		} 
		if(xhr.status === 401) {
			alert('You must login');
			window.location.href = '/login-page';
			return;
		}
		if(xhr.status === 403) {
			alert('You must login');
			window.location.href = '/login-page';
			return;
		}
	});
	
	xhr.send(postData);
}

document.getElementById('sendButton').addEventListener(
	'click', sendTweetForm
);


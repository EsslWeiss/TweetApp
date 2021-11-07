
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function tweetLikeAction(tweet_id) {
	const url = '/api/tweet/action';
	const method = 'POST';
	const data = JSON.stringify({
		id: tweet_id,
		action: 'like'
	});
	console.log(data);
	const csrftoken = getCookie('csrftoken');

	let xhr = new XMLHttpRequest();
	xhr.open(method, url);
	xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
	xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.setRequestHeader('X-CSRFToken', csrftoken);
	xhr.onload = () => {
		console.log(xhr.status, xhr.response);
	}
	xhr.send(data);
}


function tweetUnlikeAction(tweet_id) {
	const url = '/api/tweet/action';
	const method = 'POST';
	const data = JSON.stringify({
		id: tweet_id,
		action: 'unlike'
	});
	console.log(data);
	const csrftoken = getCookie('csrftoken');

	let xhr = new XMLHttpRequest();
	xhr.open(method, url);
	xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
	xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.setRequestHeader('X-CSRFToken', csrftoken);
	xhr.onload = () => {
		console.log(xhr.status, xhr.response);
	}
	xhr.send(data);
}


function tweetRetweetAction(tweet_id) {
	const url = '/api/tweet/action';
	const method = 'POST';
	const data = JSON.stringify({
		id: tweet_id,
		action: 'retweet'
	});
	console.log(data);
	const csrftoken = getCookie('csrftoken');

	let xhr = new XMLHttpRequest();
	xhr.open(method, url);
	xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
	xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.setRequestHeader('X-CSRFToken', csrftoken);
	xhr.onload = () => {
		console.log(xhr.status, xhr.response);
	}
	xhr.send(data);
}


function loadTweetsToHTML() {
	let tweetsBar = document.getElementById('tweets-list');
	let tweetFormContainer = document.getElementById('tweet-form-container');
	let tweetForm = document.getElementById('tweet-form');

	let xhr = new XMLHttpRequest();
	xhr.responseType = 'json';
	let url = 'api/tweets/';
	xhr.open('GET', url);
	xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
	xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	
	xhr.onload = () => {
		let tweets = xhr.response;
		let tweetsList = '';
		for(let t in tweets) {
			console.log('in tweets cycle.');
			tweetsList += '<p><small>' + tweets[t].date_created + '</small></p>';
		
			tweetsList += '<b>' + tweets[t].text_content + '</b> ' + "<br><div align='center' class='btn-group'><button id='tweet-" + tweets[t].id + "' class='btn btn-primary btn-sm' onclick='tweetLikeAction(" + tweets[t].id + ")'>" + tweets[t].likes + " like</button> <button id='tweet-" + tweets[t].id + "' class='btn btn-primary btn-sm' onclick='tweetUnlikeAction(" + tweets[t].id + ")'> unlike</button> <button id='tweet-" + tweets[t].id + "' class='btn btn-primary btn-sm' onclick='tweetRetweetAction(" + tweets[t].id + ")'> retweet</button></div>" + '<br><br>';
		}
		tweetsBar.innerHTML = tweetsList;
	}
	xhr.send();
}

document.getElementById('load-tweets').addEventListener('click', loadTweetsToHTML);


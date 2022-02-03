
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

export function loadTweets(callback) {
  const xhr = new XMLHttpRequest();	
  xhr.responseType = 'json';
  const url = 'http://localhost:8000/api/tweets';  // URL to django backend
  const method = 'GET';
  xhr.open(method, url);
  xhr.onload  = () => {
    callback(xhr.response, xhr.status)
  }
  xhr.onerror = () => {
    callback({message: 'the request was an error'}, 400)
  }
  xhr.send();
}


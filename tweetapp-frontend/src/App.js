import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';


function loadTweets(callback) {
  let tweetsBar = document.getElementById('tweets-list');

  const xhr = new XMLHttpRequest();
  xhr.responseType = 'json';
  const url = 'http://127.0.0.1:8000/api/tweets/';  // URL of django backend
  const method = 'GET';
  xhr.open(method, url);
  xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.onload  = () => {
    callback(xhr.response, xhr.status)	
  }
  xhr.onerror = () => {
    callback({message: 'the request was an error'}, 400)
  }
  xhr.send();
}


function App() {
  const [tweets, setTweets] = useState([])


  useEffect(() => {
    // my lookup
    const tweetsLoadedCallback = (response, status) => {
      if (status === 200) {
      	setTweets(response)
      }
    }

    loadTweets(tweetsLoadedCallback)
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
	<p>
		{tweets.map((tweet, index) => {
		  return <li>{tweet.content}</li>	
		})}
	</p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;

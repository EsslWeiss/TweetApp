import React, {useEffect, useState} from 'react';
import {formatRetweetItem, formatTweetItem} from './formatTweetsComponents';
import {loadTweets} from './request2EndpointsComponents';


export function Tweet(props) {
  /* Фунция возвращает твит в виде HTML кода */
  const {tweet} = props;
  const className = props.className ? props.className : 'col-10 max-auto'
  
  if (tweet.is_retweet) {
    return formatRetweetItem(tweet);
  }
  
  return formatTweetItem(tweet)
}

function TweetsList(props) {
  const [tweets, setTweets] = useState([])
  setTweets([...props.newTweet].concat(tweets));

  useEffect(() => {
    // my lookup
    const tweetsLoadedCallback = (response, status) => {
      if (status === 200) {
      	setTweets(response);
      }
    }

    loadTweets(tweetsLoadedCallback)
  }, [])
  
  return tweets.map((item, index) => {
    return <Tweet tweet={item} className={'my-5 py-5 border bg-white text-dark'} />
  })
}

export function TweetsComponent(props) {
  const [newTweet, setNewTweet] = useState([]);
  const textAreaRef = React.createRef()
  const handleClick = (event) => {
    event.preventDefault();
    const newVal = textAreaRef.current.value;
    let tempNewTweet = [...newTweet]
    tempNewTweet.unshift({
      content: newVal,
      likes: 0,
      id: 12345
    })
    setNewTweet(tempNewTweet);
    textAreaRef.current.value = '';
  }

  return <div>
    <div className='col-8 mb-5' style={{paddingLeft: '400px'}}>
      <form onSubmit={handleClick}>
        <textarea ref={textAreaRef} required={true} className='form-control' name='tweet'>  
        </textarea>
        <button type='submit' className='btn btn-primary my-3'>Tweet!</button>
      </form>
    </div>

  <TweetsList newTweet={newTweet} />
  </div>
}


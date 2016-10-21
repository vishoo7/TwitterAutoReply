# TwitterAutoReply

## Configuration
Install tweepy by running `$ pip install tweepy`

More about [tweepy](http://www.tweepy.org/)

Install markovify by running `$ pip install markovify`

More about [markovify]()

### credentials.py
In order to read or write from the Twitter account, you need to authenticate.

Go back into the "Keys and Access Tokens" tab of your Twitter app. In credentials.py, add:

```
CONSUMER_KEY = ""  
CONSUMER_SECRET = ""  
ACCESS_TOKEN = ""  
ACCESS_TOKEN_SECRET = ""  
```

Fill in the appropriate values from the Keys and Access Tokens page inside the quotation marks

### reply_list.txt
Here you maintain the list of replies separated by new lines. This will reload before ever reply so you can dynamically change the contents.

### user_tweet_history.txt (Optional)
Here you would have the tweet history of the user, used if you are in mock mode.

### main.py
```
usage: main.py [-h] --handle HANDLE [--mock]

optional arguments:
  -h, --help       show this help message and exit
  --handle HANDLE  Twitter handle (without @)
  --mock           enable mock mode
```

## Considerations
- If the user you are auto-replying to tweets in rapid succession, the loading of *reply_list.txt* may slow down performance. 
- When using filter with follow=['{userid}'] it calls *on_status* for retweets of that user's tweets and for replies to that user's tweets. [See here](https://dev.twitter.com/streaming/overview/request-parameters#follow). This is inefficient. Perhaps an alternative to *tweepy.streaming* would be better, but I am not familiar enough with the Twitter API. Currently *on_status* is being called when the streaming API returns JSON containing a key *in_reply_to_status_id*
- I do not assume responsibility for how you decide to use this app

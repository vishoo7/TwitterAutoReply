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
Call using twitter handle (without @) and optional 0 or 1 for mock mode. 1 is on, 0 is off. If last argument isn't specified mock mode is by default off

Example: `$ python3 main.py realDonaldTrump 1`

## Considerations
- If the user you are auto-replying to tweets in rapid succession, the loading of *reply_list.txt* may slow down performance. 
- I do not assume responsibility for how you decide to use this app